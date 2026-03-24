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
        self.width = width  # Visible grid width
        self.height = height  # Visible grid height
        self.grid = Grid(width, height)  # Initialize grid with 2-row buffer
        self.score = 0  
        self.level = Level()  
        self.game_over = False  
        self.gravity_timer = 0  
        
        # Initialize blocks
        self.current_block = self.get_new_block()  
        # Spawn block at y=2 to start below hidden buffer (Rows 0 and 1)
        start_x = self.width // 2 - len(self.current_block.shape[0]) // 2
        self.current_position = [start_x, 2]  
        self.next_block = self.get_new_block()  

        # AI and movement handlers
        self.ai = AI(self)  
        self.screen_handler = ScreenHandler(width, height)  
        self.move_planner = MovePlanner(self.ai)  
        self.move_performer = MovePerformer(self)  
        self.block_locker = BlockLocker(self)  
        
        # AI state flags
        self.new_block_placed = False  
        self.target_position = None  
        self.target_rotation = 0  
        self.moving = False  
        self.failed_rotation_attempts = 0  
        self.max_failed_attempts = 10  

        # --- FIRST ROUND FIX ---
        # Force the AI to calculate the move for the first block immediately
        self.move_planner.plan_ai_move(self)

    def get_new_block(self):
        # Create block from random shape key
        shape_key = random.choice(list(shapes.keys()))  
        return create_block(shape_key)  

    def move_block(self, dx, dy):
        # Calculate new position and check for collisions against full grid
        new_pos = [self.current_position[0] + dx, self.current_position[1] + dy]  
        if not check_collision(self.grid.grid, self.current_block, new_pos):  
            self.current_position = new_pos  
            return True
        return False

    def rotate_block(self, direction):
        # Store state for potential collision recovery
        orig_pos = self.current_position[:]  
        orig_block = copy.deepcopy(self.current_block)  
        
        if direction == 'counterclockwise':  
            self.current_block.rotate_counterclockwise()  
        else:
            self.current_block.rotate()  

        # Wall kick logic if rotation causes collision
        if check_collision(self.grid.grid, self.current_block, self.current_position):  
            wall_kick_offsets = [  
                (0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (-1, 1), (1, -1), (-1, -1),
                (2, 0), (-2, 0), (0, 2), (0, -2)
            ]
            
            total_height = len(self.grid.grid)
            for dx, dy in wall_kick_offsets:  
                new_pos = [orig_pos[0] + dx, orig_pos[1] + dy]  
                
                # Check boundaries respecting the total height (buffer + visible)
                if (0 <= new_pos[0] <= self.width - len(self.current_block.shape[0]) and
                    0 <= new_pos[1] <= total_height - len(self.current_block.shape)):
                    
                    if not check_collision(self.grid.grid, self.current_block, new_pos):  
                        self.current_position = new_pos  
                        return True
            
            # Revert if all kicks fail
            self.current_position = orig_pos  
            self.current_block = orig_block  
            return False
        return True

    def update(self, delta_time):
        if self.game_over:
            return  

        self.gravity_timer += delta_time  

        # Process gravity and AI steps
        while self.gravity_timer > self.level.gravity_speed:  
            self.gravity_timer -= self.level.gravity_speed  
            if self.moving:  
                # AI move logic: Align then Drop
                self.move_performer.perform_ai_move_step_new()  
            else:
                # Standard downward movement (Gravity)
                if not self.move_block(0, 1):  
                    self.block_locker.lock_block_and_update_state()  

        # Plan move for newly spawned blocks after a lock
        if self.new_block_placed:  
            self.move_planner.plan_ai_move(self)  
            self.new_block_placed = False  

    def handle_failed_move(self):
        # Lock block immediately if AI move fails/stalls
        self.block_locker.lock_block_and_update_state()  

    def draw(self, screen):
        # Draw game state via screen handler (skips buffer rows 0-1)
        self.screen_handler.draw(
            screen, self.grid.grid, self.current_block, 
            self.current_position, self.next_block, 
            self.score, self.level.level, self.game_over
        )  

    def set_game_over(self):
        self.game_over = True  
        print("Game Over")