from .block import Block
from .colours import TETROMINO_COLOURS

# Tetromino shapes
# Key is type; value is 2D array of shape
shapes = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

# Create Block object based on shape key
def create_block(shape_key):
    shape = shapes[shape_key]               # Get shape from key
    colour = TETROMINO_COLOURS[shape_key]   # Get color from key
    return Block(shape, colour)             # Return new Block object