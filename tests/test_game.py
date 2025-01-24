"""Tests for game logic."""

import unittest
import pygame
import logging
import sys
from tetris.game import BaseGame, SpeedGame, BattleGame
from tetris.settings import Settings, HighScores
from tetris.constants import (
    GRID_WIDTH, GRID_HEIGHT, SHAPES,
    GameState
)

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   stream=sys.stdout)
logger = logging.getLogger(__name__)

class TestBaseGame(unittest.TestCase):
    """Test cases for the BaseGame class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        logger.info("Initializing Pygame for BaseGame tests")
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    def setUp(self):
        """Set up test cases."""
        logger.info("Setting up BaseGame test case")
        self.settings = Settings()
        self.high_scores = HighScores()
        self.game = BaseGame(self.screen, self.settings, self.high_scores)
        logger.info("BaseGame instance created")

    def test_initialization(self):
        """Test game initialization."""
        logger.info("Testing BaseGame initialization")
        self.assertEqual(len(self.game.grid), GRID_HEIGHT)
        self.assertEqual(len(self.game.grid[0]), GRID_WIDTH)
        self.assertIsNotNone(self.game.current_piece)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.current_state, GameState.MAIN_MENU)
        logger.info("BaseGame initialization test passed")

    def test_reset_game(self):
        """Test game reset functionality."""
        logger.info("Testing game reset")
        # Modify game state
        self.game.score = 1000
        self.game.game_over = True
        self.game.grid[0][0] = SHAPES[0]['color']
        logger.info("Modified game state: score=%d, game_over=%s", 
                   self.game.score, self.game.game_over)
        
        # Reset game
        self.game.reset_game()
        logger.info("Game reset performed")
        
        # Verify reset state
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertTrue(all(cell is None for row in self.game.grid for cell in row))
        self.assertIsNotNone(self.game.current_piece)
        logger.info("Reset state verified")

    def test_piece_movement(self):
        """Test piece movement mechanics."""
        logger.info("Testing piece movement")
        original_x = self.game.current_piece.x
        original_y = self.game.current_piece.y
        logger.info("Initial piece position: (%d, %d)", original_x, original_y)
        
        # Test valid movements
        right_collision = self.game.check_collision(x_offset=1)
        left_collision = self.game.check_collision(x_offset=-1)
        down_collision = self.game.check_collision(y_offset=1)
        logger.info("Collision checks - right: %s, left: %s, down: %s",
                   right_collision, left_collision, down_collision)
        
        self.assertFalse(right_collision)
        self.assertFalse(left_collision)
        self.assertFalse(down_collision)
        
        # Test wall collision
        self.game.current_piece.x = 0
        left_wall_collision = self.game.check_collision(x_offset=-1)
        logger.info("Left wall collision check: %s", left_wall_collision)
        self.assertTrue(left_wall_collision)
        
        # Test floor collision
        self.game.current_piece.y = GRID_HEIGHT - 1
        floor_collision = self.game.check_collision(y_offset=1)
        logger.info("Floor collision check: %s", floor_collision)
        self.assertTrue(floor_collision)

    def test_piece_rotation(self):
        """Test piece rotation mechanics."""
        logger.info("Testing piece rotation")
        # Use I piece for testing
        self.game.current_piece.shape = SHAPES[0]['shape']
        original_shape = [row[:] for row in self.game.current_piece.shape]
        logger.info("Original shape: %s", original_shape)
        
        # Test rotation near center
        self.game.current_piece.x = GRID_WIDTH // 2
        self.game.current_piece.y = GRID_HEIGHT // 2
        self.game.current_piece.rotate()
        logger.info("Shape after center rotation: %s", self.game.current_piece.shape)
        self.assertNotEqual(self.game.current_piece.shape, original_shape)
        
        # Test rotation near wall
        self.game.current_piece.x = 0
        original_shape = [row[:] for row in self.game.current_piece.shape]
        logger.info("Shape before wall rotation: %s", original_shape)
        if self.game.check_collision():
            self.game.current_piece.shape = original_shape
            logger.info("Wall rotation prevented, shape unchanged")
        else:
            logger.info("Shape after wall rotation: %s", self.game.current_piece.shape)

    def test_line_clearing(self):
        """Test line clearing mechanics."""
        logger.info("Testing line clearing")
        # Fill a line
        y = GRID_HEIGHT - 1
        for x in range(GRID_WIDTH):
            self.game.grid[y][x] = SHAPES[0]['color']
        logger.info("Bottom line filled")
        
        lines_cleared = self.game.clear_lines()
        logger.info("Lines cleared: %d", lines_cleared)
        self.assertEqual(lines_cleared, 1)
        self.assertEqual(self.game.score, 100)
        logger.info("Score after clearing: %d", self.game.score)
        
        # Verify line was cleared
        self.assertTrue(all(cell is None for cell in self.game.grid[y]))
        logger.info("Line clear verification passed")
        
        # Test multiple lines
        for y in range(GRID_HEIGHT - 4, GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.game.grid[y][x] = SHAPES[0]['color']
        logger.info("Multiple lines filled")
        
        lines_cleared = self.game.clear_lines()
        logger.info("Multiple lines cleared: %d", lines_cleared)
        self.assertEqual(lines_cleared, 4)
        # Score should be: previous 100 + (100 * 4) * 4 = 1700
        self.assertEqual(self.game.score, 1700)
        logger.info("Final score: %d", self.game.score)

    def test_game_over_condition(self):
        """Test game over condition."""
        logger.info("Testing game over condition")
        
        # Test game over by collision with existing blocks
        for x in range(GRID_WIDTH):
            self.game.grid[0][x] = SHAPES[0]['color']
        logger.info("Top row filled")
        
        self.game.spawn_new_piece()
        self.assertTrue(self.game.check_collision())
        logger.info("New piece collides with filled top row")
        
        # Test game over by piece above grid
        self.game.reset_game()
        self.game.current_piece.y = -2  # Force piece above grid
        logger.info("Piece positioned above grid at y=%d", self.game.current_piece.y)
        
        self.game.lock_piece()
        self.assertTrue(self.game.game_over)
        logger.info("Game over triggered by piece above grid")

    def test_piece_movement(self):
        """Test piece movement mechanics."""
        logger.info("Testing piece movement")
        original_x = self.game.current_piece.x
        original_y = self.game.current_piece.y
        logger.info("Initial piece position: (%d, %d)", original_x, original_y)
        
        # Test valid movements
        right_collision = self.game.check_collision(x_offset=1)
        left_collision = self.game.check_collision(x_offset=-1)
        down_collision = self.game.check_collision(y_offset=1)
        logger.info("Collision checks - right: %s, left: %s, down: %s",
                   right_collision, left_collision, down_collision)
        
        self.assertFalse(right_collision)
        self.assertFalse(left_collision)
        self.assertFalse(down_collision)
        
        # Test wall collision
        self.game.current_piece.x = 0
        left_wall_collision = self.game.check_collision(x_offset=-1)
        logger.info("Left wall collision check: %s", left_wall_collision)
        self.assertTrue(left_wall_collision)
        
        # Test floor collision
        self.game.current_piece.y = GRID_HEIGHT - 1
        floor_collision = self.game.check_collision(y_offset=1)
        logger.info("Floor collision check: %s", floor_collision)
        self.assertTrue(floor_collision)

    def test_piece_rotation(self):
        """Test piece rotation mechanics."""
        logger.info("Testing piece rotation")
        # Use I piece for testing
        self.game.current_piece.shape = SHAPES[0]['shape']
        original_shape = [row[:] for row in self.game.current_piece.shape]
        logger.info("Original shape: %s", original_shape)
        
        # Test rotation near center
        self.game.current_piece.x = GRID_WIDTH // 2
        self.game.current_piece.y = GRID_HEIGHT // 2
        self.game.current_piece.rotate()
        logger.info("Shape after center rotation: %s", self.game.current_piece.shape)
        self.assertNotEqual(self.game.current_piece.shape, original_shape)
        
        # Test rotation near wall
        self.game.current_piece.x = 0
        original_shape = [row[:] for row in self.game.current_piece.shape]
        logger.info("Shape before wall rotation: %s", original_shape)
        if self.game.check_collision():
            self.game.current_piece.shape = original_shape
            logger.info("Wall rotation prevented, shape unchanged")
        else:
            logger.info("Shape after wall rotation: %s", self.game.current_piece.shape)

    def test_line_clearing(self):
        """Test line clearing mechanics."""
        logger.info("Testing line clearing")
        # Fill a line
        y = GRID_HEIGHT - 1
        for x in range(GRID_WIDTH):
            self.game.grid[y][x] = SHAPES[0]['color']
        logger.info("Bottom line filled")
        
        lines_cleared = self.game.clear_lines()
        logger.info("Lines cleared: %d", lines_cleared)
        self.assertEqual(lines_cleared, 1)
        self.assertEqual(self.game.score, 100)
        logger.info("Score after clearing: %d", self.game.score)
        
        # Verify line was cleared
        self.assertTrue(all(cell is None for cell in self.game.grid[y]))
        logger.info("Line clear verification passed")
        
        # Test multiple lines
        for y in range(GRID_HEIGHT - 4, GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.game.grid[y][x] = SHAPES[0]['color']
        logger.info("Multiple lines filled")
        
        lines_cleared = self.game.clear_lines()
        logger.info("Multiple lines cleared: %d", lines_cleared)
        self.assertEqual(lines_cleared, 4)
        # Score should be: previous 100 + (100 * 4) * 4 = 1700
        self.assertEqual(self.game.score, 1700)
        logger.info("Final score: %d", self.game.score)

class TestSpeedGame(unittest.TestCase):
    """Test cases for the SpeedGame class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        logger.info("Initializing Pygame for SpeedGame tests")
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    def setUp(self):
        """Set up test cases."""
        logger.info("Setting up SpeedGame test case")
        self.settings = Settings()
        self.high_scores = HighScores()
        self.game = SpeedGame(self.screen, self.settings, self.high_scores)
        logger.info("SpeedGame instance created")

    def test_speed_increase(self):
        """Test speed increase mechanics."""
        logger.info("Testing speed increase")
        initial_speed = self.game.fall_speed
        logger.info("Initial fall speed: %f", initial_speed)
        
        # Clear enough lines to trigger speed increase
        for i in range(self.game.lines_for_speed_up):
            y = GRID_HEIGHT - 1
            for x in range(GRID_WIDTH):
                self.game.grid[y][x] = SHAPES[0]['color']
            lines_cleared = self.game.clear_lines()
            logger.info("Cleared line %d/%d", i + 1, self.game.lines_for_speed_up)
        
        logger.info("New fall speed: %f", self.game.fall_speed)
        self.assertLess(self.game.fall_speed, initial_speed)
        self.assertGreaterEqual(self.game.fall_speed, self.game.min_fall_speed)

    def test_minimum_speed_limit(self):
        """Test minimum speed limit."""
        logger.info("Testing minimum speed limit")
        # Force multiple speed increases
        for i in range(20):
            y = GRID_HEIGHT - 1
            for x in range(GRID_WIDTH):
                self.game.grid[y][x] = SHAPES[0]['color']
            self.game.clear_lines()
            logger.info("Speed after %d lines: %f", i + 1, self.game.fall_speed)
        
        logger.info("Final fall speed: %f", self.game.fall_speed)
        self.assertGreaterEqual(self.game.fall_speed, self.game.min_fall_speed)

class TestBattleGame(unittest.TestCase):
    """Test cases for the BattleGame class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        logger.info("Initializing Pygame for BattleGame tests")
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    def setUp(self):
        """Set up test cases."""
        logger.info("Setting up BattleGame test case")
        self.settings = Settings()
        self.high_scores = HighScores()
        self.game = BattleGame(self.screen, self.settings, self.high_scores)
        logger.info("BattleGame instance created")

    def test_initialization(self):
        """Test battle mode initialization."""
        logger.info("Testing BattleGame initialization")
        # Test player 2 grid
        self.assertIsNotNone(self.game.player2_grid)
        self.assertEqual(len(self.game.player2_grid), GRID_HEIGHT)
        self.assertEqual(len(self.game.player2_grid[0]), GRID_WIDTH)
        
        # Test player 2 piece
        self.assertIsNotNone(self.game.player2_piece)
        self.assertIsInstance(self.game.player2_piece, Tetrimino)
        
        # Test scores and timers
        self.assertEqual(self.game.player2_score, 0)
        self.assertEqual(self.game.ai_move_timer, 0)
        self.assertEqual(self.game.ai_move_delay, 200)
        logger.info("BattleGame initialization test passed")

    def test_player2_piece_movement(self):
        """Test player 2 piece movement."""
        logger.info("Testing player 2 piece movement")
        original_x = self.game.player2_piece.x
        original_y = self.game.player2_piece.y
        logger.info("Initial position: (%d, %d)", original_x, original_y)
        
        # Test valid movements
        self.assertFalse(self.game.check_player2_collision(x_offset=1))
        self.assertFalse(self.game.check_player2_collision(x_offset=-1))
        self.assertFalse(self.game.check_player2_collision(y_offset=1))
        logger.info("Valid movement checks passed")
        
        # Test wall collision
        self.game.player2_piece.x = 0
        self.assertTrue(self.game.check_player2_collision(x_offset=-1))
        logger.info("Wall collision check passed")
        
        # Test floor collision
        self.game.player2_piece.y = GRID_HEIGHT - 1
        self.assertTrue(self.game.check_player2_collision(y_offset=1))
        logger.info("Floor collision check passed")

    def test_player2_line_clearing(self):
        """Test player 2 line clearing."""
        logger.info("Testing player 2 line clearing")
        # Fill a line
        y = GRID_HEIGHT - 1
        for x in range(GRID_WIDTH):
            self.game.player2_grid[y][x] = SHAPES[0]['color']
        logger.info("Bottom line filled")
        
        # Clear lines and check score
        self.game.clear_player2_lines()
        self.assertEqual(self.game.player2_score, 100)
        logger.info("Single line clear score: %d", self.game.player2_score)
        
        # Fill multiple lines
        for y in range(GRID_HEIGHT - 4, GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.game.player2_grid[y][x] = SHAPES[0]['color']
        logger.info("Multiple lines filled")
        
        # Clear lines and check score
        self.game.clear_player2_lines()
        # Score should be: previous 100 + (100 * 4) * 4 = 1700
        self.assertEqual(self.game.player2_score, 1700)
        logger.info("Multiple line clear score: %d", self.game.player2_score)

    def test_ai_update(self):
        """Test AI update mechanics."""
        logger.info("Testing AI update")
        initial_timer = self.game.ai_move_timer
        logger.info("Initial AI timer: %d", initial_timer)
        
        # Store initial piece position
        initial_x = self.game.player2_piece.x
        initial_y = self.game.player2_piece.y
        logger.info("Initial piece position: (%d, %d)", initial_x, initial_y)
        
        # Force AI update
        self.game.clock.tick(60)  # Simulate time passing
        self.game.update_ai()
        
        # Verify timer was updated
        self.assertNotEqual(self.game.ai_move_timer, initial_timer)
        logger.info("New AI timer: %d", self.game.ai_move_timer)
        
        # Force multiple updates to ensure piece moves
        for _ in range(10):
            self.game.clock.tick(60)
            self.game.update_ai()
        
        # Verify piece has moved
        current_x = self.game.player2_piece.x
        current_y = self.game.player2_piece.y
        logger.info("Final piece position: (%d, %d)", current_x, current_y)
        self.assertTrue(current_x != initial_x or current_y != initial_y)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        logger.info("Cleaning up Pygame environment")
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
