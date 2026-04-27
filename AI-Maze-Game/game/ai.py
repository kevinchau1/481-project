# game/ai.py
import math
from ai.astar import astar
from ai.weights import get_weight
from game.block import WALL_BLOCK


# AI states
STATE_IDLE      = "idle"
STATE_MOVING    = "moving"
STATE_BLOCKED   = "blocked"
STATE_AT_GOAL   = "at_goal"


class AI:
    def __init__(self, board, fps=60, countdown_seconds=5):
        self.board         = board
        self.position      = board.ai_start
        self.path          = []
        self.path_cost     = None
        self.step_timer    = 0
        self.step_interval = 8  # Faster movement

        # Direction AI is facing (for rendering)
        self.direction     = (0, 1)  # Default facing right (row_delta, col_delta)

        # Current state (for rendering)
        self.state         = STATE_IDLE

        # Countdown
        self.fps               = fps
        self.countdown_seconds = countdown_seconds
        self.countdown_timer   = fps * countdown_seconds
        self.countdown_active  = True

    # ── Pathfinding ──────────────────────────────────────

    def _find_path(self):
        """Find the best path from current position to goal using A*."""
        result = astar(self.board, self.position, self.board.ai_goal)

        if result is None:
            self.path      = []
            self.path_cost = None
            self.state     = STATE_BLOCKED
        else:
            self.path      = result
            self.path_cost = self._calculate_cost(result)
            self.state     = STATE_MOVING

    def _calculate_cost(self, path):
        """Sum up the movement cost of every cell in the path."""
        return sum(get_weight(self.board.get_cell(*cell)) for cell in path)

    def recalculate(self):
        """Called when player places a block. Only recalculates if AI has started."""
        if not self.countdown_active:
            self._find_path()

    # ── Movement ─────────────────────────────────────────

    def update(self):
        if self.countdown_active:
            self.countdown_timer -= 1
            if self.countdown_timer <= 0:
                self.countdown_active = False
                self._find_path()
            return

        if self.is_at_goal():
            self.state = STATE_AT_GOAL
            return

        if not self.path:
            self.state = STATE_BLOCKED
            return

        # Check next step
        if len(self.path) > 1:
            next_pos     = self.path[1]
            next_cell_id = self.board.get_cell(*next_pos)
            weight       = get_weight(next_cell_id)

            if weight is None:
                # WALL_BLOCK — completely impassable, recalculate
                self.state = STATE_BLOCKED
                self._find_path()
                return

            if next_cell_id != 0:
                # Non-wall block — AI steps on it and removes it
                self.board.remove_block(*next_pos)

        # Move forward
        self.step_timer += 1
        if self.step_timer >= self.step_interval:
            self.step_timer = 0
            self._advance()

    def _advance(self):
        """Move AI one step forward and update direction."""
        if len(self.path) > 1:
            next_pos = self.path[1]

            # Update direction based on movement
            dr = next_pos[0] - self.position[0]
            dc = next_pos[1] - self.position[1]
            if (dr, dc) != (0, 0):
                self.direction = (dr, dc)

            self.path.pop(0)
            self.position = self.path[0]
            self.state    = STATE_MOVING

    # ── Status ───────────────────────────────────────────

    def is_at_goal(self):
        return self.position == self.board.ai_goal

    def has_path(self):
        return len(self.path) > 0

    def get_countdown_seconds_left(self):
        return math.ceil(self.countdown_timer / self.fps)

    def reset(self):
        self.position         = self.board.ai_start
        self.step_timer       = 0
        self.path             = []
        self.path_cost        = None
        self.direction        = (0, 1)
        self.state            = STATE_IDLE
        self.countdown_timer  = self.fps * self.countdown_seconds
        self.countdown_active = True