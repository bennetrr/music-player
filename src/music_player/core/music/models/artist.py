__all__ = ['Artist']

from pydantic import AnyUrl

from .playable_container import PlayableContainer


class Artist(PlayableContainer):
    """An artist."""

    name: str
    cover_uri: AnyUrl | None
