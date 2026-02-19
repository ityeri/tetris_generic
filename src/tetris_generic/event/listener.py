from typing import Callable

from tetris_generic.event.events import TetrisEvent


type Listener[T: TetrisEvent] = Callable[[T], None]

class ListenerManager:
    def __init__(self):
        self._listeners: dict[type[TetrisEvent], list[Listener]] = dict()

    def add_listener[T: TetrisEvent](self, event_type: type[T], listener: Listener[T]):
        self.get_listener_list(event_type).append(listener)

    def get_listener_list[T: TetrisEvent](self, event_type: type[T]) -> list[Listener[T]]:
        if event_type not in self._listeners:
            self._listeners[event_type] = list()

        return self._listeners[event_type]

    def call_event[T: TetrisEvent](self, event: T):
        for listener in self.get_listener_list(type(event)): listener(event)