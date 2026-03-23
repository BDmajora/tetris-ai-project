from block import Block

# Define the shapes of the tetrominoes
# Each key represents a tetromino type, and its value is a 2D array representing the shape
shapes = {
    'I': [[1, 1, 1, 1]],          # I shape: a straight line
    'O': [[1, 1], [1, 1]],        # O shape: a square block
    'T': [[0, 1, 0], [1, 1, 1]],  # T shape: a T-like structure
    'S': [[0, 1, 1], [1, 1, 0]],  # S shape: a zigzag structure
    'Z': [[1, 1, 0], [0, 1, 1]],  # Z shape: a reverse zigzag
    'J': [[1, 0, 0], [1, 1, 1]],  # J shape: a J-like structure
    'L': [[0, 0, 1], [1, 1, 1]]   # L shape: an L-like structure
}

# Define the colours for the blocks
# Each key represents a tetromino type, and its value is an RGB color tuple
colours = {
    'I': (0, 255, 255),   # Cyan color for I shape
    'O': (255, 255, 0),   # Yellow color for O shape
    'T': (128, 0, 128),   # Purple color for T shape
    'S': (0, 255, 0),     # Green color for S shape
    'Z': (255, 0, 0),     # Red color for Z shape
    'J': (0, 0, 255),     # Blue color for J shape
    'L': (255, 165, 0)    # Orange color for L shape
}

def create_block(shape_key):
    """Create a Block object based on the shape key.
    
    Args:
        shape_key (str): The key representing the tetromino type.
        
    Returns:
        Block: A Block object with the corresponding shape and color.
    """
    shape = shapes[shape_key]  # Get the shape based on the shape key
    colour = colours[shape_key]  # Get the color based on the shape key
    return Block(shape, colour)  # Return a new Block object with the shape and color
