# rendering/draw_ai.py
import pygame
import math
from rendering.draw_board import PADDING, TITLE_BAR_HEIGHT, cell_to_pixel
from game.ai import STATE_MOVING, STATE_BLOCKED, STATE_AT_GOAL, STATE_IDLE

# Colors per state
STATE_COLORS = {
    STATE_IDLE:    (0,   200, 200),   # dim cyan
    STATE_MOVING:  (0,   255, 255),   # bright cyan
    STATE_BLOCKED: (255, 80,  80),    # red = stuck
    STATE_AT_GOAL: (255, 215, 0),     # gold = reached goal
}


def draw_path(screen, path, CELL_SIZE):
    # Draw yellow dots along the A* path.
    if not path:
        return

    PATH_COLOR  = (255, 255, 0)
    PATH_RADIUS = max(2, CELL_SIZE // 6)

    for row, col in path[1:-1]:
        x, y = cell_to_pixel(row, col, CELL_SIZE)
        cx = x + CELL_SIZE // 2
        cy = y + CELL_SIZE // 2
        pygame.draw.circle(screen, PATH_COLOR, (cx, cy), PATH_RADIUS)


def draw_ai(screen, ai, CELL_SIZE):
    """
    Draw AI circle with:
    - Color based on current state
    - Arrow indicating current direction
    """
    row, col  = ai.position
    x, y      = cell_to_pixel(row, col, CELL_SIZE)
    cx        = x + CELL_SIZE // 2
    cy        = y + CELL_SIZE // 2
    AI_RADIUS = max(4, CELL_SIZE // 2 - 4)

    color = STATE_COLORS.get(ai.state, (0, 255, 255))

    # Outer glow
    pygame.draw.circle(screen, tuple(c // 3 for c in color), (cx, cy), AI_RADIUS + 5)
    # Main circle
    pygame.draw.circle(screen, color, (cx, cy), AI_RADIUS)
    # Center dot
    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), max(2, CELL_SIZE // 12))

    # Direction arrow
    _draw_direction_arrow(screen, cx, cy, ai.direction, AI_RADIUS, color)


def _draw_direction_arrow(screen, cx, cy, direction, radius, color):
    # Draw a small arrow on the AI indicating its current facing direction.
    dr, dc = direction

    # Angle: col = x axis, row = y axis (y is flipped in pygame)
    angle  = math.atan2(dr, dc)  # radians
    length = radius * 0.7

    # Arrow tip
    tip_x = cx + int(length * math.cos(angle))
    tip_y = cy + int(length * math.sin(angle))

    # Arrow base (perpendicular wings)
    wing_angle  = 0.5  # radians
    wing_length = radius * 0.35

    wing1_x = tip_x - int(wing_length * math.cos(angle - wing_angle))
    wing1_y = tip_y - int(wing_length * math.sin(angle - wing_angle))

    wing2_x = tip_x - int(wing_length * math.cos(angle + wing_angle))
    wing2_y = tip_y - int(wing_length * math.sin(angle + wing_angle))

    pygame.draw.polygon(screen, (255, 255, 255), [(tip_x, tip_y), (wing1_x, wing1_y), (wing2_x, wing2_y)])