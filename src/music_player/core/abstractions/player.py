from abc import ABC, abstractmethod
from dataclasses import dataclass

from music_player.core.utils.event_listener import EventListener

@dataclass(frozen=True)
class PositionChangeEvent:
    """Event triggered when the playback position changes."""

    position: float
    """Current playback position in seconds."""


class Player(ABC):
    """Abstract base class for a music player."""

    position_change_event: EventListener[PositionChangeEvent]

    @abstractmethod
    def play(self, track_uri: str):
        """Play the specified track."""

    @abstractmethod
    def pause(self):
        """Pause the currently playing track."""

    @abstractmethod
    def resume(self):
        """Resume the currently paused track."""

    @abstractmethod
    def stop(self):
        """Stop the currently playing track."""
