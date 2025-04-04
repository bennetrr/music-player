from collections.abc import Callable


class EventListener[TEvent]:
    type TListener = Callable[[TEvent], None]
    _listeners: list[TListener]

    def __init__(self):
        self._listeners = []

    def add_listener(self, listener: TListener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: TListener):
        if listener in self._listeners:
            self._listeners.remove(listener)

    def call(self, event: TEvent):
        for listener in self._listeners:
            listener(event)
