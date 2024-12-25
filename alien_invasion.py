import os
import pickle
import random

import pygame
from pygame.mixer import Sound

from bonus import Medkit, Shield
from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        self.score = 0
        self.level = 0
        self.ship = Ship(self)
        self.shoot_sound = Sound(os.path.join('resources', 'laser.wav'))
        self.enemy_death_sound = Sound(os.path.join('resources', 'enemy_died.wav'))
        self.damage_sound = Sound(os.path.join('resources', 'damage.wav'))
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.health = self.settings.health
        self.shield = False

        self.game_active = True
        self.running = False

    def run_game(self):
        """Запуск основного цикла игры."""
        self._create_fleet()
        self.running = True

        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bonuses()
                self._update_bullets()
                self._update_aliens()
                self._check_bullet_alien_collisions()
            self._update_screen()

    def spawn_bonus(self):
        rand = random.random()
        if rand > 0.5:
            bonus = Medkit(self)
        else:
            bonus = Shield(self)
        x = random.random() * self.screen.get_width()
        bonus.x = x
        bonus.y = 50
        self.bonuses.add(bonus)

    def save_game(self, filename='savegame.pkl'):
        """Сохраняет текущий уровень, очки и здоровье в файл."""
        game_data = {
            "level": self.level,
            "score": self.score,
            "health": self.health,
            "shield": self.shield
        }
        with open(filename, "wb") as file:
            pickle.dump(game_data, file)
        print("Игра сохранена!")

    def load_game(self, filename='savegame.pkl'):
        """Загружает сохраненные данные игры."""
        try:
            with open(filename, "rb") as file:
                game_data = pickle.load(file)
                self.level = game_data["level"]
                self.score = game_data["score"]
                self.health = game_data["health"]
                self.shield = game_data['shield']

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            print("Игра загружена!")
        except FileNotFoundError:
            print("Файл сохранения не найден!")

    def _check_events(self):
        """Обрабатывает события клавиатуры и мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:
            self.save_game()  # Сохранение игры
        elif event.key == pygame.K_l:
            self.load_game()  # Загрузка игры
        elif event.key == pygame.K_q:
            self.running = False

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bonuses(self):
        self.bonuses.update()

        for bonus in self.bonuses:
            if bonus.rect.colliderect(self.ship.rect):
                bonus.apply()
                self.bonuses.remove(bonus)
            elif bonus.rect.top >= self.settings.screen_height:
                self.bonuses.remove(bonus)
                break

    def _fire_bullet(self):
        """Создаёт новый снаряд и добавляет его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.shoot_sound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и удаляет старые снаряды."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Создаёт флот инопланетян."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создаёт одного инопланетянина и помещает его в ряд."""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Проверяет, достиг ли флот края, и обновляет позиции всех инопланетян."""
        self.aliens.update()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._damage()
                break

    def _damage(self):
        self.damage_sound.play()
        if not self.shield:
            self.health -= 1
        self.shield = False
        self.aliens.empty()
        if self.health <= 0:
            self.game_active = False
        else:
            self._create_fleet()

    def _check_bullet_alien_collisions(self):
        """Обрабатывает столкновение пуль с пришельцами."""
        killed = len(pygame.sprite.groupcollide(self.bullets, self.aliens, True, True))
        self.score += killed * self.settings.alien_kill_points

        if killed:
            self.enemy_death_sound.play()
            if random.random() <= self.settings.bonus_spawn_chance:
                self.spawn_bonus()
            if not self.aliens:
                self.level += 1
                self.bullets.empty()
                self._create_fleet()

    def _update_screen(self):
        """Обновляет изображение на экране и переключается на новый экран."""
        self.screen.fill(self.settings.bg_color)

        if self.game_active:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.bonuses.draw(self.screen)

            # Отображение здоровья
            font = pygame.font.SysFont(None, 36)
            if self.shield:
                health_text = f"Здоровье: {self.health} (+1)"
            else:
                health_text = f"Здоровье: {self.health}"
            health_surface = font.render(health_text, True, (0, 255, 0))
            health_rect = health_surface.get_rect()
            health_rect.topright = (self.settings.screen_width - 50, 50)
            self.screen.blit(health_surface, health_rect)
        else:
            font = pygame.font.SysFont(None, 48)
            message = f"Игра окончена! Ваш счёт: {self.score}"
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
