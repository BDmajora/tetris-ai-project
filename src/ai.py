import copy
from .grid import remove_complete_lines
from .blocks import create_block, shapes
from .position import check_collision, merge_grid_and_block

class AI:
    def __init__(self, game, hole_weight=3, height_weight=9, column_weight=5):
        # Initialize AI with the game instance and weights for scoring
        self.game = game
        self.hole_weight = hole_weight
        self.height_weight = height_weight
        self.column_weight = column_weight

    def get_best_move(self):
        # Find the best move by evaluating all possible rotations and positions
        best_score = float('-inf')
        best_move = None

        for rotation in range(4):
            # Rotate the block up to 4 times (0, 90, 180, 270 degrees)
            block = copy.deepcopy(self.game.current_block)
            for _ in range(rotation):
                block.rotate()

            # Try each possible horizontal position
            for x in range(self.game.width - len(block.shape[0]) + 1):
                score, _ = self.simulate_move(block, x)
                if score > best_score:
                    best_score = score
                    best_move = (rotation, x)

        return best_move

    def simulate_move(self, block, x):
        # Simulate placing the block at the given x position
        grid_copy = copy.deepcopy(self.game.grid.grid)
        y = 0
        while not check_collision(grid_copy, block, (x, y)):
            y += 1
        y -= 1

        if y < 0:
            # If the block cannot be placed, return a negative infinite score
            return float('-inf'), grid_copy

        # Merge the block into the grid and remove completed lines
        merge_grid_and_block(grid_copy, block, (x, y))
        grid_copy, lines_removed = remove_complete_lines(grid_copy)

        # Evaluate the resulting grid state
        score = self.evaluate_grid(grid_copy, lines_removed)
        return score, grid_copy

    def evaluate_grid(self, grid, lines_removed):
        # Calculate a score based on the grid state and lines removed
        height_penalty = self.get_column_heights_penalty(grid)
        holes_penalty = self.get_holes_penalty(grid)
        bumpiness_penalty = self.get_bumpiness_penalty(grid)
        hole_score, column_score = self.get_hole_and_column_score(grid)
        
        return (lines_removed * 10 - height_penalty - holes_penalty - bumpiness_penalty 
                - hole_score - column_score + self.get_height_score(grid))

    def get_column_heights_penalty(self, grid):
        # Calculate a penalty based on the heights of the columns
        heights = [0] * len(grid[0])
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                if grid[y][x] != (0, 0, 0):
                    heights[x] = len(grid) - y
                    break
        return sum(heights)

    def get_holes_penalty(self, grid):
        # Calculate a penalty based on the number of holes in the grid
        holes = 0
        for x in range(len(grid[0])):
            block_found = False
            for y in range(len(grid)):
                if grid[y][x] != (0, 0, 0):
                    block_found = True
                elif block_found and grid[y][x] == (0, 0, 0):
                    holes += 1
        return holes * 5

    def get_bumpiness_penalty(self, grid):
        # Calculate a penalty based on the bumpiness of the grid
        heights = []
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                if grid[y][x] != (0, 0, 0):
                    heights.append(len(grid) - y)
                    break
            else:
                heights.append(0)
        bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))
        return bumpiness

    def get_hole_and_column_score(self, grid):
        # Calculate scores based on holes and column configuration
        hole_count, column_count = self.get_hole_and_column_count(grid)
        hole_score = hole_count * self.hole_weight
        column_score = column_count * self.column_weight
        return hole_score, column_score

    def get_hole_and_column_count(self, grid):
        # Count the number of holes and isolated columns in the grid
        height = len(grid)
        width = len(grid[0])
        hole_count = 0
        column_count = 0
        column_list = [0] * width
        for x in range(width):
            empty_count = 0
            for y in range(height - 1, -1, -1):
                if grid[y][x] == (0, 0, 0):
                    empty_count += 1
                else:
                    hole_count += empty_count
                    empty_count = 0
            column_list[x] = empty_count

        column_height_limit = 3
        if column_list[0] >= column_list[1] + column_height_limit:
            column_count += 1
        if column_list[width - 1] >= column_list[width - 2] + column_height_limit:
            column_count += 1
        for i in range(1, width - 1):
            if column_list[i] >= column_list[i - 1] + column_height_limit and column_list[i] >= column_list[i + 1] + column_height_limit:
                column_count += 1

        return hole_count, column_count

    def get_height_score(self, grid):
        # Calculate a score based on the height of the highest block
        position_height = len(grid) - min(y for y, row in enumerate(grid) if any(cell != (0, 0, 0) for cell in row))
        height_score = (position_height / len(grid)) * self.height_weight
        return height_score

    def drop_block(self, block, position):
        # Drop the block to the lowest possible y position at the given x position
        x, y = position
        while not check_collision(self.game.grid.grid, block, (x, y)):
            y += 1
        y -= 1
        return (x, y)
