class GameBoard:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.winner = ''
        self.initialize_board()

    ####################################################
    # Initialize the board with 0s
    ####################################################

    def initialize_board(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    ####################################################
    # A very simple algorithm to place O on the board
    ####################################################

    # def run_algorithm_to_place_O(self):
    #     for rowo in range(self.grid_size):
    #         for colo in range(self.grid_size):
    #             if (self.board[rowo][colo] == 0):
    #                 self.board[rowo][colo] = "O"
    #                 return (True, rowo, colo)

    #     return (False, -1, -1)

    def is_winning_move(self, player, row, col):
        n = len(self.board)
        # Check row
        if all(self.board[row][j] == player for j in range(n)):
            return True
        # Check column
        if all(self.board[i][col] == player for i in range(n)):
            return True
        # Check main diagonal
        if row == col and all(self.board[i][i] == player for i in range(n)):
            return True
        # Check secondary diagonal
        if row + col == n - 1 and all(self.board[i][n - i - 1] == player for i in range(n)):
            return True
        return False


    def get_empty_positions(self):
        empty_positions = []
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    empty_positions.append((i, j))
        return empty_positions

#####################################################
# a more advanced algorithm to place O on the board #
#####################################################
    def run_better_algorithm_to_place_O(self):
        grid_size = len(self.board)
        empty_positions = self.get_empty_positions()
        num_moves = sum(1 for row in self.board for 
                        cell in row if cell != 0)

        # Second move: Place "O" in center or corner
        if num_moves == 1:
            center = grid_size // 2
            if self.board[center][center] == 0:
                self.board[center][center] = "O"
                return (True, center, center)
            else:
                for row, col in [(0, 0), (0, grid_size - 1), 
                            (grid_size - 1, 0), 
                            (grid_size - 1, grid_size - 1)]:
                    if self.board[row][col] == 0:
                        self.board[row][col] = "O"                        
                        return (True, row, col)

        # Try to win or block X from winning
        for row, col in empty_positions:
            # Check if placing "O" would win the game
            self.board[row][col] = "O"
            if self.is_winning_move("O", row, col):
                return (True, row, col)
            self.board[row][col] = 0

        # Check if placing "O" would block X from winning
        for row, col in empty_positions:
            self.board[row][col] = "X"
            if self.is_winning_move("X", row, col):
                self.board[row][col] = "O"
                return (True, row, col)
            self.board[row][col] = 0

        # Place "O" in a corner if it started in a corner
        if self.board[0][0] == "O" \
            or self.board[0][grid_size - 1] == "O" \
            or self.board[grid_size - 1][0] == "O" \
            or self.board[grid_size - 1][grid_size - 1] == "O":
            for row, col in [(0, 0), (0, grid_size - 1), 
                        (grid_size - 1, 0), 
                        (grid_size - 1, grid_size - 1)]:
                if self.board[row][col] == 0:
                    self.board[row][col] = "O"
                    (True, row, col)
                    return (True, row, col)

        # Place "O" in a non-corner side
        for row, col in empty_positions:
            if row not in [0, grid_size - 1] \
            and col not in [0, grid_size - 1]:
                self.board[row][col] = "O"
                return (True, row, col)

        # Place "O" in any available space
        for row, col in empty_positions:
            self.board[row][col] = "O"
            return (True, row, col)

        return (False, -1, -1)    

####################################################
# Check if someone won in any row, column or diagonal
####################################################

    def check_if_anybody_won(self):
        # Check if someone won horizontally

        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
                self.winner = self.board[row][0]
                return True
        # Check if someone won vertically
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                self.winner = self.board[0][col]
                return True
        # Check if someone won diagonally
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winner = self.board[0][0]
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.winner = self.board[0][2]
            return True

        return False

    ####################################################
    # Check if the self.board is full
    ####################################################

    def check_if_board_is_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    return False
        return True

    ####################################################
    # Check if there is a draw by checking if the board is full
    # and no one has won
    ####################################################

    def check_if_its_a_draw(self):
        return not (self.check_if_anybody_won()) and self.check_if_board_is_full()

    ####################################################
    # Place the X
    ####################################################
    def place_X(self, row, col):
        self.board[row][col] = "X"

####################################################
# get the winner/loser/or draw display message
####################################################
    def get_winner_display_message(self):
        if self.winner == 'X':
            return 'X Wins!'
        elif self.winner == 'O':
            return 'O Wins!'
        else:
            return 'Draw!'
