from src.character import character
import pygame as pg



class Boss(character.Character):
    def __init__(self, x, y):
        super().__init__()

        self.current_state = 0
        self.current_position = (x, y)
        self.size = (200, 200)

        self._config_character_status()

        self.load_sprite_sheet("move", "Boss", 5)

        self.initial_sprite = self.sprite_sheet["move"][0]

        self.hitbox = pg.Rect(self.current_position, self.size)

    def _config_character_status(self):
        self.speed = 1
        self.strength = 350
        self.life = 1000

    def update_position(self, farmer_position):
        # Atualiza a posição do inimigo para perseguir o Farmer
        farmer_x, farmer_y = farmer_position
        enemy_x, enemy_y = self.current_position

        if enemy_x < farmer_x:
            enemy_x += self._speed
        elif enemy_x > farmer_x:
            enemy_x -= self._speed

        if enemy_y < farmer_y:
            enemy_y += self._speed
        elif enemy_y > farmer_y:
            enemy_y -= self._speed

        self.current_state += 1

        if self.current_state >= 5:
            self.current_state = 0

        self.current_position = (enemy_x, enemy_y)

        if self.hitbox is not None:
            self.update_hitbox()
