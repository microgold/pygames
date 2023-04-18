import pygame
from ImageSprite import ImageSprite
from BombSprite import BombSprite


class InvaderSprite(pygame.sprite.Sprite):
    def __init__(self, name1, name2, x, y, parent, points, level = 1):      
        super().__init__()  
        self.imageSprite1 = ImageSprite(name1, x, y)
        self.imageSprite2 = ImageSprite(name2, x, y)
        self.explosion =    ImageSprite('explosion', x, y)
        self.imageSprite = self.imageSprite1
        self.parent = parent
        self.speed = .01 * (.9 + level/10.0)
        self.currentDirection = 'right'
        self.position = (x, y)
        self.rect = self.imageSprite.image.get_rect().move(self.position)
        self.dead = False
        self.death_time = 0
        self.bomb_active = False
        self.points = points

    # update the position of the 2 sprites representing the alien
    def update(self):
        self.imageSprite.rect = self.imageSprite.image.get_rect().move(self.position)
        self.imageSprite1.rect = self.imageSprite.rect
        self.imageSprite2.rect = self.imageSprite.rect

    # Draw the sprite on the screen

    def draw(self, surface):
        self.imageSprite.draw(surface)

    def move_left(self):
        (x, y) = self.position
        self.position = (x - self.speed, y)

    def move_right(self):
        (x, y) = self.position
        self.position = (x + self.speed, y)
    
    def move_down(self):
        (x, y) = self.position
        self.position = (x, y + 10)
    
    # switch between the 2 images representing the alien
    def switch_image(self, imageNumber):
        if self.dead == True: return
        if (imageNumber == 1):
            self.imageSprite = self.imageSprite1
        else:
            self.imageSprite = self.imageSprite2

    def get_width(self):
        return self.imageSprite.get_width()

    def get_height(self):
        return self.imageSprite.get_height()
    
    def kill(self):
        self.imageSprite = self.explosion
        self.imageSprite.draw(self.imageSprite.image)
        self.imageSprite.update()
        self.dead = True
        self.death_time = pygame.time.get_ticks()

    