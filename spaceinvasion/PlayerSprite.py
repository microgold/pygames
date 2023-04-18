import pygame
import pyganim
from ImageSprite import ImageSprite

class PlayerSprite(ImageSprite):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.dead = False
        self.speed = .1
        self.death_time = 0
        self.animate_explosion = pyganim.PygAnimation(
            [("images/shipexplosion/frame1.gif", 250), ("images/shipexplosion/frame2.gif", 250), 
              ("images/shipexplosion/frame3.gif", 250), ("images/shipexplosion/frame4.gif", 250),
              ("images/shipexplosion/frame5.gif", 250), ("images/shipexplosion/frame6.gif", 250),
                  ("images/shipexplosion/frame7.gif", 250), ("images/shipexplosion/frame8.gif", 250),], loop=False)

    # just call the super class to adjust the rect
    def update(self):
        super().update()

    # Draw the sprite on the screen
    def kill(self):
        self.animate_explosion.play()
        self.dead = True
        self.death_time = pygame.time.get_ticks()


    def draw(self, surface):
        if not self.dead:
            super().draw(surface)
        else:
            self.animate_explosion.blit(surface, self.rect)
            if (pygame.time.get_ticks() - self.death_time) > 5000:
                self.dead = False

    def move_left(self):
        (x, y) = self.position
        self.position = (x - self.speed, y)

    def move_right(self):
        (x, y) = self.position
        self.position = (x + self.speed, y)

