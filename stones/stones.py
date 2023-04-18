import pygame
import random

from StoneSprite import StoneSprite
from PlayerSprite import PlayerSprite
from Functions import detect_collisions
from Functions import remove_sprite_from_group
from ScoreSprite import ScoreSprite
from HiScoreSprite import HiScoreSprite
from TimeSprite import TimeSprite
from GameBoard import GameBoard
from CoordinateSprite import CoordinateSprite
from MessageSprite import MessageSprite

# Set up Pygame
pygame.init()

window_length = 400

# Set up window
WINDOW_SIZE = (window_length, window_length)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Gem Collector')


# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# create an array of colors
colors = [GREEN, RED, BLUE]

# Set up font
font = pygame.font.Font(None, 36)

# size of piece on board
piece_size = 20

small_font = pygame.font.Font(None, 16)

# Set up grid
GRID_SIZE = 20

player_limit = 3

GRID_LENGTH = window_length / GRID_SIZE


gems_collected = 0
gems_score = 0
start_time = 0
already_played = False

gem_group = pygame.sprite.Group()
score_group = pygame.sprite.Group()
player = PlayerSprite(3, 0, piece_size)
hi_score = HiScoreSprite()
play_again_message = MessageSprite('Play again? (y/n)', 30, 90)
gems_collected_message = MessageSprite('Gems collected: ', 0, 30)
coordinates = CoordinateSprite(0, 0)
game_time = TimeSprite()
score = ScoreSprite()
score_group.add(score, hi_score, coordinates, game_time)

game_board = GameBoard(GRID_SIZE, piece_size, player_limit, gem_group)


victory_sound = pygame.mixer.Sound('sounds/victory.wav')
got_coin_sound = pygame.mixer.Sound('sounds/stonegrab.wav')
waka_sound = pygame.mixer.Sound('sounds/waka.mp3')


# Set time limit in seconds
time_limit = 15


def process_events():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_n and times_up == True):
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check if player has moved
            if event.key == pygame.K_UP and player.row > player_limit:
                player.row -= 1
                player.update()
            elif event.key == pygame.K_DOWN and player.row < GRID_LENGTH - 1:
                player.row += 1
                player.update()
            elif event.key == pygame.K_LEFT and player.column > 0:
                player.column -= 1
                player.update()
            elif event.key == pygame.K_RIGHT and player.column < GRID_LENGTH - 1:
                player.column += 1
                player.update()
            elif event.key == pygame.K_y and times_up == True:
                initialize_game_state()
    return running


def initialize_game_state():
    global gems_collected, gems_score, start_time, times_up, already_played
    print("Initializing game state")
    gem_group.empty()
    start_time = pygame.time.get_ticks()
    times_up = False
    player.row = player_limit
    player.column = 0
    player.update()
    game_time.update_time(time_limit, 0)
    score.update_score(0)
    gems_collected = 0
    gems_score = 0
    already_played = False

    game_board.initialize_board()


initialize_game_state()

# Main game loop
running = True
while running:

    running = process_events()  # process the keyboard

    # Check if player has picked up a gem
    if game_board.check_for_gem(player) and (times_up == False):
        # gem found, update score
        gems_collected += 1
        gems_score += game_board.get_cell_value(player.row, player.column)
        score.update_score(gems_score)
        # remove the gem from the board and the gem sprite
        game_board.remove_gem(player)
        which_sprite = detect_collisions(player, gem_group, piece_size)
        remove_sprite_from_group(which_sprite, gem_group)
        got_coin_sound.play()

    # Update coordinates
    coordinates.update_coordinatees(player.row, player.column)

    # Update time
    game_time.update_time(time_limit,
                          pygame.time.get_ticks() - start_time)

    # Check if time is up
    if (pygame.time.get_ticks() - start_time > time_limit * 1000) and (times_up == False):
        times_up = True

    # empty the screen
    window.fill(WHITE)

    # Check if time is up
    if times_up:
        if already_played == False:
            hi_score.current_score = gems_score
            victory_sound.play()
            already_played = True

        gems_collected_message.update_message(
            f'You collected {str(gems_collected)} gems!')

        gems_collected_message.update()
        gems_collected_message.draw(window)
        play_again_message.draw(window)
    else:
        # draw the player and game time
        player.draw(window)
        game_time.draw(window)

    # draw the gems
    gem_group.draw(window)

    # update the stats
    score_group.update()

    # draw the stats
    score_group.draw(window)
    pygame.display.flip()
