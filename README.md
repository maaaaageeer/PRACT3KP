# Создаю MD файл отчета

md_content = """
# Практическая работа №3: Развитие игры “Инопланетное вторжение”

## Цель работы

Дополнить базовую игру “Инопланетное вторжение” функциональностью, которая сделает игровой процесс более увлекательным и технологичным.

### Основные дополнения:
- Звуковые эффекты.
- Система уровней.
- Сохранение и загрузка прогресса.
- Интерактивные объекты с бонусами.
- Сборка игры в исполняемый файл.

---

## Этапы выполнения

### 1. **Добавление звуковых эффектов**

#### Задача:
Добавить звуковые эффекты для:
- Выстрелов (`laser.wav`).
- Уничтожения врагов (`enemy_died.wav`).
- Получения урона (`damage.wav`).

#### Реализация:
- Подготовлены звуковые файлы в формате `.wav`.
- Использован модуль `pygame.mixer`:
  ```python
  self.shoot_sound = Sound(os.path.join('resources', 'laser.wav'))
  self.shoot_sound.play() ```

- Звуковые эффекты связаны с игровыми событиями:
    - Звук выстрела (`laser.wav`) проигрывается при создании объекта снаряда.
    - Звук уничтожения инопланетянина (`enemy_died.wav`) проигрывается при удалении объекта пришельца:
        
      ```  python
      
        
        if killed:     self.enemy_death_sound.play()
        
    - Звук получения урона (`damage.wav`) проигрывается, если инопланетянин достигает нижней границы или сталкивается с кораблем:
        
      ```  python
        
  
        
        self.damage_sound.play()
        

### 2. Система уровней

#### Реализация:

- Введена переменная `self.level` для отслеживания текущего уровня игры:
    
    ```python
    

    
    self.level = 0```
    
- Сложность игры увеличивается с каждым уровнем:
    - Скорость движения инопланетян увеличивается:
        
       ``` python
        
        
        self.speed[0] += self.settings.alien_speed_increment[0] * self.level self.speed[1] += self.settings.alien_speed_increment[1] * self.level
        
    - Переход на новый уровень осуществляется после уничтожения всего флота:
        
        ```python
        
      
        
        if not self.aliens:     self.level += 1     self._create_fleet()
        
    - Позиции снарядов обнуляются:
        
        ```python
        
     
        
        self.bullets.empty()
        

### 3. Сохранение и загрузка прогресса

#### Реализация:

- Для сериализации данных использован модуль `pickle`.
- Создана структура данных для сохранения:
    
    ```python
    
   
    
    game_data = {     "level": self.level,     "score": self.score,     "health": self.health,     "shield": self.shield }
    
- Добавлены методы сохранения и загрузки:
    - Сохранение игры:
        
        ```python
        
   
        
        def save_game(self, filename='savegame.pkl'):     with open(filename, "wb") as file:         pickle.dump(game_data, file)
        
    - Загрузка игры:
        
       ``` python
        
       
        
        def load_game(self, filename='savegame.pkl'):     with open(filename, "rb") as file:         game_data = pickle.load(file)         self.level = game_data["level"]         self.score = game_data["score"]         self.health = game_data["health"]         self.shield = game_data["shield"]```
        
- Сохранение вызывается по нажатию клавиши `S`, а загрузка — по клавише `L`:
    
    ```python
    
    
    elif event.key == pygame.K_s:     self.save_game() elif event.key == pygame.K_l:     self.load_game()
    

### 4. Интерактивные объекты

#### Реализация:

- Создан базовый класс `Bonus` для интерактивных объектов:
    
    ```python
    
    Копировать код
    
    class Bonus(Sprite, ABC):     def __init__(self, ai_game, image):         self.image = pygame.image.load(image)         self.rect = self.image.get_rect()
    
- Добавлены классы `Medkit` и `Shield`, которые наследуются от `Bonus`:
    - `Medkit` увеличивает здоровье:
        
        ```python
        
        
        def apply(self):     self.game.health = min(self.game.health + 1, self.settings.health)
        
    - `Shield` временно защищает корабль:
        
       ``` python
        
      
        
        def apply(self):     self.game.shield = True
        
- Реализован метод появления бонусов с вероятностью:
    
    ```
    
    
    def spawn_bonus(self):     if random.random() <= self.settings.bonus_spawn_chance:         bonus = Medkit(self) if random.random() > 0.5 else Shield(self)         self.bonuses.add(bonus)
    

### 5. Сборка игры в исполняемый файл

#### Реализация:

1. Установлен инструмент `PyInstaller`:
    
    ```bash
    
   
    
    pip install pyinstaller
    
2. Создана структура проекта:
    
    
    
    
    
    ```project/ ├── main.py ├── resources/ │   ├── ship.bmp │   ├── alien.bmp │   ├── medkit.bmp │   ├── shield.bmp │   ├── laser.wav │   └── enemy_died.wav```
    
3. Для Windows создан скрипт сборки:
    
    ```bat
    
  
    
    @echo off pyinstaller --onefile --add-data "resources;resources" main.py
    
4. Для macOS/Linux:
    
    ```bash
    
  
    pyinstaller --onefile --add-data "resources:resources" main.py
    
5. Исполняемый файл размещён в папке `dist`.

### Итоги работы:

- Реализована базовая игра "Инопланетное вторжение" с расширенной функциональностью.
- Добавлены звуковые эффекты, уровни сложности, интерактивные бонусы, сохранение/загрузка прогресса.
- Созданы исполняемые файлы для различных операционных систем.
