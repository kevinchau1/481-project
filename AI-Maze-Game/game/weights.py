from block import EMPTY, LIGHT_BLOCK, MEDIUM_BLOCK, HEAVY_BLOCK, TRAP_BLOCK, WALL_BLOCK

# AI uses this in astar.py to calculate path cost
BLOCK_WEIGHTS = {
    EMPTY:        1, # normal movement cost
    LIGHT_BLOCK:  3,
    MEDIUM_BLOCK: 7,
    HEAVY_BLOCK:  15,
    TRAP_BLOCK:   20, # most expensive
    WALL_BLOCK:   None, # None means blocking block, AI cannot pass this.
}

def get_weight(block_id):
    # returns the movement cost for a given block type
    # if block_id isnt in the dict for some reason, just return 1
    if block_id not in BLOCK_WEIGHTS:
        print("warning: unknown block id", block_id, "- defaulting to weight 1")
        return 1

    return BLOCK_WEIGHTS[block_id]

def is_passable(block_id):
    # returns True if AI can walk through this block
    weight = get_weight(block_id)
    if weight == None:
        return False
    return True
