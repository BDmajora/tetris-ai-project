def check_collision(grid, block, offset):
    off_x, off_y = offset  # Extract offset coordinates
    for y, row in enumerate(block.shape):  # Iterate over each row of the block
        for x, cell in enumerate(row):  # Iterate over each cell in the row
            if cell:  # Only check cells that are part of the block
                try:
                    if grid[y + off_y][x + off_x] != (0, 0, 0):  # Check if the grid cell is not empty
                        return True  # Collision detected
                except IndexError:
                    return True  # Collision if accessing out of grid bounds
    return False  # No collision detected

def merge_grid_and_block(grid, block, offset):
    off_x, off_y = offset  # Extract offset coordinates
    for y, row in enumerate(block.shape):  # Iterate over each row of the block
        for x, cell in enumerate(row):  # Iterate over each cell in the row
            if cell:  # Only merge cells that are part of the block
                grid[y + off_y][x + off_x] = block.colour  # Place the block's color in the grid
