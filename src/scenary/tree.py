import uuid
import random
import pygame as pg

from src.utils.path import FileGetter


class Tree:
    def __init__(self):
        self.current_position = (random.randrange(100, 1160), random.randrange(100, 620))
        self.size = (100,100)
        self._assets = FileGetter("assets/img")
        self.tree = pg.image.load(
            self._assets.get_filepath("tree.png")
        )

        self.hitbox = pg.Rect(self.current_position, self.size)

    def draw(
        self,
        screen: pg.Surface,
        x: int,
        y: int,
    ):
        screen.blit(self.tree, (x, y))

        # self._hitbox = pg.Rect((x, y), self.tree.get_size())
        self.current_position = (x, y)


class Bush:
    def __init__(self):
        self.current_position = None
        self._assets = FileGetter("assets/img")
        self.tree = pg.image.load(
            self._assets.get_filepath("bush.png")
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