# main.py
# entry point of the game

import pygame
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.board import Board
from game.block import LIGHT_BLOCK
from game.maze import generate_maze
from game.config import get_board_size, compute_cell_size, get_screen_size
from game.player import Player
from rendering.draw_board import draw_board, PADDING, TITLE_BAR_HEIGHT, SIDEBAR_WIDTH
from rendering.draw_blocks import draw_all_blocks
from rendering.draw_sidebar import draw_sidebar, get_button_rects
from rendering.draw_ai import draw_ai, draw_path

FPS = 60


# Convert a mouse position on the screen into a board cell.
def pixel_to_cell(x, y, board, CELL_SIZE):
    grid_left = PADDING
    grid_top = TITLE_BAR_HEIGHT + PADDING
    grid_right = grid_left + board.cols * CELL_SIZE
    grid_bottom = grid_top + board.rows * CELL_SIZE

    # Ignore clicks outside the playable grid.
    if not (grid_left <= x < grid_right and grid_top <= y < grid_bottom):
        return None

    col = (x - grid_left) // CELL_SIZE
    row = (y - grid_top) // CELL_SIZE
    return row, col


def main():
    pygame.init()

    difficulty = "very_hard"  # "easy"/ "medium"/ "hard"/ "very_hard"
    rows, cols = get_board_size(difficulty)
    board = Board(rows, cols)

    CELL_SIZE = compute_cell_size(rows, cols)

    screen_width, screen_height = get_screen_size()
    generate_maze(board)

    # ── Player ───────────────────────────────────────────
    player = Player()
    player.select_block(LIGHT_BLOCK)

    # ── Window ───────────────────────────────────────────
    screen_width, screen_height = get_screen_size()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("CPSC 481 AI Maze Game")
    clock = pygame.time.Clock()

    # ── Fonts ────────────────────────────────────────────
    font_block = pygame.font.SysFont("Courier", 13, bold=True)
    font_label = pygame.font.SysFont("Courier", 11)
    font_title = pygame.font.SysFont("Courier", 15, bold=True)

    # ── State ────────────────────────────────────────────
    drag_source = None

    # ── Game loop ────────────────────────────────────────
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            # Left click either selects a sidebar block or interacts with the grid.
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button_rects = get_button_rects(screen_width)
                clicked_sidebar = False
                for block_id, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        player.select_block(block_id)
                        clicked_sidebar = True
                        break
                # If the click was on the sidebar, do not also treat it like a board click.
                if clicked_sidebar:
                    continue

                clicked_cell = pixel_to_cell(*event.pos, board, CELL_SIZE)
                if clicked_cell is None:
                    continue

                row, col = clicked_cell

                # Clicking an existing block starts a drag.
                if not board.is_empty(row, col):
                    drag_source = (row, col)
                else:
                    # Clicking an empty cell tries to place the selected block there.
                    try:
                        player.place_selected_block(board, row, col)
                    except ValueError:
                        pass

            # Releasing the mouse finishes a drag and tries to move the block.
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drag_source is None:
                    continue

                target_cell = pixel_to_cell(*event.pos, board, CELL_SIZE)
                if target_cell is not None and target_cell != drag_source:
                    try:
                        player.move_block(board, *drag_source, *target_cell)
                    except ValueError:
                        pass

                drag_source = None

        # Draw the board, blocks, and sidebar every frame.
                # draw everything
        draw_board(screen, board, screen_width, screen_height, CELL_SIZE)
        draw_all_blocks(screen, board, font_block, CELL_SIZE)
        draw_sidebar(screen, screen_width, screen_height, player.selected_block, font_label, font_title)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
