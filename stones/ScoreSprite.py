import pygame


class ScoreSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        BLACK = (0, 0, 0)
        self.score = 0
        self.small_font = pygame.font.Font(None, 16)
        self.image = self.small_font.render(
            f'Score: {self.score}', True, BLACK)
    # Draw the sprite on the screen

    def update(self):
        BLACK = (0, 0, 0)
        self.image = self.small_font.render(
            f'Score: {self.score}', True, BLACK)
        self.rect = self.image.get_rect().move(0, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_score(self, score):
        self.score = score
