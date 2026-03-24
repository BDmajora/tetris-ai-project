import math

class Level:
    def __init__(self):
        # NES standard level and line progression metrics
        self.level = 0
        self.lines_cleared_total = 0
        self.lines_until_next_level = 10
        
        # NES Frame Table: Frames per 1-cell drop at 60 FPS
        self.nes_frames = [
            48, 43, 38, 33, 28, 23, 18, 13, 8, 6,  # Levels 0-9
            5, 5, 5, 4, 4, 4, 3, 3, 3,             # Levels 10-18
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2,          # Levels 19-28
            1                                      # Level 29+ (Kill Screen)
        ]
        self.gravity_speed = self._calculate_delay(self.level)

    def _calculate_delay(self, level):
        # Conversion of NES frames to temporal seconds (frames / 60)
        index = min(level, len(self.nes_frames) - 1)
        frame_count = self.nes_frames[index]
        return frame_count / 60.0

    def update_level(self, lines_removed):
        # Update line counts and handle iterative level-up logic
        self.lines_cleared_total += lines_removed
        self.lines_until_next_level -= lines_removed
        
        while self.lines_until_next_level <= 0:
            self.level += 1
            self.lines_until_next_level += 10
            self.gravity_speed = self._calculate_delay(self.level)
            
            print(f"Level progression: {self.level}")
            print(f"Gravity delay: {self.gravity_speed:.4f}s")

    def get_score(self, lines_removed):
        # NES Original Scoring Multiplier implementation
        scoring = {1: 40, 2: 100, 3: 300, 4: 1200}
        return scoring.get(lines_removed, 0) * (self.level + 1)