"""Module for Tetrimino (Tetris piece) handling."""

class Tetrimino:
    """Class representing a Tetris piece (Tetrimino)."""
    
    def __init__(self, x, y, shape_info):
        """Initialize a new Tetrimino.
        
        Args:
            x (int): Initial x position
            y (int): Initial y position
            shape_info (dict): Dictionary containing 'shape' and 'color'
        """
        self.x = x
        self.y = y
        self.shape = shape_info['shape']
        self.color = shape_info['color']
        print(f"Created new Tetrimino at ({x}, {y}) with shape: {self.shape}")

    def move(self, dx, dy):
        """Move the piece by the given delta.
        
        Args:
            dx (int): Change in x position
            dy (int): Change in y position
        """
        self.x += dx
        self.y += dy
        print(f"Moved Tetrimino to ({self.x}, {self.y})")

    def rotate(self):
        """Rotate the piece clockwise."""
        self.shape = list(zip(*self.shape[::-1]))
        self.shape = [list(row) for row in self.shape]
        print("Rotated Tetrimino")
