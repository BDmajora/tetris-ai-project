import math

class Level:
    def __init__(self):
        self.level = 0  # NES starts at Level 0
        self.lines_cleared = 0
        
        # NES Frame Table (Frames per 1-cell drop at 60 FPS)
        self.nes_frames = [
            48, 43, 38, 33, 28, 23, 18, 13, 8, 6,  # Levels 0-9
            5, 5, 5, 4, 4, 4, 3, 3, 3,             # Levels 10-18
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2,          # Levels 19-28
            1                                      # Level 29+ (Kill Screen)
        ]
        self.gravity_speed = self._calculate_delay(self.level)

    def _calculate_delay(self, level):
        # Convert NES frames to seconds: seconds = frames / 60
        frame_count = self.nes_frames[min(level, len(self.nes_frames) - 1)]
        return frame_count / 60.0

    def update_level(self, lines_removed):
        self.lines_cleared += lines_removed
        
        # Level up every 10 lines
        if self.lines_cleared >= 10:
            self.level += 1
            self.lines_cleared -= 10 # Carry over extra lines if multiple cleared
            self.gravity_speed = self._calculate_delay(self.level)
            
            print(f"--- LEVEL UP: {self.level} ---")
            print(f"NES Speed: {self.gravity_speed:.4f}s per drop")

    def get_score(self, lines_removed):
        # NES Original Scoring
        scoring = {1: 40, 2: 100, 3: 300, 4: 1200}
        return scoring.get(lines_removed, 0) * (self.level + 1)