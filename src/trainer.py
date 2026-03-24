import torch
import torch.nn as nn
import torch.optim as optim
import random
import copy
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
            nn.Linear(64, 1) # Single Q-value for the state
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
        
        # Huber Loss is less sensitive to outliers than MSE
        self.criterion = nn.SmoothL1Loss() 
        
        self.epsilon = 1.0
        self.gamma = 0.99 
        self.tau = 0.005 # Slower sync for more stability

    def remember(self, state, reward, next_state, done):
        self.memory.append((state, reward, next_state, done))

    def train_from_past(self, batch_size=128):
        if len(self.memory) < batch_size: 
            return
        
        batch = random.sample(self.memory, batch_size)
        states, rewards, next_states, dones = zip(*batch)

        # Convert to tensors
        state_t = torch.FloatTensor(states).to(self.device)
        reward_t = torch.FloatTensor(rewards).to(self.device) # CLAMP REMOVED
        next_state_t = torch.FloatTensor(next_states).to(self.device)
        done_t = torch.FloatTensor(dones).to(self.device)

        # 1. Get current predicted values (Q-values)
        current_q = self.model(state_t).squeeze()
        
        # 2. Predict future values with the Target Network
        with torch.no_grad():
            next_q = self.target_model(next_state_t).squeeze()
            # Standard Bellman Equation
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
        if self.epsilon > 0.02: # Slightly lower floor for better exploitation
            self.epsilon *= 0.9995