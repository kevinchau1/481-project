# AI Maze Game

## Project Overview
**AI Maze Game** is a **weighted-block puzzle game** built in Python using **Pygame**, where the player places blocks of different weights to block an AI from reaching a goal. The AI uses **A\*** pathfinding to navigate the grid efficiently based on block weights.  

---

## Project Structure
### `main.py`
- Entry point of the game.
- Initializes Pygame, loads configuration, sets up the game loop, and handles events.

### `game/` Directory
- `board.py` – Defines the grid/board, including dimensions and methods to update cells.  
- `block.py` – Defines block types, weights, and special properties (like “trap” blocks).  
- `player.py` – Handles player actions, such as placing blocks on the board.  
- `ai.py` – AI logic for determining the best path using the weighted grid.  
- `game_loop.py` – Updates the game state, handles input, and triggers rendering.

### `ai/` Directory
- `astar.py` – Implements the **A\*** pathfinding algorithm.  
- `dijkstra.py` – Optional alternative algorithm.  
- `weights.py` – Defines block weight logic and calculates path costs.

### `rendering/`  
- `draw_board.py` – Draws the grid and background.  
- `draw_blocks.py` – Draws blocks with proper weights and styles.  
- `draw_ai.py` – Draws the AI and optionally its predicted path.

### `assets/`  
- `images/` – Sprites and block images.  
- `sounds/` – Game sounds and effects.  
- `fonts/` – Fonts for displaying scores, messages, and UI.
