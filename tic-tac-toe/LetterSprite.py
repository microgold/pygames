import pygame


class LetterSprite(pygame.sprite.Sprite):

    def __init__(self, letter, row, column,
                 grid_width, grid_height):
        super().__init__()
        font = pygame.font.Font(None, 150)
        self.image = font.render(letter, True, (0, 0, 0))
        self.rect = self.image.get_rect().move(
            row * grid_width + grid_width / 3,
            column * grid_height + grid_height / 3)

    def update(self):
        pass

    def draw(self, surface):
        letter_piece = self.image
        surface.blit(letter_piece, self.rect)
