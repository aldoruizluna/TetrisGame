"""Tests for game logic."""

import unittest
import pygame
import logging
import sys
from tetris.game import BaseGame, SpeedGame, BattleGame
from tetris.settings import Settings, HighScores
from tetris.constants import (
    SCREEN_DIMENSIONS,
    COLORS,
    SHAPES,
    GameState
)

# Configure logging
logging.basicConfig(level=logging.DEBUG,
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
        cls.screen = pygame.display.set_mode((SCREEN_DIMENSIONS['WIDTH'], SCREEN_DIMENSIONS['HEIGHT']))

    def setUp(self):
        """Set up test cases."""
        logger.info("Setting up BaseGame test case")
        self.settings = Settings()
        self.high_scores = HighScores()
        self.game = BaseGame(self.screen, self.settings, self.high_scores)

    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(len(self.game.grid), SCREEN_DIMENSIONS['GRID_HEIGHT'])
        self.assertEqual(len(self.game.grid[0]), SCREEN_DIMENSIONS['GRID_WIDTH'])
        self.assertIsNotNone(self.game.current_piece)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.current_state, GameState.PLAYING)
        self.assertEqual(self.game.fall_speed, BaseGame.FALL_SPEEDS[self.settings.difficulty])

    def test_reset_game(self):
        """Test game reset functionality."""
        # Modify game state
        self.game.score = 1000
        self.game.game_over = True
        self.game.grid[0][0] = COLORS["BLUE"]
        
        # Reset game
        self.game.reset_game()
        
        # Verify reset state
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertTrue(all(cell is None for row in self.game.grid for cell in row))
        self.assertIsNotNone(self.game.current_piece)
        self.assertEqual(self.game.fall_speed, BaseGame.FALL_SPEEDS[self.settings.difficulty])

    def test_piece_movement(self):
        """Test piece movement mechanics."""
        original_x = self.game.current_piece.x
        original_y = self.game.current_piece.y
        
        # Test valid movements
        self.assertFalse(self.game.check_collision(x_offset=1))
        self.assertFalse(self.game.check_collision(x_offset=-1))
        self.assertFalse(self.game.check_collision(y_offset=1))
        
        # Test wall collision
        self.game.current_piece.x = 0
        self.assertTrue(self.game.check_collision(x_offset=-1))
        
        # Test floor collision
        self.game.current_piece.y = SCREEN_DIMENSIONS['GRID_HEIGHT'] - 1
        self.assertTrue(self.game.check_collision(y_offset=1))

    def test_piece_rotation(self):
        """Test piece rotation mechanics."""
        original_shape = [row[:] for row in self.game.current_piece.shape]
        
        # Test rotation
        self.game.current_piece.rotate()
        rotated_shape = self.game.current_piece.shape
        
        # Verify shape changed
        self.assertNotEqual(original_shape, rotated_shape)
        
        # Verify dimensions maintained
        self.assertEqual(len(original_shape), len(rotated_shape[0]))
        self.assertEqual(len(original_shape[0]), len(rotated_shape))

    def test_line_clearing(self):
        """Test line clearing mechanics."""
        # Fill a line
        row_index = SCREEN_DIMENSIONS['GRID_HEIGHT'] - 1
        for col in range(SCREEN_DIMENSIONS['GRID_WIDTH']):
            self.game.grid[row_index][col] = COLORS["BLUE"]
        
        # Clear lines
        lines_cleared = self.game.clear_lines()
        
        # Verify line was cleared
        self.assertEqual(lines_cleared, 1)
        self.assertTrue(all(cell is None for cell in self.game.grid[0]))
        
        # Verify score update
        self.assertEqual(self.game.score, 100)

    def test_game_over_condition(self):
        """Test game over conditions."""
        # Fill top row to force game over
        for col in range(SCREEN_DIMENSIONS['GRID_WIDTH']):
            self.game.grid[0][col] = COLORS["BLUE"]
        
        # Spawn new piece
        self.game.spawn_new_piece()
        
        # Verify game over
        self.assertTrue(self.game.game_over)

class TestSpeedGame(unittest.TestCase):
    """Test cases for the SpeedGame class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        pygame.init()
        cls.screen = pygame.display.set_mode((SCREEN_DIMENSIONS['WIDTH'], SCREEN_DIMENSIONS['HEIGHT']))

    def setUp(self):
        """Set up test cases."""
        self.settings = Settings()
        self.high_scores = HighScores()
        self.game = SpeedGame(self.screen, self.settings, self.high_scores)

    def test_speed_increase(self):
        """Test speed increase mechanics."""
        initial_speed = self.game.fall_speed
        
        # Clear multiple lines to trigger significant speed increase
        for _ in range(3):  # Clear 3 lines
            row_index = SCREEN_DIMENSIONS['GRID_HEIGHT'] - 1
            for col in range(SCREEN_DIMENSIONS['GRID_WIDTH']):
                self.game.grid[row_index][col] = COLORS["BLUE"]
            self.game.clear_lines()
        
        # The speed should have increased (fall_speed decreased)
        self.assertLess(self.game.fall_speed, initial_speed)

    def test_minimum_speed_limit(self):
        """Test minimum speed limit."""
        # Clear many lines to reach minimum speed
        for _ in range(20):  # Clear 20 lines
            row_index = SCREEN_DIMENSIONS['GRID_HEIGHT'] - 1
            for col in range(SCREEN_DIMENSIONS['GRID_WIDTH']):
                self.game.grid[row_index][col] = COLORS["BLUE"]
            self.game.clear_lines()
        
        # Record speed after many lines
        speed_after_many_lines = self.game.fall_speed
        
        # Clear one more line
        row_index = SCREEN_DIMENSIONS['GRID_HEIGHT'] - 1
        for col in range(SCREEN_DIMENSIONS['GRID_WIDTH']):
            self.game.grid[row_index][col] = COLORS["BLUE"]
        self.game.clear_lines()
        
        # Speed should not decrease further (should stay at minimum)
        self.assertEqual(self.game.fall_speed, speed_after_many_lines)

class TestBattleGame(unittest.TestCase):
    """Test cases for the BattleGame class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        pygame.init()
        cls.screen = pygame.display.set_mode((SCREEN_DIMENSIONS['WIDTH'], SCREEN_DIMENSIONS['HEIGHT']))

    def setUp(self):
        """Set up test cases."""
        self.settings = Settings()
        self.high_scores = HighScores()
        self.game = BattleGame(self.screen, self.settings, self.high_scores)

    def test_initialization(self):
        """Test battle mode initialization."""
        self.assertEqual(self.game.opponent_score, 0)
        self.assertIsNotNone(self.game.current_piece)

    def test_opponent_scoring(self):
        """Test opponent scoring mechanics."""
        initial_score = self.game.opponent_score
        
        # Clear a line
        row_index = SCREEN_DIMENSIONS['GRID_HEIGHT'] - 1
        for col in range(SCREEN_DIMENSIONS['GRID_WIDTH']):
            self.game.grid[row_index][col] = COLORS["BLUE"]
        
        self.game.clear_lines()
        self.assertGreater(self.game.opponent_score, initial_score)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
