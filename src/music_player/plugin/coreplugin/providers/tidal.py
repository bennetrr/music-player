import asyncio
import concurrent.futures
from datetime import datetime, timedelta
from logging import getLogger
from typing import Any

import tidalapi
from pydantic import BaseModel

from music_player.core.authentication import (
    AuthenticationResult,
    CodeAuthenticationStrategy,
    LinkAuthenticationStrategy,
)
from music_player.core.music import Album, Artist, Playable, PlayableContainer, Playlist, Provider, SearchResult, Track
from music_player.core.plugin_manager import PluginContext

logger = getLogger(__name__)

type TidalObject = tidalapi.Artist | tidalapi.Album | tidalapi.Playlist | tidalapi.Track


class _Credentials(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expiry_time: datetime


class _Config(BaseModel): ...


class TidalProvider(Provider):
    """Provider for the TIDAL music streaming service using the `tidalapi <https://tidalapi.netlify.app/>`_ package."""

    _tidal: tidalapi.Session

    def __init__(self, context: PluginContext) -> None:
        """Initialize the provider."""
        super().__init__(context)

        tidal_config = tidalapi.Config()
        self._tidal = tidalapi.Session(tidal_config)

    @property
    def id(self) -> str:
        """A unique ID of the music provider instance."""
        return 'tidal'

    async def login(self) -> AuthenticationResult:
        """Log in to the service."""
        credentials = self._context.get_credentials(_Credentials)

        if credentials is not None:
            logger.debug('Attempting to restore session')

            self._tidal.load_oauth_session(**credentials.model_dump())

            if self._tidal.check_login():
                logger.debug('Successfully logged in with stored credentials')
                self._save_credentials()
                return AuthenticationResult(result=True)

        logger.debug('Starting login flow')

        login_details, future = self._tidal.login_oauth()
        expires = datetime.now().astimezone() + timedelta(seconds=login_details.expires_in)
        login_task = self._context.loop.create_task(self._handle_second_login_step(future))

        # TODO: Schedule token refreshing somewhere #0

        return AuthenticationResult(
            result=login_task,
            strategies=[
                LinkAuthenticationStrategy(link=f'https://{login_details.verification_uri_complete}', expires=expires),
                CodeAuthenticationStrategy(
                    link=f'https://{login_details.verification_uri}', code=login_details.user_code, expires=expires
                ),
            ],
        )

    async def _handle_second_login_step(self, future: concurrent.futures.Future[None]) -> bool:
        await asyncio.wrap_future(future)

        if not self._tidal.check_login():
            logger.error('Failed to log in')
            return False

        self._save_credentials()
        logger.debug('Successfully logged in')
        return True

    def _save_credentials(self) -> None:
        self._context.set_credentials(
            _Credentials(
                token_type=self._tidal.token_type,
                access_token=self._tidal.access_token,
                refresh_token=self._tidal.refresh_token,
                expiry_time=self._tidal.expiry_time,
            )
        )

    async def _get_tidal_object(self, arg: PlayableContainer | Playable) -> TidalObject:
        match arg:
            case Artist():
                return self._tidal.artist(arg.id)
            case Album():
                return self._tidal.album(arg.id)
            case Playlist():
                return self._tidal.playlist(arg.id)
            case Track():
                return self._tidal.track(arg.id)
            case _:
                raise TypeError(f'Invalid argument type: {type(arg)}')

    async def _to_search_result(
        self,
        artists: list[tidalapi.Artist] | None = None,
        albums: list[tidalapi.Album] | None = None,
        playlists: list[tidalapi.Playlist] | None = None,
        tracks: list[tidalapi.Track] | None = None,
        **_: Any,  # noqa: ANN401
    ) -> SearchResult:
        return SearchResult(
            artists=[
                Artist(provider_id=self.id, id=str(x.id), name=x.name, cover_uri=x.image(750)) for x in artists or []
            ],
            albums=[
                Album(
                    provider_id=self.id,
                    id=str(x.id),
                    name=x.name,
                    artist=x.artist.name,
                    artist_id=str(x.artist.id),
                    cover_uri=x.image(1280),
                    year=x.year,
                    duration=x.duration,
                    number_of_tracks=x.num_tracks,
                )
                for x in albums or []
            ],
            playlists=[
                Playlist(
                    provider_id=self.id,
                    id=str(x.id),
                    name=x.name,
                    cover_uri=x.image(1080),
                    duration=x.duration,
                    number_of_tracks=x.num_tracks,
                )
                for x in playlists or []
            ],
            tracks=[
                Track(
                    provider_id=self.id,
                    id=str(x.id),
                    title=x.name,
                    artist=x.artist.name,
                    artist_id=str(x.artist.id),
                    album=x.album.name,
                    album_id=str(x.album.id),
                    cover_uri=x.album.image(1280),
                    duration=x.duration,
                )
                for x in tracks or []
            ],
        )

    async def search(self, query: str) -> SearchResult:
        """Search the provider's library."""
        results = self._tidal.search(query)
        return await self._to_search_result(**results)

    async def list(self, arg: PlayableContainer) -> SearchResult:
        """List the content in the provider's library."""
        obj = await self._get_tidal_object(arg)

        match obj:
            case tidalapi.Artist():
                return await self._to_search_result(
                    albums=[*obj.get_albums(), *obj.get_ep_singles(), *obj.get_other()], tracks=obj.get_top_tracks()
                )
            case tidalapi.Album():
                return await self._to_search_result(tracks=obj.tracks())
            case tidalapi.Playlist():
                return await self._to_search_result(tracks=obj.tracks())
            case _:
                raise TypeError(f'Invalid argument type: {type(arg)}')

    async def resolve_uri(self, playable: Playable) -> str:
        """Resolve a playable object to a URI."""
        raise NotImplementedError
