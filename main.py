import pygame
import copy
from game import Game

def main():
    # Initialize the pygame module
    pygame.init()
    
    # Create a screen with a width and height of 600 pixels
    # This size is chosen to give space for displaying score and level
    screen = pygame.display.set_mode((600, 600))
    
    # Create a clock object to manage the game's frame rate
    clock = pygame.time.Clock()
    
    # Create an instance of the Game class with a grid width of 10 blocks and height of 20 blocks
    game = Game(10, 20)

    # Main game loop
    while True:
        # Calculate the time passed since the last frame, converted to seconds
        delta_time = clock.tick(60) / 1000.0  # Targeting 60 frames per second
        
        # Handle events in the game (e.g., key presses, quitting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                return  # Exit the main function
        
        # Update the game state based on the elapsed time
        game.update(delta_time)
        
        # Fill the screen with a black color to clear previous drawings
        screen.fill((0, 0, 0))
        
        # Draw the current game state onto the screen
        game.draw(screen)
        
        # Update the display to show the drawn frame
        pygame.display.flip()

# Check if this script is being run directly (not imported)
if __name__ == "__main__":
    main()
