from game.block import BLOCK_LIST, EMPTY, WALL_BLOCK
from ai.weights import money_cost

# Players can place any non-empty block type defined in block.py.
VALID_BLOCK_IDS = {block["id"] for block in BLOCK_LIST if block["id"] != EMPTY}

# how many coins each player starts with
STARTING_BUDGET = 100


class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.selected_block = None
        self.budget = STARTING_BUDGET    # coins available to spend

    # Save which block type the player wants to place next.
    def select_block(self, block_id):
        if block_id not in VALID_BLOCK_IDS:
            raise ValueError(f"Invalid block id: {block_id}")
        self.selected_block = block_id

    # Clear the current selection so no block is "active."
    def clear_selection(self):
        self.selected_block = None

    # Returns True if the player can afford the currently selected block
    def can_afford(self, block_id):
        cost = money_cost(block_id)
        return self.budget >= cost

    # The AI start and goal cells are reserved and should not be edited.
    def _is_protected_cell(self, board, row, col):
        return (row, col) == board.ai_start or (row, col) == board.ai_goal

    # Pre-generated maze walls are part of the map itself.
    # Treat them as locked so the player cannot drag or delete them.
    def _is_locked_block(self, board, row, col):
        return board.get_cell(row, col) == WALL_BLOCK

    # A block can only be placed if one is selected, the cell is usable,
    # AND the player has enough coins
    def can_place_block(self, board, row, col):
        if self.selected_block is None:
            return False
        if not board.in_bounds(row, col):
            return False
        if self._is_protected_cell(board, row, col):
            return False
        if not board.is_empty(row, col):
            return False
        if not self.can_afford(self.selected_block):   # budget check
            return False
        return True

    # Place the currently selected block onto the board after validation.
    def place_selected_block(self, board, row, col):
        if self.selected_block is None:
            raise ValueError("No block selected.")
        if not self.can_afford(self.selected_block):
            raise ValueError(f"Not enough coins! Need {money_cost(self.selected_block)}, have {self.budget}.")
        if not self.can_place_block(board, row, col):
            raise ValueError(f"Cannot place block at ({row}, {col}).")

        # deduct the coin cost
        cost = money_cost(self.selected_block)
        self.budget -= cost

        board.place_block(row, col, self.selected_block)
        print(f"{self.name} placed block {self.selected_block} for {cost} coins. Budget left: {self.budget}")
        return self.selected_block

    # A move is only valid if the source is a real movable block.
    # Empty cells, protected cells, and locked wall cells cannot be moved.
    # Moving a block is FREE - no coin cost, its already been paid for
    def can_move_block(self, board, from_row, from_col, to_row, to_col):
        if not board.in_bounds(from_row, from_col):
            return False
        if not board.in_bounds(to_row, to_col):
            return False
        if self._is_protected_cell(board, from_row, from_col):
            return False
        if self._is_protected_cell(board, to_row, to_col):
            return False
        if board.is_empty(from_row, from_col):
            return False
        if self._is_locked_block(board, from_row, from_col):
            return False
        if not board.is_empty(to_row, to_col):
            return False
        return True

    # Move the block - free to move since the coin was already paid on placement
    def move_block(self, board, from_row, from_col, to_row, to_col):
        if not self.can_move_block(board, from_row, from_col, to_row, to_col):
            raise ValueError(
                f"Cannot move block from ({from_row}, {from_col}) to ({to_row}, {to_col})."
            )

        block_id = board.get_cell(from_row, from_col)
        board.remove_block(from_row, from_col)
        board.place_block(to_row, to_col, block_id)
        return block_id

    # Remove a block and REFUND the coins back to the player
    def remove_block(self, board, row, col):
        if not board.in_bounds(row, col):
            raise IndexError(f"Cell ({row}, {col}) is outside the board.")
        if self._is_protected_cell(board, row, col):
            raise ValueError("Cannot remove the AI start or goal cell.")
        if board.is_empty(row, col):
            raise ValueError(f"Cell ({row}, {col}) is already empty.")
        if self._is_locked_block(board, row, col):
            raise ValueError("Cannot remove a locked wall block.")

        # refund the coin cost when block is removed
        block_id = board.get_cell(row, col)
        refund = money_cost(block_id)
        self.budget += refund

        board.remove_block(row, col)
        print(f"{self.name} removed block {block_id}, refunded {refund} coins. Budget: {self.budget}")

    def reset_budget(self):
        # call this between player 1 and player 2 turns
        self.budget = STARTING_BUDGET
        print(f"{self.name} budget reset to {STARTING_BUDGET}")