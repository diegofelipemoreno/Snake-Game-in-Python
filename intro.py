import pygame
from store import Store

INTRO_IMG = "assets/intro.jpg"

class Intro:
    """
    Initializes the Intro component.
    """
    def __init__(self):   
        self.store = Store()

    def render(self, matrix):
      """
      Renders the Message on the matrix.
        
      Args:
      Object: matrix The board matrix.
      """
      if self.store.show_intro:
        intro_image = pygame.image.load(INTRO_IMG).convert()

        matrix.blit(intro_image, (320, -5))
        pygame.display.update()

