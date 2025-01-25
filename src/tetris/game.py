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
    SHAPES,
    COLORS, GameState
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
        self.current_state = GameState.PLAYING
        self.spawn_new_piece()

    def spawn_new_piece(self):
        """Create and spawn a new tetrimino."""
        if self.game_over:
            self.current_state = GameState.GAME_OVER
            return

        # Get a random shape
        shape_info = random.choice(SHAPES)
        
        # Calculate starting position
        start_x = SCREEN_DIMENSIONS['GRID_WIDTH'] // 2 - len(shape_info['shape'][0]) // 2
        start_y = 0
        
        # Create the new piece
        self.current_piece = Tetrimino(start_x, start_y, shape_info)
        
        # Check if the new piece can be placed
        if self.check_collision():
            self.game_over = True
            self.current_state = GameState.GAME_OVER

    def check_collision(self, x_offset=0, y_offset=0, shape=None):
        """Check if the current piece collides with anything."""
        if not self.current_piece:
            return False

        # Use provided shape or current piece's shape
        piece_shape = shape if shape is not None else self.current_piece.shape

        # Check each cell of the piece
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
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
                        self.current_state = GameState.GAME_OVER
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
            self.current_state = GameState.GAME_OVER

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
        if self.current_state == GameState.GAME_OVER:
            return

        if not self.current_piece:
            self.spawn_new_piece()
            if self.check_collision():
                self.game_over = True
                self.current_state = GameState.GAME_OVER
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
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return GameState.QUIT
                
            if event.type == pygame.KEYDOWN:
                if self.current_state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN:  # Enter key to restart
                        self.reset_game()
                        return GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:  # ESC key for main menu
                        return GameState.MAIN_MENU
                    elif event.key == pygame.K_q:  # Q key to quit
                        return GameState.QUIT
                    continue  # Ignore other keys in game over state
                    
                if event.key == pygame.K_ESCAPE:
                    return GameState.PAUSE
                    
                if event.key == pygame.K_LEFT:
                    if not self.check_collision(x_offset=-1):
                        self.current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    if not self.check_collision(x_offset=1):
                        self.current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    if not self.check_collision(y_offset=1):
                        self.current_piece.move(0, 1)
                elif event.key == pygame.K_UP:
                    # Store current shape
                    current_shape = self.current_piece.shape
                    # Rotate the piece
                    self.current_piece.rotate()
                    # If rotation causes collision, revert back
                    if self.check_collision():
                        self.current_piece.shape = current_shape
                elif event.key == pygame.K_SPACE:
                    # Hard drop
                    while not self.check_collision(y_offset=1):
                        self.current_piece.move(0, 1)
                    self.lock_piece()
        
        return None

    def draw(self):
        """Draw the game state."""
        self.clear_screen()
        self.draw_grid()
        self.draw_filled_blocks()
        
        if self.current_state == GameState.PLAYING:
            self.draw_current_piece()
            self.draw_score()
        elif self.current_state == GameState.GAME_OVER:
            self.render_game_over()
        
        if pygame.get_init():
            pygame.display.flip()

    def clear_screen(self):
        """Clear the screen with black color."""
        self.screen.fill(COLORS["BLACK"])

    def draw_grid(self):
        """Draw the grid border and lines."""
        # Draw grid border
        border_rect = pygame.Rect(
            SCREEN_DIMENSIONS['GRID_OFFSET_X'] - 2,
            SCREEN_DIMENSIONS['GRID_OFFSET_Y'] - 2,
            SCREEN_DIMENSIONS['GRID_WIDTH'] * SCREEN_DIMENSIONS['BLOCK_SIZE'] + 4,
            SCREEN_DIMENSIONS['GRID_HEIGHT'] * SCREEN_DIMENSIONS['BLOCK_SIZE'] + 4
        )
        pygame.draw.rect(self.screen, COLORS["WHITE"], border_rect, 2)
        
        # Draw grid lines
        for x in range(SCREEN_DIMENSIONS['GRID_WIDTH'] + 1):
            pygame.draw.line(
                self.screen,
                COLORS["GRAY"],
                (SCREEN_DIMENSIONS['GRID_OFFSET_X'] + x * SCREEN_DIMENSIONS['BLOCK_SIZE'], SCREEN_DIMENSIONS['GRID_OFFSET_Y']),
                (SCREEN_DIMENSIONS['GRID_OFFSET_X'] + x * SCREEN_DIMENSIONS['BLOCK_SIZE'], 
                 SCREEN_DIMENSIONS['GRID_OFFSET_Y'] + SCREEN_DIMENSIONS['GRID_HEIGHT'] * SCREEN_DIMENSIONS['BLOCK_SIZE'])
            )
        for y in range(SCREEN_DIMENSIONS['GRID_HEIGHT'] + 1):
            pygame.draw.line(
                self.screen,
                COLORS["GRAY"],
                (SCREEN_DIMENSIONS['GRID_OFFSET_X'], SCREEN_DIMENSIONS['GRID_OFFSET_Y'] + y * SCREEN_DIMENSIONS['BLOCK_SIZE']),
                (SCREEN_DIMENSIONS['GRID_OFFSET_X'] + SCREEN_DIMENSIONS['GRID_WIDTH'] * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                 SCREEN_DIMENSIONS['GRID_OFFSET_Y'] + y * SCREEN_DIMENSIONS['BLOCK_SIZE'])
            )

    def draw_filled_blocks(self):
        """Draw filled blocks on the grid."""
        for y in range(SCREEN_DIMENSIONS['GRID_HEIGHT']):
            for x in range(SCREEN_DIMENSIONS['GRID_WIDTH']):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        self.grid[y][x],
                        (SCREEN_DIMENSIONS['GRID_OFFSET_X'] + x * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                         SCREEN_DIMENSIONS['GRID_OFFSET_Y'] + y * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                         SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1,
                         SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1)
                    )

    def draw_current_piece(self):
        """Draw the current piece on the grid."""
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

    def draw_score(self):
        """Draw the current score on the screen."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, COLORS["WHITE"])
        self.screen.blit(score_text, (10, 10))

    def render_game_over(self):
        """Render the game over screen."""
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
        
        if pygame.get_init():
            pygame.display.flip()

    def render_main_menu(self):
        """Render the main menu screen."""
        # Code to display the main menu goes here
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
        if pygame.get_init():
            pygame.display.flip()

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
