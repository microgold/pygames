import pygame
import random
from StoneSprite import StoneSprite


class GameBoard:
    def __init__(self, size, piece_size, player_limit, gemGroup):
        self.grid_size = size
        self.piece_size = piece_size
        self.player_limit = player_limit
        self.grid = []
        self.gemGroup = gemGroup
        GREEN = (0, 150, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        self.colors = [GREEN, RED, BLUE]

    def initialize_board(self):
        self.grid = []
        for i in range(self.grid_size):
            self.grid.append([])
            for j in range(self.grid_size):
                self.grid[i].append(0)

        # Place gems randomly on the self.grid
        num_gems = 20
        for i in range(num_gems):
            gem_placed = False
            while not gem_placed:
                row = random.randint(self.player_limit, self.grid_size - 1)
                column = random.randint(0, self.grid_size - 1)
                if self.grid[row][column] == 0:
                    self.grid[row][column] = random.randint(1, 3)
                    gem_placed = True
                    self.gemGroup.add(StoneSprite(
                        self.colors[self.grid[row][column]-1], row, column, self.piece_size, self.grid[row][column]))

    def check_for_gem(self, player):
        if self.grid[player.row][player.column] > 0:
            return True
        else:
            return False

    def remove_gem(self, player):
        self.grid[player.row][player.column] = 0

    def get_cell_value(self, row, column):
        return self.grid[row][column]
