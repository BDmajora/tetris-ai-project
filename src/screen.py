import pygame
from .level import Level

class ScreenHandler:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, screen, grid, current_block, current_position, next_block, score, level, game_over):
        self.draw_grid(screen, grid)
        if not game_over:
            self.draw_block(screen, current_block, current_position)
        else:
            self.draw_game_over(screen)
        self.draw_score_and_level(screen, score, level)
        self.draw_next_block(screen, next_block)

    def draw_grid(self, screen, grid):
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                color = cell if cell else (0, 0, 0)  # Use black for empty cells
                pygame.draw.rect(
                    screen, color,
                    (x * 30, y * 30, 30, 30), 0
                )
                # Draw grid lines
                pygame.draw.rect(
                    screen, (40, 40, 40),
                    (x * 30, y * 30, 30, 30), 1
                )

    def draw_block(self, screen, block, offset):
        off_x, off_y = offset
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen, block.colour,
                        ((off_x + x) * 30, (off_y + y) * 30, 30, 30), 0
                    )

    def draw_game_over(self, screen):
        font = pygame.font.Font(None, 72)  # None uses the default pygame font, 72 is the size
        text_surface = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(self.width * 15, self.height * 15))
        screen.blit(text_surface, text_rect)
    
    def draw_score_and_level(self, screen, score, level):
        font = pygame.font.Font(None, 36)  # None uses the default pygame font, 36 is the size
        score_text = font.render("Score", True, (255, 255, 255))
        score_value = font.render(f"{score}", True, (255, 255, 255))
        level_text = font.render("Level", True, (255, 255, 255))
        level_value = font.render(f"{level}", True, (255, 255, 255))  # Pass level directly
        next_block_text = font.render("Next Block", True, (255, 255, 255))

        screen.blit(score_text, (self.width * 30 + 50, 10))
        screen.blit(score_value, (self.width * 30 + 50, 50))
        screen.blit(level_text, (self.width * 30 + 50, 90))
        screen.blit(level_value, (self.width * 30 + 50, 130))
        screen.blit(next_block_text, (self.width * 30 + 50, 170))

    def draw_next_block(self, screen, next_block):
        start_x = self.width * 30 + 50
        start_y = 210
        for y, row in enumerate(next_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen, next_block.colour,
                        (start_x + x * 30, start_y + y * 30, 30, 30), 0
                    )