class RewardSystem:
    def __init__(self):
        self.prev_score = 0

    def get_heuristic_score(self, metrics, lines_cleared):
        # Weighted evaluation of board state and line clearing efficiency
        score = (lines_cleared ** 2) * 50.0 
        score -= (metrics['holes'] * 4.0)
        score -= (metrics['blockades'] * 2.0)
        score -= (metrics['bumpiness'] * 0.3)
        score -= (metrics['max_height'] * 1.0)
        score -= (metrics['total_height'] * 0.2)
        return score

    def calculate_reward(self, lines_cleared, metrics, game_over):
        # Terminal state penalty
        if game_over:
            return -100.0

        # Calculate comparative state value based on heuristic metrics
        current_score = self.get_heuristic_score(metrics, lines_cleared)
        reward = current_score 
        
        # Incremental bonus to incentivize line-clearing behavior
        if lines_cleared > 0:
            reward += (lines_cleared * 10)
            
        return reward