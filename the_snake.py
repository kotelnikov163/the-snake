from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Координаты центра экрана:
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет обьектов:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
# Розовый,  если забыли передать цвет.
DEFAULT_COLOR = (255, 0, 255)

# Скорость движения змейки:
SPEED = 20
# Настройка игрового окна:
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject():
    """Базовый класс всех игровых объектов на поле."""

    def __init__(self, body_color=DEFAULT_COLOR):
        """Инициализирует базовые параметры объекта."""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw_cell(self, position, color=None, draw_border=True):
        """Отрисовывает одну ячейку(квадрат) в заданной позиции."""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)

        if draw_border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод отрисовки."""
        raise NotImplementedError('Метод draw должен быть переопределен!')


class Apple(GameObject):
    """Класс яблока, которое собирает змейка."""

    def __init__(self, positions=None):
        """Инициализирует яблоко и задает ему случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)

        self.randomize_position(positions)

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position)

    def randomize_position(self, positions=None):
        """Устанавливает случайную позицию, избегая занятых клеток."""
        if positions is None:
            positions = [self.position]

        while True:
            x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in positions:
                break


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(self):
        """Инициализирует змейку и сбрасывает ее в начальное состояние."""
        super().__init__(body_color=SNAKE_COLOR)

        self.reset()

    def reset(self):
        """Сбрасывает змейку в центр."""
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет текущее направление движения на основе ввода."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку."""
        if self.last:
            self.draw_cell(self.last,
                           BOARD_BACKGROUND_COLOR,
                           draw_border=False)

        self.draw_cell(self.get_head_position())

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_x = (head_x + delta_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры, запускающая игровой цикл."""
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:

        # Тик времени
        clock.tick(SPEED)

        # Обработка нажатия
        handle_keys(snake)

        # Обновление направления
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Определение столкновений
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
