import pygame as pg

from src.character.actions import Movement
from src.character.character import Character
from src.exceptions import UnknownMovement


class Farmer(Character):
    def __init__(self):
        super().__init__()
        self.total = 0

        self.current_position = (0, 0)
        self.current_state = 0

        self._possible_movements = ['forward', 'backward', 'left', 'right']
        self._sprite_sheet = ['Weed Reaper Front', 'Weed Reaper Back', 'Weed Reaper Left', 'Weed Reaper Right']  # , 'Weed Reaper Back']
        self._total_of_sprites = [13, 13, 9, 9]

        for possible_movement, sprite_sheet, total in zip(
            self._possible_movements,
            self._sprite_sheet,
            self._total_of_sprites
        ):
            self.load_sprite_sheet(
                possible_movement,
                sprite_sheet,
                total
            )

        self.initial_sprite = self.sprite_sheet['forward']

    def _config_character_status(self):
        self.speed = 1 * self.size()
        self.strength = 0.3

    def size(self):
        return 34

    def move(self, to: Movement):
        match to:
            case Movement.FORWARD:
                self._move_forward()
            case Movement.BACKWARD:
                self._move_backward()
            case Movement.LEFT:
                self._move_forward()
            case Movement.RIGHT:
                self._move_right()
            case _:
                raise UnknownMovement(to)

    def _move_forward(self):
        pass

    def _move_backward(self):
        pass

    def _move_left(self):
        pass

    def _move_right(self):
        pass

    def set_total_of_sprites(self):
        print(self.last_dir)
        match self.last_dir:
            case 'forward':
                self.total = 13
            case 'backward':
                self.total = 13
            case 'right':
                self.total = 9
            case 'left':
                self.total = 9

        print(self.total)
