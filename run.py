import pygame
import sys
import os
from src.game import Game
from src.optimize import run_model_optimization 
from src.logger import TrainingLogger
from src.plot_results import generate_graphs

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tetris AI Training")
    clock = pygame.time.Clock()
    
    # Initialize the Logger
    logger = TrainingLogger()
    
    game = Game(10, 20)
    game.agent.load_brain()
    
    saved_stats = game.agent.load_stats()
    if saved_stats:
        game_count = saved_stats.get('game_count', 1)
        high_score = saved_stats.get('high_score', 0)
        print(f"Resuming session. Current High Score: {high_score}")
    else:
        game_count = 1
        high_score = 0

    try:
        while True:
            delta_time = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Save and Optimize
                    game.agent.save_brain()
                    game.agent.save_stats({'game_count': game_count, 'high_score': high_score})
                    run_model_optimization() 
                    
                    # Generate Graph on exit
                    print("\nGenerating training report...")
                    generate_graphs() 
                    
                    pygame.quit()
                    return

            if game.game_over:
                is_new_high_score = game.score > high_score
                if is_new_high_score:
                    high_score = game.score
                    print(f"🏆 NEW HIGH SCORE: {high_score}")
                
                optimization_report = None
                # Save every 10 games or on a new record
                if game_count % 10 == 0 or is_new_high_score:
                    game.agent.save_brain()
                    game.agent.save_stats({'game_count': game_count, 'high_score': high_score})
                    optimization_report = run_model_optimization()

                # Log to JSON history
                logger.log(game_count, game.score, game.agent.epsilon, optimization_report)

                # Restart logic
                current_agent = game.agent 
                game = Game(10, 20)
                game.agent = current_agent 
                game.ai.agent = current_agent 
                
                game_count += 1
                print(f"Starting Game {game_count}... Epsilon: {game.agent.epsilon:.4f}")

            game.update(delta_time)
            screen.fill((0, 0, 0))
            game.draw(screen)
            pygame.display.flip()

    except KeyboardInterrupt:
        print("\nSession interrupted. Saving progress...")
        game.agent.save_brain()
        game.agent.save_stats({'game_count': game_count, 'high_score': high_score})
        run_model_optimization() 
        
        # Also generate graphs on Ctrl+C
        generate_graphs()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()