import pygame


class CoordinateSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        self.x = x
        self.y = y
        self.small_font = pygame.font.Font(None, 16)
        self.image = self.small_font.render(
            f'coordinates: ({x}, {y})', True, BLACK)
        self.rect = self.image.get_rect().move(280, 0)
    # Draw the sprite on the screen

    def update(self):
        BLACK = (0, 0, 0)
        self.image = self.small_font.render(
            f'coordinates: ({self.x}, {self.y})', True, BLACK)
        self.rect = self.image.get_rect().move(280, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_coordinatees(self, x, y):
        self.x = x
        self.y = y
