import time
import pygame
from GameBoard import GameBoard
from GameBoardSquareSprite import GameBoardSquareSprite

from LetterSprite import LetterSprite

game_window = None

# game window dimensions
window_width = 600
window_height = 600

# grid dimensions
grid_size = 3
grid_width = window_width / grid_size
grid_height = window_height / grid_size

# initialize the font object for rendering text
font = None
smallfont = None

# game over flag
game_over = False
X_placed = False
O_placed = False

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# initialize the board

board = None
group = None


def initialize_game_values():
    global board
    global game_over
    global X_placed
    global O_placed
    global clock
    global group

    game_over = False
    X_placed = False
    O_placed = False

    board = GameBoard(grid_size)

    clock = pygame.time.Clock()

    group = pygame.sprite.Group()

    initialize_game_board()


# Create game window


def initialize_game_board():
    for row in range(3):
        for column in range(3):
            game_board_square = GameBoardSquareSprite(
                (0, 255, 0),  row, column, grid_width, grid_height)
            group.add(game_board_square)


def initialize_game():
    global game_window
    global font
    global smallfont

    initialize_game_values()
    # Initialize pygame
    pygame.init()
    game_window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Tic-Tac-Toe')
    # Create font object
    font = pygame.font.Font(None, 150)
    smallfont = pygame.font.Font(None, 50)

    initialize_game_board()

    return game_window


game_window = initialize_game()


####################################################
# Draw the game over screen showing who won
####################################################
def draw_game_over_screen():
    game_window.fill(WHITE)
    winner_message = board.get_winner_display_message()

    text = font.render(winner_message, True, BLACK)

    # get the width of the text
    text_width = text.get_width()

    play_again_text = smallfont.render('Play Again (y/n)?', True, BLACK)

    play_again_text_width = play_again_text.get_width()

    game_window.blit(
        text, (window_width/2 - text_width/2, window_height/2 - 100))

    game_window.blit(play_again_text,
                     (window_width/2 - play_again_text_width/2, window_height/2 + 50))

####################################################
# Draw the game board with all the X's and O's
####################################################


def draw_the_board():
    group.draw(game_window)


####################################################
# Draw a letter X or O on the game board
####################################################
def draw_tic_tac_toe_letter(row, col, letter):
    letter_piece = font.render(letter, True, BLACK)
    game_window.blit(
        letter_piece, (
            col * grid_height + grid_height/4,
            row * grid_width + grid_width/4)
    )

####################################################
# Handle mouse down for X and place X on the board
####################################################


def handle_mouse_down_for_X():
    (col, row) = pygame.mouse.get_pos()
    row = int(row / grid_width)
    col = int(col / grid_height)
    board.place_X(row, col)
    letterX = LetterSprite('X', col, row, grid_height, grid_width)
    group.add(letterX)


####################################################
# Check for quit event
####################################################


def check_for_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                initialize_game_values()
                game_window.fill(WHITE)
                return True
            elif event.key == pygame.K_n:
                pygame.quit()
                quit()


####################################################
# Run the event processing and check for quit and mouse down
####################################################


def run_event_processing():
    global X_placed
    global game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # quit the game
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_down_for_X()  # Handle mouse down for X
            X_placed = True


def check_for_win_or_draw():
    global game_over
    if (board.check_if_anybody_won()):
        game_over = True
    elif (board.check_if_its_a_draw()):
        game_over = True
        board.winner = 'Nobody'

    return game_over


####################################################
# Main game loop
####################################################
while True:
    if game_over:
        pygame.display.flip()
        pygame.time.delay(1000)
        draw_game_over_screen()
        check_for_quit_event()  # Run the event processing to check for quit
    else:
        game_window.fill(WHITE)
        run_event_processing()  # check for quit and mouse down
        game_over = check_for_win_or_draw()  # Check for win or draw
        draw_the_board()  # Draw the game board
        pygame.display.flip()  # Update the display

        # Check if anyone won after X was placed
        if game_over:
            continue

        # AI Goes here to place O
        if X_placed:
            # Wait for 1/2 second to make it look like AI is thinking
            pygame.time.delay(500)
            (O_placed, rowo, colo) = board.run_better_algorithm_to_place_O()
            if O_placed:
                letterO = LetterSprite(
                    'O', colo, rowo, grid_width, grid_height)
                group.add(letterO)
                O_placed = False
            game_over = board.check_if_anybody_won()
            draw_the_board()  # Draw the board again to show the O
            X_placed = False

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
