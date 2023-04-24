import time
import pygame

game_window = None

# game window dimensions
window_width = 600
window_height = 600

# grid dimensions
grid_size = 3
grid_width = window_width / grid_size
grid_height = window_height / grid_size

# Specify the winner X or O
winner = ''

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


def initialize_game_values():
    global board
    global game_over
    global X_placed
    global O_placed
    global winner
    global clock

    game_over = False
    X_placed = False
    O_placed = False
    winner = ''

    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    clock = pygame.time.Clock()

# Create game window


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
    return game_window


game_window = initialize_game()


####################################################
# A very simple algorithm to place O on the board
####################################################
# def run_algorithm_to_place_o():
#     for rowo in range(grid_size):
#         for colo in range(grid_size):
#             if (board[rowo][colo] == 0):
#                 board[rowo][colo] = "O"
#                 return True

#     return False

def is_winning_move(player, row, col):
    n = len(board)
    # Check row
    if all(board[row][j] == player for j in range(n)):
        return True
    # Check column
    if all(board[i][col] == player for i in range(n)):
        return True
    # Check main diagonal
    if row == col and all(board[i][i] == player for i in range(n)):
        return True
    # Check secondary diagonal
    if row + col == n - 1 and all(board[i][n - i - 1] == player for i in range(n)):
        return True
    return False


def get_empty_positions():
    empty_positions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 0:
                empty_positions.append((i, j))
    return empty_positions

#####################################################
# a more advanced algorithm to place O on the board #
#####################################################
def run_better_algorithm_to_place_O():
    grid_size = len(board)
    empty_positions = get_empty_positions()
    num_moves = sum(1 for row in board for 
                    cell in row if cell != 0)

    # Second move: Place "O" in center or corner
    if num_moves == 1:
        center = grid_size // 2
        if board[center][center] == 0:
            board[center][center] = "O"
            return True
        else:
            for row, col in [(0, 0), (0, grid_size - 1), 
                         (grid_size - 1, 0), 
                         (grid_size - 1, grid_size - 1)]:
                if board[row][col] == 0:
                    board[row][col] = "O"
                    return True

    # Try to win or block X from winning
    for row, col in empty_positions:
        # Check if placing "O" would win the game
        board[row][col] = "O"
        if is_winning_move("O", row, col):
            return True
        board[row][col] = 0

    # Check if placing "O" would block X from winning
    for row, col in empty_positions:
        board[row][col] = "X"
        if is_winning_move("X", row, col):
            board[row][col] = "O"
            return True
        board[row][col] = 0

    # Place "O" in a corner if it started in a corner
    if board[0][0] == "O" \
        or board[0][grid_size - 1] == "O" \
        or board[grid_size - 1][0] == "O" \
        or board[grid_size - 1][grid_size - 1] == "O":
        for row, col in [(0, 0), (0, grid_size - 1), 
                     (grid_size - 1, 0), 
                     (grid_size - 1, grid_size - 1)]:
            if board[row][col] == 0:
                board[row][col] = "O"
                return True

    # Place "O" in a non-corner side
    for row, col in empty_positions:
        if row not in [0, grid_size - 1] \
           and col not in [0, grid_size - 1]:
            board[row][col] = "O"
            return True

    # Place "O" in any available space
    for row, col in empty_positions:
        board[row][col] = "O"
        return True

    return False

####################################################
# Check if someone won in any row, column or diagonal
####################################################


def check_if_anyone_won():
    # Check if someone won horizontally
    global winner

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != 0:
            winner = board[row][0]
            return True
    # Check if someone won vertically
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            winner = board[0][col]
            return True
    # Check if someone won diagonally
    if board[0][0] == board[1][1] == board[2][2] != 0:
        winner = board[0][0]
        return True
    if board[0][2] == board[1][1] == board[2][0] != 0:
        winner = board[0][2]
        return True

    return False

####################################################
# Check if the board is full
####################################################


def check_if_board_is_full():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                return False
    return True


####################################################
# Check if there is a draw by checking if the board is full
# and no one has won
####################################################

def check_if_draw():
    return not (check_if_anyone_won()) and check_if_board_is_full()


####################################################
# Draw the game over screen showing who won
####################################################
def draw_game_over_screen():
    game_window.fill(WHITE)
    if winner == "X":
        text = font.render('X Wins!', True, BLACK)
    elif winner == "O":
        text = font.render('O Wins!', True, BLACK)
    else:
        text = font.render('Draw!', True, BLACK)

    playAgainText = smallfont.render('Play Again (y/n)?', True, BLACK)

    game_window.blit(text, (window_width/2 - 200, window_height/2 - 100))

    game_window.blit(playAgainText,
                     (window_width/2 - 200, window_height/2 + 50))

####################################################
# Draw the game board with all the X's and O's
####################################################


def draw_the_board():
    for row in range(grid_size):
        for col in range(grid_size):
            draw_game_board_square(row, col)
            # Render letter X
            if (board[row][col] == "X"):
                draw_tic_tac_toe_letter(row, col, 'X')
           # Render letter O
            if (board[row][col] == "O"):
                draw_tic_tac_toe_letter(row, col, 'O')

####################################################
# Draw a single square on the game board
####################################################


def draw_game_board_square(row, col):
    rect = pygame.Rect(col * grid_width, row *
                       grid_height, grid_width, grid_height)
    pygame.draw.rect(game_window, BLACK, rect, 3)


####################################################
# Draw a letter X or O on the game board
####################################################
def draw_tic_tac_toe_letter(row, col, letter):
    letter_piece = font.render(letter, True, BLACK)
    game_window.blit(
        letter_piece, (col * grid_width + grid_width/4,
                       row * grid_height + grid_height/4))

####################################################
# Handle mouse down for X and place X on the board
####################################################


def handle_mouse_down_for_x():
    (col, row) = pygame.mouse.get_pos()
    row = int(row / grid_height)
    col = int(col / grid_width)
    board[row][col] = "X"

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
# Check for win or draw
####################################################

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
            handle_mouse_down_for_x()  # Handle mouse down for X
            X_placed = True


def check_for_win_or_draw():
    global game_over
    global winner
    if (check_if_anyone_won()):
        game_over = True
    elif (check_if_draw()):
        game_over = True
        winner = 'Nobody'

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
            O_placed = run_better_algorithm_to_place_O()
            game_over = check_if_anyone_won()
            draw_the_board()  # Draw the board again to show the O
            X_placed = False

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
