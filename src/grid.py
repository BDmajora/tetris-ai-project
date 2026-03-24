import pygame
from .colours import BLACK, GRAY

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Initialize grid with two buffer rows for overflow management
        self.grid = [[BLACK for _ in range(width)] for _ in range(height + 2)]

    def draw(self, screen):
        # Render visible rows while skipping buffer overhead
        for y in range(2, self.height + 2):
            for x in range(self.width):
                # Calculate screen coordinates based on block size
                draw_y = (y - 2) * 30
                # Render cell fill and border
                pygame.draw.rect(screen, self.grid[y][x], (x * 30, draw_y, 30, 30), 0)
                pygame.draw.rect(screen, GRAY, (x * 30, draw_y, 30, 30), 1)

def remove_complete_lines(grid):
    # Filter rows to identify incomplete lines
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]
    # Calculate total rows cleared
    lines_removed = len(grid) - len(new_grid)
    # Maintain grid dimensions by inserting empty rows at the top
    for _ in range(lines_removed):
        new_grid.insert(0, [BLACK for _ in range(len(grid[0]))])
    return new_grid, lines_removed