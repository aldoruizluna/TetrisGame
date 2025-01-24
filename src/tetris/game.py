"""
Main game module containing game logic for a Tetris game.

This module includes the BaseGame class, which serves as the foundation for all game modes,
inclusive of SpeedGame and BattleGame. The game logic handles piece movement, collision detection,
line clearing, and game state management.
"""

import random  # Import the random module to generate random pieces
import pygame  # Import Pygame for graphics and game mechanics
import logging  # Import logging module for debugging
import unittest  # Import unittest module for testing
from .constants import (  # Import constants used in the game
    SCREEN_DIMENSIONS,
    COLORS,
    SHAPES, GameState
)
from .tetrimino import Tetrimino  # Import the Tetrimino class for game pieces

# Initialize logger
logger = logging.getLogger(__name__)

class MockSettings:
    """Mock settings class for testing purposes."""
    def __init__(self, difficulty="Easy"):
        self.difficulty = difficulty

class BaseGame:
    """Base class for all game modes."""
    
    # Cache fall speeds for different difficulty levels
    FALL_SPEEDS = {
        "Easy": SCREEN_DIMENSIONS['BLOCK_SIZE'] * 6,
        "Normal": SCREEN_DIMENSIONS['BLOCK_SIZE'] * 5,
        "Hard": SCREEN_DIMENSIONS['BLOCK_SIZE'] * 4
    }
    
    def __init__(self, screen, settings, high_scores):
        """Initialize the game."""
        self.screen = screen
        self.settings = settings
        self.high_scores = high_scores
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.current_state = GameState.PLAYING
        self.running = True
        self.reset_game()
        pygame.event.set_grab(True)

    def reset_game(self):
        """Reset the game state."""
        grid_width = SCREEN_DIMENSIONS['GRID_WIDTH']
        grid_height = SCREEN_DIMENSIONS['GRID_HEIGHT']
        self.grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]
        self.current_piece = None
        self.fall_time = 0
        self.fall_speed = self.FALL_SPEEDS.get(self.settings.difficulty, self.FALL_SPEEDS["Normal"])
        self.game_over = False
        self.score = 0
        self.spawn_new_piece()

    def spawn_new_piece(self):
        """Create and spawn a new tetrimino."""
        start_x = SCREEN_DIMENSIONS['GRID_WIDTH'] // 2 - 1
        start_y = 0
        shape_info = random.choice(SHAPES)
        self.current_piece = Tetrimino(start_x, start_y, shape_info)

    def check_collision(self, x_offset=0, y_offset=0, shape=None):
        """Check if the current piece collides with anything."""
        if not self.current_piece:
            return False
        
        # Use provided shape or current piece's shape
        shape = shape if shape is not None else self.current_piece.shape
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:  # If the cell is part of the piece
                    # Calculate absolute position of the cell
                    abs_x = self.current_piece.x + x + x_offset
                    abs_y = self.current_piece.y + y + y_offset

                    # Check for collisions with walls or existing blocks
                    if (abs_x < 0 or abs_x >= SCREEN_DIMENSIONS['GRID_WIDTH'] or 
                        abs_y >= SCREEN_DIMENSIONS['GRID_HEIGHT'] or 
                        (abs_y >= 0 and self.grid[abs_y][abs_x] is not None)):
                        return True  # Collision detected
        return False  # No collision detected

    def lock_piece(self):
        """Lock the current piece in place."""
        if not self.current_piece:
            return
            
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    abs_y = self.current_piece.y + y
                    abs_x = self.current_piece.x + x
                    
                    # Check if piece is within grid bounds
                    if 0 <= abs_y < SCREEN_DIMENSIONS['GRID_HEIGHT'] and 0 <= abs_x < SCREEN_DIMENSIONS['GRID_WIDTH']:
                        self.grid[abs_y][abs_x] = self.current_piece.color
                    else:
                        self.game_over = True
                        return

        # Clear any completed lines and update score
        lines_cleared = self.clear_lines()
        if lines_cleared > 0:
            self.score += lines_cleared * 100

        # Spawn a new piece
        self.spawn_new_piece()
        
        # Check if the new piece can be placed
        if self.check_collision():
            self.game_over = True

    def clear_lines(self):
        """Clear completed lines."""
        lines_cleared = 0
        y = SCREEN_DIMENSIONS['GRID_HEIGHT'] - 1
        
        while y >= 0:
            if all(cell is not None for cell in self.grid[y]):
                lines_cleared += 1
                # Move all lines above this one down
                for move_y in range(y, 0, -1):
                    self.grid[move_y] = self.grid[move_y - 1][:]
                # Clear the top line
                self.grid[0] = [None] * SCREEN_DIMENSIONS['GRID_WIDTH']
            else:
                y -= 1

        return lines_cleared

    def update(self):
        """Update game state."""
        if not self.current_piece:
            self.spawn_new_piece()
            return

        if self.current_state == GameState.PLAYING and not self.game_over:
            # Update fall time
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            # Move piece down if enough time has passed
            if self.fall_time >= self.fall_speed:
                self.fall_time = 0
                
                # Check if piece can move down
                if not self.check_collision(y_offset=1):
                    self.current_piece.move(0, 1)
                else:
                    # Lock the piece and spawn a new one
                    self.lock_piece()
                    if self.game_over:
                        self.current_state = GameState.GAME_OVER

    def handle_input(self, events):
        """Handle player input."""
        # Handle input events such as key presses
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Move left if no collision
                if event.key == pygame.K_LEFT:
                    if not self.check_collision(x_offset=-1):  
                        self.current_piece.move(-1, 0)
                # Move right if no collision
                elif event.key == pygame.K_RIGHT:
                    if not self.check_collision(x_offset=1):  
                        self.current_piece.move(1, 0)
                # Move down if no collision
                elif event.key == pygame.K_DOWN:
                    if not self.check_collision(y_offset=1):  
                        self.current_piece.move(0, 1)
                # Rotate the piece
                elif event.key == pygame.K_UP:
                    self.current_piece.rotate()  
                # Exit the game
                elif event.key == pygame.K_ESCAPE:
                    self.running = False  
                # Navigate between game screens
                elif self.current_state == GameState.MAIN_MENU:
                    if event.key == pygame.K_RETURN:
                        self.current_state = GameState.PLAYING  # Start the game
                elif self.current_state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()  # Reset the game
                elif self.current_state == GameState.PLAYING:
                    pass  # Game is already running

    def draw(self):
        """Draw the game state."""
        self.screen.fill(COLORS["BLACK"])  # Clear screen with black background
        
        if self.current_state == GameState.PLAYING:
            # Draw the grid border
            border_rect = pygame.Rect(
                SCREEN_DIMENSIONS['GRID_OFFSET_X'] - 2,
                SCREEN_DIMENSIONS['GRID_OFFSET_Y'] - 2,
                SCREEN_DIMENSIONS['GRID_WIDTH'] * SCREEN_DIMENSIONS['BLOCK_SIZE'] + 4,
                SCREEN_DIMENSIONS['GRID_HEIGHT'] * SCREEN_DIMENSIONS['BLOCK_SIZE'] + 4
            )
            pygame.draw.rect(self.screen, COLORS["WHITE"], border_rect, 2)
            
            # Draw the grid
            for y, row in enumerate(self.grid):
                for x, cell in enumerate(row):
                    if cell is not None:
                        pygame.draw.rect(
                            self.screen,
                            cell,
                            (SCREEN_DIMENSIONS['GRID_OFFSET_X'] + x * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                             SCREEN_DIMENSIONS['GRID_OFFSET_Y'] + y * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                             SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1,
                             SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1)
                        )
            
            # Draw the current piece
            if self.current_piece:
                for y, row in enumerate(self.current_piece.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            pygame.draw.rect(
                                self.screen,
                                self.current_piece.color,
                                (SCREEN_DIMENSIONS['GRID_OFFSET_X'] + (self.current_piece.x + x) * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                                 SCREEN_DIMENSIONS['GRID_OFFSET_Y'] + (self.current_piece.y + y) * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                                 SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1,
                                 SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1)
                            )
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, COLORS["WHITE"])
            self.screen.blit(score_text, (10, 10))
        
        elif self.current_state == GameState.GAME_OVER:
            # Draw game over screen
            font = pygame.font.Font(None, 48)
            game_over_text = font.render("GAME OVER", True, COLORS["RED"])
            score_text = font.render(f"Final Score: {self.score}", True, COLORS["WHITE"])
            restart_text = font.render("Press ENTER to restart", True, COLORS["WHITE"])
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_DIMENSIONS['WIDTH']//2, SCREEN_DIMENSIONS['HEIGHT']//2 - 50))
            score_rect = score_text.get_rect(center=(SCREEN_DIMENSIONS['WIDTH']//2, SCREEN_DIMENSIONS['HEIGHT']//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_DIMENSIONS['WIDTH']//2, SCREEN_DIMENSIONS['HEIGHT']//2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # Force the display to update
        pygame.display.flip()

    def render_main_menu(self):
        """Render the main menu screen."""
        # Code to display the main menu goes here
        pass

    def render_game_over(self):
        """Render the game over screen."""
        # Code to display the game over screen goes here
        pass

class SpeedGame(BaseGame):
    """Class for the Speed Game mode."""
    def __init__(self, screen, settings, high_scores):
        super().__init__(screen, settings, high_scores)
        self.speed_factor = 1.0
        self.lines_cleared = 0
        self.min_fall_speed = 50  # Minimum fall speed (fastest)

    def clear_lines(self):
        """Clear completed lines and update speed."""
        lines_cleared = super().clear_lines()
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            # Increase speed by 10% for each line cleared
            self.speed_factor *= (0.9 ** lines_cleared)
            # Calculate new fall speed
            new_fall_speed = int(self.FALL_SPEEDS[self.settings.difficulty] * self.speed_factor)
            # Ensure fall speed doesn't go below minimum
            self.fall_speed = max(self.min_fall_speed, new_fall_speed)
        return lines_cleared

    def update(self):
        """Update the game state for the Speed Game mode."""
        super().update()

    def draw(self):
        """Draw the game elements on the screen for the Speed Game mode."""
        super().draw()

class BattleGame(BaseGame):
    """Class for the Battle Game mode."""
    def __init__(self, screen, settings, high_scores):
        super().__init__(screen, settings, high_scores)
        self.opponent_score = 0
        self.opponent_lines_cleared = 0
        self.opponent_level = 1

    def clear_lines(self):
        """Clear completed lines and update opponent score."""
        lines_cleared = super().clear_lines()
        if lines_cleared > 0:
            # Update opponent score based on lines cleared
            self.opponent_lines_cleared += lines_cleared
            self.opponent_score += lines_cleared * 100 * self.opponent_level
            # Level up opponent every 10 lines
            self.opponent_level = (self.opponent_lines_cleared // 10) + 1
        return lines_cleared

    def update(self):
        """Update the game state for the Battle Game mode."""
        super().update()

    def draw(self):
        """Draw the game elements on the screen for the Battle Game mode."""
        super().draw()
        # Draw opponent score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Opponent: {self.opponent_score}", True, COLORS["WHITE"])
        self.screen.blit(score_text, (10, 10))

class TestBaseGame(unittest.TestCase):
    def test_spawn_new_piece(self):
        game = BaseGame(None, MockSettings(), None)
        game.reset_game()
        self.assertIsNotNone(game.current_piece)

    def test_check_collision(self):
        game = BaseGame(None, MockSettings(), None)
        game.reset_game()
        game.current_piece = Tetrimino(0, 0, {'shape': [[1, 1], [1, 1]], 'color': COLORS["YELLOW"]})
        self.assertTrue(game.check_collision())

    def test_lock_piece(self):
        game = BaseGame(None, MockSettings(), None)
        game.reset_game()
        game.current_piece = Tetrimino(0, 0, {'shape': [[1, 1], [1, 1]], 'color': COLORS["YELLOW"]})
        game.lock_piece()
        self.assertIsNotNone(game.grid[0][0])

    def test_clear_lines(self):
        game = BaseGame(None, MockSettings(), None)
        game.reset_game()
        game.grid = [[1 for _ in range(10)] for _ in range(10)]
        lines_cleared = game.clear_lines()
        self.assertEqual(lines_cleared, 10)

if __name__ == '__main__':
    unittest.main()
