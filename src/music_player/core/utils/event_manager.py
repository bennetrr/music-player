__all__ = ['EventManager']

from collections.abc import Callable


class EventManager[TPayload]:
    """Class for managing event listeners."""

    type TListener = Callable[[TPayload], None]  # type: ignore[valid-type]
    _listeners: list[TListener]

    def __init__(self) -> None:
        """Initialize the event manager."""
        self._listeners = []

    def listen(self, listener: TListener) -> None:
        """Add a listener to the event manager."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unlisten(self, listener: TListener) -> None:
        """Remove a listener from the event manager."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def invoke(self, payload: TPayload) -> None:
        """Invoke all listeners with the given payload."""
        for listener in self._listeners:
            listener(payload)
