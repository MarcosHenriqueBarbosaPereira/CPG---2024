import random
import sys

import pygame as pg

from src.character.farmer import Farmer
from src.contants import MAX_FPS
from src.scenary.grass import Grass
from src.utils.path import FileGetter
from src.settings import global_screen


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

        self._game_state = {
            "is_over": False
        }

        self._farmer = Farmer()
        self._setup()

    def is_running(self) -> bool:
        return self._running

    def stop(self):
        self._running = False

    def main_loop(self):
        index_of_farmer_animation = 0
        last_key_pressed = None

        random_grass_positions = []
        for _ in range(10):
            row = random.randrange(0, self.width)
            col = random.randrange(0, self.height)

            random_grass_positions.append((row, col))

        grass = Grass()

        while self.is_running():
            self._main_game_screen.fill((0, 0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.stop()
                elif event.type == pg.VIDEORESIZE:
                    self._resize()
                elif self._game_state["is_over"]:
                    pass
                elif event.type == pg.KEYDOWN:
                    index_of_farmer_animation += 1
                    if last_key_pressed != event.key:
                        last_key_pressed = event.key
                        index_of_farmer_animation = 0
                    elif index_of_farmer_animation >= self._farmer.total:
                        index_of_farmer_animation = 0

                    self.move(pg.key.name(event.key), index_of_farmer_animation)
            self._main_game_screen.blit(self._bg_image, (0, 0))

            self._farmer.draw(
                self._farmer.initial_sprite,
                self._main_game_screen,
                self._farmer.current_position[0],
                self._farmer.current_position[1],
                self._farmer.current_state
            )

            if self._game_state["is_over"]:
                self._show_loose_dialog_message('Game Over!')

                key = pg.key.get_pressed()
                if key[pg.K_SPACE]:
                    self._game_state["is_over"] = False

            pg.display.update()
            self._main_game_clock.tick(MAX_FPS)

    def move(self, key, index):
        speed_in_y = 0
        speed_in_x = 0

        match key:
            case 'down':
                speed_in_x = 0
                speed_in_y += self._farmer.speed
                self._farmer.initial_sprite = self._farmer.sprite_sheet.get('forward', None)
                self._farmer.last_dir = 'forward'
            case 'up':
                speed_in_x = 0
                speed_in_y -= self._farmer.speed
                self._farmer.initial_sprite = self._farmer.sprite_sheet.get('backward', None)
                self._farmer.last_dir = 'backward'
            case 'right':
                speed_in_x += self._farmer.speed
                self._farmer.initial_sprite = self._farmer.sprite_sheet.get('right', None)
                self._farmer.last_dir = 'right'
                speed_in_y = 0
            case 'left':
                speed_in_x -= self._farmer.speed
                self._farmer.initial_sprite = self._farmer.sprite_sheet.get('left', None)
                self._farmer.last_dir = 'left'
                speed_in_y = 0
            case _:
                return

        self._farmer.set_total_of_sprites()
        if self._farmer.total >= index:
            self._farmer.draw(
                self._farmer.initial_sprite,
                self._main_game_screen,
                self._farmer.current_position[0],
                self._farmer.current_position[1],
                self._farmer.current_state
            )

        if self._farmer.initial_sprite is None:
            self._farmer.initial_sprite = self._farmer.sprite_sheet.get(self._farmer.last_dir)
        else:
            self._farmer.current_position = (
                self._farmer.current_position[0] + speed_in_x,
                self._farmer.current_position[1] + speed_in_y
            )

            self._farmer.current_state = index

        collided = self.check_collision_with_borders(self._farmer.current_position)
        if collided:
            self._farmer.current_position = (
                self._farmer.current_position[0] - speed_in_x,
                self._farmer.current_position[1] - speed_in_y
            )
        else:
            pass

        self._farmer.draw(
            self._farmer.initial_sprite,
            self._main_game_screen,
            self._farmer.current_position[0],
            self._farmer.current_position[1],
            self._farmer.current_state
        )

    def check_collision_with_borders(self, farmer_position: tuple) -> bool:
        collided = False
        if farmer_position[0] > (self.width - 128) or farmer_position[0] < 0:
            self._game_over()
            collided = True
        elif farmer_position[1] > (self.height - 128) or farmer_position[1] < 0:
            self._game_over()
            collided = True

        return collided

    def _game_over(self):
        self._game_state["is_over"] = True

    def _show_loose_dialog_message(self, message):
        """ Function to display a popup message """

        red = (255, 0, 0)
        font = pg.font.Font("src/assets/fonts/EaseOfUse.ttf", 50)
        width, height = self._main_game_screen.get_size()
        screen = pg.display.set_mode((width, height))
        popup_surface = pg.Surface((400, 200))

        text_surface = font.render(message, True, red)
        text_rect = text_surface.get_rect(center=(200, 100))
        popup_surface.blit(text_surface, text_rect)
        screen.blit(popup_surface, (width // 2 - 200, height // 2 - 100))
        pg.display.update()

    def _setup(self):
        pg.init()

        # set initial values for configurations
        self._main_game_screen = global_screen
        self._main_game_clock = pg.time.Clock()

        self._running = True

        # configuring
        pg.display.set_caption(self.window_title)

        self._load_assets()

    def _load_assets(self):
        self._bg_image = pg.image.load(
            self._assets.get_filepath("img\grass background.jpg")
        )

        self._resize()

    def _resize(self):
        current_size = self._main_game_screen.get_size()

        self._bg_image = pg.transform.scale(self._bg_image, current_size)

    @property
    def size(self):
        return self._main_game_screen.get_size()

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]
