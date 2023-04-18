import pygame


class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.position = (x, y)
        self.name = name
        self.image = pygame.image.load(f'images/{name}.gif')
        self.rect = self.image.get_rect().move(50, 300)

    # nothing to do here, the sprite never moves
    def update(self):
        self.rect = self.image.get_rect().move(self.position)

    # Draw the sprite on the screen

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()
