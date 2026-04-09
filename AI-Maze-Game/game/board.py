ROWS = 10
COLS = 10
 
class Board:
 
    def __init__(self):
        self.rows = 10
        self.cols = 10

        # make the grid, 0 means empty
        self.grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(0)
            self.grid.append(row)

        # where the AI starts and where the goal is
        self.ai_start = (0, 0)
        self.ai_goal = (9, 9)

    def place_block(self, row, col, block_type):
        # put a block on the grid
        # TODO: check if block_type is valid??
        if row < 0 or col < 0:
            print("thats outside the grid!")
            return
        if row > self.rows or col > self.cols:
            print("thats outside the grid!")
            return

        self.grid[row][col] = block_type

    def remove_block(self, row, col):
        # set it back to empty
        self.grid[row][col] = 0

    def get_cell(self, row, col):
        return self.grid[row][col]

    def is_empty(self, row, col):
        if self.grid[row][col] == 0:
            return True
        else:
            return False

    def print_board(self):
        # Test block
        print("current board:")
        for i in range(self.rows):
            row_str = ""
            for j in range(self.cols):
                row_str = row_str + str(self.grid[i][j]) + " "
            print(row_str)
        print("")

    def reset_board(self):
        # clear everything
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 0

    def get_neighbors(self, row, col):
        # returns cells you can move to from this cell
        # only up down left right, no diagonals for now
        neighbors = []

        up    = (row - 1, col)
        down  = (row + 1, col)
        left  = (row, col - 1)
        right = (row, col + 1)

        all_directions = [up, down, left, right]

        for direction in all_directions:
            r = direction[0]
            c = direction[1]
            # make sure its inside the grid
            if r >= 0 and c >= 0 and r < self.rows and c < self.cols:
                neighbors.append((r, c))

        return neighbors