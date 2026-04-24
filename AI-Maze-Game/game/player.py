from game.block import BLOCK_LIST, EMPTY


# Players can place any non-empty block type defined in block.py.
VALID_BLOCK_IDS = {block["id"] for block in BLOCK_LIST if block["id"] != EMPTY}


class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.selected_block = None

    # Save which block type the player wants to place next.
    def select_block(self, block_id):
        if block_id not in VALID_BLOCK_IDS:
            raise ValueError(f"Invalid block id: {block_id}")
        self.selected_block = block_id

    # Clear the current selection so no block is "active."
    def clear_selection(self):
        self.selected_block = None

    # The AI start and goal cells are reserved and should not be edited.
    def _is_protected_cell(self, board, row, col):
        return (row, col) == board.ai_start or (row, col) == board.ai_goal

    # A block can only be placed if one is selected and the target cell is usable.
    def can_place_block(self, board, row, col):
        if self.selected_block is None:
            return False
        if not board.in_bounds(row, col):
            return False
        if self._is_protected_cell(board, row, col):
            return False
        if not board.is_empty(row, col):
            return False
        return True

    # Place the currently selected block onto the board after validation.
    def place_selected_block(self, board, row, col):
        if self.selected_block is None:
            raise ValueError("No block selected.")
        if not self.can_place_block(board, row, col):
            raise ValueError(f"Cannot place block at ({row}, {col}).")

        board.place_block(row, col, self.selected_block)
        return self.selected_block

    # A move is valid when the source has a block and the destination is empty.
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
        if not board.is_empty(to_row, to_col):
            return False
        return True

    # Move the block by copying its id, clearing the old cell, then filling the new one.
    def move_block(self, board, from_row, from_col, to_row, to_col):
        if not self.can_move_block(board, from_row, from_col, to_row, to_col):
            raise ValueError(
                f"Cannot move block from ({from_row}, {from_col}) to ({to_row}, {to_col})."
            )

        block_id = board.get_cell(from_row, from_col)
        board.remove_block(from_row, from_col)
        board.place_block(to_row, to_col, block_id)
        return block_id

    # Remove a block unless the cell is protected or already empty.
    def remove_block(self, board, row, col):
        if not board.in_bounds(row, col):
            raise IndexError(f"Cell ({row}, {col}) is outside the board.")
        if self._is_protected_cell(board, row, col):
            raise ValueError("Cannot remove the AI start or goal cell.")
        if board.is_empty(row, col):
            raise ValueError(f"Cell ({row}, {col}) is already empty.")

        board.remove_block(row, col)
