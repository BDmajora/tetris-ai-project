class TetrisHeuristics:
    """Numerical evaluation of a static grid state."""
    
    @staticmethod
    def get_column_heights(grid):
        width = len(grid[0])
        heights = [0] * width
        for x in range(width):
            for y in range(len(grid)):
                if grid[y][x] != (0, 0, 0):
                    heights[x] = len(grid) - y
                    break
        return heights

    @staticmethod
    def get_holes(grid):
        holes = 0
        for x in range(len(grid[0])):
            block_found = False
            for y in range(len(grid)):
                if grid[y][x] != (0, 0, 0):
                    block_found = True
                elif block_found and grid[y][x] == (0, 0, 0):
                    holes += 1
        return holes

    @staticmethod
    def get_bumpiness(heights):
        return sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))

    @staticmethod
    def get_hole_and_column_count(grid):
        height, width = len(grid), len(grid[0])
        hole_count, column_list = 0, [0] * width
        
        for x in range(width):
            empty_count = 0
            for y in range(height - 1, -1, -1):
                if grid[y][x] == (0, 0, 0):
                    empty_count += 1
                else:
                    hole_count += empty_count
                    empty_count = 0
            column_list[x] = empty_count
            
        return hole_count, column_list