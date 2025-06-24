__all__ = ['PlaybackStatus']

from enum import StrEnum


class PlaybackStatus(StrEnum):
    """Playback status of the player."""

    STOPPED = 'stopped'
    PLAYING = 'playing'
    ERROR = 'error'
