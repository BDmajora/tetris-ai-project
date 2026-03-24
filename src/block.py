class Block:
    def __init__(self, shape, colour):
        self.shape = shape
        self.colour = colour
        self.rotation = 0

    def rotate_clockwise(self):
        # Matrix transposition for 90-degree clockwise rotation
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.rotation = (self.rotation + 1) % 4

    def rotate_counterclockwise(self):
        # Matrix transposition for 90-degree counter-clockwise rotation
        self.shape = [list(row) for row in zip(*self.shape)][::-1]
        self.rotation = (self.rotation - 1) % 4

    def rotate(self, direction='clockwise'):
        # Directional wrapper for rotation methods
        if direction == 'clockwise':
            self.rotate_clockwise()
        elif direction == 'counterclockwise':
            self.rotate_counterclockwise()