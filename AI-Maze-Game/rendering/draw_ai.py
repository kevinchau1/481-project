# draw_ai.py
import pygame
from rendering.draw_board import PADDING, TITLE_BAR_HEIGHT, cell_to_pixel

# Colors
AI_COLOR      = (0, 255, 255)    # cyan
PATH_COLOR    = (255, 255, 0)    # yellow
#PATH_ALPHA    = 120

#AI_RADIUS     = CELL_SIZE // 2 - 6
#PATH_RADIUS   = CELL_SIZE // 6


def draw_path(screen, path, CELL_SIZE):
    # Draw yellow dots along the A* path
    if not path:
        return
    
    PATH_RADIUS = max(2, CELL_SIZE // 6)
    
    for row, col in path[1:-1]:  # Skip start and goal
        x, y = cell_to_pixel(row, col)
        cx = x + CELL_SIZE // 2
        cy = y + CELL_SIZE // 2
        pygame.draw.circle(screen, PATH_COLOR, (cx, cy), PATH_RADIUS)


def draw_ai(screen, row, col, CELL_SIZE):
    # Draw the AI as a cyan circle
    x, y = cell_to_pixel(row, col, CELL_SIZE)
    cx = x + CELL_SIZE // 2
    cy = y + CELL_SIZE // 2

    AI_RADIUS = max(4, CELL_SIZE // 2 - 6)

    # Outer glow
    pygame.draw.circle(screen, (0, 150, 150), (cx, cy), AI_RADIUS + 4)
    # Inner circle
    pygame.draw.circle(screen, AI_COLOR, (cx, cy), AI_RADIUS)
    # Center dot
    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), max(2, CELL_SIZE // 10))