__all__ = ['TrackMetadata']

from pydantic import BaseModel


class TrackMetadata(BaseModel):
    """
    Metadata for a track.

    :var title: The title of the track.
    :var artist: The artist of the track.
    :var album: The album where the track is on.
    :var duration: The duration of the track in seconds.
    :var cover_url: The URL of the cover image for the track.
    """

    title: str
    artist: str
    album: str | None
    duration: int | None
    cover_url: str | None
