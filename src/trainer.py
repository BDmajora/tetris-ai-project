import torch
import torch.nn as nn
import torch.optim as optim
import random
import copy
import os
import json
from collections import deque

class TetrisBrain(nn.Module):
    def __init__(self):
        super(TetrisBrain, self).__init__()
        # 8 Inputs: Holes, Blockades, Bumpiness, Max Height, Total Height, 
        # Row Trans, Col Trans, Wells
        self.network = nn.Sequential(
            nn.Linear(8, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1) 
        )

    def forward(self, x):
        return self.network(x)

class DQNAgent:
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = TetrisBrain().to(self.device)
        self.target_model = copy.deepcopy(self.model).to(self.device)
        self.target_model.eval()
        
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.0001) 
        self.memory = deque(maxlen=50000) 
        
        # Huber Loss (SmoothL1) is much more stable for Tetris than MSE
        self.criterion = nn.SmoothL1Loss() 
        
        self.epsilon = 1.0
        self.gamma = 0.99 
        self.tau = 0.005 # Slower sync for more stability

    # --- SAVE/LOAD METHODS ---
    def save_brain(self, filename="tetris_brain.pth"):
        """Saves the neural network weights to a file."""
        torch.save(self.model.state_dict(), filename)
        print(f"--- Brain saved to {filename} ---")

    def load_brain(self, filename="tetris_brain.pth"):
        """Loads weights and ensures the target model matches."""
        if os.path.exists(filename):
            self.model.load_state_dict(torch.load(filename))
            # Sync the target model immediately so they start on the same page
            self.target_model = copy.deepcopy(self.model).to(self.device)
            self.target_model.eval()
            
            # Lower epsilon because we are resuming with a pre-trained model
            self.epsilon = 0.2 
            print(f"--- Brain loaded from {filename}. Resuming with reduced exploration. ---")
            return True
        print("--- No saved brain found. Starting with fresh weights. ---")
        return False

    def save_stats(self, stats, filename="stats.json"):
        """Saves session metadata like high score and game count."""
        with open(filename, 'w') as f:
            json.dump(stats, f)
        print(f"--- Stats saved to {filename} ---")

    def load_stats(self, filename="stats.json"):
        """Loads session metadata if it exists."""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                print(f"--- Stats loaded from {filename} ---")
                return json.load(f)
        return None

    # --- TRAINING LOGIC ---
    def remember(self, state, reward, next_state, done):
        self.memory.append((state, reward, next_state, done))

    def train_from_past(self, batch_size=128):
        if len(self.memory) < batch_size: 
            return
        
        batch = random.sample(self.memory, batch_size)
        states, rewards, next_states, dones = zip(*batch)

        state_t = torch.FloatTensor(states).to(self.device)
        reward_t = torch.FloatTensor(rewards).to(self.device)
        next_state_t = torch.FloatTensor(next_states).to(self.device)
        done_t = torch.FloatTensor(dones).to(self.device)

        # 1. Get current predicted values (Q-values)
        current_q = self.model(state_t).squeeze()
        
        # 2. Predict future values with the Target Network
        with torch.no_grad():
            next_q = self.target_model(next_state_t).squeeze()
            target_q = reward_t + (1 - done_t) * self.gamma * next_q

        # 3. Optimize the main model
        loss = self.criterion(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        
        # Keep gradients from exploding
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        self.optimizer.step()

        # 4. SOFT UPDATE: Gradually update the target network
        for target_param, local_param in zip(self.target_model.parameters(), self.model.parameters()):
            target_param.data.copy_(self.tau * local_param.data + (1.0 - self.tau) * target_param.data)

        # 5. Decay Epsilon
        if self.epsilon > 0.02:
            self.epsilon *= 0.9995