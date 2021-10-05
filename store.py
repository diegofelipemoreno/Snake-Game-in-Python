class Store:
  _singleton = None
  def __new__(cls, *args, **kwargs):
    if not cls._singleton:
      cls._singleton = super(Store, cls).__new__(cls, *args, **kwargs)
    return cls._singleton

  def __init__(self):
    self._show_intro = True
    self._is_game_started = False
    self._is_game_over = False
    self._snake_length = 1
    self._is_snake_dead = False
    self._is_game_close = False
    self.ground_dimensions = (0, 0)
    self.ground_margins = (0, 0)

  @property
  def show_intro(self):
      return self._show_intro

  @property
  def is_game_started(self):
      return self._is_game_started

  @property
  def is_game_over(self):
      return self._is_game_over

  @property
  def snake_length(self):
      return self._snake_length

  @property
  def is_snake_dead(self):
      return self._is_snake_dead

  @property
  def is_game_close(self):
      return self._is_game_close

  @show_intro.setter
  def show_intro(self, value):
    self._show_intro = value

  @is_game_started.setter
  def is_game_started(self, value):
    self._is_game_started = value

  @is_game_over.setter
  def is_game_over(self, value):
    self._is_game_over = value

  @snake_length.setter
  def snake_length(self, value):
    self._snake_length = value

  @is_snake_dead.setter
  def is_snake_dead(self, value):
    self._is_snake_dead = value

  @is_game_close.setter
  def is_game_close(self, value):
    self._is_game_close = value