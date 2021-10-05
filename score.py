import pygame
from store import Store

SCORE_IMG = "assets/scorebk.jpg"

class Score:
    """
    Initializes the Score component.

    Args:
    Object: config The Score configuration.
    """
    def __init__(self, config):
        self.dimensions = config.get("dimensions")
        self.color = config["color"]
        self.size = config["size"]
        self.font = None
        self.store = Store()
        self.score_value = self.store.snake_length
        self.x = self.dimensions[0]
        self.y = self.dimensions[1]

    def render(self, matrix):
        """
        Renders the score on the board.
        
        Args:
        Object: matrix The board matrix.
        """
        self.score_value = self.store.snake_length
        background_image = pygame.image.load(SCORE_IMG).convert()
        self.font = pygame.font.Font(None, self.size)
        score = self.font.render(str(self.score_value), True, self.color)

        matrix.blit(background_image, (0, -10))
        matrix.blit(score, (650, 20))