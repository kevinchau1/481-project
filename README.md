# AI Maze Game

## Project Overview
**AI Maze Game** is a **weighted-block puzzle game** built in Python using **Pygame**, where the player places blocks of different weights to block an AI from reaching a goal. The AI uses **A\*** pathfinding to navigate the grid efficiently based on block weights.  

---
## Requirements

- Python 3.10 or higher
- Pygame

---
# How to setup
**1. Clone the repository**
``git clone https://github.com/kevinchau1/481-project.git``<br>
``cd 481-project``

**2. Install dependencies**
pip install pygame

---
## How to Run

python main.py

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
- `config.py` – Configurations for game window dimensions, difficulties, and budgets.

### `ai/` Directory
- `astar.py` – Implements the **A\*** pathfinding algorithm.  
- `weights.py` – Defines block weight logic and calculates path costs.

### `rendering/`  
- `draw_board.py` – Draws the grid and background.  
- `draw_blocks.py` – Draws blocks with proper weights and styles.  
- `draw_ai.py` – Draws the AI and optionally its predicted path.
- `draw_sidebar.py` – Draws the sidebar of weighted blocks.
