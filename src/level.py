import math

class Level:
    def __init__(self):
        self.level = 1
        self.lines_cleared = 0
        self.base_delay = 0.5  # Starting delay (0.5 seconds)
        self.min_delay = 0.01  # Hard cap to prevent infinite loops
        self.gravity_speed = self.base_delay

    def update_level(self, lines_removed):
        self.lines_cleared += lines_removed
        
        # Only change speed when a new level is reached (every 10 lines)
        if self.lines_cleared >= 10:
            self.level += 1
            self.lines_cleared = 0  # Reset for the next level
            
            # QUADRATIC SPEED INCREASE: $O(n^2)$
            # We calculate the speed based on Level squared.
            # As Level goes up, the delay drops exponentially fast.
            # Formula: Delay = Base / (1 + 0.1 * Level^2)
            coefficient = 0.1
            new_delay = self.base_delay / (1 + (coefficient * (self.level ** 2)))
            
            # Apply new speed with a safety floor
            self.gravity_speed = max(new_delay, self.min_delay)
            
            print(f"--- LEVEL UP: {self.level} ---")
            print(f"New Gravity Delay: {self.gravity_speed:.4f}s")

    def get_score(self, lines_removed):
        # Traditional scoring scaled by the current level
        scoring = {1: 40, 2: 100, 3: 300, 4: 1200}
        return scoring.get(lines_removed, 0) * self.level