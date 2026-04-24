# draw_board.py
# draws the grid and background
# grid sits on the LEFT, sidebar is on the RIGHT

import pygame

# colors
WHITE       = (255, 255, 255)
GRAY        = (200, 200, 200)   # grid lines
DARK_GRAY   = (30,  30,  30)    # main background
PANEL_COLOR = (20,  20,  20)    # title bar background
SIDEBAR_COLOR = (18, 18, 25)    # sidebar background, slightly blue-tinted
GOAL_COLOR  = (255, 215,   0)   # gold for goal cell
START_COLOR = (0,   200, 255)   # cyan for AI start cell
TITLE_COLOR = (255, 255, 255)

# layout constants
CELL_SIZE        = 60
PADDING          = 20
TITLE_BAR_HEIGHT = 60
SIDEBAR_WIDTH    = 200    # right panel width

# helper: converts (row, col) to pixel (x, y) on screen
def cell_to_pixel(row, col):
    x = PADDING + col * CELL_SIZE
    y = TITLE_BAR_HEIGHT + PADDING + row * CELL_SIZE
    return x, y


def draw_background(screen):
    screen.fill(DARK_GRAY)


def draw_sidebar_background(screen, screen_width, screen_height):
    # fill the sidebar area
    sidebar_x = screen_width - SIDEBAR_WIDTH
    sidebar_rect = pygame.Rect(sidebar_x, 0, SIDEBAR_WIDTH, screen_height)
    pygame.draw.rect(screen, SIDEBAR_COLOR, sidebar_rect)

    # divider line between grid and sidebar
    pygame.draw.line(
        screen,
        GOAL_COLOR,
        (sidebar_x, TITLE_BAR_HEIGHT),
        (sidebar_x, screen_height),
        2
    )


def draw_title(screen, screen_width):
    # title bar across the full width
    title_rect = pygame.Rect(0, 0, screen_width, TITLE_BAR_HEIGHT)
    pygame.draw.rect(screen, PANEL_COLOR, title_rect)

    # gold underline
    pygame.draw.line(screen, GOAL_COLOR, (0, TITLE_BAR_HEIGHT), (screen_width, TITLE_BAR_HEIGHT), 2)

    # centered title text
    font = pygame.font.SysFont("Courier", 26, bold=True)
    title_surface = font.render("CPSC 481 AI Maze Game", True, TITLE_COLOR)
    title_x = (screen_width - SIDEBAR_WIDTH) // 2 - title_surface.get_width() // 2
    title_y = TITLE_BAR_HEIGHT // 2 - title_surface.get_height() // 2
    screen.blit(title_surface, (title_x, title_y))


def draw_grid(screen, board):
    for row in range(board.rows):
        for col in range(board.cols):
            x, y = cell_to_pixel(row, col)
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)


def draw_start_and_goal(screen, board):
    # start cell
    start_row, start_col = board.ai_start
    sx, sy = cell_to_pixel(start_row, start_col)
    start_rect = pygame.Rect(sx, sy, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, START_COLOR, start_rect)
    pygame.draw.rect(screen, GRAY, start_rect, 1)

    # goal cell
    goal_row, goal_col = board.ai_goal
    gx, gy = cell_to_pixel(goal_row, goal_col)
    goal_rect = pygame.Rect(gx, gy, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, GOAL_COLOR, goal_rect)
    pygame.draw.rect(screen, GRAY, goal_rect, 1)


def draw_board(screen, board, screen_width, screen_height):
    draw_background(screen)
    draw_sidebar_background(screen, screen_width, screen_height)
    draw_title(screen, screen_width)
    draw_grid(screen, board)
    draw_start_and_goal(screen, board)