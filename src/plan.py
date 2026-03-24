class MovePlanner:
    def __init__(self, ai):
        self.ai = ai

    def plan_ai_move(self, game):
        best_move = self.ai.get_best_move()
        
        # If AI returns None (Panic Mode), pick a dummy move so it doesn't just freeze
        if best_move is None:
            print("AI BRAIN PANIC: No safe moves found! Emergency drop initiated.")
            game.target_rotation = game.current_block.rotation
            game.target_position = game.current_position[0]
            game.moving = True
            return

        game.target_rotation = best_move[0]
        game.target_position = best_move[1]
        game.moving = True
        game.failed_rotation_attempts = 0