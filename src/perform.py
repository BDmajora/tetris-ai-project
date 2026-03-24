class MovePerformer:
    def __init__(self, game):
        self.game = game
        self.attempt_count = 0

    def perform_ai_move_step_new(self):
        # Execute one step of the planned AI move
        g = self.game
        
        # 1. Handle rotations first
        if g.current_block.rotation != g.target_rotation:
            if not g.rotate_block('counterclockwise'):
                # Move down to find space if rotation fails
                g.move_block(0, 1)
            return

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