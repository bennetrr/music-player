__all__ = ['TrackMetadata']

from pydantic import BaseModel


class TrackMetadata(BaseModel):
    """Metadata for a track."""

    title: str
    """The title of the track."""
    artist: str
    """The artist of the track."""
    album: str | None
    """The album where the track is on."""
    duration: int | None
    """The duration of the track in seconds."""
    cover_url: str | None
    """The URL of the cover image for the track."""
