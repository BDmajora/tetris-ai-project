import copy
from .grid import remove_complete_lines
from .position import check_collision, merge_grid_and_block
from .heuristics import TetrisHeuristics

class AI:
    def __init__(self, game, weight_manager):
        self.game = game
        self.wm = weight_manager  # The Judge
        self.h = TetrisHeuristics()  # The Sensors

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        
        # Survival Fallback: Move to center if everything looks like certain death
        fallback_move = (0, self.game.width // 2 - 1)

        for rotation in range(4):
            # 1. Create a test block and apply rotation
            test_block = copy.copy(self.game.current_block)
            for _ in range(rotation): 
                test_block.rotate_clockwise()

            # 2. Constraint Search: Only check X values where the block actually fits
            # This prevents the 'Snail' effect of checking 40+ useless positions
            block_width = len(test_block.shape[0])
            for x in range(0, self.game.width - block_width + 1):
                score, grid_after = self.simulate_move(self.game.grid.grid, test_block, x)
                
                if grid_after is None: 
                    continue

                # 3. Lookahead: How does the NEXT block perform on this resulting grid?
                future_score = self._get_best_future_score(grid_after, self.game.next_block)
                total = score + future_score

                if total > best_score:
                    best_score = total
                    best_move = (rotation, x)
        
        if best_move is None:
            print("AI BRAIN PANIC: No valid moves found. Attempting fallback.")
            return fallback_move
            
        return best_move

    def simulate_move(self, start_grid, block, x):
        """Returns the score and resulting grid for a specific move."""
        # Initial check: if it collides at the very top, this path is a Game Over
        if check_collision(start_grid, block, (x, 0)):
            return float('-inf'), None

        # Faster row-by-row copy for simulation
        grid_copy = [row[:] for row in start_grid]
        
        # Drop the block as far as it can go (Hard Drop simulation)
        y = 0
        while not check_collision(grid_copy, block, (x, y + 1)):
            y += 1
            if y >= len(grid_copy): break
        
        # Merge and clear lines to see the "future" state
        merge_grid_and_block(grid_copy, block, (x, y))
        final_grid, lines_removed = remove_complete_lines(grid_copy)
        
        # Evaluate the grid using our Heuristics
        metrics = self.h.get_all_metrics(final_grid)
        score = self.wm.get_score(metrics, lines_removed)
        
        return score, final_grid

    def _get_best_future_score(self, grid, next_block):
        """One-step lookahead logic."""
        best_future = float('-inf')
        
        for rotation in range(4):
            test_block = copy.copy(next_block)
            for _ in range(rotation): 
                test_block.rotate_clockwise()

            block_width = len(test_block.shape[0])
            # Check reachable width for the next block
            for x in range(0, len(grid[0]) - block_width + 1):
                score, _ = self.simulate_move(grid, test_block, x)
                if score > best_future:
                    best_future = score
        
        # If the next block has no moves, return a penalty (-1000) 
        # instead of -inf to keep the AI trying to survive.
        return best_future if best_future != float('-inf') else -1000