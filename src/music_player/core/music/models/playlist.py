__all__ = ['Playlist']


from .playable_container import PlayableContainer


class Playlist(PlayableContainer):
    """A playlist."""

    name: str
    cover_uri: str | None
    number_of_tracks: int
    duration: int
