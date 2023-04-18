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

    def run_algorithm_to_place_O(self):
        for rowo in range(self.grid_size):
            for colo in range(self.grid_size):
                if (self.board[rowo][colo] == 0):
                    self.board[rowo][colo] = "O"
                    return (True, rowo, colo)

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
