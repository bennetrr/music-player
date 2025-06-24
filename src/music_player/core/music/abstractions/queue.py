__all__ = ['Queue', 'RepeatMode']

from abc import ABC, abstractmethod
from typing import Literal

from music_player.core.music.abstractions.player import Player
from music_player.core.music.models import Track, TrackMetadata

type RepeatMode = Literal['off', 'one', 'all']


class Queue(ABC):
    """
    Abstract base class for a track queue.

    A queue manages which track is currently playing and which tracks will play next.
    It is also responsible for resolving the ``Track`` objects into actual URIs before playing them.

    The actual playback is handled by a ``Player`` implementation.
    An exception to this are remote music players, which likely have their own queue.
    In this case, the queue should be synchronized with the remote player.
    """

    @abstractmethod
    def __init__(self, player: Player) -> None:
        """Initialize the queue with a player."""

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
    def is_playing(self) -> bool:
        """
        Check if a track is currently playing.

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
        Get the currently playing track.

        :return: The currently playing track or ``None`` if no track is playing.
        """

    # endregion

    # region Queue Management
    @property
    @abstractmethod
    def items(self) -> list[TrackMetadata]:
        """Get all tracks that are in the queue."""

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

        :return: The current playback position in seconds or ``None`` if the track is continuous (e.g. a radio station).
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

    # endregion
