class MovePlanner:
    def __init__(self, ai):
        self.ai = ai

    def plan_ai_move(self, game):
        # AI returns (rotation_count, final_x_coordinate)
        best_move = self.ai.get_best_move()
        
        if best_move:
            # Validate that best_move is a tuple/list with (int, int)
            if (isinstance(best_move, (list, tuple)) and 
                len(best_move) >= 2 and 
                isinstance(best_move[0], int) and 
                isinstance(best_move[1], int)):
                
                # Assign target rotation and X target
                game.target_rotation = best_move[0]
                
                # FIX: Set target_position as a single integer X 
                # This prevents the 'int vs list' TypeError in MovePerformer
                game.target_position = best_move[1]
                
                game.moving = True
                game.failed_rotation_attempts = 0 
                
                print(f"AI planned move to X: {game.target_position} with {game.target_rotation} rotations")
            else:
                print(f"Unexpected best_move structure: {best_move}")
                game.moving = False
        else:
            # No valid move found by the AI brain
            game.moving = False