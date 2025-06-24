__all__ = ['Player']

from abc import ABC, abstractmethod

from music_player.core.music.enums import PlaybackStatus, RepeatMode
from music_player.core.music.models import Track, TrackMetadata
from music_player.core.utils import EventManager


class Player(ABC):
    """
    A player is responsible for managing the queue and playing tracks.

    A player can be implemented in two ways:

    - As a local player that uses the device's speakers (or a bluetooth speaker connected to the device)
    - As a remote player that forwards the track URIs to another device (e.g., a hifi system)
    """

    _playback_status_change_event: EventManager[PlaybackStatus]
    _playback_error_event: EventManager[str]
    _track_change_event: EventManager[TrackMetadata]
    _position_change_event: EventManager[float]
    _volume_change_event: EventManager[float]

    def __init__(self) -> None:
        """Initialize the music player."""
        self._playback_status_change_event = EventManager()
        self._playback_error_event = EventManager()
        self._track_change_event = EventManager()
        self._position_change_event = EventManager()
        self._volume_change_event = EventManager()

    @abstractmethod
    def close(self) -> None:
        """Clean up resources."""

    # region Playback Control
    @abstractmethod
    def play(self) -> None:
        """
        Start or resume the playback.

        :raises QueueOutOfBoundsError: If the queue is empty.
        :raises AlreadyPlayingError: If a track is already playing.
        """

    @abstractmethod
    def pause(self) -> None:
        """
        Pause the playback.

        :raises NotPlayingError: If no track is playing.
        """

    @property
    @abstractmethod
    def status(self) -> PlaybackStatus:
        """
        Returns the current playback status.

        :return: Whether a track is currently playing.
        """

    # endregion

    # region Current Track Control
    @abstractmethod
    def next(self) -> None:
        """
        Jump to the next track in the queue.

        This will also start playback if it was paused.

        :raises QueueOutOfBoundsError: If there is no next track in the queue.
        """

    @property
    @abstractmethod
    def has_next(self) -> bool:
        """
        Check if there is a next track in the queue.

        :return: Whether there is a next track.
        """

    @abstractmethod
    def previous(self) -> None:
        """
        Jump to the previous track in the queue.

        This will also start playback if it was paused.

        :raises QueueOutOfBoundsError: If there is no previous track in the queue.
        """

    @property
    @abstractmethod
    def has_previous(self) -> bool:
        """
        Check if there is a previous track in the queue.

        :return: Whether there is a previous track.
        """

    @property
    @abstractmethod
    def index(self) -> int:
        """Get the index of the playing track."""

    @index.setter
    @abstractmethod
    def index(self, value: int) -> None:
        """
        Set the index of the playing track.

        :raises QueueOutOfBoundsError: When the given index is not in the queue.
        """

    @property
    @abstractmethod
    def current(self) -> TrackMetadata | None:
        """
        Get the metadata of the currently playing track.

        :return: The currently playing track or ``None`` if no track is playing.
        """

    # endregion

    # region Queue Management
    @property
    @abstractmethod
    def items(self) -> list[TrackMetadata]:
        """Get the metadata of all queued tracks."""

    @abstractmethod
    def __len__(self) -> int:
        """
        Get the number of tracks in the queue.

        :return: The number of tracks in the queue.
        """

    @abstractmethod
    def add(self, track: Track | list[Track]) -> None:
        """
        Add a track / list of tracks to the end of the queue.

        :param track: The track / list of tracks to add.
        """

    @abstractmethod
    def add_after_current(self, track: Track | list[Track]) -> None:
        """
        Add a track / list of tracks to the queue right after the current track.

        :param track: The track / list of tracks to add.
        """

    @abstractmethod
    def remove(self, track: Track) -> None:
        """
        Remove a track from the queue.

        :param track: The track to remove.
        :raises QueueOutOfBoundsError: If the track is not in the queue.
        """

    @abstractmethod
    def move(self, track: Track, to: int) -> None:
        """
        Move a track to a new index.

        :param track: The track to move.
        :param to: The new index for the track.
        :raises QueueOutOfBoundsError: If the track or the index are not in the queue.
        """

    @abstractmethod
    def clear(self) -> None:
        """Remove all tracks from the queue."""

    @property
    @abstractmethod
    def shuffle(self) -> bool:
        """
        Check if the queue is shuffled.

        :return: Whether the queue is shuffled.
        """

    @shuffle.setter
    @abstractmethod
    def shuffle(self, value: bool) -> None:
        """
        Set whether the queue should be shuffled.

        :param value: Whether the queue should be shuffled.
        """

    @property
    @abstractmethod
    def repeat(self) -> RepeatMode:
        """
        Check if the queue is set to repeat.

        :return: Whether the queue is set to repeat.
        """

    @repeat.setter
    @abstractmethod
    def repeat(self, value: RepeatMode) -> None:
        """
        Set the repeat mode for the queue.

        :param value: The new repeat mode. Can be 'off', 'one', or 'all'.
        """

    # endregion

    # region Player Control
    @property
    @abstractmethod
    def position(self) -> float | None:
        """
        Get the current playback position.

        :return: The current playback position in seconds or ``None``
                 if the track is continuous (e.g., a radio station).
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

    # region Event Getters
    @property
    def playback_status_change_event(self) -> EventManager[PlaybackStatus]:
        """Invoked when the playback status changes."""
        return self._playback_status_change_event

    @property
    def playback_error_event(self) -> EventManager[str]:
        """Invoked when an error occurs during playback."""
        return self._playback_error_event

    @property
    def track_change_event(self) -> EventManager[TrackMetadata]:
        """Invoked when the currently playing track changes."""
        return self._track_change_event

    @property
    def position_change_event(self) -> EventManager[float]:
        """Invoked when the playback position changes."""
        return self._position_change_event

    @property
    def volume_change_event(self) -> EventManager[float]:
        """Invoked when the volume changes."""
        return self._volume_change_event

    # endregion
