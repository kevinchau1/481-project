# game/config.py

# ── Window settings ──────────────────────────────────────
FIXED_WIDTH  = 800
FIXED_HEIGHT = 700

PADDING          = 20
TITLE_BAR_HEIGHT = 60
SIDEBAR_WIDTH    = 200


# ── Difficulty settings ─────────────────────────────────
LEVELS = {
    "easy":      (11, 11),
    "medium":    (15, 15),
    "hard":      (21, 21),
    "very_hard": (25, 25),
}

# budget per diff.
BUDGETS = {
    "easy":      100,
    "medium":    175,
    "hard":      300,
    "very_hard": 450,
}

# ── Cell size calculation ───────────────────────────────
def compute_cell_size(rows, cols):
    """
    Calculate CELL_SIZE so that the board always fits within the window
    """
    available_width = FIXED_WIDTH - SIDEBAR_WIDTH - PADDING * 2
    available_height = FIXED_HEIGHT - TITLE_BAR_HEIGHT - PADDING * 2

    cell_size = min(
        available_width // cols,
        available_height // rows
    )

    # avoid cells that are too small
    return max(8, cell_size)


# ── Helpers ─────────────────────────────────────────────
def get_board_size(difficulty):
    return LEVELS.get(difficulty, LEVELS["easy"])

def get_budget(difficulty):
    return BUDGETS.get(difficulty, BUDGETS["easy"])

def get_screen_size():
    return FIXED_WIDTH, FIXED_HEIGHT