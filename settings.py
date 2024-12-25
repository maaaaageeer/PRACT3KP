class Settings:
    """Класс для хранения настроек игры Alien Invasion."""

    def __init__(self):
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Настройки корабля
        self.ship_speed = 1.5
        self.health = 3

        # Настройки снарядов
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Настройки инопланетян
        self.alien_speed = (0.5, 0.2)
        self.alien_speed_increment = (0.1, 0.05)
        self.alien_kill_points = 15

        # Настройки бонусов
        self.bonus_speed = (0.1, 0.25)
        self.bonus_spawn_chance = 0.2
