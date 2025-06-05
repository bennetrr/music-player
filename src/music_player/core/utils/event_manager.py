"""Class for managing events."""

__all__ = ['EventManager']

from collections.abc import Callable


class EventManager[TEvent]:
    """Class for managing event listeners."""

    type TListener = Callable[[TEvent], None]  # type: ignore[valid-type]
    _listeners: list[TListener]

    def __init__(self) -> None:
        """Initialize the event manager."""
        self._listeners = []

    def listen(self, listener: TListener) -> None:
        """Add a listener to the event manager."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove(self, listener: TListener) -> None:
        """Remove a listener from the event manager."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def invoke(self, event: TEvent) -> None:
        """Invoke all listeners with the given event."""
        for listener in self._listeners:
            listener(event)
