# Board is 10 x 10 (unless changed)
DEFAULT_ROWS = 10
DEFAULT_COLS = 10
EMPTY_CELL = 0


class Board:
    def __init__(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, ai_start=(0, 0), ai_goal=None):
        # Validate input
        if rows <= 0 or cols <= 0:
            raise ValueError("Board dimensions must be positive integers.")

        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY_CELL for _ in range(self.cols)] for _ in range(self.rows)] # 2D list

        self.ai_start = ai_start
        self.ai_goal = ai_goal if ai_goal is not None else (self.rows - 1, self.cols - 1)

        # Makes sure start and goal are inside the board
        if not self.in_bounds(*self.ai_start):
            raise ValueError("AI start position must be inside the board.")
        if not self.in_bounds(*self.ai_goal):
            raise ValueError("AI goal position must be inside the board.")

    # Checks if a position is valid
    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    # Throws an error if position is invalid
    def _require_in_bounds(self, row, col):
        if not self.in_bounds(row, col):
            raise IndexError(f"Cell ({row}, {col}) is outside the board.")

    def place_block(self, row, col, block_type):
        self._require_in_bounds(row, col)
        self.grid[row][col] = block_type

    # sets a cell to empty (0)
    def remove_block(self, row, col):
        self._require_in_bounds(row, col)
        self.grid[row][col] = EMPTY_CELL

    def get_cell(self, row, col):
        self._require_in_bounds(row, col)
        return self.grid[row][col]

    def is_empty(self, row, col):
        return self.get_cell(row, col) == EMPTY_CELL

    # Loops through every cell and sets it to 0
    def reset_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = EMPTY_CELL

    # return all the adjacent cells
    def get_neighbors(self, row, col):
        self._require_in_bounds(row, col)

        neighbors = []
        for next_row, next_col in (
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ):
            if self.in_bounds(next_row, next_col):
                neighbors.append((next_row, next_col))

        return neighbors

    def print_board(self):
        print("current board:")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print("")

# Simple Test
# Create a board
board = Board(rows=4, cols=4)

# Print empty board
board.print_board()

# Place some blocks
board.place_block(1, 1, 1)
board.place_block(2, 2, 2)

# Print board again
board.print_board()

# Check a cell
print("Cell (1,1):", board.get_cell(1, 1))

# Check if empty
print("Is (0,0) empty?", board.is_empty(0, 0))

# Get neighbors of (1,1)
neighbors = board.get_neighbors(1, 1)
print("Neighbors of (1,1):", neighbors)
