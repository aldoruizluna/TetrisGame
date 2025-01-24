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
from .game_objects import Tetrimino  # Import the Tetrimino class for game pieces

# Initialize logger
logger = logging.getLogger(__name__)

class MockSettings:
    """Mock settings class for testing purposes."""
    def __init__(self, difficulty="Easy"):
        self.difficulty = difficulty

class BaseGame:
    """Base class for all game modes."""
    
    def __init__(self, screen, settings, high_scores):
        """Initialize the game."""
        # Set the screen for rendering
        self.screen = screen  
        # Store game settings
        self.settings = settings  
        # Store high scores
        self.high_scores = high_scores  
        # Set the window title
        pygame.display.set_caption("Tetris")  
        # Create a clock to manage frame rate
        self.clock = pygame.time.Clock()  
        # Initialize game state
        self.current_state = GameState.MAIN_MENU  
        # Flag to keep the game running
        self.running = True  
        # Call method to reset the game state
        self.reset_game()  

    def reset_game(self):
        """Reset the game state."""
        # Create a grid for the game based on GRID_WIDTH and GRID_HEIGHT
        self.grid = [[None for _ in range(SCREEN_DIMENSIONS['GRID_WIDTH'])] for _ in range(SCREEN_DIMENSIONS['GRID_HEIGHT'])]
        # No current piece at the start
        self.current_piece = None  
        # Timer for piece falling
        self.fall_time = 0  
        # Default fall speed in milliseconds
        self.fall_speed = SCREEN_DIMENSIONS['BLOCK_SIZE']  
        # Adjust fall speed based on difficulty settings
        if self.settings.difficulty == "Easy":
            self.fall_speed = SCREEN_DIMENSIONS['BLOCK_SIZE'] * 6
        elif self.settings.difficulty == "Hard":
            self.fall_speed = SCREEN_DIMENSIONS['BLOCK_SIZE'] * 4
        # Game is not over initially
        self.game_over = False  
        # Initialize score to zero
        self.score = 0  
        # Spawn the first piece
        self.spawn_new_piece()  
        print("Game reset: current_piece initialized.")

    def spawn_new_piece(self):
        """Create and spawn a new tetrimino."""
        # Calculate starting position for the new piece
        start_x = SCREEN_DIMENSIONS['GRID_WIDTH'] // 2 - 1  # Center horizontally
        start_y = 0  # Start at the top of the grid
        # Create a new Tetrimino with a random shape
        shape_info = random.choice(SHAPES)
        shape = shape_info['shape']
        color = shape_info['color']
        self.current_piece = Tetrimino(start_x, start_y, {'shape': shape, 'color': color})

    def check_collision(self, x_offset=0, y_offset=0, shape=None):
        """Check if the current piece collides with anything."""
        # Use current piece shape if none provided
        if shape is None:
            shape = self.current_piece.shape  

        # Check each cell in the piece's shape for collisions
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:  # If the cell is part of the piece
                    # Calculate absolute position of the cell
                    abs_x = self.current_piece.x + x + x_offset
                    abs_y = self.current_piece.y + y + y_offset

                    # Check for collisions with walls or existing blocks
                    if (abs_x < 0 or abs_x >= SCREEN_DIMENSIONS['WIDTH'] or 
                        abs_y >= SCREEN_DIMENSIONS['HEIGHT'] or 
                        (abs_y >= 0 and self.grid[abs_y][abs_x] is not None)):
                        return True  # Collision detected
        return False  # No collision detected

    def lock_piece(self):
        """Lock the current piece in place."""
        # Iterate over each cell in the piece's shape
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:  # If the cell is part of the piece
                    abs_y = self.current_piece.y + y
                    if abs_y < 0:  # If any part of the piece is above the grid
                        self.game_over = True  # Set game over flag
                        return  # Exit the method
                    # Lock the piece in the grid
                    self.grid[abs_y][self.current_piece.x + x] = self.current_piece.color  

        # Clear any completed lines
        self.clear_lines()  
        # Spawn a new piece
        self.spawn_new_piece()  
        # Check if the new piece collides immediately
        if self.check_collision():  
            self.game_over = True  # Set game over flag

    def clear_lines(self):
        """Clear completed lines and update score."""
        # Initialize lines cleared counter
        lines_cleared = 0  
        # Start from the bottom of the grid
        y = SCREEN_DIMENSIONS['HEIGHT'] - 1  
        while y >= 0:
            # Check if the line is filled
            if all(cell is not None for cell in self.grid[y]):  
                # Increment lines cleared counter
                lines_cleared += 1  
                # Move lines down
                for move_y in range(y, 0, -1):  
                    self.grid[move_y] = self.grid[move_y - 1][:]
                # Clear the top line
                self.grid[0] = [None] * SCREEN_DIMENSIONS['WIDTH']  
            else:
                # Move up to the next line
                y -= 1  

        # Update score based on lines cleared
        if lines_cleared > 0:
            self.score += lines_cleared * 100 * lines_cleared  
        return lines_cleared  # Return the number of lines cleared

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

    def update(self):
        """Update game state."""
        # Update game logic, piece movement, etc.
        if self.current_state == GameState.PLAYING:
            self.fall_time += self.clock.get_rawtime()
            if self.fall_time >= self.fall_speed:
                self.fall_time = 0
                if not self.check_collision(y_offset=1):
                    self.current_piece.move(0, 1)
                else:
                    self.lock_piece()

    def draw(self):
        """Draw the game state."""
        self.screen.fill((0, 0, 0))  # Clear the screen
        if self.current_state == GameState.MAIN_MENU:
            self.render_main_menu()
        elif self.current_state == GameState.GAME_OVER:
            self.render_game_over()
        elif self.current_state == GameState.PLAYING:
            # Draw the grid
            for y, row in enumerate(self.grid):
                for x, cell in enumerate(row):
                    if cell is not None:
                        pygame.draw.rect(self.screen, cell,
                                       (SCREEN_DIMENSIONS['GRID_OFFSET_X'] + x * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                                        SCREEN_DIMENSIONS['GRID_OFFSET_Y'] + y * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                                        SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1, SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1))
            # Draw the current piece
            if self.current_piece:
                for y, row in enumerate(self.current_piece.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            pygame.draw.rect(self.screen, self.current_piece.color,
                                           (SCREEN_DIMENSIONS['GRID_OFFSET_X'] + (self.current_piece.x + x) * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                                            SCREEN_DIMENSIONS['GRID_OFFSET_Y'] + (self.current_piece.y + y) * SCREEN_DIMENSIONS['BLOCK_SIZE'],
                                            SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1, SCREEN_DIMENSIONS['BLOCK_SIZE'] - 1))
        pygame.display.flip()  # Update the display
        print(f"Current state: {self.current_state}, current_piece: {self.current_piece}")

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
        self.speed_factor = 1.0  # Example speed factor to control game speed

    def update(self):
        """Update the game state for the Speed Game mode."""
        # Implement speed-specific logic here
        pass

    def draw(self):
        """Draw the game elements on the screen for the Speed Game mode."""
        # Implement drawing logic here
        pass

class BattleGame(BaseGame):
    """Class for the Battle Game mode."""
    def __init__(self, screen, settings, high_scores):
        super().__init__(screen, settings, high_scores)
        self.opponent_score = 0  # Example opponent score

    def update(self):
        """Update the game state for the Battle Game mode."""
        # Implement battle-specific logic here
        pass

    def draw(self):
        """Draw the game elements on the screen for the Battle Game mode."""
        # Implement drawing logic here
        pass

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
