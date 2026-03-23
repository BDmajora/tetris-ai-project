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
        best_score, best_move = float('-inf'), None
        for rotation in range(4):
            block = copy.deepcopy(self.game.current_block)
            for _ in range(rotation):
                block.rotate()

            for x in range(self.game.width - len(block.shape[0]) + 1):
                score, _ = self.simulate_move(block, x)
                if score > best_score:
                    best_score, best_move = score, (rotation, x)
        return best_move

    def simulate_move(self, block, x):
        grid_copy = copy.deepcopy(self.game.grid.grid)
        y = self._drop_block_sim(grid_copy, block, x)

        if y < 0: return float('-inf'), grid_copy

        merge_grid_and_block(grid_copy, block, (x, y))
        grid_copy, lines_removed = remove_complete_lines(grid_copy)
        
        return self.evaluate_grid(grid_copy, lines_removed), grid_copy

    def _drop_block_sim(self, grid, block, x):
        y = 0
        while not check_collision(grid, block, (x, y)):
            y += 1
        return y - 1

    def evaluate_grid(self, grid, lines_removed):
        h = self.evaluator
        heights = h.get_column_heights(grid)
        holes = h.get_holes(grid)
        bumpiness = h.get_bumpiness(heights)
        hole_count, col_list = h.get_hole_and_column_count(grid)
        
        # Scoring Logic
        score = (lines_removed * 10)
        score -= sum(heights) 
        score -= (holes * 5)
        score -= bumpiness
        score -= (hole_count * self.wm.hole_weight)
        
        # Calculate height score based on max height
        max_h = max(heights) if heights else 0
        score += (max_h / len(grid)) * self.wm.height_weight
        
        return score