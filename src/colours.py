import random

# Black color
BLACK = (0, 0, 0)

# White color
WHITE = (255, 255, 255)

# Gray color
GRAY = (128, 128, 128)

# Tetromino colors
# Key is type; value is random RGB tuple
TETROMINO_COLOURS = {
    'I': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
    'O': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
    'T': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
    'S': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
    'Z': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
    'J': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
    'L': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
}