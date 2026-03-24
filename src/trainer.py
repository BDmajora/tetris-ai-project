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
        # Input layer: 8 heuristic features (Holes, Blockades, Bumpiness, Height metrics, Transitions, Wells)
        self.network = nn.Sequential(
            nn.Linear(8, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1) 
        )

    def forward(self, x):
        # Forward pass to predict state-value
        return self.network(x)

class DQNAgent:
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = TetrisBrain().to(self.device)
        self.target_model = copy.deepcopy(self.model).to(self.device)
        self.target_model.eval()
        
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.0001) 
        self.memory = deque(maxlen=50000) 
        
        # SmoothL1Loss (Huber Loss) utilized for gradient stability
        self.criterion = nn.SmoothL1Loss() 
        
        self.epsilon = 1.0
        self.gamma = 0.99 
        self.tau = 0.005 # Target network synchronization coefficient

    def save_brain(self, filename="tetris_brain.pth"):
        # Persist model state dictionary to disk
        torch.save(self.model.state_dict(), filename)
        print(f"Model parameters saved: {filename}")

    def load_brain(self, filename="tetris_brain.pth"):
        # Restore model state and synchronize target network
        if os.path.exists(filename):
            self.model.load_state_dict(torch.load(filename))
            self.target_model = copy.deepcopy(self.model).to(self.device)
            self.target_model.eval()
            
            # Reduce exploration rate for pre-trained weight resumption
            self.epsilon = 0.2 
            print(f"Model parameters loaded: {filename}")
            return True
        return False

    def save_stats(self, stats, filename="stats.json"):
        # Persist session metadata and high scores
        with open(filename, 'w') as f:
            json.dump(stats, f)
        print(f"Session metadata saved: {filename}")

    def load_stats(self, filename="stats.json"):
        # Retrieve session metadata if available
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return None

    def remember(self, state, reward, next_state, done):
        # Append transition experience to replay buffer
        self.memory.append((state, reward, next_state, done))

    def train_from_past(self, batch_size=128):
        # Batch training logic via experience replay
        if len(self.memory) < batch_size: 
            return
        
        batch = random.sample(self.memory, batch_size)
        states, rewards, next_states, dones = zip(*batch)

        state_t = torch.FloatTensor(states).to(self.device)
        reward_t = torch.FloatTensor(rewards).to(self.device)
        next_state_t = torch.FloatTensor(next_states).to(self.device)
        done_t = torch.FloatTensor(dones).to(self.device)

        # Predicted Q-values from local network
        current_q = self.model(state_t).squeeze()
        
        # Target Q-value calculation using Bellman equation and target network
        with torch.no_grad():
            next_q = self.target_model(next_state_t).squeeze()
            target_q = reward_t + (1 - done_t) * self.gamma * next_q

        # Backpropagation and gradient clipping
        loss = self.criterion(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        self.optimizer.step()

        # Polyak averaging (soft update) for target network stability
        for target_param, local_param in zip(self.target_model.parameters(), self.model.parameters()):
            target_param.data.copy_(self.tau * local_param.data + (1.0 - self.tau) * target_param.data)

        # Geometric exploration decay
        if self.epsilon > 0.02:
            self.epsilon *= 0.9995