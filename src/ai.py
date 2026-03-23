import copy
from .grid import remove_complete_lines
from .position import check_collision, merge_grid_and_block
from .heuristics import TetrisHeuristics
from .weights import WeightManager

class AI:
    def __init__(self, game, hole_weight=3, height_weight=9, column_weight=5, use_quantized=False):
        self.game = game
        self.wm = WeightManager(hole_weight, height_weight, column_weight, use_quantized)
        self.evaluator = TetrisHeuristics()

    def get_best_move(self):
        """
        Two-piece lookahead: Evaluates the best current move based on
        the best possible subsequent move for the next block.
        """
        best_score = float('-inf')
        best_move = None
        
        current_block = self.game.current_block
        next_block = self.game.next_block

        # 1. Simulate all possible moves for the CURRENT block
        for rotation in range(4):
            block = copy.deepcopy(current_block)
            for _ in range(rotation):
                block.rotate()

            # Boundary check: Ensure rotation doesn't push block out of bounds
            block_width = len(block.shape[0])
            for x in range(self.game.width - block_width + 1):
                score_now, grid_after_move = self.simulate_move(self.game.grid.grid, block, x)
                
                if score_now == float('-inf'):
                    continue

                # 2. LOOKAHEAD: Score the best possible outcome for the NEXT block
                score_future = self._get_best_future_score(grid_after_move, next_block)
                
                total_score = score_now + score_future

                if total_score > best_score:
                    best_score = total_score
                    best_move = (rotation, x)
                    
        return best_move

    def _get_best_future_score(self, grid, next_block):
        """Finds the max evaluation score possible for the next piece on a given grid."""
        best_future = float('-inf')
        
        for rotation in range(4):
            block = copy.deepcopy(next_block)
            for _ in range(rotation):
                block.rotate()
                
            block_width = len(block.shape[0])
            for x in range(self.game.width - block_width + 1):
                score, _ = self.simulate_move(grid, block, x)
                if score > best_future:
                    best_future = score
        
        return best_future if best_future != float('-inf') else -10000

    def simulate_move(self, start_grid, block, x):
        """Simulates placing a block and returns the score and resulting grid."""
        grid_copy = copy.deepcopy(start_grid)
        y = self._drop_block_sim(grid_copy, block, x)

        if y < 0: 
            return float('-inf'), None

        merge_grid_and_block(grid_copy, block, (x, y))
        grid_final, lines_removed = remove_complete_lines(grid_copy)
        
        return self.evaluate_grid(grid_final, lines_removed), grid_final

    def _drop_block_sim(self, grid, block, x):
        """Simulates gravity until the block hits something."""
        if check_collision(grid, block, (x, 0)):
            return -1
            
        y = 0
        while not check_collision(grid, block, (x, y)):
            y += 1
        return y - 1

    def evaluate_grid(self, grid, lines_removed):
        """
        The Scoring Engine.
        Uses a mix of static weights and dynamic penalties to judge the board state.
        """
        h = self.evaluator
        heights = h.get_column_heights(grid)
        
        # NEW: The 'Bottom-Up' fix. Holes + how many blocks are on top of them.
        holes, blockades = h.get_holes_and_blockades(grid)
        
        # NEW: Well penalty to prevent deep 1-cell gaps.
        wells = h.get_wells(heights)
        
        bumpiness = h.get_bumpiness(heights)
        max_h = max(heights) if heights else 0
        
        # SCORING LOGIC
        # ---------------------------------------------------------
        score = (lines_removed ** 2) * 40  # Reward clearing multiple lines at once
        
        # Penalties (Higher value = more weight)
        score -= (holes * 35)              # Base penalty for an empty space
        score -= (blockades * 20)          # PENALTY: Covering an existing hole
        score -= (bumpiness * 4)           # Prefer a flat surface
        score -= (wells * 10)              # Avoid deep, narrow columns
        
        # Height management
        score -= sum(heights) * 2          # Keep average height low
        score -= (max_h * self.wm.height_weight)  # Strong penalty for approaching the top
        
        return score