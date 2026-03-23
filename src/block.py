class Block:
    def __init__(self, shape, colour):
        self.shape = shape  # 2D array of block shape
        self.colour = colour  # Colour of block
        self.rotation = 0  # Rotation state (0-3)

    def rotate_clockwise(self):
        # Rotate shape 90 degrees clockwise
        new_shape = [list(row) for row in zip(*self.shape[::-1])]
        self.shape = new_shape
        self.rotation = (self.rotation + 1) % 4

    def rotate_counterclockwise(self):
        # Rotate shape 90 degrees counterclockwise
        new_shape = [list(row) for row in zip(*self.shape)][::-1]
        self.shape = new_shape
        self.rotation = (self.rotation - 1) % 4

    def rotate(self, direction='counterclockwise'):
        if direction == 'clockwise':
            self.rotate_clockwise()
        elif direction == 'counterclockwise':
            self.rotate_counterclockwise()
        else:
            raise ValueError("Invalid direction. Use 'clockwise' or 'counterclockwise'.")