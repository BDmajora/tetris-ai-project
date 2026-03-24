import pygame
import random
import copy
from .grid import Grid
from .blocks import create_block, shapes
from .position import check_collision, merge_grid_and_block
from .level import Level
from .ai import AI
from .weights import WeightManager  
from .screen import ScreenHandler
from .plan import MovePlanner
from .perform import MovePerformer
from .lock import BlockLocker

class Game:
    def __init__(self, width, height):
        self.width = width  
        self.height = height  
        self.grid = Grid(width, height)  
        self.score = 0  
        self.level = Level()  
        self.game_over = False  
        self.gravity_timer = 0  
        
        # 1. Initialize the Judge (WeightManager)
        # Reduced hole_w from 200 to 45 to prevent the AI from "towering"
        # because it's too scared of creating a single hole.
        self.weight_manager = WeightManager(
            hole_w=45,    
            height_w=12,   
            bump_w=5,      
            trans_w=10     
        )

        # 2. Initialize blocks
        self.current_block = self.get_new_block()  
        
        # Proper centering logic for spawn
        start_x = self.width // 2 - len(self.current_block.shape[0]) // 2
        self.current_position = [start_x, 0] # Spawn at the top buffer
        self.next_block = self.get_new_block()  

        # 3. AI and movement handlers
        self.ai = AI(self, self.weight_manager)  
        self.screen_handler = ScreenHandler(width, height)  
        self.move_planner = MovePlanner(self.ai)  
        self.move_performer = MovePerformer(self)  
        self.block_locker = BlockLocker(self)  
        
        # AI state flags
        self.target_position = None  
        self.target_rotation = 0  
        self.moving = False  

        # Initial AI plan
        self.move_planner.plan_ai_move(self)

    def get_new_block(self):
        shape_key = random.choice(list(shapes.keys()))  
        return create_block(shape_key)  

    def move_block(self, dx, dy):
        new_pos = [self.current_position[0] + dx, self.current_position[1] + dy]  
        if not check_collision(self.grid.grid, self.current_block, new_pos):  
            self.current_position = new_pos  
            return True
        return False

    def rotate_block(self, direction):
        """Standard rotation with wall-kick safety."""
        orig_pos = self.current_position[:]  
        orig_block = copy.deepcopy(self.current_block)  
        
        if direction == 'counterclockwise':  
            self.current_block.rotate_counterclockwise()  
        else:
            self.current_block.rotate_clockwise() # Updated to match stable Block class

        if check_collision(self.grid.grid, self.current_block, self.current_position):  
            wall_kick_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0), (2, 0), (-2, 0)]
            
            for dx, dy in wall_kick_offsets:  
                new_pos = [orig_pos[0] + dx, orig_pos[1] + dy]  
                if not check_collision(self.grid.grid, self.current_block, new_pos):  
                    self.current_position = new_pos  
                    return True
            
            # Revert if stuck
            self.current_position = orig_pos  
            self.current_block = orig_block  
            return False
        return True

    def update(self, delta_time):
        if self.game_over:
            return  

        # 1. AI EXECUTION
        # Instead of moving one step at a time, we allow the AI to finish its move
        # in a single update frame. This kills the "Snail Pace" bug.
        if self.moving:
            # We use a loop to ensure the block is in position before gravity hits
            while self.moving:
                self.move_performer.perform_ai_move_step_new()
            
            # Once target X and Rotation are reached, we Hard Drop
            while self.move_block(0, 1):
                pass
            
            self.block_locker.lock_block_and_update_state()
            self.move_planner.plan_ai_move(self)
            return # Skip standard gravity for this frame to avoid double-stepping

        # 2. GRAVITY (Fallback/Safety)
        self.gravity_timer += delta_time  
        if self.gravity_timer > self.level.gravity_speed:  
            self.gravity_timer = 0 
            
            if not self.move_block(0, 1):  
                self.block_locker.lock_block_and_update_state()
                self.move_planner.plan_ai_move(self)

    def draw(self, screen):
        self.screen_handler.draw(
            screen, self.grid.grid, self.current_block, 
            self.current_position, self.next_block, 
            self.score, self.level.level, self.game_over
        )  

    def set_game_over(self):
        self.game_over = True  
        print(f"Final Score: {self.score} - Game Over")