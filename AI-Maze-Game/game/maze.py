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

    # Randomly remove some walls to open extra paths
    _open_extra_paths(board)

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

def _open_extra_paths(board, removal_chance=0.05):
    """
    Randomly removes interior walls to create extra paths through the maze.
    Only removes walls that are surrounded by at least 2 open cells
    to avoid opening dead-end gaps on the border.

    removal_chance: probability (0.0 - 1.0) that an eligible wall is removed.
                    Higher = more open paths. Default 0.15 = ~15%.
    """
    for r in range(1, board.rows - 1):
        for c in range(1, board.cols - 1):
            if _is_protected(board, r, c):
                continue

            # Only target wall cells
            if board.get_cell(r, c) != WALL_BLOCK:
                continue

            # Count adjacent open cells
            open_neighbors = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if board.in_bounds(nr, nc) and board.is_empty(nr, nc):
                    open_neighbors += 1

            # Only remove walls that connect 2+ open areas
            if open_neighbors >= 2 and random.random() < removal_chance:
                board.remove_block(r, c)