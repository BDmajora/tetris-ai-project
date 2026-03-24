# lock.py

from .grid import remove_complete_lines
from .position import check_collision, merge_grid_and_block

class BlockLocker:
    def __init__(self, game):
        self.game = game

    def lock_block_and_update_state(self):
        g = self.game

        # 1. Lock the old block into the grid
        merge_grid_and_block(g.grid.grid, g.current_block, g.current_position)
        
        # 2. Clear lines and capture the count for scoring
        # We replace the '_' with 'lines_removed' to feed the Level class
        g.grid.grid, lines_removed = remove_complete_lines(g.grid.grid)

        # 3. UPDATE SCORE AND LEVEL
        if lines_removed > 0:
            # Calculate points using the NES formula from Level class
            points = g.level.get_score(lines_removed)
            g.score += points
            
            # Update the level and gravity speed
            g.level.update_level(lines_removed)

        # 4. Spawn the NEW block at the visible top (Y=2)
        g.current_block = g.next_block
        g.next_block = g.get_new_block()
        
        # Set X to center, Y to 2
        new_x = g.width // 2 - len(g.current_block.shape[0]) // 2
        g.current_position = [new_x, 2]

        # 5. Check for Top-Out (Game Over)
        # If the new block collides immediately upon spawning, it's Game Over
        if check_collision(g.grid.grid, g.current_block, g.current_position):
            g.set_game_over()
        
        g.new_block_placed = True