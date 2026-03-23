import pygame
from grid import Grid
from blocks import create_block, shapes
from position import check_collision, merge_grid_and_block
from level import Level
import random
import copy
from ai import AI
from screen import ScreenHandler
from plan import MovePlanner
from perform import MovePerformer
from lock import BlockLocker

class Game:
    def __init__(self, width, height):
        self.width = width  # Width of the game grid
        self.height = height  # Height of the game grid
        self.grid = Grid(width, height)  # Initialize the game grid
        self.current_block = self.get_new_block()  # Get the first block
        self.current_position = [self.width // 2 - len(self.current_block.shape[0]) // 2, 0]  # Initial block position
        self.next_block = self.get_new_block()  # Get the next block
        self.score = 0  # Initialize score
        self.level = Level()  # Initialize level
        self.game_over = False  # Game over flag
        self.gravity_timer = 0  # Timer to manage gravity effect
        self.ai = AI(self)  # Initialize AI
        self.new_block_placed = False  # Flag for new block placement
        self.target_position = None  # Target position for AI
        self.target_rotation = 0  # Target rotation for AI
        self.moving = False  # Moving flag
        self.screen_handler = ScreenHandler(width, height)  # Screen handler for drawing
        self.move_planner = MovePlanner(self.ai)  # Move planner for AI
        self.move_performer = MovePerformer(self)  # Move performer for AI
        self.block_locker = BlockLocker(self)  # Block locker for handling block locking
        self.failed_rotation_attempts = 0  # Counter for failed rotation attempts
        self.max_failed_attempts = 10  # Max allowed failed rotation attempts

    def get_new_block(self):
        """Get a new random block."""
        shape_key = random.choice(list(shapes.keys()))  # Randomly select a shape key
        return create_block(shape_key)  # Create a block with the selected shape

    def move_block(self, dx, dy):
        """Move the current block by (dx, dy)."""
        new_position = [self.current_position[0] + dx, self.current_position[1] + dy]  # Calculate new position
        if not check_collision(self.grid.grid, self.current_block, new_position):  # Check for collision
            self.current_position = new_position  # Update position if no collision
            print(f"Moved block to {self.current_position}")  # Log the move
            return True
        print(f"Cannot move block to {new_position}, collision detected.")  # Log collision
        return False

    def rotate_block(self, direction):
        """Rotate the current block in the given direction."""
        original_position = self.current_position[:]  # Save original position
        original_block = copy.deepcopy(self.current_block)  # Save original block state
        
        if direction == 'counterclockwise':  # Check direction
            self.current_block.rotate_counterclockwise()  # Rotate block counterclockwise
            print(f"Trying counterclockwise rotation at position: {self.current_position}")  # Log rotation attempt
        else:
            self.current_block.rotate()  # Rotate block clockwise
            print(f"Trying clockwise rotation at position: {self.current_position}")  # Log rotation attempt

        if check_collision(self.grid.grid, self.current_block, self.current_position):  # Check for collision
            print(f"Collision detected after {direction} rotation at {self.current_position} with shape: {self.current_block.shape}")  # Log collision
            wall_kick_offsets = [  # Define wall kick offsets
                (0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (-1, 1), (1, -1), (-1, -1),
                (2, 0), (-2, 0), (0, 2), (0, -2),
                (2, 1), (2, -1), (-2, 1), (-2, -1)
            ]
            for offset in wall_kick_offsets:  # Try each wall kick offset
                new_position = [original_position[0] + offset[0], original_position[1] + offset[1]]  # Calculate new position
                print(f"Trying wall kick offset: {offset} -> New position: {new_position}")  # Log wall kick attempt
                if (0 <= new_position[0] < self.width - len(self.current_block.shape[0]) and
                    0 <= new_position[1] < self.height - len(self.current_block.shape)):
                    self.current_position = new_position  # Update position
                    if not check_collision(self.grid.grid, self.current_block, self.current_position):  # Check for collision
                        print("Successful wall kick")  # Log successful wall kick
                        return True
            print("All wall kicks failed, resetting to original position and block")  # Log failed wall kicks
            self.current_position = original_position  # Reset to original position
            self.current_block = original_block  # Reset to original block
            return False
        else:
            print(f"Rotated block to position: {self.current_position}")  # Log successful rotation
            return True

    def update(self, delta_time):
        """Update the game state."""
        if self.game_over:
            return  # Do nothing if game is over

        self.gravity_timer += delta_time  # Increment gravity timer

        while self.gravity_timer > self.level.gravity_speed:  # Check if gravity effect should be applied
            self.gravity_timer -= self.level.gravity_speed  # Reduce gravity timer
            if self.moving:  # Check if block is moving
                self.move_performer.perform_ai_move_step_new()  # Perform AI move step
            else:
                if not self.move_block(0, 1):  # Move block down
                    self.block_locker.lock_block_and_update_state()  # Lock block if it cannot move further

        if self.new_block_placed:  # Check if a new block was placed
            self.move_planner.plan_ai_move(self)  # Plan AI move for the new block
            self.new_block_placed = False  # Reset new block placed flag

    def handle_failed_move(self):
        """Handle a failed move attempt."""
        print("Handling failed move...")  # Log failed move handling
        self.block_locker.lock_block_and_update_state()  # Lock block and update state

    def draw(self, screen):
        """Draw the game state to the screen."""
        self.screen_handler.draw(screen, self.grid.grid, self.current_block, self.current_position, self.next_block, self.score, self.level.level, self.game_over)  # Draw the game

    def set_game_over(self):
        """Set the game status to over."""
        self.game_over = True  # Set game over flag
        print("Game Over")  # Log game over
