import pygame as pg

from src.contants import MAX_FPS
from src.utils.path import FileGetter


class WeedReaper:
    def __init__(
        self,
        window_title: str,
        window_height: int,
        window_width: int,
    ):
        self.window_title = window_title

        self._size = (window_width, window_height)
        self._running = False

        self._assets = FileGetter("assets")

        self._setup()

    def is_running(self) -> bool:
        return self._running

    def stop(self):
        self._running = False

    def main_loop(self):
        while self.is_running():
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.stop()
                elif event.type == pg.VIDEORESIZE:
                    self._resize()

            self._main_game_screen.blit(self._bg_image, (0, 0))
            pg.display.flip()

            self._main_game_clock.tick(MAX_FPS)

    def _setup(self):
        pg.init()

        # set initial values for configurations
        self._main_game_screen = pg.display.set_mode(self._size, pg.RESIZABLE)
        self._main_game_clock = pg.time.Clock()

        self._running = True

        # configuring
        pg.display.set_caption(self.window_title)

        self._load_assets()

    def _load_assets(self):
        self._bg_image = pg.image.load(
            self._assets.get_filepath("grass background.jpg")
        )

    def _resize(self):
        current_size = self._main_game_screen.get_size()

        self._bg_image = pg.transform.scale(self._bg_image, current_size)

    @property
    def size(self):
        return self._size

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]
