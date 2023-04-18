import pygame


class LivesSprite(pygame.sprite.Sprite):
    def __init__(self, window_width):
        super().__init__()
        WHITE = (255, 255, 255)
        self.window_width = window_width
        self.lives = 3
        self.livesImage = pygame.image.load('images/man.gif')
        self.livesImage = pygame.transform.scale(self.livesImage, (40, 32))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.small_font = pygame.font.Font(None, 32)
        self.image = self.small_font.render(
            f'Lives: {self.lives}', True, WHITE)
    # Draw the sprite on the screen

    def update(self):
        WHITE = (255, 255, 255)
        self.image = self.small_font.render(
            f'Lives:', True, WHITE)
        self.rect = self.image.get_rect().move(self.window_width - 250, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for i in range(self.lives):
            surface.blit(self.livesImage, (self.window_width - 180 + i * 50, 0))

    def update_lives(self, lives):
        self.lives = lives
