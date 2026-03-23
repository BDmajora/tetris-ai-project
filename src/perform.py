import copy

class MovePerformer:
    def __init__(self, game):
        self.game = game
        self.attempt_count = 0

    def perform_ai_move_step_new(self):
        game = self.game
        max_attempts = 50  # Maximum number of attempts for AI to perform a move

        while game.moving and self.attempt_count < max_attempts:
            self.attempt_count += 1  # Increment attempt counter

            if not self.ensure_valid_target_position():
                return  # Exit if target position is invalid

            if game.target_rotation > 0:
                if not self.rotate_block(game, 'counterclockwise'):
                    game.target_rotation -= 1  # Decrement target rotation and try again
                    continue

            if game.current_position[0] < game.target_position[0]:
                if not game.move_block(1, 0):  # Move right
                    print(f"AI move step failed on attempt {self.attempt_count}, trying again")
                    continue
            elif game.current_position[0] > game.target_position[0]:
                if not game.move_block(-1, 0):  # Move left
                    print(f"AI move step failed on attempt {self.attempt_count}, trying again")
                    continue
            else:
                if not game.move_block(0, 1):  # Move down
                    game.block_locker.lock_block_and_update_state()
                    print(f"AI move completed, new block position: {game.current_position}")
                    game.failed_rotation_attempts = 0
                    game.moving = False
                    self.attempt_count = 0
                    return

        if self.attempt_count >= max_attempts:
            print("AI move step failed after reaching max attempts, forcing block down")
            self.force_block_down()
            self.attempt_count = 0

    def perform_ai_move_step_old(self):
        if self.attempt_count >= self.game.max_ai_attempts:
            print("AI move step failed after reaching max attempts, stopping")
            self.game.moving = False
            self.attempt_count = 0
            self.game.handle_failed_move()  # Call a method to handle the failure
            return

        if self.game.target_position:
            target_x, target_y = self.game.target_position
            current_x, current_y = self.game.current_position

            if current_y < target_y:
                if self.game.move_block(0, 1):
                    self.attempt_count += 1
                else:
                    print(f"AI move step failed on attempt {self.attempt_count}, trying again")
                    self.attempt_count += 1
            elif current_x < target_x:
                if self.game.move_block(1, 0):
                    self.attempt_count += 1
                else:
                    print(f"AI move step failed on attempt {self.attempt_count}, trying again")
                    self.attempt_count += 1
            elif current_x > target_x:
                if self.game.move_block(-1, 0):
                    self.attempt_count += 1
                else:
                    print(f"AI move step failed on attempt {self.attempt_count}, trying again")
                    self.attempt_count += 1
            else:
                print("AI successfully moved the block to the target position")
                self.game.moving = False
                self.attempt_count = 0
        else:
            self.attempt_count = 0
            self.game.moving = False

    def ensure_valid_target_position(self):
        game = self.game
        if isinstance(game.target_position, list) and len(game.target_position) == 2 and all(isinstance(i, int) for i in game.target_position):
            return True
        else:
            print(f"Invalid target_position: {game.target_position}")
            game.moving = False
            return False

    def rotate_block(self, game, direction):
        game.rotate_block(direction)
        if check_collision(game.grid.grid, game.current_block, game.current_position):
            game.failed_rotation_attempts += 1
            print(f"AI rotation failed, retrying move. Failed attempts: {game.failed_rotation_attempts}")
            if game.failed_rotation_attempts >= game.max_failed_attempts:
                print(f"Exceeded max failed rotation attempts ({game.max_failed_attempts}), moving on.")
                game.failed_rotation_attempts = 0
                return False
            if game.move_block(0, 1):
                print(f"Moved block down to retry rotation. New position: {game.current_position}")
            else:
                print("Failed to move block down for retry.")
            return False
        return True

    def force_block_down(self):
        game = self.game
        while not check_collision(game.grid.grid, game.current_block, [game.current_position[0], game.current_position[1] + 1]):
            game.move_block(0, 1)
        game.block_locker.lock_block_and_update_state()
        print("Forced block down to avoid collision lock")
        game.moving = False

def check_collision(grid, block, position):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                grid_x = position[0] + x
                grid_y = position[1] + y
                if grid_x < 0 or grid_x >= len(grid[0]) or grid_y < 0 or grid_y >= len(grid):
                    return True
                if grid[grid_y][grid_x]:
                    return True
    return False
