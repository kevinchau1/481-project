from game.board import Board
from game.block import Block
from ai.astar import astar

board = Board(10, 10)
# place some blocks manually -- Will delete later.
path = astar(board, start=(0,0), goal=(9,9))
print(path)
