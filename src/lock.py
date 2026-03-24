# lock.py

from .grid import remove_complete_lines
from .position import check_collision, merge_grid_and_block

class BlockLocker:
    def __init__(self, game):
        self.game = game

    def lock_block_and_update_state(self):
        # 1. Lock the old block
        merge_grid_and_block(self.game.grid.grid, self.game.current_block, self.game.current_position)
        
        # 2. Clear lines
        self.game.grid.grid, _ = remove_complete_lines(self.game.grid.grid)

        # 3. CRITICAL: Spawn the NEW block at the visible top (Y=2)
        self.game.current_block = self.game.next_block
        self.game.next_block = self.game.get_new_block()
        
        # Set X to center, Y to 2
        new_x = self.game.width // 2 - len(self.game.current_block.shape[0]) // 2
        self.game.current_position = [new_x, 2] # <--- THIS MUST BE 2

        # 4. Check for Top-Out (Game Over)
        if check_collision(self.game.grid.grid, self.game.current_block, self.game.current_position):
            self.game.set_game_over()
        
        self.game.new_block_placed = True
