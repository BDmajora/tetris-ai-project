import pygame
import sys
from src.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tetris AI Training")
    clock = pygame.time.Clock()
    
    # 1. Initialize the first game
    game = Game(10, 20)
    
    # --- LOAD PREVIOUS PROGRESS ---
    # Load the neural network weights
    game.agent.load_brain()
    
    # Load the metadata (Game Count and High Score)
    saved_stats = game.agent.load_stats()
    if saved_stats:
        game_count = saved_stats.get('game_count', 1)
        high_score = saved_stats.get('high_score', 0)
        print(f"Resuming from Game {game_count}. High Score to beat: {high_score}")
    else:
        game_count = 1
        high_score = 0
        print("Starting fresh training session.")

    try:
        while True:
            delta_time = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Save both brain and stats before closing
                    game.agent.save_brain()
                    game.agent.save_stats({'game_count': game_count, 'high_score': high_score})
                    pygame.quit()
                    return

            # 2. Check if the AI died
            if game.game_over:
                print(f"Game {game_count} Finished. Final Score: {game.score}")
                
                # Check for new High Score
                is_new_high_score = False
                if game.score > high_score:
                    high_score = game.score
                    is_new_high_score = True
                    print(f"🏆 NEW ALL-TIME HIGH SCORE: {high_score} 🏆")

                # Prepare stats for saving
                current_stats = {
                    'game_count': game_count,
                    'high_score': high_score
                }

                # Save every 10 games OR immediately if it's a new record
                if game_count % 10 == 0 or is_new_high_score:
                    game.agent.save_brain()
                    game.agent.save_stats(current_stats)

                # Preserve the current agent instance across game restarts
                current_agent = game.agent 
                
                # 3. RESTART: Create a new game and re-inject the brain
                game = Game(10, 20)
                game.agent = current_agent 
                game.ai.agent = current_agent 
                
                game_count += 1
                print(f"Starting Game {game_count}... Epsilon: {game.agent.epsilon:.4f}")

            # Standard Update and Rendering
            game.update(delta_time)
            screen.fill((0, 0, 0))
            game.draw(screen)
            pygame.display.flip()

    except KeyboardInterrupt:
        # Save progress if the user interrupts the script (Ctrl+C)
        print("\nTraining session interrupted. Performing safety save...")
        final_stats = {'game_count': game_count, 'high_score': high_score}
        game.agent.save_brain()
        game.agent.save_stats(final_stats)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()