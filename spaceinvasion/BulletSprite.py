import pygame


# Create the sprite


class BulletSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_width, bullet_height, speed):
        super().__init__()
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)
        small_font = pygame.font.Font(None, 16)

        self.position = (x, y)
        self.speed = speed

        # Create a surface for the sprite
        self.image = pygame.Surface([bullet_width, bullet_height])
        self.image.fill(GREEN)
        # Draw the rectangle to the sprite surface
        self.rect = self.image.get_rect().move(x, y)

    # nothing to do here, the sprite never moves
    def update(self):
        (x, y) = self.position
        self.rect = self.image.get_rect().move(x, y)

    # Draw the sprite on the screen

    def draw(self, surface):
        surface.blit(self.image, self.rect)
