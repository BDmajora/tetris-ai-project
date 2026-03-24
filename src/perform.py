class MovePerformer:
    def __init__(self, game):
        self.game = game
        self.attempt_count = 0

    def perform_ai_move_step_new(self):
        g = self.game
        if g.target_position is None:
            return

        # Handle Rotation first
        if g.current_block.rotation != g.target_rotation:
            g.rotate_block('counterclockwise')
            return

        # Handle Horizontal Movement
        curr_x = g.current_position[0]
        target_x = g.target_position

        if curr_x < target_x:
            g.move_block(1, 0)
        elif curr_x > target_x:
            g.move_block(-1, 0)
        else:
            # Target reached! Now let gravity or a "Soft Drop" take over
            # If you want the AI to "Slam" the block down:
            # g.move_block(0, 1) 
            pass

        # 2. Handle horizontal movement to target X
        # target_position is expected to be an integer X coordinate
        curr_x = g.current_position[0]
        target_x = g.target_position

        if curr_x < target_x:
            g.move_block(1, 0)
        elif curr_x > target_x:
            g.move_block(-1, 0)
        else:
            # 3. Drop block vertically once X is reached
            if not g.move_block(0, 1):
                # Lock block if downward move is blocked
                g.block_locker.lock_block_and_update_state()
                g.moving = False