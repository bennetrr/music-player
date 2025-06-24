__all__ = ['Artist']

from pydantic import AnyUrl

from music_player.core.music.models import TrackContainer


class Artist(TrackContainer):
    """An artist."""

    name: str
    cover_uri: AnyUrl | None
