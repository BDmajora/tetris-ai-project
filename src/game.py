import pygame
import random
import copy
from .grid import Grid
from .blocks import create_block, shapes
from .position import check_collision, merge_grid_and_block
from .level import Level
from .ai import AI
from .screen import ScreenHandler
from .plan import MovePlanner
from .perform import MovePerformer
from .lock import BlockLocker

class Game:
    def __init__(self, width, height):
        self.width = width  # Grid width
        self.height = height  # Grid height
        self.grid = Grid(width, height)  # Initialize grid
        self.current_block = self.get_new_block()  # First block
        self.current_position = [self.width // 2 - len(self.current_block.shape[0]) // 2, 0]  # Start position
        self.next_block = self.get_new_block()  # Next block
        self.score = 0  # Score tracker
        self.level = Level()  # Level tracker
        self.game_over = False  # Game state flag
        self.gravity_timer = 0  # Gravity timing
        self.ai = AI(self)  # AI instance
        self.new_block_placed = False  # Placement flag
        self.target_position = None  # AI target position
        self.target_rotation = 0  # AI target rotation
        self.moving = False  # Movement state
        self.screen_handler = ScreenHandler(width, height)  # Drawing handler
        self.move_planner = MovePlanner(self.ai)  # Path planner
        self.move_performer = MovePerformer(self)  # Movement executor
        self.block_locker = BlockLocker(self)  # Locking handler
        self.failed_rotation_attempts = 0  # Rotation failure count
        self.max_failed_attempts = 10  # Rotation failure limit

    def get_new_block(self):
        # Select random shape and create block
        shape_key = random.choice(list(shapes.keys()))  
        return create_block(shape_key)  

    def move_block(self, dx, dy):
        # Calculate new coordinates and check collision
        new_position = [self.current_position[0] + dx, self.current_position[1] + dy]  
        if not check_collision(self.grid.grid, self.current_block, new_position):  
            self.current_position = new_position  # Update if clear
            print(f"Moved block to {self.current_position}")  
            return True
        print(f"Cannot move block to {new_position}, collision detected.")  
        return False

    def rotate_block(self, direction):
        # Save state for potential reset
        original_position = self.current_position[:]  
        original_block = copy.deepcopy(self.current_block)  
        
        # Apply rotation based on direction
        if direction == 'counterclockwise':  
            self.current_block.rotate_counterclockwise()  
            print(f"Trying counterclockwise rotation at position: {self.current_position}")  
        else:
            self.current_block.rotate()  
            print(f"Trying clockwise rotation at position: {self.current_position}")  

        # Handle collisions with wall kick logic
        if check_collision(self.grid.grid, self.current_block, self.current_position):  
            print(f"Collision detected after {direction} rotation at {self.current_position}")  
            wall_kick_offsets = [  
                (0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (-1, 1), (1, -1), (-1, -1),
                (2, 0), (-2, 0), (0, 2), (0, -2),
                (2, 1), (2, -1), (-2, 1), (-2, -1)
            ]
            for offset in wall_kick_offsets:  
                new_position = [original_position[0] + offset[0], original_position[1] + offset[1]]  
                print(f"Trying wall kick offset: {offset} -> New position: {new_position}")  
                
                # Check grid boundaries
                if (0 <= new_position[0] < self.width - len(self.current_block.shape[0]) and
                    0 <= new_position[1] < self.height - len(self.current_block.shape)):
                    self.current_position = new_position  
                    if not check_collision(self.grid.grid, self.current_block, self.current_position):  
                        print("Successful wall kick")  
                        return True
            
            # Reset if all kicks fail
            print("All wall kicks failed, resetting position and block")  
            self.current_position = original_position  
            self.current_block = original_block  
            return False
        else:
            print(f"Rotated block to position: {self.current_position}")  
            return True

    def update(self, delta_time):
        # Exit if game over
        if self.game_over:
            return  

        self.gravity_timer += delta_time  # Update timer

        # Apply gravity based on level speed
        while self.gravity_timer > self.level.gravity_speed:  
            self.gravity_timer -= self.level.gravity_speed  
            if self.moving:  
                self.move_performer.perform_ai_move_step_new()  # AI controlled step
            else:
                if not self.move_block(0, 1):  # Natural fall
                    self.block_locker.lock_block_and_update_state()  # Lock on impact

        # Plan move for new blocks
        if self.new_block_placed:  
            self.move_planner.plan_ai_move(self)  
            self.new_block_placed = False  

    def handle_failed_move(self):
        # Process move failure and lock block
        print("Handling failed move...")  
        self.block_locker.lock_block_and_update_state()  

    def draw(self, screen):
        # Render game state via screen handler
        self.screen_handler.draw(screen, self.grid.grid, self.current_block, self.current_position, self.next_block, self.score, self.level.level, self.game_over)  

    def set_game_over(self):
        # Terminate game and log event
        self.game_over = True  
        print("Game Over")