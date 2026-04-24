import random
from mazes import ALL_MAZES

def load_random_maze(board):
    maze = random.choice(ALL_MAZES)
    for row in range(board.rows):
        for col in range(board.cols):
            board.grid[row][col] = maze[row][col]