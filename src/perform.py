class MovePerformer:
    def __init__(self, game):
        self.game = game

    def perform_ai_move_step_new(self):
        """
        Executes the AI's plan by snapping the block into the correct 
        rotation and X-position instantly.
        """
        g = self.game
        
        # 1. Safety check: Don't move if we don't have a plan or aren't active
        if g.target_position is None or not g.moving:
            return

        # 2. PRIORITY: Rotation
        # We rotate first. Using a while loop makes it happen in one frame.
        while g.current_block.rotation != g.target_rotation:
            if not g.rotate_block('clockwise'):
                # If we get stuck (shouldn't happen with AI pathing), stop.
                g.moving = False 
                return 

        # 3. Horizontal movement
        # Snap to the target X position immediately.
        while g.current_position[0] != g.target_position:
            curr_x = g.current_position[0]
            target_x = g.target_position
            
            direction = 1 if curr_x < target_x else -1
            if not g.move_block(direction, 0):
                # Blocked by the stack or wall. 
                g.moving = False 
                return
        
        # 4. Target Reached! 
        # Once we are in the correct column and rotation, we stop the 'moving' phase.
        # The Game's update loop will now take over and Hard Drop the block.
        g.moving = False