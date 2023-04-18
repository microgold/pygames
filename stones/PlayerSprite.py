import pygame
import pyganim

# Create the sprite


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, row, column, piece_size):
        super().__init__()

        self.row = row
        self.column = column
        self.piece_size = piece_size
        self.anim = pyganim.PygAnimation(
            [("images/pacopen.png", 250), ("images/pacclose.png", 250)])
        self.anim.scale((piece_size, piece_size))
        self.anim.play()
        self.rect = pygame.Rect(
            column*piece_size, row*self.piece_size, self.piece_size, self.piece_size)

    def update(self):
        self.rect = self.anim.getRect().move(
            self.column*self.piece_size, self.row*self.piece_size)

    def draw(self, surface):
        self.anim.blit(surface, self.rect)
