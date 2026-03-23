class MovePlanner:
    def __init__(self, ai):
        self.ai = ai

    def plan_ai_move(self, game):
        best_move = self.ai.get_best_move()
        if best_move:
            # Check if best_move has at least 2 values and the expected structure
            if isinstance(best_move, (list, tuple)) and len(best_move) >= 2 and isinstance(best_move[0], int) and isinstance(best_move[1], int):
                if len(best_move) >= 4:
                    game.target_rotation, x, _, _ = best_move[:4]  # Unpack only the first four values
                else:
                    game.target_rotation, x = best_move[:2]  # Unpack the first two values and set default for others
                    _ = 0  # Set default value for unused variables
                game.target_position = [x, 0]
                game.moving = True
                print(f"AI planned move to position: {game.target_position} with rotations: {game.target_rotation}")
            else:
                print(f"Unexpected best_move structure: {best_move}")
                game.moving = False
        else:
            game.moving = False
