__all__ = ['Player']

from abc import ABC, abstractmethod

from music_player.core.music.enums import PlaybackStatus, RepeatMode
from music_player.core.music.models import Playable, Track
from music_player.core.plugin_manager import BasePlugin, PluginContext
from music_player.core.utils import EventManager


class Player(BasePlugin, ABC):
    """
    A player is responsible for managing the queue and playing tracks.

    A player can be implemented in two ways:

    - As a local player that uses the device's speakers (or a bluetooth speaker connected to the device)
    - As a remote player that forwards the playable URIs to another device (e.g., a hifi system)
    """

    _playback_status_change_event: EventManager[PlaybackStatus]
    _playback_error_event: EventManager[Exception]
    _track_change_event: EventManager[Track]
    _position_change_event: EventManager[float]
    _volume_change_event: EventManager[float]

    def __init__(self, context: PluginContext) -> None:
        """Initialize the player."""
        super().__init__(context)

        self._playback_status_change_event = EventManager()
        self._playback_error_event = EventManager()
        self._track_change_event = EventManager()
        self._position_change_event = EventManager()
        self._volume_change_event = EventManager()

    def close(self) -> None:
        """Clean up resources."""

    # region Playback Control
    @abstractmethod
    def play(self) -> None:
        """
        Start or resume the playback.

        :raises QueueOutOfBoundsError: If the queue is empty.
        :raises AlreadyPlayingError: If ``status`` is ``PLAYING``.
        """

    @abstractmethod
    def pause(self) -> None:
        """
        Pause the playback.

        :raises NotPlayingError: If ``status`` is not ``PLAYING``.
        """

    @property
    @abstractmethod
    def status(self) -> PlaybackStatus:
        """
        Returns the current playback status.

        :return: The current playback status.
        """

    # endregion

    # region Current Queue Item Control
    @abstractmethod
    def next(self) -> None:
        """
        Jump to the next item in the queue.

        This will also start playback if it was paused.

        :raises QueueOutOfBoundsError: If there is no next item.
        """

    @property
    @abstractmethod
    def has_next(self) -> bool:
        """
        Check if there is a next item in the queue.

        :return: Whether there is a next item.
        """

    @abstractmethod
    def previous(self) -> None:
        """
        Jump to the previous item in the queue.

        This will also start playback if it was paused.

        :raises QueueOutOfBoundsError: If there is no previous item.
        """

    @property
    @abstractmethod
    def has_previous(self) -> bool:
        """
        Check if there is a previous item in the queue.

        :return: Whether there is a previous item.
        """

    @property
    @abstractmethod
    def index(self) -> int:
        """Get the index of the playing item."""

    @index.setter
    @abstractmethod
    def index(self, value: int) -> None:
        """
        Set the index of the playing item.

        :raises QueueOutOfBoundsError: When the given index is not in the queue.
        """

    @property
    @abstractmethod
    def current(self) -> Track | None:
        """
        Get the currently playing track.

        :return: The currently playing track or ``None`` if no track is playing.
        """

    # endregion

    # region Queue Management
    @property
    @abstractmethod
    def items(self) -> list[Playable]:
        """Get all queued items."""

    @abstractmethod
    def __len__(self) -> int:
        """
        Get the number of items in the queue.

        :return: The number of items in the queue.
        """

    @abstractmethod
    def add(self, playable: Playable | list[Playable]) -> None:
        """
        Add an item / list of items to the end of the queue.

        :param playable: The item(s) to add.
        """

    @abstractmethod
    def add_after_current(self, playable: Playable | list[Playable]) -> None:
        """
        Add an item / list of items to the queue after the current item.

        :param playable: The item(s) to add.
        """

    @abstractmethod
    def remove(self, playable: Playable) -> None:
        """
        Remove an item from the queue.

        :param playable: The item to remove.
        :raises QueueOutOfBoundsError: If the given item is not in the queue.
        """

    @abstractmethod
    def move(self, playable: Playable, to: int) -> None:
        """
        Move an item to a new index.

        :param playable: The item to move.
        :param to: The new index for the item.
        :raises QueueOutOfBoundsError: If the item or the index are not in the queue.
        """

    @abstractmethod
    def clear(self) -> None:
        """Remove all items from the queue."""

    @property
    @abstractmethod
    def shuffle(self) -> bool:
        """
        Return whether the queue is shuffled.

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
        Return the active repeat mode.

        :return: The repeat mode.
        """

    @repeat.setter
    @abstractmethod
    def repeat(self, value: RepeatMode) -> None:
        """
        Set the repeat mode.

        :param value: The repeat mode.
        """

    # endregion

    # region Player Control
    @property
    @abstractmethod
    def position(self) -> float | None:
        """
        Get the current playback position.

        :return: The current playback position in seconds or ``None``
                 if the currently playing item is e.g., a radio.
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
    def playback_error_event(self) -> EventManager[Exception]:
        """Invoked when an error occurs during playback."""
        return self._playback_error_event

    @property
    def track_change_event(self) -> EventManager[Track]:
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
