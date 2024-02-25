__package__ = "ArcherGame"
import pygame
from enum import Enum
import math

WHITE = (255, 255, 255)
GRAY = (227, 228, 221)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHTGRAY = (240, 240, 240)
DARKGRAY = (100, 100, 100)

class ArrowStates(Enum):
    READY = 1
    FIRED = 2
    MOVING = 3


class Archer(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.num_frames = 5
        self.frame_width, self.frame_height = self.image.get_width() // 5, self.image.get_height()
        self.frames = self.get_frames(self.image, self.frame_width, self.frame_height, self.num_frames)
        self.current_frame = 0
        self.animation_speed = 5  # Adjust this value to control the speed of the animation
        self.animation_counter = 0
    
    def get_frames(self, image, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames
    
    def reset(self):
        self.current_frame = 0
        self.animation_counter = 0
    
    def animate(self):        
        if self.animation_counter >= self.animation_speed:
            self.current_frame += 1
            self.animation_counter = 0  # Reset counter after updating frame
        self.animation_counter += 1
    
    def draw(self, screen):
        screen.blit(self.frames[self.current_frame - 1], self.position)
    
        

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.position = position
        self.starting_position = position
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 10
        self.arrow_state = ArrowStates.READY
        self.num_arrows = 10  # Number of arrows per game
        
    def initial_update(self):
        if self.arrow_state == ArrowStates.MOVING:
            self.position = self.starting_position
    
    def update(self):
        if self.arrow_state == ArrowStates.MOVING:
            (x,y) = self.position
            self.position = (x + self.speed, y)
            self.rect = self.image.get_rect(topleft=self.position)
    
    def reset(self):
        arrow_state = ArrowStates.READY
        self.position = self.starting_position
    
    def decrement_arrows(self):
        self.num_arrows -= 1
        
    def fire(self):
        self.arrow_state = ArrowStates.FIRED
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
class ArrowMarker(pygame.sprite.Sprite):
    def __init__(self, position, color):
        super().__init__()
        self.position = position
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=position)
        self.color = color
        pygame.draw.circle(self.image, self.color, (2, 2), 2)
    
class Target(pygame.sprite.Sprite):
    def __init__(self, position, radius):
        super().__init__()
        colors = [WHITE, BLACK, BLUE, RED, YELLOW]
        self.position = position
        self.radius = radius
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=position)
        for i, color in enumerate(colors):
            pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius - i * 10)
        # draw a black line around the outer edge of the target
        pygame.draw.circle(self.image, BLACK, (self.radius, self.radius), self.radius, 1)
        # draw a black circle outline inside the smallest circle of the target
        pygame.draw.circle(self.image, BLACK, (self.radius, self.radius), self.radius * 0.1, 1)    
        

        
    def draw(self, screen):       
            screen.blit(self.image, self.rect)
    
    def get_mark_color(self, hit_deviation):
        # Function to determine the color of the mark based on the hit deviation
        if abs(hit_deviation) <= self.radius * 0.2:  # Bullseye (Yellow)
            return BLACK  # Black mark for visibility
        elif abs(hit_deviation) <= self.radius * 0.4:  # Red
            return LIGHTGRAY  # White or grey mark for visibility
        elif abs(hit_deviation) <= self.radius * 0.6:  # Blue
            return LIGHTGRAY  # Black mark should be visible on blue
        elif abs(hit_deviation) <= self.radius * 0.8:  # BLACK
            return LIGHTGRAY  # Black mark should be visible on blue
        else:  # Black or White ring
            return DARKGRAY  # White mark for visibility on blac
            
    def calculate_score(self, deviation):
        abs_deviation = abs(deviation)
        if abs_deviation <= self.radius * 0.1:  # Bullseye
            return 10
        if abs_deviation <= self.radius * 0.2:  # Yellow
            return 9
        elif abs_deviation <= self.radius * 0.4: # Red
            return 7
        elif abs_deviation <= self.radius * 0.6: # Blue
            return 5
        elif abs_deviation <= self.radius: # Black
            return 2
        else:
            return 1  # white ring

class Stand(pygame.sprite.Sprite):
        def __init__(self, image, position, width, height):
            super().__init__()
            colors = [WHITE, BLACK, BLUE, RED, YELLOW]
            self.position = position
            self.width = width
            self.height = height
            self.image = image
            self.rect = self.image.get_rect(center=position)

        def draw(self, screen):       
                screen.blit(self.image, self.rect)   
        
class MovingBar (pygame.sprite.Sprite):
    def __init__(self, position, width, height):
        super().__init__()
        # Bar settings
        self.bar_width,  self.bar_height = 200, 20
        self.bar_x,  self.bar_y = (width - self.bar_width) // 2, height - 50
        self.button_width,  self.button_height = 20, 20
        self.button_x,  self.button_y = self.bar_x, self.bar_y
        self.button_direction = 1
        self.button_increment = 0
        
        
        self.button_position = [  
    1.0,          2.02248126,   3.11218166,   4.31316746,
   5.66839299,   7.21927146,   9.00526119,  11.06347135,
  13.42829116,  16.1310463 ,  19.19968592,  22.65850337,
  26.52789347,  30.82414874,  35.5592966 ,  40.74097919,
  46.37237704,  52.45217726,  58.97458669,  65.92938974,
  73.3020505 ,  81.07385797,  89.222113  ,  97.7203551 ,
 106.53862682, 115.64377309, 124.99977248, 134.56809712,
 144.30809765, 154.17740939, 164.13237562, 174.1284838 ,
 184.12459198, 194.07955821, 203.94886995, 213.68887048,
 223.25719512, 232.61319451, 241.71834078, 250.5366125 ,
 259.0348546 , 267.18310963, 274.9549171 , 282.32757786,
 289.28238091, 295.80479034, 301.88459056, 307.51598841,
 312.697671  , 317.43281886, 321.72907413, 325.59846423,
 329.05728168, 332.1259213 , 334.82867644, 337.19349625,
 339.25170641, 341.03769614, 342.58857461, 343.94380014,
 345.14478594, 346.23448634, 347.2569676 , 348.2569676 ]

      
    def update(self):
        self.button_increment += self.button_direction
       
        if (self.button_increment < 0): 
            self.button_increment = 0
            self.button_direction = 1
            
        if  self.button_increment > len(self.button_position) - 1: 
            self.button_increment = len(self.button_position) - 1
            self.button_direction = -1

        self.button_x = int (self.bar_x +  float(self.button_position[self.button_increment]) * float(self.bar_width) / 385.0)
        
    
    
    def draw(self, screen):
            # Draw the moving bar
        pygame.draw.rect(screen, BLUE, (self.bar_x, self.bar_y, self.bar_width, self.bar_height))
        pygame.draw.rect(screen, GREEN, (self.button_x, self.button_y, self.button_width, self.button_height))


class GameText (pygame.sprite.Sprite):
    def __init__(self, text, font_size, color, position):
        super().__init__()
        self.text = text
        self.position = position
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.SysFont(None, self.font_size)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.position)
    
    def update_text(self, text):
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.position)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

