"""Abstract base class for a music player."""

__all__ = ['Player']

from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict

from music_player.core.utils import EventManager


class PositionChangeEvent(BaseModel):
    """
    Event that is invoked when the playback position changes.

    :var position: The current playback position in seconds.
    """

    model_config = ConfigDict(frozen=True)

    position: float


class PlaybackErrorEvent(BaseModel):
    """Event that is invoked when an error occurs during playback."""

    model_config = ConfigDict(frozen=True)


class Player(ABC):
    """
    Abstract base class for music players.

    A music player is responsible for playing tracks, but it does not manage the playback queue.
    This is handled by an ``Queue`` implementation.
    """

    _position_change_event: EventManager[PositionChangeEvent]
    _playback_error_event: EventManager[PlaybackErrorEvent]

    def __init__(self) -> None:
        """Initialize the music player."""
        self._position_change_event = EventManager()

    @abstractmethod
    def play(self, track_uri: str) -> None:
        """
        Play the specified track.

        :param track_uri: The URI of the track to play.
        """

    @abstractmethod
    def pause(self) -> None:
        """
        Pause the playback.

        :raises NotPlayingError: If no track is playing.
        """

    @abstractmethod
    def resume(self) -> None:
        """
        Resume the currently paused track.

        :raises AlreadyPlayingError: If a track is already playing.
        """

    @property
    @abstractmethod
    def is_playing(self) -> bool:
        """
        Check if a track is currently playing.

        :return: Whether a track is currently playing.
        """

    @property
    @abstractmethod
    def position(self) -> float:
        """
        Get the current playback position.

        :return: The current playback position in seconds.
        """

    @position.setter
    @abstractmethod
    def position(self, value: float) -> None:
        """
        Set the playback position.

        :param value: The new playback position in seconds.
        :raises NotPlayingError: If no track is playing.
        :raises PositionOutOfBoundsError: If the position is out of bounds for the current track.
        """

    @property
    @abstractmethod
    def volume(self) -> float:
        """
        Get the current volume.

        :return: The current volume as a percentage.
        """

    @volume.setter
    @abstractmethod
    def volume(self, value: float) -> None:
        """
        Set the volume.

        :param value: The new volume as a percentage.
        :raises VolumeOutOfBoundsError: If the volume is not between 0 % and 100 %.
        """

    @property
    def position_change_event(self) -> EventManager[PositionChangeEvent]:
        """Event listener that is invoked when the playback position changes."""
        return self._position_change_event

    @property
    def playback_error_event(self) -> EventManager[PlaybackErrorEvent]:
        """Event listener that is invoked when an error occurs during playback."""
        return self._playback_error_event

    @abstractmethod
    def close(self) -> None:
        """Clean up resources used by the music player."""
