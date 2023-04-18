import pygame


# Create the sprite
class GameBoardSquareSprite(pygame.sprite.Sprite):
    def __init__(self, color, row, column, width, height):
        super().__init__()
        self.width = width
        self.height = height
        # Create a surface for the sprite
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect().move(row*width, column*height)
        # Draw the rectangle to the sprite surface
        pygame.draw.rect(self.image, color, pygame.Rect(
            0, 0, width, height),  2)

    # Draw the sprite on the screen

    def draw(self, surface):
        surface.blit(self.image, 0, 0)
