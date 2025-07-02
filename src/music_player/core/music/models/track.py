__all__ = ['Track']


from .playable import Playable


class Track(Playable):
    """
    A track.

    :var title: The title of the track.
    :var artist: The artist of the track.
    :var album: The album where the track is on.
    :var cover_uri: The URL of the cover image for the track.
    :var duration: The duration of the track in seconds.
    """

    title: str
    artist: str
    artist_id: str
    album: str | None
    album_id: str | None
    cover_uri: str | None
    duration: int | None
