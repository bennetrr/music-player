__all__ = ['Album']


from .playable_container import PlayableContainer


class Album(PlayableContainer):
    """An album."""

    name: str
    artist: str
    artist_id: str
    cover_uri: str | None
    year: int | None
    number_of_tracks: int
    duration: int
