import os

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс для представления одного инопланетянина."""

    def __init__(self, ai_game):
        """Инициализирует инопланетянина и задаёт его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load(os.path.join('resources', 'alien.bmp'))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = list(self.settings.alien_speed)
        self.speed[0] += self.settings.alien_speed_increment[0] * ai_game.level
        self.speed[1] += self.settings.alien_speed_increment[1] * ai_game.level

    def update(self):
        """Перемещает инопланетянина."""
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect.x = self.x
        self.rect.y = self.y

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            self.speed[0] *= -1