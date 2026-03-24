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
        self.width = width  
        self.height = height  
        self.grid = Grid(width, height)  
        self.score = 0  
        self.level = Level()  
        self.game_over = False  
        self.gravity_timer = 0  
        
        self.agent = agent if agent else DQNAgent()
        self.reward_system = RewardSystem() 

        self.current_block = self.get_new_block()  
        start_x = self.width // 2 - len(self.current_block.shape[0]) // 2
        self.current_position = [start_x, 0] 
        self.next_block = self.get_new_block()  

        self.ai = AI(self, self.agent)  
        self.screen_handler = ScreenHandler(width, height)  
        self.move_planner = MovePlanner(self.ai)  
        self.move_performer = MovePerformer(self)  
        self.block_locker = BlockLocker(self)  
        
        self.target_position = None  
        self.target_rotation = 0  
        self.moving = False  

        self.move_planner.plan_ai_move(self)

    def get_new_block(self):
        shape_key = random.choice(list(shapes.keys()))  
        return create_block(shape_key)  

    def update(self, delta_time):
        if self.game_over:
            return  

        if self.moving:
            # Execute the planned move
            while self.moving:
                self.move_performer.perform_ai_move_step_new()
            
            # Hard drop after positioning
            while self.move_block(0, 1):
                pass
            
            old_score = self.score
            self.block_locker.lock_block_and_update_state()
            
            # Calculate lines cleared for the reward system
            score_diff = self.score - old_score
            lines_cleared = 0
            if score_diff >= 800: lines_cleared = 4
            elif score_diff >= 500: lines_cleared = 3
            elif score_diff >= 300: lines_cleared = 2
            elif score_diff >= 100: lines_cleared = 1

            # Get metrics and calculate the refined reward
            current_metrics = self.ai.h.get_all_metrics(self.grid.grid)
            reward = self.reward_system.calculate_reward(lines_cleared, current_metrics, self.game_over)
            
            # Learn from this move
            self.ai.collect_experience(self.grid.grid, reward, self.game_over)
            
            if not self.game_over:
                self.move_planner.plan_ai_move(self)
            return 

        self.gravity_timer += delta_time  
        if self.gravity_timer > self.level.gravity_speed:  
            self.gravity_timer = 0 
            if not self.move_block(0, 1):  
                self.block_locker.lock_block_and_update_state()
                self.move_planner.plan_ai_move(self)

    def move_block(self, dx, dy):
        new_pos = [self.current_position[0] + dx, self.current_position[1] + dy]  
        if not check_collision(self.grid.grid, self.current_block, new_pos):  
            self.current_position = new_pos  
            return True
        return False

    def rotate_block(self, direction):
        """Crucial for MovePerformer: Handles rotation and simple wall-kicks."""
        orig_pos = self.current_position[:]  
        orig_block = copy.deepcopy(self.current_block)  
        
        if direction == 'counterclockwise':  
            self.current_block.rotate_counterclockwise()  
        else:
            self.current_block.rotate_clockwise() 

        # If rotating causes a collision, try to 'kick' it into a valid spot
        if check_collision(self.grid.grid, self.current_block, self.current_position):  
            wall_kick_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in wall_kick_offsets:  
                new_pos = [orig_pos[0] + dx, orig_pos[1] + dy]  
                if not check_collision(self.grid.grid, self.current_block, new_pos):  
                    self.current_position = new_pos  
                    return True
            # If all kicks fail, revert
            self.current_position = orig_pos  
            self.current_block = orig_block  
            return False
        return True

    def draw(self, screen):
        self.screen_handler.draw(
            screen, self.grid.grid, self.current_block, 
            self.current_position, self.next_block, 
            self.score, self.level.level, self.game_over
        )  

    def set_game_over(self):
        self.game_over = True
        # Provide the final death metrics for the last training step
        dead_metrics = self.ai.h.get_all_metrics(self.grid.grid)
        final_reward = self.reward_system.calculate_reward(0, dead_metrics, True)
        self.ai.collect_experience(self.grid.grid, final_reward, True)
        print(f"Game Over! Score: {self.score} | Epsilon: {self.agent.epsilon:.3f}")