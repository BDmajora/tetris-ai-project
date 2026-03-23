class TetrisHeuristics:
    """Numerical evaluation of a static grid state with bottom-up awareness."""
    
    @staticmethod
    def get_column_heights(grid):
        """Returns a list of the height of each column."""
        width = len(grid[0])
        height = len(grid)
        heights = [0] * width
        for x in range(width):
            for y in range(height):
                if grid[y][x] != (0, 0, 0):
                    heights[x] = height - y
                    break
        return heights

    @staticmethod
    def get_bumpiness(heights):
        """Measures the variance between adjacent column heights."""
        return sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))

    @staticmethod
    def get_holes_and_blockades(grid):
        """
        Calculates:
        1. Holes: Empty spaces with at least one block above them.
        2. Blockades: The total count of blocks sitting on top of holes.
        """
        width = len(grid[0])
        height = len(grid)
        holes = 0
        blockades = 0
        
        for x in range(width):
            found_block = False
            blocks_in_col = 0
            for y in range(height):
                if grid[y][x] != (0, 0, 0):
                    found_block = True
                    blocks_in_col += 1
                elif found_block and grid[y][x] == (0, 0, 0):
                    # We found a hole!
                    holes += 1
                    # Every block we've seen so far in this column is 'blocking' this hole
                    blockades += blocks_in_col
                    
        return holes, blockades

    @staticmethod
    def get_wells(heights):
        """
        A 'well' is a vertical gap surrounded by higher columns.
        Deep wells are dangerous as they are hard to fill.
        """
        wells = 0
        for i in range(len(heights)):
            # Get height of left and right neighbors (use high value if at edge)
            left = heights[i-1] if i > 0 else 100 
            right = heights[i+1] if i < len(heights) - 1 else 100
            
            # If both neighbors are higher, it's a well
            if left > heights[i] and right > heights[i]:
                depth = min(left, right) - heights[i]
                # Penalize deeper wells exponentially
                wells += (depth * (depth + 1)) // 2
        return wells