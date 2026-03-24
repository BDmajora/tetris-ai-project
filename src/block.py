class Block:
    def __init__(self, shape, colour):
        self.shape = shape
        self.colour = colour
        self.rotation = 0

    def rotate_clockwise(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.rotation = (self.rotation + 1) % 4

    def rotate_counterclockwise(self):
        self.shape = [list(row) for row in zip(*self.shape)][::-1]
        self.rotation = (self.rotation - 1) % 4

    def rotate(self, direction='clockwise'):
        if direction == 'clockwise':
            self.rotate_clockwise()
        elif direction == 'counterclockwise':
            self.rotate_counterclockwise()