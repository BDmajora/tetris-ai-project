import pygame
from src.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tetris AI Training")
    clock = pygame.time.Clock()
    
    # 1. Initialize the first game
    game = Game(10, 20)
    
    # Track which "Generation" or Game Number we are on
    game_count = 1

    while True:
        delta_time = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 2. Check if the AI died
        if game.game_over:
            print(f"Game {game_count} Finished. Final Score: {game.score}")
            
            # Save the brain (the agent) so we don't lose progress
            current_brain = game.agent 
            
            # 3. RESTART: Create a new game but pass in the existing brain
            game = Game(10, 20)
            game.agent = current_brain # Inject the learned knowledge
            game.ai.agent = current_brain # Ensure AI class uses the same brain
            
            game_count += 1
            print(f"Starting Game {game_count}... Epsilon: {game.agent.epsilon:.4f}")

        # Standard Update/Draw
        game.update(delta_time)
        screen.fill((0, 0, 0))
        game.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()