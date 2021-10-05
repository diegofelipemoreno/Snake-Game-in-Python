import pygame
import time
import pdb
from store import Store

BOARD_IMG = "assets/board.jpg"
LOSE_MESSAGE = "You Lost! Press Enter to play Again"
SNAKE_SPEED = 8

class Ground:
  def __init__(self, config, snake, food, score, message, intro):
    """
    Initializes the ground component.

    Args:
    Object: config The Ground configuration.
    """
    self.dimensions = config.get("dimensions")
    self.margins = config.get("margins")
    self.matrix = pygame.display.set_mode(self.dimensions)
    self.pixel_size = config.get("pixel_size")
    self.x = 0
    self.y = 0
    self.x_change = 0       
    self.y_change = 0
    self.board_img = None
    self.score = score
    self.food = food
    self.snake = snake
    self.store = Store()
    self.message = message
    self.intro = intro
    self.clock = pygame.time.Clock()

  def init_matrix(self):
    """
    Initializes the Game matrix.
    """
    self.matrix = pygame.display.set_mode(self.dimensions)
    self.board_img = pygame.image.load(BOARD_IMG)
    self.render()
    self.listen_events()

  def _set_default_coord(self):
    """
    Sets the ground center x, y coordinates by default.
    """
    self.x = round((self.dimensions[0]/2)/self.pixel_size) * self.pixel_size
    self.y = round((self.dimensions[1]/2)/self.pixel_size) * self.pixel_size

  def keydown_event_handler(self, key_down_type):
    """
    Handles the ground keydown event actions when the ground game is running.

    Args:
    string: key_down_type The type event key.
    """
    if key_down_type == pygame.K_LEFT:
        is_snake_back_left = self.snake.is_moving_back(self.x - self.pixel_size, self.y)
        self.x_change = self.pixel_size if is_snake_back_left else - self.pixel_size 
        self.y_change = 0

    if key_down_type == pygame.K_RIGHT:
        is_snake_back_right = self.snake.is_moving_back(self.x + self.pixel_size, self.y)
        self.x_change = -self.pixel_size if is_snake_back_right else self.pixel_size
        self.y_change = 0

    if key_down_type == pygame.K_UP:
        is_snake_back_up = self.snake.is_moving_back(self.x, self.y - self.pixel_size)
        self.x_change = 0
        self.y_change = self.pixel_size if is_snake_back_up else - self.pixel_size

    if key_down_type == pygame.K_DOWN:
        is_snake_back_down = self.snake.is_moving_back(self.x, self.y + self.pixel_size)
        self.x_change = 0
        self.y_change = - self.pixel_size if is_snake_back_down else self.pixel_size   
  
  def is_matrix_coord_available(self):
    """
    Validates if the current coordinates are valid on the matrix,
    they doesn't hit the boundaries of the screen or the snake itself.

    Returns: Boolean
    """
    is_valid_coord = True
    if self.x >= self.dimensions[0] - (self.pixel_size * 2) or self.x - self.margins[0] <= self.pixel_size :
        is_valid_coord = False

    if self.y >= self.dimensions[1] - (self.pixel_size * 2) or self.y - self.margins[1] <= self.pixel_size :
        is_valid_coord = False

    return is_valid_coord

  def listen_events(self):
    """
    Listens all the ground events.
    """
    while not self.store.is_game_over:
      while self.store.is_game_close:
        self.message.render(self.matrix, LOSE_MESSAGE)
        self.message.listen_events(self.run)
        
      self.listen_board_events()

      if self.is_matrix_coord_available():
        self.x += self.x_change
        self.y += self.y_change
 
        self.snake.add_size(self.x, self.y, self.food.x, self.food.y)

        if self.snake.has_eaten:
          self.food.add_coord(self.snake.coordinates)

        self.snake.set_movement(self.x, self.y)
        self.render()
      else:
        self.game_close_handler()
      
      if self.snake.is_eat_itself([self.food.prev_x, self.food.prev_y]):
        self.game_close_handler()
      
      self.clock.tick(SNAKE_SPEED)  
  
  def listen_board_events(self):
    """
    Listens the pygame events when the ground game is running.
    """
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.store.is_game_over = True
      if event.type == pygame.KEYDOWN: 
        self.keydown_event_handler(event.key)
        
        self.store.show_intro = False
        self.store.is_game_started = True

  def game_close_handler(self):
    """
    Handles the ground game, when the state 'game_close' is on True.
    """
    self.store.is_game_close = True
    self.store.is_snake_dead = True
    self.store.is_game_started = False
    self.render()
    time.sleep(1.5)
    self.restart()   

  def restart(self):
    """
    Restarts the ground game with the values by default.
    """
    self.store.is_snake_dead = False
    self.store.is_game_over = False
    self.store.is_game_started = True
    self.x_change = 0
    self.y_change = 0
    self.store.snake_length = 1

    self.snake.restart_coord(self.matrix)

  def render(self):
    """
    Renders the ground game.
    """
    self.board_img.convert().get_rect(topleft=(self.x, self.y))
    self.matrix.blit(self.board_img, self.margins)
    self.snake.render(self.matrix)
    self.food.render(self.matrix)
    self.score.render(self.matrix)
    self.intro.render(self.matrix)
    pygame.display.update()

  def run(self):
    """
    Initializes the ground game.
    """
    self.store.is_game_over = False
    self.store.is_game_close = False
    self.store.ground_dimensions = self.dimensions
    self.store.ground_margins = self.margins

    self.food.add_coord(self.snake.coordinates)
    self._set_default_coord()
    self.init_matrix()

