# draw_sidebar.py
# draws the block selection panel on the right side
# player will later click/drag from here to place blocks on the grid

import pygame
from draw_board import SIDEBAR_WIDTH, TITLE_BAR_HEIGHT, GOAL_COLOR
from draw_blocks import BLOCK_COLORS
from block import LIGHT_BLOCK, MEDIUM_BLOCK, HEAVY_BLOCK, TRAP_BLOCK, WALL_BLOCK
from weights import get_weight

# the blocks the player can pick from, in order
SELECTABLE_BLOCKS = [
    LIGHT_BLOCK,
    MEDIUM_BLOCK,
    HEAVY_BLOCK,
    TRAP_BLOCK,
    WALL_BLOCK,
]

BLOCK_NAMES = {
    LIGHT_BLOCK:  "Light",
    MEDIUM_BLOCK: "Medium",
    HEAVY_BLOCK:  "Heavy",
    TRAP_BLOCK:   "Trap",
    WALL_BLOCK:   "Wall",
}

# sidebar block button size + spacing
BUTTON_SIZE    = 44
BUTTON_PADDING = 40
BUTTON_START_Y = TITLE_BAR_HEIGHT + 30   # where the first button starts


def get_button_rects(screen_width):
    # returns a dict of block_id -> pygame.Rect for each sidebar button
    # used both for drawing and for click detection in player.py later
    rects = {}
    sidebar_x = screen_width - SIDEBAR_WIDTH
    center_x  = sidebar_x + SIDEBAR_WIDTH // 2

    y = BUTTON_START_Y
    for block_id in SELECTABLE_BLOCKS:
        btn_x = center_x - BUTTON_SIZE // 2
        rects[block_id] = pygame.Rect(btn_x, y, BUTTON_SIZE, BUTTON_SIZE)
        y += BUTTON_SIZE + BUTTON_PADDING

    return rects


def draw_sidebar(screen, screen_width, screen_height, selected_block_id, font_label, font_title):
    sidebar_x = screen_width - SIDEBAR_WIDTH

    # --- sidebar title ---
    title = font_title.render("BLOCKS", True, GOAL_COLOR)
    title_x = sidebar_x + SIDEBAR_WIDTH // 2 - title.get_width() // 2
    screen.blit(title, (title_x, TITLE_BAR_HEIGHT + 8))

    # --- draw each block button ---
    button_rects = get_button_rects(screen_width)

    for block_id in SELECTABLE_BLOCKS:
        rect = button_rects[block_id]

        if block_id not in BLOCK_COLORS or BLOCK_COLORS[block_id] is None:
            continue

        base_color, glow_color, text_color = BLOCK_COLORS[block_id]

        # base fill
        pygame.draw.rect(screen, base_color, rect)

        # top highlight strip
        highlight_rect = pygame.Rect(rect.x, rect.y, rect.w, rect.h // 4)
        highlight_color = (
            min(base_color[0] + 60, 255),
            min(base_color[1] + 60, 255),
            min(base_color[2] + 60, 255),
        )
        pygame.draw.rect(screen, highlight_color, highlight_rect)

        # border — thicker + brighter if selected
        if block_id == selected_block_id:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)   # white border = selected
        else:
            pygame.draw.rect(screen, glow_color, rect, 2)

        # block name below the button
        name = font_label.render(BLOCK_NAMES[block_id], True, (200, 200, 200))
        name_x = rect.x + rect.w // 2 - name.get_width() // 2
        screen.blit(name, (name_x, rect.bottom + 3))

        # cost label below the name
        weight = get_weight(block_id)
        cost_text = f"cost: {weight}" if weight is not None else "blocked"
        cost = font_label.render(cost_text, True, (120, 120, 120))
        cost_x = rect.x + rect.w // 2 - cost.get_width() // 2
        screen.blit(cost, (cost_x, rect.bottom + 16))

    # --- hint text at the bottom ---
    hint_lines = [
        "click to select",
        "then click grid",
        "to place block",
    ]
    hint_y = screen_height - 80
    for line in hint_lines:
        hint = font_label.render(line, True, (80, 80, 100))
        hint_x = sidebar_x + SIDEBAR_WIDTH // 2 - hint.get_width() // 2
        screen.blit(hint, (hint_x, hint_y))
        hint_y += 16