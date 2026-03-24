import pygame
from .colours import BLACK, GRAY

class Grid:
    def __init__(self, width, height):
        self.width = width  # Grid width
        self.height = height  # Visible grid height
        # Initialize grid with 2 extra buffer rows at top
        self.grid = [[BLACK for _ in range(width)] for _ in range(height + 2)]

    def draw(self, screen):
        # Render visible rows only, skipping first 2 buffer rows
        for y in range(2, self.height + 2):
            for x in range(self.width):
                # Map internal row index to screen Y coordinate
                draw_y = (y - 2) * 30
                # Draw cell and border
                pygame.draw.rect(screen, self.grid[y][x], (x * 30, draw_y, 30, 30), 0)
                pygame.draw.rect(screen, GRAY, (x * 30, draw_y, 30, 30), 1)

def remove_complete_lines(grid):
    # Filter out lines that contain at least one BLACK cell
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]
    # Determine number of lines cleared
    lines_removed = len(grid) - len(new_grid)
    # Reinsert empty rows at top of grid
    for _ in range(lines_removed):
        new_grid.insert(0, [BLACK for _ in range(len(grid[0]))])
    return new_grid, lines_removed