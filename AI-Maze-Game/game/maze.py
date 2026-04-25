# game/maze.py
import random
from game.block import WALL_BLOCK


# ── Public ───────────────────────────────────────────────

def generate_maze(board):

    # Fill entire board with walls
    for r in range(board.rows):
        for c in range(board.cols):
            if not _is_protected(board, r, c):
                board.place_block(r, c, WALL_BLOCK)

    # Carve paths starting from ai_start
    _carve(board, *board.ai_start)

    # Guarantee goal is reachable by clearing one adjacent direction
    _clear_goal_entrance(board)

    # Make sure start and goal cells are always clear
    board.remove_block(*board.ai_start)
    board.remove_block(*board.ai_goal)


# ── Private ──────────────────────────────────────────────

def _is_protected(board, row, col):
    """Returns True if the cell is the AI start or goal."""
    return (row, col) == board.ai_start or (row, col) == board.ai_goal


def _carve(board, row, col):
    """Recursively carves paths through the maze from the given cell."""
    board.remove_block(row, col)

    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(directions)

    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if board.in_bounds(nr, nc) and not board.is_empty(nr, nc):
            board.remove_block(row + dr // 2, col + dc // 2)
            _carve(board, nr, nc)


def _clear_goal_entrance(board):
    """Clears cells adjacent to the goal to ensure it is always reachable."""
    goal_row, goal_col = board.ai_goal

    directions = random.choice([
        [(-1, 0), (-2, 0)],  # from above
        [(0, -1), (0, -2)],  # from the left
    ])

    for dr, dc in directions:
        nr, nc = goal_row + dr, goal_col + dc
        if board.in_bounds(nr, nc) and not _is_protected(board, nr, nc):
            board.remove_block(nr, nc)