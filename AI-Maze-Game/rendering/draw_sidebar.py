# draw_sidebar.py
# draws the block selection panel on the right side

import pygame
from rendering.draw_board import GOAL_COLOR
from rendering.draw_blocks import BLOCK_COLORS
from game.block import LIGHT_BLOCK, MEDIUM_BLOCK, HEAVY_BLOCK, TRAP_BLOCK, WALL_BLOCK
from ai.weights import money_cost
from game.config import SIDEBAR_WIDTH, TITLE_BAR_HEIGHT

SELECTABLE_BLOCKS = [
    LIGHT_BLOCK,
    MEDIUM_BLOCK,
    HEAVY_BLOCK,
    TRAP_BLOCK,
    WALL_BLOCK,
]

BLOCK_NAMES = {
    LIGHT_BLOCK: "Light",
    MEDIUM_BLOCK: "Medium",
    HEAVY_BLOCK: "Heavy",
    TRAP_BLOCK: "Trap",
    WALL_BLOCK: "Wall",
}

BUTTON_SIZE    = 44
BUTTON_PADDING = 40
BUTTON_START_Y = TITLE_BAR_HEIGHT + 70 # pushed down to make room for budget display

def get_button_rects(screen_width):
    rects = {}
    sidebar_x = screen_width - SIDEBAR_WIDTH
    center_x  = sidebar_x + SIDEBAR_WIDTH // 2

    y = BUTTON_START_Y
    for block_id in SELECTABLE_BLOCKS:
        btn_x = center_x - BUTTON_SIZE // 2
        rects[block_id] = pygame.Rect(btn_x, y, BUTTON_SIZE, BUTTON_SIZE)
        y += BUTTON_SIZE + BUTTON_PADDING

    return rects


def draw_budget(screen, screen_width, budget, font_label, font_title):
    sidebar_x = screen_width - SIDEBAR_WIDTH
    center_x  = sidebar_x + SIDEBAR_WIDTH // 2

    # budget label
    label = font_title.render("BUDGET", True, (150, 150, 170))
    screen.blit(label, (center_x - label.get_width() // 2, TITLE_BAR_HEIGHT + 10))

    # pick color based on how much budget is left
    if budget > 60:
        budget_color = (0, 255, 120)      # green - plenty left
    elif budget > 25:
        budget_color = (255, 180, 0)      # amber - getting low
    else:
        budget_color = (255, 50, 50)      # red - almost broke

    # coin amount, big and bold
    amount = font_title.render(f"{budget} coins", True, budget_color)
    screen.blit(amount, (center_x - amount.get_width() // 2, TITLE_BAR_HEIGHT + 26))

    # thin divider line under budget
    pygame.draw.line(
        screen,
        (40, 40, 60),
        (sidebar_x + 10, TITLE_BAR_HEIGHT + 52),
        (screen_width - 10, TITLE_BAR_HEIGHT + 52),
        1
    )


def draw_sidebar(screen, screen_width, screen_height, selected_block_id, font_label, font_title, budget):
    sidebar_x = screen_width - SIDEBAR_WIDTH

    #budget display at the top
    draw_budget(screen, screen_width, budget, font_label, font_title)

    #BLOCKS title
    title = font_title.render("BLOCKS", True, GOAL_COLOR)
    title_x = sidebar_x + SIDEBAR_WIDTH // 2 - title.get_width() // 2
    screen.blit(title, (title_x, TITLE_BAR_HEIGHT + 56))

    #draw each block button
    button_rects = get_button_rects(screen_width)

    for block_id in SELECTABLE_BLOCKS:
        rect = button_rects[block_id]

        if block_id not in BLOCK_COLORS or BLOCK_COLORS[block_id] is None:
            continue

        base_color, glow_color, text_color = BLOCK_COLORS[block_id]

        cost = money_cost(block_id)
        cant_afford = budget < cost and block_id != WALL_BLOCK

        # dim the block if player cant afford it
        if cant_afford:
            draw_color = tuple(max(0, c - 80) for c in base_color)
            border_color = (60, 60, 60)
        else:
            draw_color = base_color
            border_color = glow_color

        # base fill
        pygame.draw.rect(screen, draw_color, rect)

        # top highlight strip
        highlight_rect = pygame.Rect(rect.x, rect.y, rect.w, rect.h // 4)
        highlight_color = (
            min(draw_color[0] + 60, 255),
            min(draw_color[1] + 60, 255),
            min(draw_color[2] + 60, 255),
        )
        pygame.draw.rect(screen, highlight_color, highlight_rect)

        # border — white if selected, dimmed if cant afford
        if block_id == selected_block_id:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
        else:
            pygame.draw.rect(screen, border_color, rect, 2)

        # block name
        name_color = (100, 100, 100) if cant_afford else (200, 200, 200)
        name = font_label.render(BLOCK_NAMES[block_id], True, name_color)
        name_x = rect.x + rect.w // 2 - name.get_width() // 2
        screen.blit(name, (name_x, rect.bottom + 3))

        # coin cost label (not A* weight)
        if block_id == WALL_BLOCK:
            cost_text = "pre-placed"
        else:
            cost_text = f"{cost} coins"
        cost_label_color = (80, 80, 80) if cant_afford else (120, 120, 120)
        cost_surf = font_label.render(cost_text, True, cost_label_color)
        cost_x = rect.x + rect.w // 2 - cost_surf.get_width() // 2
        screen.blit(cost_surf, (cost_x, rect.bottom + 16))

    # hint text at the bottom
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