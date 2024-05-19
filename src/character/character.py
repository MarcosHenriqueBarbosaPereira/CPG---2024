from abc import abstractmethod

import pygame as pg

from src.utils.path import FileGetter


class Character:
    def __init__(self):
        self._life = 1000
        self._strength = 10
        self._speed = 1

        self.size = (100, 100)
        self.current_position = (0, 0)

        self.sprite_sheet = {}

        self._sprites = FileGetter('sprites')
        self.last_dir = 'forward'

        self._config_character_status()

        self.hitbox = pg.Rect(self.current_position, self.size)

        self.last_sprite_on_screen = None

    def update_hitbox(self):
        self.hitbox.topleft = self.current_position

    def load_sprite_sheet(
        self,
        sheet_key: str,
        sprite_sheet: str = None,
        total_of_images: int = None,
    ):
        self.sprite_sheet[sheet_key] = [
            pg.image.load(
                self._sprites.get_filepath(f'{sprite_sheet}-{index + 1}.png')
            ) for index in range(total_of_images)
        ]

    def load_sprite_sheet_attack(
        self,
        sheet_key: str,
        sprite_sheet: str = None,
        total_of_images: int = None,
    ):
        self.sprite_sheet[f"{sheet_key}_attack"] = [
            pg.image.load(
                self._sprites.get_filepath(f'{sprite_sheet}{index}.png')
            ) for index in range(total_of_images)
        ]

    def draw(
        self,
        sprite_sheet_config: list,
        surface: pg.Surface,
        x: int,
        y: int,
        index_of_cells: int
    ):
        try:
            sprite = surface.blit(
                sprite_sheet_config[index_of_cells],
                (x, y,),
            )

            self.last_sprite_on_screen = sprite

            if self.hitbox is not None:
                self.update_hitbox()
        except IndexError:
            pass

    def check_collision(self, other):
        return self.hitbox.colliderect(other.hitbox)

    def check_collision_by_coordinate(self, x: float, y: float, size: tuple[float, float]):
        return self.hitbox.colliderect(x, y, size[0], size[1])

    @abstractmethod
    def _config_character_status(self):
        raise NotImplementedError()

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, life):
        self._life = life

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, strength):
        self._strength = strength

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
