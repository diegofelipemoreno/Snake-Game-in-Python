import pygame
from store import Store

MESSAGE_IMG = "assets/modal.jpg"

class Message:
    """
    Initializes the Message component.
    """
    def __init__(self):   
        self.store = Store()

    def listen_events(self, callback):
      """
      Listens the key down events.

      Args:
      Function: callback The callback after the message is close.
      """
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
            self.store.is_game_over = True
            self.store.is_game_close = False

          if event.key == pygame.K_RETURN:
            callback()

    def render(self, matrix, text):
      """
      Renders the Message on the matrix.
        
      Args:
      Object: matrix The board matrix.
      String: text The text message to set on the matrix.
      """
      if not self.store.is_game_over:
        self.font = pygame.font.Font(None, 30)
        background_image = pygame.image.load(MESSAGE_IMG).convert_alpha()

        matrix.blit(background_image, (0, 0))
        pygame.display.update()

