class Block:
    def __init__(self, shape, colour):
        self.shape = shape  # 2D array representing the block shape
        self.colour = colour  # Colour of the block
        self.rotation = 0  # Rotation state of the block (0-3)

    def rotate_clockwise(self):
        """Rotate the block 90 degrees clockwise."""
        # Rotate the shape 90 degrees clockwise by transposing and reversing the rows
        new_shape = [list(row) for row in zip(*self.shape[::-1])]
        self.shape = new_shape
        # Update the rotation state
        self.rotation = (self.rotation + 1) % 4

    def rotate_counterclockwise(self):
        """Rotate the block 90 degrees counterclockwise."""
        # Rotate the shape 90 degrees counterclockwise by transposing and reversing the columns
        new_shape = [list(row) for row in zip(*self.shape)][::-1]
        self.shape = new_shape
        # Update the rotation state
        self.rotation = (self.rotation - 1) % 4

    def rotate(self, direction='counterclockwise'):
        """Rotate the block in the specified direction."""
        if direction == 'clockwise':
            # Rotate the block clockwise
            self.rotate_clockwise()
        elif direction == 'counterclockwise':
            # Rotate the block counterclockwise
            self.rotate_counterclockwise()
        else:
            # Raise an error if the direction is invalid
            raise ValueError("Invalid direction for rotation. Use 'clockwise' or 'counterclockwise'.")
