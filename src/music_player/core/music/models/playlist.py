__all__ = ['Playlist']

from pydantic import AnyUrl

from .playable_container import PlayableContainer


class Playlist(PlayableContainer):
    """A playlist."""

    name: str
    cover_uri: AnyUrl | None
    number_of_tracks: int
    duration: int
