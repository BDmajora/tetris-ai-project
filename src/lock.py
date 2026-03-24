from .grid import remove_complete_lines
from .position import check_collision, merge_grid_and_block

class BlockLocker:
    def __init__(self, game):
        self.game = game

    def lock_block_and_update_state(self):
        g = self.game

        # Persistent integration of current block into grid state
        merge_grid_and_block(g.grid.grid, g.current_block, g.current_position)
        
        # Row clearing logic and line count retrieval
        g.grid.grid, lines_removed = remove_complete_lines(g.grid.grid)

        # Scoring and level progression updates based on cleared lines
        if lines_removed > 0:
            points = g.level.get_score(lines_removed)
            g.score += points
            g.level.update_level(lines_removed)

        # Buffer-to-active block transition and new block generation
        g.current_block = g.next_block
        g.next_block = g.get_new_block()
        
        # Spawn coordinates: centered X, vertical offset Y=2
        new_x = g.width // 2 - len(g.current_block.shape[0]) // 2
        g.current_position = [new_x, 2]

        # Terminal state check: immediate collision on spawn indicates Top-Out
        if check_collision(g.grid.grid, g.current_block, g.current_position):
            g.set_game_over()
        
        g.new_block_placed = True