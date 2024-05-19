import uuid

import pygame as pg

from src.utils.path import FileGetter


class Tree:
    def __init__(self, name: str):
        self._assets = FileGetter("assets")
        self.tree = pg.image.load(
            self._assets.get_filepath(name)
        )

        self._hit_box = None

    def draw(
        self,
        screen: pg.Surface,
        x: int,
        y: int,
    ):
        screen.blit(self.tree, (x, y))

        self._hit_box = pg.Rect((x, y), self.tree.get_size())


class Bush:
    def __init__(self):
        self.current_position = None
        self._assets = FileGetter("assets")
        self.tree = pg.image.load(
            self._assets.get_filepath("img/bush.png")
        )

        self.id = str(uuid.uuid4())

        self.hitbox = None

    def draw(
        self,
        screen: pg.Surface,
        x: int,
        y: int,
    ):
        screen.blit(self.tree, (x, y))

        self.hitbox = pg.Rect((x, y), self.tree.get_size())
        self.current_position = (x, y)
