# ai/weights.py
from game.block import EMPTY, LIGHT_BLOCK, MEDIUM_BLOCK, HEAVY_BLOCK, TRAP_BLOCK, WALL_BLOCK

# Movement cost for each block type
BLOCK_WEIGHTS = {
    EMPTY:        1,
    LIGHT_BLOCK:  3,
    MEDIUM_BLOCK: 7,
    HEAVY_BLOCK:  15,
    TRAP_BLOCK:   20,
    WALL_BLOCK:   None,  # None = impassable
}

def get_weight(block_id):
    # Returns movement cost for a given block type
    if block_id not in BLOCK_WEIGHTS:
        print("warning: unknown block id", block_id, "- defaulting to weight 1")
        return 1
    return BLOCK_WEIGHTS[block_id]

def is_passable(block_id):
    # Returns True if the AI can walk through this block
    weight = get_weight(block_id)
    return weight is not None