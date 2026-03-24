def check_collision(grid, block, position):
    # Validation of block position against grid boundaries and occupied cells
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                grid_x = position[0] + x
                grid_y = position[1] + y
                
                # Boundary validation: X-axis limits and Y-axis floor
                if grid_x < 0 or grid_x >= len(grid[0]) or grid_y >= len(grid):
                    return True
                
                # Occupancy validation: Intersection with non-empty grid cells
                if grid_y >= 0:
                    if grid[grid_y][grid_x] != (0, 0, 0):
                        return True
    return False

def merge_grid_and_block(grid, block, position):
    # Persistent transfer of block color data to grid coordinates
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                grid_x = position[0] + x
                grid_y = position[1] + y
                # Coordinate bounds check for safe memory access
                if 0 <= grid_y < len(grid) and 0 <= grid_x < len(grid[0]):
                    grid[grid_y][grid_x] = block.colour