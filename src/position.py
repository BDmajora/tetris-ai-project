def check_collision(grid, block, position):
    # Check if block collides with grid boundaries or existing blocks
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                grid_x = position[0] + x
                grid_y = position[1] + y
                
                # Boundary checks
                if grid_x < 0 or grid_x >= len(grid[0]) or grid_y >= len(grid):
                    return True
                
                # Collision check (only check if within vertical grid bounds)
                if grid_y >= 0:
                    # Explicitly check if cell is NOT black (0, 0, 0)
                    if grid[grid_y][grid_x] != (0, 0, 0):
                        return True
    return False

def merge_grid_and_block(grid, block, position):
    # Transfer block color to grid cells at final position
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                grid_x = position[0] + x
                grid_y = position[1] + y
                # Only merge if within grid bounds
                if 0 <= grid_y < len(grid) and 0 <= grid_x < len(grid[0]):
                    grid[grid_y][grid_x] = block.colour