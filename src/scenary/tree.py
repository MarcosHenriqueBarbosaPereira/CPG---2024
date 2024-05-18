import pygame as pg

from src.utils.path import FileGetter


class Tree:
    def __init__(self, name: str):
        self._assets = FileGetter("assets")
        self.tree = pg.image.load(
            self._assets.get_filepath(name)
        )

    def draw(
        self,
        screen: pg.Surface,
        x: int,
        y: int,
    ):
        screen.blit(self.tree, (x, y))


