from typing import Literal

import pygame as pg

from src.utils.path import FileGetter


grass_images = {}


class Grass:
    def __init__(self):
        self.initial_state_index = 0
        self._sprites = FileGetter("sprites")

        self._load_image()

    def _load_image(self):
        global grass_images
        if "grass_1" in grass_images and "grass_2" in grass_images:
            return

        for grass_model in range(1, 3, 1):
            grass_images[f'grass_{grass_model}'] = [
                pg.image.load(
                    self._sprites.get_filepath(f'Grass {grass_model}-{_ + 1}.png')
                ).convert_alpha() for _ in range(5)
            ]

    def draw(self, screen: pg.Surface, model: Literal["grass_1", "grass_2"], y: int, x: int):
        global grass_images
        screen.blit(grass_images[model][self.initial_state_index], (x, y))

    def move_grass(self):
        self.initial_state_index += 1

        if self.initial_state_index >= 5:
            self.initial_state_index = 0

