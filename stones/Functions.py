import pygame
import pyganim

from PlayerSprite import PlayerSprite


def detect_collisions(playerSprite: PlayerSprite, group: pygame.sprite.Group, piece_size: int):

    for sprite in group.sprites():
        # detect collision with a sprite
        playerRect = pygame.Rect((playerSprite.column * piece_size,
                                  playerSprite.row * piece_size), (piece_size, piece_size))
        if playerRect.colliderect(sprite.rect):
            return sprite
    return None


def remove_sprite_from_group(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    if sprite != None:
        group.remove(sprite)
        sprite.kill()
