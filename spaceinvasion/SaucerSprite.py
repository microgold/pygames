import random
import pygame
from ImageSprite import ImageSprite


class SaucerSprite(pygame.sprite.Sprite):
    def __init__(self, name1, name2, name3, x, y, level = 1):      
        super().__init__()  
        self.active = False
        self.imageSprite1 = ImageSprite(name1, x, y)
        self.imageSprite2 = ImageSprite(name2, x, y)
        self.imageSprite3 = ImageSprite(name3, x, y)
        self.imageSprite  = self.imageSprite1
        self.explosion = pygame.font.Font(None, 32)
        self.imageSprite = self.imageSprite1
        self.points =  random.randint(1, 6) * 50
        self.saucerScore = self.explosion.render(str(self.points), True, (255, 255, 255))
        self.speed = .05 * (.9 + level/10.0)
        self.position = (x, y)
        self.rect = self.imageSprite.image.get_rect().move(self.position)
        self.dead = False
        self.death_time = 0

    def reset(self, x, y, level = 1):
        self.imageSprite = self.imageSprite1
        self.points =  random.randint(1, 6) * 50
        self.saucerScore = self.explosion.render(str(self.points), True, (255, 255, 255))
        self.speed = .05 * (.9 + level/10.0)
        self.currentDirection = 'left'
        self.position = (x, y)
        self.rect = self.imageSprite.image.get_rect().move(self.position)
        self.dead = False
        self.death_time = 0

    # update the position of the 2 sprites representing the alien
    def update(self):
        self.rect = self.imageSprite.rect
        if self.dead == True: return
        self.imageSprite.rect = self.imageSprite.image.get_rect().move(self.position)
        self.imageSprite1.rect = self.imageSprite.rect
        self.imageSprite2.rect = self.imageSprite.rect
        self.imageSprite3.rect = self.imageSprite.rect
        self.rect = self.imageSprite.rect

    # Draw the sprite on the screen

    def draw(self, surface):
        if self.dead == True:
            surface.blit(self.saucerScore, self.rect)
        else:
            self.imageSprite.draw(surface)

    def move_left(self):
        if self.dead == True: return
        (x, y) = self.position
        self.position = (x - self.speed, y)
    
    # switch between the 3 images representing the saucer
    def switch_image(self, imageNumber):
        if self.dead == True: return
        if (imageNumber == 1):
            self.imageSprite = self.imageSprite1
        elif (imageNumber == 2):
            self.imageSprite = self.imageSprite2
        else:
            self.imageSprite = self.imageSprite3
    

    def get_width(self):
        return self.imageSprite.get_width()

    def get_height(self):
        return self.imageSprite.get_height()
    
    def kill(self):
        self.dead = True
        self.death_time = pygame.time.get_ticks()

    