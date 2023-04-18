import pygame


class HiScoreSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        f = open('files/hiscore.txt', 'r')
        self.hi_score = int(f.read())
        print(f'read hi score of {self.hi_score}')
        f.close()
        self.current_score = -1
        self.small_font = pygame.font.Font(None, 16)
        self.image = self.small_font.render(
            f'HiScore: {self.hi_score}', True, BLACK)
        self.rect = self.image.get_rect().move(150, 0)
    # Draw the sprite on the screen

    def update(self):
        self.update_high_score(self.current_score)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_high_score(self, score):
        BLACK = (0, 0, 0)
        if self.hi_score < score:
            self.hi_score = score
            self.image = self.small_font.render(
                f'HiScore: {self.hi_score}', True, BLACK)
            self.rect = self.image.get_rect().move(150, 0)
            print(f'write hi score of {self.hi_score}')
            f = open('files/hiscore.txt', 'w')
            f.write(str(score))
            f.close()
        else:
            pass
