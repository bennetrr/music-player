import asyncio
import concurrent.futures
from datetime import datetime, timedelta
from logging import getLogger

import tidalapi
from pydantic import BaseModel

from music_player.core.authentication import (
    AuthenticationResult,
    CodeAuthenticationStrategy,
    LinkAuthenticationStrategy,
)
from music_player.core.music import Provider, SearchResult, Track, TrackContainer, TrackMetadata
from music_player.core.plugin_manager import PluginContext

logger = getLogger(__name__)


class Credentials(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expiry_time: datetime


class Config(BaseModel): ...


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
        credentials = self._context.get_credentials(Credentials)

        if credentials is not None:
            logger.debug('Attempting to restore session')

            self._tidal.load_oauth_session(**credentials.model_dump())

            if self._tidal.check_login():
                logger.info('Successfully logged in with stored credentials')
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
        """Handle the second login step."""
        await asyncio.wrap_future(future)

        if not self._tidal.check_login():
            logger.error('Failed to log in')
            return False

        self._save_credentials()
        logger.info('Successfully logged in')
        return True

    def _save_credentials(self) -> None:
        """Save the credentials to the credential store."""
        self._context.set_credentials(
            Credentials(
                token_type=self._tidal.token_type,
                access_token=self._tidal.access_token,
                refresh_token=self._tidal.refresh_token,
                expiry_time=self._tidal.expiry_time,
            )
        )

    async def search(self, query: str) -> SearchResult:
        """Search the provider's library."""
        return NotImplemented

    async def list(self, arg: TrackContainer) -> SearchResult:
        """List the content in the provider's library."""
        return NotImplemented

    async def resolve_uri(self, track: Track) -> str:
        """Resolve a track to a playable URI."""
        return NotImplemented

    async def get_metadata(self, track: Track) -> TrackMetadata:
        """Get the metadata for a track."""
        return NotImplemented
