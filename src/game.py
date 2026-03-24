import pygame
import random
import copy
from .grid import Grid
from .blocks import create_block, shapes
from .position import check_collision
from .level import Level
from .ai import AI
from .trainer import DQNAgent 
from .screen import ScreenHandler
from .plan import MovePlanner
from .perform import MovePerformer
from .lock import BlockLocker
from .reward import RewardSystem 

class Game:
    def __init__(self, width, height, agent=None):
        # Initialize core game state and dimensions
        self.width = width  
        self.height = height  
        self.grid = Grid(width, height)  
        self.score = 0  
        self.level = Level()  
        self.game_over = False  
        self.gravity_timer = 0  
        
        # Neural network agent and reward evaluation system
        self.agent = agent if agent else DQNAgent()
        self.reward_system = RewardSystem() 

        # Block state management
        self.current_block = self.get_new_block()  
        start_x = self.width // 2 - len(self.current_block.shape[0]) // 2
        self.current_position = [start_x, 0] 
        self.next_block = self.get_new_block()  

        # Systems architecture initialization
        self.ai = AI(self, self.agent)  
        self.screen_handler = ScreenHandler(width, height)  
        self.move_planner = MovePlanner(self.ai)  
        self.move_performer = MovePerformer(self)  
        self.block_locker = BlockLocker(self)  
        
        # Move execution and AI trajectory state
        self.target_position = None  
        self.target_rotation = 0  
        self.moving = False  

        # Initial trajectory planning
        self.move_planner.plan_ai_move(self)

    def get_new_block(self):
        # Select random shape and instantiate block object
        shape_key = random.choice(list(shapes.keys()))  
        return create_block(shape_key)  

    def update(self, delta_time):
        if self.game_over:
            return  

        if self.moving:
            # Execute automated move steps
            while self.moving:
                self.move_performer.perform_ai_move_step_new()
            
            # Finalize vertical placement via hard drop
            while self.move_block(0, 1):
                pass
            
            old_score = self.score
            self.block_locker.lock_block_and_update_state()
            
            # Map score delta to line clearing metrics
            score_diff = self.score - old_score
            lines_cleared = 0
            if score_diff >= 800: lines_cleared = 4
            elif score_diff >= 500: lines_cleared = 3
            elif score_diff >= 300: lines_cleared = 2
            elif score_diff >= 100: lines_cleared = 1

            # Calculate reward and store transition experience
            current_metrics = self.ai.h.get_all_metrics(self.grid.grid)
            reward = self.reward_system.calculate_reward(lines_cleared, current_metrics, self.game_over)
            self.ai.collect_experience(self.grid.grid, reward, self.game_over)
            
            if not self.game_over:
                self.move_planner.plan_ai_move(self)
            return 

        # Standard gravity-based movement logic
        self.gravity_timer += delta_time  
        if self.gravity_timer > self.level.gravity_speed:  
            self.gravity_timer = 0 
            if not self.move_block(0, 1):  
                self.block_locker.lock_block_and_update_state()
                self.move_planner.plan_ai_move(self)

    def move_block(self, dx, dy):
        # Update block position if collision check passes
        new_pos = [self.current_position[0] + dx, self.current_position[1] + dy]  
        if not check_collision(self.grid.grid, self.current_block, new_pos):  
            self.current_position = new_pos  
            return True
        return False

    def rotate_block(self, direction):
        # Handle rotation and basic wall-kick recovery logic
        orig_pos = self.current_position[:]  
        orig_block = copy.deepcopy(self.current_block)  
        
        if direction == 'counterclockwise':  
            self.current_block.rotate_counterclockwise()  
        else:
            self.current_block.rotate_clockwise() 

        # Apply offset offsets if initial rotation results in collision
        if check_collision(self.grid.grid, self.current_block, self.current_position):  
            wall_kick_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in wall_kick_offsets:  
                new_pos = [orig_pos[0] + dx, orig_pos[1] + dy]  
                if not check_collision(self.grid.grid, self.current_block, new_pos):  
                    self.current_position = new_pos  
                    return True
            # Revert state if all offsets fail
            self.current_position = orig_pos  
            self.current_block = orig_block  
            return False
        return True

    def draw(self, screen):
        # Delegate rendering to screen handler
        self.screen_handler.draw(
            screen, self.grid.grid, self.current_block, 
            self.current_position, self.next_block, 
            self.score, self.level.level, self.game_over
        )  

    def set_game_over(self):
        # Terminate session and log final terminal state metrics
        self.game_over = True
        dead_metrics = self.ai.h.get_all_metrics(self.grid.grid)
        final_reward = self.reward_system.calculate_reward(0, dead_metrics, True)
        self.ai.collect_experience(self.grid.grid, final_reward, True)
        print(f"Game Over! Score: {self.score} | Epsilon: {self.agent.epsilon:.3f}")