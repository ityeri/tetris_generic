from typing import Callable

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

from tetris_generic import TetrisGame, ControlType

type KeyListener = Callable[[ControlType], None]
type KeyType = Keys | str

class KeyMap:
    def __init__(self, game: TetrisGame, key_map: dict[ControlType, list[tuple[KeyType]]]):
        self.game: TetrisGame = game
        self.key_map: dict[ControlType, list[tuple[KeyType]]] = key_map
        self.listeners: list[KeyListener] = list()

    def get_keys(self, control_type: ControlType) -> list[tuple[Keys]]:
        if control_type not in self.key_map:
            self.key_map[control_type] = []

        return self.key_map[control_type]

    def trigger_control(self, control_type: ControlType):
        self.game.trigger_control(control_type)
        for listener in self.listeners:
            listener(control_type)

    def on_key(self) -> Callable[[KeyListener], None]:
        def wrapper(listener: KeyListener):
            self.listeners.append(listener)

        return wrapper

    def create_key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        for control_type, keys in self.key_map.items():
            control_handler = lambda event, ct=control_type: self.trigger_control(ct)

            for key in keys:
                kb.add(*key)(control_handler)

        return kb
