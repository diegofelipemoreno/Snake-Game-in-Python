
import pygame
import random
from store import Store

FOOD_IMG = "assets/apple.png"

class Food:
    """
    Initializes the Food component.

    Args:
    Object: config The Food configuration.
    """
    def __init__(self, config):
        self.color = config["color"]
        self.pixel_size = config["pixel_size"]
        self.x = 0       
        self.y = 0
        self.prev_x = 0       
        self.prev_y = 0
        self.store = Store()
        self.food_img = pygame.image.load(FOOD_IMG)

    def get_random_coord(self):
        """
        Gets the x,y random coordinates.

        Returns: List
        """
        random_x = round(random.randrange(self.store.ground_margins[0] + (self.pixel_size * 2), self.store.ground_dimensions [0] - (self.pixel_size * 3)))
        random_y = round(random.randrange(self.store.ground_margins[1] + (self.pixel_size * 2), self.store.ground_dimensions [1] - (self.pixel_size * 3)))

        return [round(random_x/self.pixel_size) * self.pixel_size, round(random_y/self.pixel_size) * self.pixel_size]

    def add_coord(self, snake_coord):
        """
        Adds the food coordinates on the matrix.
        """
        random_coord = self.get_random_coord()
        is_food_on_snake_body = [random_coord[0], random_coord[1]] in snake_coord

        if is_food_on_snake_body:
            self.add_coord(snake_coord)
            return

        self.prev_x = self.x       
        self.prev_y = self.y
        self.x = random_coord[0]
        self.y = random_coord[1]

    def render(self, matrix):
        """
        Renders the food on the board.
        
        Args:
        Object: matrix The board matrix.
        """
        self.food_img.convert()
        rectangle = self.food_img.get_rect(topleft=(self.x, self.y))
    
        matrix.blit(self.food_img, rectangle)

