# ai/weights.py
from game.block import EMPTY, LIGHT_BLOCK, MEDIUM_BLOCK, HEAVY_BLOCK, TRAP_BLOCK, WALL_BLOCK

BLOCK_WEIGHTS = {
    EMPTY:        1,
    LIGHT_BLOCK:  2,
    MEDIUM_BLOCK: 4,
    HEAVY_BLOCK:  7,
    TRAP_BLOCK:   10,
    WALL_BLOCK:   None,
}

BLOCK_MONEY_COSTS = {
    LIGHT_BLOCK:  10,
    MEDIUM_BLOCK: 30,
    HEAVY_BLOCK:  60,
    TRAP_BLOCK:   90,
    WALL_BLOCK:   0,
}

def get_weight(block_id):
    if block_id not in BLOCK_WEIGHTS:
        print("warning: unknown block id", block_id, "- defaulting to weight 1")
        return 1
    return BLOCK_WEIGHTS[block_id]

def is_passable(block_id):
    weight = get_weight(block_id)
    return weight is not None

def money_cost(block_id):
    if block_id not in BLOCK_MONEY_COSTS:
        return 0
    return BLOCK_MONEY_COSTS[block_id]