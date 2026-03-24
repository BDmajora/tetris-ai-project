import pygame

class ScreenHandler:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, screen, grid, current_block, current_position, next_block, score, level, game_over):
        # Orchestrate rendering of all game components
        self.draw_grid(screen, grid)
        if not game_over:
            self.draw_block(screen, current_block, current_position)
        else:
            self.draw_game_over(screen)
        self.draw_score_and_level(screen, score, level)
        self.draw_next_block(screen, next_block)

    def draw_grid(self, screen, grid):
        # Render the game board starting from the third row to hide the spawn buffer
        for y in range(2, len(grid)):
            for x, cell in enumerate(grid[y]):
                # Map internal grid index to visible screen coordinates
                draw_y = (y - 2) * 30
                color = cell if cell else (0, 0, 0)
                
                # Render cell background and structural borders
                pygame.draw.rect(screen, color, (x * 30, draw_y, 30, 30), 0)
                pygame.draw.rect(screen, (40, 40, 40), (x * 30, draw_y, 30, 30), 1)

    def draw_block(self, screen, block, offset):
        # Render the active piece relative to the visible coordinate system
        off_x, off_y = offset
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = off_y + y
                    # Visibility check: Only render segments below the buffer zone
                    if grid_y >= 2:
                        draw_y = (grid_y - 2) * 30
                        pygame.draw.rect(
                            screen, block.colour,
                            ((off_x + x) * 30, draw_y, 30, 30), 0
                        )

    def draw_game_over(self, screen):
        # Display terminal state overlay centered on the game board
        font = pygame.font.Font(None, 72)
        text_surface = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(self.width * 15, self.height * 15))
        screen.blit(text_surface, text_rect)
    
    def draw_score_and_level(self, screen, score, level):
        # Render session metadata and UI labels to the sidebar
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score", True, (255, 255, 255))
        score_value = font.render(f"{score}", True, (255, 255, 255))
        level_text = font.render("Level", True, (255, 255, 255))
        level_value = font.render(f"{level}", True, (255, 255, 255))
        next_block_text = font.render("Next Block", True, (255, 255, 255))

        # UI Positioning: Right-aligned relative to the grid
        ui_x = self.width * 30 + 50
        screen.blit(score_text, (ui_x, 10))
        screen.blit(score_value, (ui_x, 50))
        screen.blit(level_text, (ui_x, 90))
        screen.blit(level_value, (ui_x, 130))
        screen.blit(next_block_text, (ui_x, 170))

    def draw_next_block(self, screen, next_block):
        # Render a preview of the queued piece in the UI sidebar
        start_x = self.width * 30 + 50
        start_y = 210
        for y, row in enumerate(next_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen, next_block.colour,
                        (start_x + x * 30, start_y + y * 30, 30, 30), 0
                    )