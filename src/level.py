# level.py

# Define a list of gravity speeds for different levels
# Gravity speed decreases as the level increases, making the game harder
gravity_speeds = [
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,  # Levels 1-10
    0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,  # Levels 11-20
    0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,  # Levels 21-30
    0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,  # Levels 31-40
    0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1   # Levels 41-50
]

# Define a Level class to manage the game level, lines cleared, and gravity speed
class Level:
    def __init__(self):
        self.level = 1  # Initialize the starting level
        self.lines_cleared = 0  # Initialize the lines cleared counter
        self.gravity_speed = gravity_speeds[self.level - 1]  # Set the initial gravity speed based on the level

    # Method to update the level and gravity speed based on the lines removed
    def update_level(self, lines_removed):
        self.lines_cleared += lines_removed  # Update the total lines cleared
        if self.lines_cleared >= 10:  # Check if the lines cleared reaches 10
            self.level += 1  # Increase the level
            self.lines_cleared = 0  # Reset the lines cleared counter
            # Determine the new gravity speed based on the current level
            speed_index = (self.level - 1) // 10  # Calculate the index for gravity speeds
            self.gravity_speed = gravity_speeds[min(speed_index, len(gravity_speeds) - 1)]  # Update the gravity speed

    # Method to calculate the score based on the number of lines removed
    def get_score(self, lines_removed):
        # Scoring system for different number of lines removed at once
        scoring = {1: 40, 2: 100, 3: 300, 4: 1200}
        # Calculate the score based on the lines removed and the current level
        return scoring.get(lines_removed, 0) * self.level
