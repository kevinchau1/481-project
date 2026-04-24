# ai/astar.py
import heapq
from ai.weights import get_weight, is_passable


def heuristic(a, b):
    # Manhattan distance heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(board, start, goal):
    """
    A* pathfinding on a Board object.

    Parameters:
        board : Board      - board object from game/board.py
        start : (row, col) - starting position
        goal  : (row, col) - target position

    Returns:
        list of (row, col) - path from start to goal
        None               - if no path exists
    """

    # Validate start and goal positions
    if not board.in_bounds(*start):
        raise ValueError(f"Start {start} is outside the board.")
    if not board.in_bounds(*goal):
        raise ValueError(f"Goal {goal} is outside the board.")

    # Check if goal is blocked by a wall
    if not is_passable(board.get_cell(*goal)):
        return None

    # open_set: (f_score, g_score, node)
    open_set = []
    heapq.heappush(open_set, (0, 0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, g, current = heapq.heappop(open_set)

        # Reached the goal
        if current == goal:
            return _reconstruct_path(came_from, current)

        # Skip if a shorter path was already found
        if g > g_score.get(current, float("inf")):
            continue

        for neighbor in board.get_neighbors(*current):
            cell_id = board.get_cell(*neighbor)

            # Skip impassable cells (walls)
            if not is_passable(cell_id):
                continue

            # new g = current g + movement cost of the next cell
            weight = get_weight(cell_id)
            new_g = g_score[current] + weight

            if new_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = new_g
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, new_g, neighbor))
                came_from[neighbor] = current

    return None  # No path found


def _reconstruct_path(came_from, current):
    # Trace back from goal to start
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    return path[::-1]