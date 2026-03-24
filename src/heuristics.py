class TetrisHeuristics:
    """Numerical evaluation of a static grid state with advanced survival awareness."""
    
    @staticmethod
    def get_column_heights(grid):
        width = len(grid[0])
        height = len(grid)
        heights = [0] * width
        for x in range(width):
            for y in range(height):
                # If cell is NOT black (0,0,0), it's a block
                if grid[y][x] != (0, 0, 0):
                    heights[x] = height - y
                    break
        return heights

    @staticmethod
    def get_bumpiness(heights):
        return sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))

    @staticmethod
    def get_holes_and_blockades(grid):
        width = len(grid[0])
        height = len(grid)
        holes = 0
        blockades = 0
        for x in range(width):
            found_block = False
            blocks_above_current_hole = 0
            for y in range(height):
                if grid[y][x] != (0, 0, 0):
                    found_block = True
                    blocks_above_current_hole += 1
                elif found_block and grid[y][x] == (0, 0, 0):
                    # We found an empty space underneath a block
                    holes += 1
                    blockades += blocks_above_current_hole
        return holes, blockades

    @staticmethod
    def get_transitions(grid):
        """
        Calculates transitions between filled and empty cells.
        Now includes 'Wall-Awareness' to encourage building against edges.
        """
        width = len(grid[0])
        height = len(grid)
        row_transitions = 0
        col_transitions = 0

        # Row Transitions (Horizontal)
        for y in range(height):
            # Treat the 'left wall' as a solid block (not empty)
            prev_cell_empty = False 
            for x in range(width):
                is_empty = (grid[y][x] == (0, 0, 0))
                if is_empty != prev_cell_empty:
                    row_transitions += 1
                prev_cell_empty = is_empty
            # Treat the 'right wall' as a solid block
            if prev_cell_empty:
                row_transitions += 1

        # Column Transitions (Vertical)
        for x in range(width):
            # Treat the 'ceiling' as empty, but 'floor' as solid
            prev_cell_empty = True 
            for y in range(height):
                is_empty = (grid[y][x] == (0, 0, 0))
                if is_empty != prev_cell_empty:
                    col_transitions += 1
                prev_cell_empty = is_empty
            # Treat the 'floor' as solid
            if prev_cell_empty:
                col_transitions += 1
                
        return row_transitions, col_transitions

    @staticmethod
    def get_wells(heights):
        """
        Calculates deep vertical 'wells'. 
        Fixed the wall height bug (previously 100).
        """
        wells_score = 0
        width = len(heights)
        for i in range(width):
            # Determine height of neighboring columns
            # If at edge, treat the wall as the height of the current column + 1
            left = heights[i-1] if i > 0 else heights[i] + 1
            right = heights[i+1] if i < width - 1 else heights[i] + 1
            
            if left > heights[i] and right > heights[i]:
                depth = min(left, right) - heights[i]
                # Triangular number scoring for depth (1=1, 2=3, 3=6...)
                wells_score += (depth * (depth + 1)) // 2
        return wells_score

    @staticmethod
    def get_all_metrics(grid):
        heights = TetrisHeuristics.get_column_heights(grid)
        holes, blockades = TetrisHeuristics.get_holes_and_blockades(grid)
        r_trans, c_trans = TetrisHeuristics.get_transitions(grid)
        
        return {
            'heights': heights,
            'max_height': max(heights) if heights else 0,
            'total_height': sum(heights),
            'holes': holes,
            'blockades': blockades,
            'row_transitions': r_trans,
            'col_transitions': c_trans,
            'bumpiness': TetrisHeuristics.get_bumpiness(heights),
            'wells': TetrisHeuristics.get_wells(heights)
        }