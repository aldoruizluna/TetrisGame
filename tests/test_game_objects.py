"""Tests for game objects."""

import unittest
import logging
import sys
from tetris.game_objects import Tetrimino
from tetris.constants import SHAPES

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   stream=sys.stdout)
logger = logging.getLogger(__name__)

class TestTetrimino(unittest.TestCase):
    """Test cases for the Tetrimino class."""

    def setUp(self):
        """Set up test cases."""
        logger.info("Setting up Tetrimino test case")
        # Test with I piece (horizontal line)
        self.i_piece = Tetrimino(0, 0, SHAPES[0])  # I piece
        # Test with O piece (square)
        self.o_piece = Tetrimino(0, 0, SHAPES[1])  # O piece
        # Test with T piece
        self.t_piece = Tetrimino(0, 0, SHAPES[6])  # T piece
        logger.info("Test pieces created: I, O, and T pieces")

    def test_initialization(self):
        """Test tetrimino initialization."""
        logger.info("Testing Tetrimino initialization")
        self.assertEqual(self.i_piece.x, 0)
        self.assertEqual(self.i_piece.y, 0)
        self.assertEqual(self.i_piece.shape, [[1, 1, 1, 1]])
        self.assertEqual(self.i_piece.color, SHAPES[0]['color'])
        logger.info("Tetrimino initialization test passed")

    def test_rotation_i_piece(self):
        """Test I piece rotation."""
        logger.info("Testing I piece rotation")
        # Initial shape (horizontal)
        logger.info("Initial I piece shape: %s", self.i_piece.shape)
        self.assertEqual(self.i_piece.shape, [[1, 1, 1, 1]])
        
        # First rotation (vertical)
        self.i_piece.rotate()
        logger.info("After first rotation: %s", self.i_piece.shape)
        self.assertEqual(self.i_piece.shape, [[1], [1], [1], [1]])
        
        # Second rotation (horizontal)
        self.i_piece.rotate()
        logger.info("After second rotation: %s", self.i_piece.shape)
        self.assertEqual(self.i_piece.shape, [[1, 1, 1, 1]])
        logger.info("I piece rotation test passed")

    def test_rotation_o_piece(self):
        """Test O piece rotation (should remain unchanged)."""
        logger.info("Testing O piece rotation")
        original_shape = [row[:] for row in self.o_piece.shape]
        logger.info("Original O piece shape: %s", original_shape)
        
        # Rotation shouldn't change O piece
        self.o_piece.rotate()
        logger.info("After rotation: %s", self.o_piece.shape)
        self.assertEqual(self.o_piece.shape, original_shape)
        
        # Multiple rotations should still not change it
        for i in range(3):
            self.o_piece.rotate()
            logger.info("After rotation %d: %s", i + 2, self.o_piece.shape)
        self.assertEqual(self.o_piece.shape, original_shape)
        logger.info("O piece rotation test passed")

    def test_rotation_t_piece(self):
        """Test T piece rotation (should have 4 unique states)."""
        logger.info("Testing T piece rotation")
        shapes = []
        
        # Collect all 4 rotations
        for i in range(4):
            shapes.append([row[:] for row in self.t_piece.shape])
            logger.info("T piece shape at rotation %d: %s", i, self.t_piece.shape)
            self.t_piece.rotate()
        
        # Verify all 4 states are unique
        unique_shapes = len(set(str(shape) for shape in shapes))
        logger.info("Number of unique shapes: %d", unique_shapes)
        self.assertEqual(unique_shapes, 4)
        
        # Verify it returns to original position after 4 rotations
        logger.info("Final shape after full rotation: %s", self.t_piece.shape)
        self.assertEqual(self.t_piece.shape, shapes[0])
        logger.info("T piece rotation test passed")

    def test_movement(self):
        """Test tetrimino movement."""
        logger.info("Testing Tetrimino movement")
        initial_x = self.i_piece.x
        initial_y = self.i_piece.y
        logger.info("Initial position: (%d, %d)", initial_x, initial_y)
        
        # Test right movement
        self.i_piece.move(1, 0)
        logger.info("After right movement: (%d, %d)", self.i_piece.x, self.i_piece.y)
        self.assertEqual(self.i_piece.x, initial_x + 1)
        self.assertEqual(self.i_piece.y, initial_y)
        
        # Test left movement
        self.i_piece.move(-1, 0)
        logger.info("After left movement: (%d, %d)", self.i_piece.x, self.i_piece.y)
        self.assertEqual(self.i_piece.x, initial_x)
        self.assertEqual(self.i_piece.y, initial_y)
        
        # Test downward movement
        self.i_piece.move(0, 1)
        logger.info("After downward movement: (%d, %d)", self.i_piece.x, self.i_piece.y)
        self.assertEqual(self.i_piece.x, initial_x)
        self.assertEqual(self.i_piece.y, initial_y + 1)
        
        # Test diagonal movement
        self.i_piece.move(1, 1)
        logger.info("After diagonal movement: (%d, %d)", self.i_piece.x, self.i_piece.y)
        self.assertEqual(self.i_piece.x, initial_x + 1)
        self.assertEqual(self.i_piece.y, initial_y + 2)
        logger.info("Movement test passed")

    def test_all_shapes(self):
        """Test initialization of all shape types."""
        logger.info("Testing initialization of all shapes")
        for i, shape_data in enumerate(SHAPES):
            logger.info("Testing shape %d", i)
            piece = Tetrimino(0, 0, shape_data)
            self.assertEqual(piece.shape, shape_data['shape'])
            self.assertEqual(piece.color, shape_data['color'])
            logger.info("Shape %d test passed", i)
        logger.info("All shapes test passed")

if __name__ == '__main__':
    unittest.main()
