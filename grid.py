import pygame
from colours import BLACK, GRAY

class Grid:
    def __init__(self, width, height):
        """
        Initialize the game grid with specified width and height.
        
        Args:
            width (int): The width of the grid in cells.
            height (int): The height of the grid in cells.
        """
        self.width = width  # Width of the grid
        self.height = height  # Height of the grid
        self.grid = [[BLACK for _ in range(width)] for _ in range(height)]  # Initialize grid with BLACK cells

    def draw(self, screen):
        """
        Draw the grid on the screen.
        
        Args:
            screen (pygame.Surface): The surface to draw the grid on.
        """
        for y in range(self.height):  # Iterate over each row
            for x in range(self.width):  # Iterate over each column
                pygame.draw.rect(screen, self.grid[y][x], (x * 30, y * 30, 30, 30), 0)  # Draw the cell
                pygame.draw.rect(screen, GRAY, (x * 30, y * 30, 30, 30), 1)  # Draw the cell border

def remove_complete_lines(grid):
    """
    Remove complete lines from the grid and return the new grid and the number of lines removed.
    
    Args:
        grid (list of list of tuple): The current game grid.
        
    Returns:
        new_grid (list of list of tuple): The grid after removing complete lines.
        lines_removed (int): The number of lines removed.
    """
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]  # Filter out complete lines
    lines_removed = len(grid) - len(new_grid)  # Calculate number of lines removed
    for _ in range(lines_removed):  # Add new empty lines at the top
        new_grid.insert(0, [BLACK for _ in range(len(grid[0]))])
    return new_grid, lines_removed  # Return the new grid and number of lines removed
