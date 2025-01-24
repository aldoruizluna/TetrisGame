"""Module containing the core game objects."""

class Tetrimino:
    """Class representing a Tetris piece."""
    
    def __init__(self, x, y, shape_data):
        """Initialize a new Tetrimino.
        
        Args:
            x (int): Initial x position
            y (int): Initial y position
            shape_data (dict): Dictionary containing 'shape' and 'color' keys
        """
        self.x = x
        self.y = y
        self.shape = shape_data['shape']
        self.color = shape_data['color']

    def rotate(self):
        """Rotate the piece 90 degrees clockwise."""
        self.shape = list(zip(*self.shape[::-1]))
        self.shape = [list(row) for row in self.shape]

    def move(self, dx, dy):
        """Move the piece by the given delta.
        
        Args:
            dx (int): Change in x position
            dy (int): Change in y position
        """
        self.x += dx
        self.y += dy
