import abc
import os
from abc import ABC

import pygame
from pygame.sprite import Sprite


class Bonus(Sprite, ABC):

    def __init__(self, ai_game, image):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.game = ai_game
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = list(self.settings.bonus_speed)

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect.x = self.x
        self.rect.y = self.y

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            self.speed[0] *= -1

    @abc.abstractmethod
    def apply(self):
        pass


class Medkit(Bonus):

    def __init__(self, ai_game):
        super().__init__(ai_game, os.path.join('resources', 'medkit.bmp'))

    def apply(self):
        self.game.health = min(self.game.health + 1, self.settings.health)


class Shield(Bonus):

    def __init__(self, ai_game):
        super().__init__(ai_game, os.path.join('resources', 'shield.bmp'))

    def apply(self):
        self.game.shield = True