class RewardSystem:
    def __init__(self):
        self.prev_score = 0

    def get_heuristic_score(self, metrics, lines_cleared):
        # We mirror your old successful weights here
        # But we keep them in a smaller range (divided by 10) for the Neural Network
        score = (lines_cleared ** 2) * 50.0 
        score -= (metrics['holes'] * 4.0)
        score -= (metrics['blockades'] * 2.0)
        score -= (metrics['bumpiness'] * 0.3)
        score -= (metrics['max_height'] * 1.0)
        score -= (metrics['total_height'] * 0.2)
        return score

    def calculate_reward(self, lines_cleared, metrics, game_over):
        if game_over:
            return -100.0 # Massive slap for dying

        current_score = self.get_heuristic_score(metrics, lines_cleared)
        
        # The reward is how much BETTER the board got after this move
        # This prevents "farming" because it can't gain points without improving
        reward = current_score 
        
        # Additional bonus for clearing lines to encourage aggressive play
        if lines_cleared > 0:
            reward += (lines_cleared * 10)
            
        return reward