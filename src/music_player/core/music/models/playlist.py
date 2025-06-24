__all__ = ['Playlist']

from pydantic import AnyUrl

from music_player.core.music import TrackContainer


class Playlist(TrackContainer):
    """A playlist."""

    name: str
    cover_uri: AnyUrl | None
    number_of_tracks: int
    duration: int
