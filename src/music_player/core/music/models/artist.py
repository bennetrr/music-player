__all__ = ['Artist']

from pydantic import AnyUrl

from .track_container import TrackContainer


class Artist(TrackContainer):
    """An artist."""

    name: str
    cover_uri: AnyUrl | None
