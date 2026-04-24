# main.py
# entry point of the game

import pygame
import sys

sys.path.append("game")
sys.path.append("rendering")
sys.path.append("ai")

from board import Board
from block import LIGHT_BLOCK, MEDIUM_BLOCK, HEAVY_BLOCK, TRAP_BLOCK, WALL_BLOCK
from draw_board import draw_board, CELL_SIZE, PADDING, TITLE_BAR_HEIGHT, SIDEBAR_WIDTH
from draw_blocks import draw_all_blocks
from draw_sidebar import draw_sidebar, get_button_rects

FPS = 60


def main():
    pygame.init()

    board = Board()

    screen_width  = board.cols * CELL_SIZE + PADDING * 2 + SIDEBAR_WIDTH
    screen_height = board.rows * CELL_SIZE + PADDING * 2 + TITLE_BAR_HEIGHT

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("CPSC 481 AI Maze Game")

    clock = pygame.time.Clock()

    font_block  = pygame.font.SysFont("Courier", 13, bold=True)
    font_label  = pygame.font.SysFont("Courier", 11)
    font_title  = pygame.font.SysFont("Courier", 15, bold=True)

    # which block the player has selected in the sidebar
    # player.py will manage this properly later
    selected_block = LIGHT_BLOCK

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
        draw_board(screen, board, screen_width, screen_height)
        draw_all_blocks(screen, board, font_block)
        draw_sidebar(screen, screen_width, screen_height, selected_block, font_label, font_title)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()