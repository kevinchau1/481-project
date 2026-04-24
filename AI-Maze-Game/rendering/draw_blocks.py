# draw_blocks.py
# draws placed blocks on the grid with neon cyberpunk style

import pygame
from draw_board import CELL_SIZE, PADDING, TITLE_BAR_HEIGHT, cell_to_pixel
from block import EMPTY, LIGHT_BLOCK, MEDIUM_BLOCK, HEAVY_BLOCK, TRAP_BLOCK, WALL_BLOCK
from weights import get_weight

# neon color palette: (base_color, glow_color, text_color)
BLOCK_COLORS = {
    EMPTY:        None,
    LIGHT_BLOCK:  ((0,  180,  80),  (0,  255, 120), (200, 255, 220)),
    MEDIUM_BLOCK: ((180, 120,   0), (255, 180,   0), (255, 240, 180)),
    HEAVY_BLOCK:  ((180,  20,  20), (255,  50,  50), (255, 200, 200)),
    TRAP_BLOCK:   ((120,   0, 180), (180,   0, 255), (230, 180, 255)),
    WALL_BLOCK:   ((30,   30,  40), (80,   80, 100), (150, 150, 170)),
}

BLOCK_INSET = 4


def draw_block(screen, row, col, block_id, font):
    if block_id == EMPTY or block_id not in BLOCK_COLORS:
        return

    base_color, glow_color, text_color = BLOCK_COLORS[block_id]

    x, y = cell_to_pixel(row, col)
    x += BLOCK_INSET
    y += BLOCK_INSET
    w = CELL_SIZE - BLOCK_INSET * 2
    h = CELL_SIZE - BLOCK_INSET * 2

    block_rect = pygame.Rect(x, y, w, h)

    # base fill
    pygame.draw.rect(screen, base_color, block_rect)

    # top highlight strip
    highlight_rect = pygame.Rect(x, y, w, h // 4)
    highlight_color = (
        min(base_color[0] + 60, 255),
        min(base_color[1] + 60, 255),
        min(base_color[2] + 60, 255),
    )
    pygame.draw.rect(screen, highlight_color, highlight_rect)

    # neon border (double pass for glow feel)
    pygame.draw.rect(screen, glow_color, block_rect, 2)
    inner_rect = pygame.Rect(x + 2, y + 2, w - 4, h - 4)
    pygame.draw.rect(screen, glow_color, inner_rect, 1)

    # weight label bottom right
    weight = get_weight(block_id)
    label_text = str(weight) if weight is not None else "X"
    label = font.render(label_text, True, text_color)
    label_x = x + w - label.get_width() - 5
    label_y = y + h - label.get_height() - 3
    screen.blit(label, (label_x, label_y))


def draw_all_blocks(screen, board, font):
    for row in range(board.rows):
        for col in range(board.cols):
            block_id = board.get_cell(row, col)
            if block_id != EMPTY:
                draw_block(screen, row, col, block_id, font)