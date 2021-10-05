import pygame
import time
from store import Store
from ground import Ground
from score import Score
from snake import Snake
from food import Food
from message import Message
from intro import Intro

class Game:
  def __init__(self, ground):
    """
    Game component constructor.

    Args:
    Object: config The ground component.
    """
    self.ground = ground

  def run(self):
    """
    Renders the game board.
    """
    pygame.init()
    self.ground.run()
    pygame.quit()
    quit()


def run_game():
    ground_config = {
       "pixel_size": 32,
       "dimensions": (730, 544),
       "margins":  (0, 64),
    }

    snake_config = {
        "pixel_size": 32
    }

    food_config = {
        "color": (255, 0, 0),
        "pixel_size": 32
    }

    score_config = {
        "color": (255,255,255),
        "size": 56,
        "dimensions": (100, 100)
    }

    my_score = Score(score_config)
    my_snake = Snake(snake_config)
    my_food = Food(food_config)
    my_ground = Ground(config=ground_config, snake=my_snake, food=my_food, score=my_score, message=Message(), intro=Intro())
    my_game = Game(ground=my_ground)

    my_game.run()

if __name__=='__main__':
    run_game()