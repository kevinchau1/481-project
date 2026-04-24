import heapq   # priority queue, always gives us the lowest f_cost cell next
from weights import get_weight, is_passable
 
# heuristic function - estimates distance from current cell to goal
# we use manhattan distance (no diagonals)
def heuristic(current, goal):
    row1, col1 = current
    row2, col2 = goal
    return abs(row1 - row2) + abs(col1 - col2)

def astar(board, start, goal):
    # open_list = cells we still need to check
    # we use a heap so we always check the lowest f_cost first
    # each item is (f_cost, row, col)
    open_list = []
    heapq.heappush(open_list, (0, start))

    # came_from lets us trace back the path at the end
    # came_from[cell] = the cell we came from to get here
    came_from = {}
    came_from[start] = None

    # g_cost[cell] = total cost to reach this cell from start
    g_cost = {}
    g_cost[start] = 0

    while open_list:
        # grab the cell with the lowest f_cost
        current_f, current_cell = heapq.heappop(open_list)

        # if we reached the goal, build and return the path
        if current_cell == goal:
            return build_path(came_from, start, goal)

        # check all neighboring cells
        row, col = current_cell
        neighbors = board.get_neighbors(row, col)

        for neighbor in neighbors:
            n_row, n_col = neighbor
            block_id = board.get_cell(n_row, n_col)

            # skip walls, AI cant go here
            if not is_passable(block_id):
                continue
            # calculate cost to move into this neighbor
            move_cost = get_weight(block_id)
            new_g = g_cost[current_cell] + move_cost
            # if we havent visited this neighbor yet, or found a cheaper path to it
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g

                h = heuristic(neighbor, goal)
                f = new_g + h

                heapq.heappush(open_list, (f, neighbor))
                came_from[neighbor] = current_cell

    # if we get here, no path was found
    print("no path found!")
    return []


def build_path(came_from, start, goal):
    # trace backwards from goal to start using came_from
    path = []
    current = goal

    # just in case goal was never reached
    if goal not in came_from:
        return []

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path
