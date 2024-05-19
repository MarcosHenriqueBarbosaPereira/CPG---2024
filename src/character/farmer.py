import pygame as pg


from src.character.character import Character
from src.exceptions import UnknownMovement
from src.settings import global_screen


class Farmer(Character):
    def __init__(self):
        super().__init__()
        self.total = 0

        self.current_position = (global_screen.get_width() / 2, global_screen.get_height() / 2)
        self.current_state = 0
        self.size = (128, 128)

        self._possible_movements = ['forward', 'backward', 'left', 'right']
        self._sprite_sheet = ['Weed Reaper Front', 'Weed Reaper Back', 'Weed Reaper Left', 'Weed Reaper Right']
        self._total_of_sprites = [13, 13, 9, 9]

        self.hitbox = pg.Rect(self.current_position, self.size)

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

        self._possible_movements = ['right', 'left', 'forward', 'backward']
        self._sprite_sheet = ['attack/Attack Right', 'attack/Attack Left', 'attack/Attack Back',
                              'attack/Attack Front']
        self._total_of_sprites = 5

        for possible_attack, sprite_sheet in zip(
            self._possible_movements,
            self._sprite_sheet
        ):
            self.load_sprite_sheet_attack(
                possible_attack,
                sprite_sheet,
                self._total_of_sprites
            )

        self.initial_sprite = self.sprite_sheet['forward']

    def _config_character_status(self):
        self.speed = 34
        self.strength = 0.3

        self._max_of_life = self.life

    def attack(self, screen: pg.Surface, keyname):
        images_of_attack = self.sprite_sheet[f"{keyname}_attack"]
        x = self.current_position[0] - 64
        y = self.current_position[1] - 64

        for image in images_of_attack:
            screen.blit(image, (x, y))
            pg.display.flip()

    def set_total_of_sprites(self):
        match self.last_dir:
            case 'forward':
                self.total = 13
            case 'backward':
                self.total = 13
            case 'right':
                self.total = 9
            case 'left':
                self.total = 9

    @property
    def max_of_life(self):
        return self._max_of_life
