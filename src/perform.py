class MovePerformer:
    def __init__(self, game):
        self.game = game

    def perform_ai_move_step_new(self):
        # Execution of AI trajectory via instantaneous rotation and horizontal translation
        g = self.game
        
        # Validation of active plan and state
        if g.target_position is None or not g.moving:
            return

        # Rotation alignment: Iterative clockwise rotation to target state
        while g.current_block.rotation != g.target_rotation:
            if not g.rotate_block('clockwise'):
                # Terminate on obstruction
                g.moving = False 
                return 

        # Horizontal positioning: X-axis translation to target coordinates
        while g.current_position[0] != g.target_position:
            curr_x = g.current_position[0]
            target_x = g.target_position
            
            direction = 1 if curr_x < target_x else -1
            if not g.move_block(direction, 0):
                # Terminate on obstruction
                g.moving = False 
                return
        
        # Signal target acquisition for hard drop
        g.moving = False