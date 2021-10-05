import pygame
from time import perf_counter
from store import Store

SNAKE_HEAD_IMG = "assets/snake.png"
SNAKE_HEAD_DEAD_IMG = "assets/snakedead.png"
SNAKE_HEAD_EAT_IMG = "assets/snakeeat.png"
SNAKE_BODY_COLOR = (51, 175, 255)
MINIMUM_PIXEL_SIZE = 20
MINIMUM_SNAKE_LENGTH_TO_EAT_ITSELF = 4
MINIMUM_SMALL_SNAKE_LENGTH = 6
MINIMUM_SNAKE_LENGTH_TO_MOVE = 1
MOVING_BACK_UNITS = 2

class Snake:
    """
    Initializes the Snake component.

    Args:
    Object: config The board configuration.
    """
    def __init__(self, config):
        self.pixel_size = config.get("pixel_size")
        self.direction = None
        self.has_eaten = False
        self.coordinates = []
        self.store = Store()
        self.is_near_to_food = False

    def save_Length(self):
        """
        Saves the snake's length on the store.
        """
        self.store.snake_length += 1 

    def get_coord_by_pixel_size(self, coord):
        """
        Gets a valid coordinate according the pixel size.
        
        Args:
        number: coord The axis coord.
        Returns: Number
        """
        return round(coord/self.pixel_size) * self.pixel_size

    def add_size(self, x, y, food_x, food_y):
        """
        Increases the snake length when it passed on a food coordinate range.
        
        Args:
        number: x The current snake x coordinate on the matrix.
        number: y The current snake x coordinate on the matrix.
        number: food_x The current food x coordinate on the matrix.
        number: food_y The current food y coordinate on the matrix.
        """
        x_coord = self.get_coord_by_pixel_size(x)
        y_coord = self.get_coord_by_pixel_size(y)
        is_passed_on_x = x_coord == food_x
        is_passed_on_y = y_coord == food_y
        self.has_eaten = False

        self.check_is_near_to_food(x, y, food_x, food_y)

        if is_passed_on_x and is_passed_on_y:
            self.coordinates.extend([
                [x_coord, y_coord],
            ])

            self.has_eaten = True
            self.save_Length()

    def check_is_near_to_food(self, x, y, food_x, food_y):
        """
        Checks is near to the food coordinates.
        
        Args:
        number: x The current snake x coordinate on the matrix.
        number: y The current snake x coordinate on the matrix.
        number: food_x The food x coordinate position.
        number: food_y The food y coordinate position.
        """
        is_near_on_x = (x - self.pixel_size) <= food_x and (x + self.pixel_size) >= food_x
        is_near_on_y = (y - self.pixel_size) <= food_y and (y + self.pixel_size) >= food_y
        
        self.is_near_to_food = is_near_on_x and is_near_on_y

    def set_movement(self, x, y):
        """
        Sets the coordinates to generate the snake's movement.
        
        Args:
        number: x The snake x coordinate position.
        number: y The snake x coordinate position.
        """
        temp_x = round(x/self.pixel_size) * self.pixel_size
        temp_y = round(y/self.pixel_size) * self.pixel_size

        if len(self.coordinates) > MINIMUM_SNAKE_LENGTH_TO_MOVE:
            del self.coordinates[0]
        self.coordinates.append([temp_x, temp_y])
        self._get_move_direction()

    def is_prev_food_on_snake(self, body_coord, prev_food_coord):
        """
        Checks if the prev food coordinates is on the snake list coordinates range.
        
        Args:
        List: body_coord The snake's body coordinates.
        List: prev_food_coord The previous food coordinates.

        returns Boolean
        """
        is_food_on_x = (
            body_coord[0] - self.pixel_size/2) <= prev_food_coord[0] and (
            body_coord[0] + self.pixel_size/2) >= prev_food_coord[0]
        is_food_on_y = (
            body_coord[1] - self.pixel_size/2) <= prev_food_coord[1] and (
            body_coord[1] + self.pixel_size/2) >= prev_food_coord[1]

        return is_food_on_x and is_food_on_y

    def is_moving_back(self, x, y):
        """
        Checks if the snake is moving back.
        
        Args:
        number: x The snake's x coordinate.
        number: y The snakes's y coordinate.

        returns Boolean
        """
        moving_back_flag = False

        if len(self.coordinates) > 1 and self.coordinates[-MOVING_BACK_UNITS] == [x, y]:
            moving_back_flag = True
        
        return moving_back_flag


    def is_eat_itself(self, prev_food_coord):
        """
        Checks if the snake eats itself.
        
        Args:
        List: prev_food_coord The previous food coordinates.
        returns Boolean
        """
        eat_itself_flag = False
    
        if len(self.coordinates) > MINIMUM_SNAKE_LENGTH_TO_EAT_ITSELF:
            snake_body = self.coordinates[:-1]
            snake_head = self.coordinates[-1]
 
            for i in snake_body:
                if i == snake_head and not self.is_prev_food_on_snake(i, prev_food_coord):
                    eat_itself_flag = True

                    return eat_itself_flag
        
        return eat_itself_flag

    def _get_move_direction(self):
        """
        Gets the current snake direction.
        """
        if len(self.coordinates):
            snake_body = self.coordinates[:-1]
            snake_head = self.coordinates[-1]
            head_x_coord = snake_head[0]
            head_y_coord = snake_head[1]

            if snake_body:
                if head_x_coord > snake_body[-1][0]:
                    self.direction = "RIGHT"
                elif head_x_coord < snake_body[-1][0]:
                    self.direction = "LEFT"
                elif head_y_coord > snake_body[-1][1]:
                    self.direction = "DOWN" 
                elif head_y_coord < snake_body[-1][1]:
                    self.direction = "UP"

    def set_body_direction(self, body_section):
        """
        Sets the snake's head position according its direction.

        Args:
        Object: body_section The snake's body part image object.

        Returns: Object
        """
        if self.direction == "UP":
            body_section = pygame.transform.rotate(body_section, 180)
        
        if self.direction == "RIGHT":
            body_section = pygame.transform.rotate(body_section, 90)
        
        if self.direction == "DOWN":
            body_section = pygame.transform.rotate(body_section, 0)
        
        if self.direction == "LEFT":
            body_section = pygame.transform.rotate(body_section, -90)
    
        return body_section

    def get_images_dict(self):
        """
        Gets the snake heads images.

        returns Object
        """     
        head_img = pygame.image.load(SNAKE_HEAD_IMG).convert_alpha()
        head_img = self.set_body_direction(head_img)
        head_img.convert() 
        
        head_dead_img = pygame.image.load(SNAKE_HEAD_DEAD_IMG).convert_alpha()
        head_dead_img = self.set_body_direction(head_dead_img)
        head_dead_img.convert()

        head_eat_img = pygame.image.load(SNAKE_HEAD_EAT_IMG).convert_alpha()
        head_eat_img = self.set_body_direction(head_eat_img)
        head_eat_img.convert()

        return {
            "head": head_img,
            "head_dead": head_dead_img,
            "head_eat": head_eat_img,
        } 

    def restart_coord(self, matrix):
        """
        Sets the initial snake position on the ground matrix.

        Args: Object: matrix The ground's matrix.
        """
        self.coordinates = [
            [self.store.ground_dimensions[0]/2, self.store.ground_dimensions[1]/2]
        ]

    def set_body_img_on_matrix(self, body_part, coord, matrix):
        """
        Sets the snake's head, head dead, body and tail on the matrix.

        Args:
        String: body_part The snake body part.
        Tuple: coord The body part x,y coord.
        Object: matrix The ground's matrix.
        """   
        images_dict = self.get_images_dict()
        rectangle = images_dict[body_part].get_rect(topleft=(coord[0] - 10, coord[1] - 10))
        
        matrix.blit(images_dict[body_part], rectangle)

    def render(self, matrix):
        """
        Renders the snake's head, body and tail on the ground.

        Args:
        Tuple: default_coord The snake initial coordinates.
        Object: matrix The ground's matrix.
        """
        snake_length = len(self.coordinates)

        for idx, coord in enumerate(self.coordinates):
            body_size = self.pixel_size - (snake_length - idx)
            body_diameter = [coord[0], coord[1], body_size, body_size]

            if  body_size < MINIMUM_PIXEL_SIZE:
              body_diameter = [coord[0], coord[1], MINIMUM_PIXEL_SIZE, MINIMUM_PIXEL_SIZE] 

            if coord == self.coordinates[-1]:
                if self.store.is_snake_dead:
                  self.set_body_img_on_matrix("head_dead", coord, matrix)
                elif self.is_near_to_food:
                   self.set_body_img_on_matrix("head_eat", coord, matrix) 
                else:
                  self.set_body_img_on_matrix("head", coord, matrix)                  
            else:
                pygame.draw.rect(matrix, SNAKE_BODY_COLOR, body_diameter) 
