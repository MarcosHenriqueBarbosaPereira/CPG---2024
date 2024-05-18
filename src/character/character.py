from abc import abstractmethod

import pygame as pg

from src.utils.path import FileGetter


class Character:
    def __init__(self):
        self._life = 1000
        self._strength = 10
        self._speed = 1

        self.sprite_sheet = {}

        self._sprites = FileGetter('sprites')
        self.last_dir = 'forward'

        self._config_character_status()

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

    @staticmethod
    def draw(
        sprite_sheet_config: list,
        surface: pg.Surface,
        x: int,
        y: int,
        index_of_cells: int
    ):
        if sprite_sheet_config is not None:
            surface.blit(
                sprite_sheet_config[index_of_cells],
                (x, y,),
            )

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

