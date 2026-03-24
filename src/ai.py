import copy
import torch
import random
from .grid import remove_complete_lines
from .position import check_collision, merge_grid_and_block
from .heuristics import TetrisHeuristics

class AI:
    def __init__(self, game, agent):
        self.game = game
        self.agent = agent  
        self.h = TetrisHeuristics()
        self.last_state_vector = None

    def get_metrics_vector(self, metrics):
        """
        SCALING: We divide by typical values to keep inputs near the 0-1 range,
        but we NO LONGER 'cap' them at 1.0. This allows the NN to recognize 
        extreme penalties (like a tower of 20 blocks high vs 10 blocks high).
        """
        return [
            float(metrics['holes']) / 10.0,
            float(metrics['blockades']) / 10.0,
            float(metrics['bumpiness']) / 10.0,
            float(metrics['max_height']) / 10.0,
            float(metrics['total_height']) / 50.0,
            float(metrics['row_transitions']) / 20.0,
            float(metrics['col_transitions']) / 20.0,
            float(metrics['wells']) / 10.0
        ]

    def get_best_move(self):
        # 1. EXPLORATION
        if random.random() < self.agent.epsilon:
            rotation = random.randint(0, 3)
            # Temporary block to calculate width for valid X range
            test_block = copy.copy(self.game.current_block)
            for _ in range(rotation): 
                test_block.rotate_clockwise()
            
            block_width = len(test_block.shape[0])
            x = random.randint(0, max(0, self.game.width - block_width))
            
            # Update last_state_vector so we can learn from this random move
            _, grid_after = self.simulate_move(self.game.grid.grid, test_block, x)
            if grid_after:
                self.last_state_vector = self.get_metrics_vector(self.h.get_all_metrics(grid_after))
            
            return (rotation, x)

        best_score = float('-inf')
        best_move = (0, self.game.width // 2 - 1)
        best_state_vector = None
        
        # 2. EVALUATION
        for rotation in range(4):
            test_block = copy.copy(self.game.current_block)
            for _ in range(rotation): 
                test_block.rotate_clockwise()

            block_width = len(test_block.shape[0])
            for x in range(0, self.game.width - block_width + 1):
                _, grid_after = self.simulate_move(self.game.grid.grid, test_block, x)
                if grid_after is None: 
                    continue

                metrics = self.h.get_all_metrics(grid_after)
                state_vector = self.get_metrics_vector(metrics)
                
                state_t = torch.FloatTensor(state_vector).to(self.agent.device)
                with torch.no_grad():
                    # The model now predicts the "Value" of the state based on the reward logic
                    score = self.agent.model(state_t).item()

                if score > best_score:
                    best_score = score
                    best_move = (rotation, x)
                    best_state_vector = state_vector
        
        self.last_state_vector = best_state_vector
        return best_move

    def simulate_move(self, start_grid, block, x):
        # Initial collision check at the top
        if check_collision(start_grid, block, (x, 0)): 
            return 0, None
            
        grid_copy = [row[:] for row in start_grid]
        y = 0
        while not check_collision(grid_copy, block, (x, y + 1)): 
            y += 1
            
        merge_grid_and_block(grid_copy, block, (x, y))
        final_grid, lines_removed = remove_complete_lines(grid_copy)
        return lines_removed, final_grid

    def collect_experience(self, next_grid, reward, done):
        if self.last_state_vector is None: 
            return
            
        next_metrics = self.h.get_all_metrics(next_grid)
        next_state_vector = self.get_metrics_vector(next_metrics)
        
        # Store experience and trigger training
        self.agent.remember(self.last_state_vector, reward, next_state_vector, done)
        self.agent.train_from_past(batch_size=128)