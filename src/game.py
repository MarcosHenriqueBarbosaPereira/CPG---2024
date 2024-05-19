import random
import sys

import pygame as pg

from datetime import datetime, timedelta
from src.character.farmer import Farmer
from src.character.enemy import Enemy
from src.contants import MAX_FPS
from src.scenary.grass import Grass
from src.scenary.tree import Tree
from src.utils.path import FileGetter
from src.settings import global_screen


class WeedReaper:
    def __init__(
        self,
        window_title: str,
        window_height: int,
        window_width: int,
        main_menu: callable
    ):
        self.main_menu = main_menu
        self.window_title = window_title

        self._size = (window_width, window_height)
        self._running = False
        self._invincible_timer = datetime.now()

        self._assets = FileGetter("assets")

        self._game_state = {
            "is_over": False,
            "is_paused": False,
            "is_started": False,
            "grass_positions": [],
            "tree_positions": [],
            "bush_positions": []
        }

        self._farmer = Farmer()
        self._enemy = [Enemy() for _ in range(5)]
        self._setup()

    def is_running(self) -> bool:
        return self._running

    def stop(self):
        self._running = False

    def restart_game(self):
        """ Reset game state to initial values """
        self._game_state["is_over"] = False
        self._farmer.current_position = (self.width // 2, self.height // 2)
        self._farmer.current_state = 0

    def main_loop(self):
        index_of_farmer_animation = 0
        last_key_pressed = None

        self._generate_random_positions("grass_positions")
        self._generate_random_positions("tree_positions", 10)
        self._generate_random_positions("bush_positions", 12)
        grass = Grass()
        tree = Tree("Arvore.png")
        bush = Tree("Arbusto.png")

        def _move_character(keyname: str):
            nonlocal index_of_farmer_animation
            nonlocal last_key_pressed

            index_of_farmer_animation += 1
            if last_key_pressed != keyname:
                last_key_pressed = keyname
                index_of_farmer_animation = 0
            elif index_of_farmer_animation >= self._farmer.total:
                index_of_farmer_animation = 0

            self.move(keyname, index_of_farmer_animation)

        is_attacking = False
        allowed_keys_to_attack = ["right", "left", "up", "down", "forward", "backward"]
        while self.is_running():
            self._main_game_screen.fill((0, 0, 0))

            keys = pg.key.get_pressed()
            if (
                keys[pg.K_DOWN] or
                keys[pg.K_UP] or
                keys[pg.K_RIGHT] or
                keys[pg.K_LEFT]
            ) and not self._game_state["is_over"]:
                if keys[pg.K_DOWN]:
                    keyname = "down"
                elif keys[pg.K_UP]:
                    keyname = "up"
                elif keys[pg.K_RIGHT]:
                    keyname = "right"
                elif keys[pg.K_LEFT]:
                    keyname = "left"
                else:
                    raise KeyError()

                _move_character(keyname)
            self._main_game_screen.blit(self._bg_image, (0, 0))

            self.generate_object_by_position_list(
                "grass_positions",
                grass
            )
            grass.move_grass()

            self.generate_object_by_position_list("tree_positions", tree)
            self.generate_object_by_position_list("bush_positions", bush)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.stop()
                elif event.type == pg.VIDEORESIZE:
                    self._resize()
                elif self._game_state["is_over"]:
                    pass
                elif event.type == pg.KEYDOWN:
                    key = getattr(event, 'key', None)
                    if key is not None:
                        keyname = pg.key.name(key)
                        if keyname == "space" and last_key_pressed in allowed_keys_to_attack:
                            is_attacking = True
                            if last_key_pressed == 'down':
                                last_key_pressed = 'backward'
                            elif last_key_pressed == 'up':
                                last_key_pressed = 'forward'

                            if last_key_pressed is not None:
                                self._farmer.attack(self._main_game_screen, last_key_pressed)
                        else:
                            _move_character(pg.key.name(key))

            if not is_attacking:
                self._farmer.draw(
                    self._farmer.initial_sprite,
                    self._main_game_screen,
                    self._farmer.current_position[0],
                    self._farmer.current_position[1],
                    self._farmer.current_state
                )

            for enemy in self._enemy:
                enemy.update_position(self._farmer.current_position)
                enemy.draw(
                    enemy.sprite_sheet["move"],
                    self._main_game_screen,
                    enemy.current_position[0],
                    enemy.current_position[1],
                    enemy.current_state
                )

                if self._farmer.check_collision(enemy) and self._farmer.life > 0 and datetime.now() - self._invincible_timer > timedelta(seconds=1):
                    self._farmer.life -= enemy.strength
                    self._invincible_timer = datetime.now()

                    print(self._farmer.life)

                    if self._farmer.life <= 0:
                        self._game_state["is_over"] = True

            if self._game_state["is_over"]:
                self._show_loose_dialog_message()
                self._farmer.life = 1000

                key = pg.key.get_pressed()
                if key[pg.K_SPACE]:
                    self.restart_game()
                elif key[pg.K_ESCAPE]:
                    self.stop()
                    self.main_menu

            pg.display.update()
            is_attacking = False
            self._main_game_clock.tick(MAX_FPS)

    def generate_object_by_position_list(self, key_of_list: str, object_to_draw):
        for pos in self._game_state[key_of_list]:
            if isinstance(object_to_draw, Grass):
                object_to_draw.draw(self._main_game_screen, "grass_1", pos[1], pos[0])
            else:
                object_to_draw.draw(self._main_game_screen, pos[1], pos[0])

    def generate_grass(self, grass_positions: list, grass: Grass):
        for pos in grass_positions:
            grass.draw(self._main_game_screen, "grass_1", pos[1], pos[0])

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
        margin = 64

        if (
            farmer_position[0] > (self.width - margin) or
            farmer_position[0] < 0 or
            farmer_position[1] > (self.height - margin) or
            farmer_position[1] < 0
        ):
            self._game_over()
            collided = True

        return collided

    def _generate_random_positions(self, key_of_state: str, quantity_of_grass: int = 100):
        self._game_state[key_of_state] = []

        for _ in range(quantity_of_grass):
            row = random.randrange(0, self.width)
            col = random.randrange(0, self.height)

            self._game_state[key_of_state].append((row, col))

    def _game_over(self):
        self._game_state["is_over"] = True

    def _show_loose_dialog_message(self):
        """ Function to display a popup message inside game screen """

        width, height = self._main_game_screen.get_size()

        font = pg.font.Font("src/assets/fonts/EaseOfUse.ttf", 50)
        font_small = pg.font.Font("src/assets/fonts/EaseOfUse.ttf", 20)

        text_game_over = font.render("Game Over", True, (255, 0, 0))
        text_game_over_rect = text_game_over.get_rect(center=(width // 2, height // 2 - 50))

        text_retry = font_small.render("Press SPACE to Retry or ESC to quit", True, (255, 255, 255))
        text_retry_rect = text_retry.get_rect(center=(width // 2, height // 2 + 20))

        self._main_game_screen.blit(text_game_over, text_game_over_rect)
        self._main_game_screen.blit(text_game_over, text_game_over_rect)
        self._main_game_screen.blit(text_retry, text_retry_rect)
        pg.display.flip()

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
            self._assets.get_filepath("img/grass-background.png")
        )

        self._resize()

    def _resize(self):
        current_size = self._main_game_screen.get_size()

        self._generate_random_positions("grass_positions")
        self._generate_random_positions("tree_positions", 10)
        self._generate_random_positions("bush_positions", 12)
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
