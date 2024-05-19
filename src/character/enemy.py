from src.character import character
import pygame as pg


class Enemy(character.Character):
    def __init__(self):
        super().__init__()

        self.current_state = 0
        self.current_position = (0, 0)
        self.size = (100, 100)

        self._config_character_status()

        self.load_sprite_sheet("move", "Mordedora", 5)

        self.initial_sprite = self.sprite_sheet["move"][0]

        self.hitbox = pg.Rect(self.current_position, self.size)

    def _config_character_status(self):
        self.speed = 3
        self.strength = 50

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
        self.update_hitbox()
