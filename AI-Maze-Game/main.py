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
from rendering.draw_board import draw_board, PADDING, TITLE_BAR_HEIGHT, SIDEBAR_WIDTH
from rendering.draw_blocks import draw_all_blocks
from rendering.draw_sidebar import draw_sidebar, get_button_rects
from rendering.draw_ai import draw_ai, draw_path

FPS = 60


def main():
    pygame.init()

    difficulty = "very_hard"  # "easy"/ "medium"/ "hard"/ "very_hard"
    rows, cols = get_board_size(difficulty)
    board = Board(rows, cols)

    CELL_SIZE = compute_cell_size(rows, cols)

    screen_width, screen_height = get_screen_size()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("CPSC 481 AI Maze Game")

    clock = pygame.time.Clock()

    font_block  = pygame.font.SysFont("Courier", 13, bold=True)
    font_label  = pygame.font.SysFont("Courier", 11)
    font_title  = pygame.font.SysFont("Courier", 15, bold=True)

    # which block the player has selected in the sidebar
    # player.py will manage this properly later
    selected_block = LIGHT_BLOCK
    generate_maze(board)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # temporary: clicking a sidebar button selects it
            # player.py will take this over later
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_rects = get_button_rects(screen_width)
                for block_id, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        selected_block = block_id

        # draw everything
        draw_board(screen, board, screen_width, screen_height, CELL_SIZE)
        draw_all_blocks(screen, board, font_block, CELL_SIZE)
        draw_sidebar(screen, screen_width, screen_height, selected_block, font_label, font_title)



        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()