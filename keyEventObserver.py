import pygame
import sys, os

class KeyEventObserver:
  def __init__(self):
    """
    Initializes the KeyEventObserver.
    """
    self.observers = []
    self._event_type = None
    self.is_game_over = False
    self.matrix = None

  @property
  def event_type(self):
    return self._event_type

  @event_type.setter
  def event_type(self, value):
    self._event_type = value
    self._update_observers()

  def add(self, observer):
    self.observers.append(observer)

  def remove(self, observer):
    self.observers.remove(observer)

  def _update_observers(self):
    for observer in self.observers:
      observer()

  def listen_events(self, pygame):
    """
    Listens the board events.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.event_type = "QUIT"

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
              self.event_type = "KEY_LEFT"

          if event.key == pygame.K_RIGHT:
              self.event_type = "KEY_RIGHT"

          if event.key == pygame.K_UP:
              self.event_type = "KEY_UP"

          if event.key == pygame.K_DOWN:
              self.event_type = "KEY_DOWN"

  def run(self):
    """
    Initializes the KeyEventObserver.
    """
    pygame.init()
    self.matrix=pygame.display.set_mode((400,300))
    pygame.display.update()
    pygame.display.set_caption('Snake game by Edureka')
    game_over=False

    while not game_over:
        self.listen_events()

    pygame.quit()
    quit()