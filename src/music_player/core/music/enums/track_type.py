__all__ = ['TrackType']

from enum import StrEnum


class TrackType(StrEnum):
    """Type of a track."""

    SONG = 'song'
    PODCAST = 'podcast'
    RADIO = 'radio'

    def is_endless(self) -> bool:
        """Check if the track is endless."""
        return self == self.RADIO
