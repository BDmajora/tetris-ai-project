class MovePlanner:
    def __init__(self, ai):
        self.ai = ai

    def plan_ai_move(self, game):
        # Retrieve optimal trajectory from AI agent
        best_move = self.ai.get_best_move()
        
        # Panic handling: Default to current state if no valid move identified
        if best_move is None:
            print("AI logic failure: No safe moves identified. Executing emergency drop.")
            game.target_rotation = game.current_block.rotation
            game.target_position = game.current_position[0]
            game.moving = True
            return

        # Target state assignment and execution signal
        game.target_rotation = best_move[0]
        game.target_position = best_move[1]
        game.moving = True
        game.failed_rotation_attempts = 0