# lock.py

from grid import remove_complete_lines
from position import check_collision, merge_grid_and_block

class BlockLocker:
    def __init__(self, game):
        self.game = game

    def lock_block_and_update_state(self):
        # Alias the game object for easier reference
        game = self.game
        
        # Log the position and shape of the block being locked
        print(f"Locking block at position: {game.current_position} with shape: {game.current_block.shape}")
        
        # Merge the current block into the grid at its current position
        merge_grid_and_block(game.grid.grid, game.current_block, game.current_position)
        
        # Remove complete lines from the grid and get the number of lines removed
        game.grid.grid, lines_removed = remove_complete_lines(game.grid.grid)
        
        # Update the game level based on the number of lines removed
        game.level.update_level(lines_removed)
        
        # Update the game score based on the number of lines removed
        game.score += game.level.get_score(lines_removed)
        
        # Set the current block to the next block and generate a new next block
        game.current_block = game.next_block
        game.next_block = game.get_new_block()
        
        # Reset the current position for the new block at the top center of the grid
        game.current_position = [game.width // 2 - len(game.current_block.shape[0]) // 2, 0]
        
        # Indicate that a new block has been placed
        game.new_block_placed = True
        
        # Check for collisions at the new position; if there is a collision, set the game over state
        if check_collision(game.grid.grid, game.current_block, game.current_position):
            game.set_game_over()
