__all__ = ['Album']

from pydantic import AnyUrl

from music_player.core.music import TrackContainer


class Album(TrackContainer):
    """An album."""

    name: str
    artist: str
    artist_id: str
    cover_uri: AnyUrl | None
    year: int | None
    number_of_tracks: int
    duration: int
