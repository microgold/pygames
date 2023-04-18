import pygame


class ScoreSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        WHITE = (255, 255, 255)
        self.score = 0
        self.small_font = pygame.font.Font(None, 32)
        self.image = self.small_font.render(
            f'Score: {self.score}', True, WHITE)
    # Draw the sprite on the screen

    def update(self):
        WHITE = (255, 255, 255)
        self.image = self.small_font.render(
            f'Score: {self.score}', True, WHITE)
        self.rect = self.image.get_rect().move(0, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_score(self, score):
        self.score = score
