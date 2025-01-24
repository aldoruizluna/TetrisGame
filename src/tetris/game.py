"""
Main game module containing game logic for a Tetris game.

This module includes the BaseGame class, which serves as the foundation for all game modes,
including SpeedGame and BattleGame. The game logic handles piece movement, collision detection,
line clearing, and game state management.
"""

import random  # Import the random module to generate random pieces
import pygame  # Import Pygame for graphics and game mechanics
from .constants import (  # Import constants used in the game
    SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, GRID_WIDTH, GRID_HEIGHT,
    GRID_OFFSET_X, GRID_OFFSET_Y, BLACK, WHITE, RED, GRAY, SHAPES, GameState
)
from .game_objects import Tetrimino  # Import the Tetrimino class for game pieces

class BaseGame:
    """Base class for all game modes."""
    
    def __init__(self, screen, settings, high_scores):
        """
        Initialize the game.

        Args:
            screen: Pygame screen surface
            settings: Game settings instance
            high_scores: High scores instance
        """
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
        """
        Reset the game state.
        """
        # Create a grid for the game
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        # No current piece at the start
        self.current_piece = None  
        # Timer for piece falling
        self.fall_time = 0  
        # Default fall speed in milliseconds
        self.fall_speed = 500  
        # Adjust fall speed based on difficulty settings
        if self.settings.difficulty == "Easy":
            self.fall_speed = 600
        elif self.settings.difficulty == "Hard":
            self.fall_speed = 400
        # Game is not over initially
        self.game_over = False  
        # Initialize score to zero
        self.score = 0  
        # Spawn the first piece
        self.spawn_new_piece()  

    def spawn_new_piece(self):
        """
        Create and spawn a new tetrimino.
        """
        # Calculate starting position for the new piece
        start_x = GRID_WIDTH // 2 - 1  # Center horizontally
        start_y = 0  # Start at the top of the grid
        # Create a new Tetrimino with a random shape
        self.current_piece = Tetrimino(start_x, start_y, random.choice(SHAPES))

    def check_collision(self, x_offset=0, y_offset=0, shape=None):
        """
        Check if the current piece collides with anything.

        Args:
            x_offset (int, optional): X offset to check. Defaults to 0.
            y_offset (int, optional): Y offset to check. Defaults to 0.
            shape (list, optional): Shape to check. Defaults to None.

        Returns:
            bool: True if collision detected, False otherwise
        """
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
                    if (abs_x < 0 or abs_x >= GRID_WIDTH or 
                        abs_y >= GRID_HEIGHT or 
                        (abs_y >= 0 and self.grid[abs_y][abs_x] is not None)):
                        return True  # Collision detected
        return False  # No collision detected

    def lock_piece(self):
        """
        Lock the current piece in place.
        """
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
        """
        Clear completed lines and update score.

        Returns:
            int: Number of lines cleared
        """
        # Initialize lines cleared counter
        lines_cleared = 0  
        # Start from the bottom of the grid
        y = GRID_HEIGHT - 1  
        while y >= 0:
            # Check if the line is filled
            if all(cell is not None for cell in self.grid[y]):  
                # Increment lines cleared counter
                lines_cleared += 1  
                # Move lines down
                for move_y in range(y, 0, -1):  
                    self.grid[move_y] = self.grid[move_y - 1][:]
                # Clear the top line
                self.grid[0] = [None] * GRID_WIDTH  
            else:
                # Move up to the next line
                y -= 1  

        # Update score based on lines cleared
        if lines_cleared > 0:
            self.score += lines_cleared * 100 * lines_cleared  
        return lines_cleared  # Return the number of lines cleared

    def handle_input(self, events):
        """
        Handle player input.

        Args:
            events: List of pygame events
        """
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

    def update(self):
        """
        Update game state.
        """
        # Update game logic, piece movement, etc.
        pass  # Implementation goes here

    def draw(self):
        """
        Draw the game state.
        """
        # Render the game elements on the screen
        pass  # Implementation goes here

class SpeedGame(BaseGame):
    """
    Speed mode game class.
    """
    
    def __init__(self, screen, settings, high_scores):
        """
        Initialize speed mode.

        Args:
            screen: Pygame screen surface
            settings: Game settings instance
            high_scores: High scores instance
        """
        super().__init__(screen, settings, high_scores)
        # Initial fall speed
        self.initial_fall_speed = 500
        # Minimum fall speed
        self.min_fall_speed = 100
        # Speed increase rate
        self.speed_increase_rate = 0.95
        # Lines required for speed up
        self.lines_for_speed_up = 5
        # Lines cleared counter
        self.lines_cleared_count = 0

    def clear_lines(self):
        """
        Clear lines and increase speed if needed.
        """
        # Clear lines and get the number of lines cleared
        lines_cleared = super().clear_lines()
        # Increase speed if needed
        if lines_cleared:
            self.lines_cleared_count += lines_cleared
            if self.lines_cleared_count >= self.lines_for_speed_up:
                self.lines_cleared_count = 0
                # Increase fall speed
                self.fall_speed = max(self.min_fall_speed, 
                                    self.fall_speed * self.speed_increase_rate)

class BattleGame(BaseGame):
    """
    Battle mode game class.
    """
    
    def __init__(self, screen, settings, high_scores):
        """
        Initialize battle mode.

        Args:
            screen: Pygame screen surface
            settings: Game settings instance
            high_scores: High scores instance
        """
        super().__init__(screen, settings, high_scores)
        # Player 2's grid
        self.player2_grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        # Player 2's current piece
        self.player2_piece = None
        # Player 2's score
        self.player2_score = 0
        # AI move timer
        self.ai_move_timer = 0
        # AI move delay
        self.ai_move_delay = 200
        # Spawn player 2's first piece
        self.spawn_player2_piece()

    def spawn_player2_piece(self):
        """
        Create and spawn a new tetrimino for player 2.
        """
        # Calculate starting position for the new piece
        start_x = GRID_WIDTH // 2 - 1
        start_y = 0
        # Create a new Tetrimino with a random shape
        self.player2_piece = Tetrimino(start_x, start_y, random.choice(SHAPES))

    def update(self):
        """
        Update both player and AI.
        """
        # Update player's game state
        super().update()
        # Update AI opponent
        self.update_ai()

    def update_ai(self):
        """
        Update AI opponent.
        """
        # Check if player 2 has a piece
        if not self.player2_piece:
            # Spawn a new piece for player 2
            self.spawn_player2_piece()
            return

        # Update AI move timer
        self.ai_move_timer += self.clock.get_rawtime()
        # Check if it's time for the AI to move
        if self.ai_move_timer >= self.ai_move_delay:
            # Reset AI move timer
            self.ai_move_timer = 0
            # Simple AI: randomly move and rotate pieces
            if random.random() < 0.3:
                # Move left
                if random.random() < 0.5:
                    if not self.check_player2_collision(x_offset=-1):
                        self.player2_piece.move(-1, 0)
                # Move right
                else:
                    if not self.check_player2_collision(x_offset=1):
                        self.player2_piece.move(1, 0)
            # Rotate piece
            if random.random() < 0.2:
                original_shape = [row[:] for row in self.player2_piece.shape]
                self.player2_piece.rotate()
                if self.check_player2_collision():
                    self.player2_piece.shape = original_shape

            # Always try to move down
            if not self.check_player2_collision(y_offset=1):
                self.player2_piece.move(0, 1)
            else:
                # Lock player 2's piece in place
                self.lock_player2_piece()

    def check_player2_collision(self, x_offset=0, y_offset=0, shape=None):
        """
        Check if player 2's piece collides with anything.

        Args:
            x_offset (int, optional): X offset to check. Defaults to 0.
            y_offset (int, optional): Y offset to check. Defaults to 0.
            shape (list, optional): Shape to check. Defaults to None.

        Returns:
            bool: True if collision detected, False otherwise
        """
        # Use player 2's piece shape if none provided
        if not shape:
            shape = self.player2_piece.shape
        
        # Calculate absolute position of the piece
        piece_x = self.player2_piece.x + x_offset
        piece_y = self.player2_piece.y + y_offset
        
        # Check each cell in the piece's shape for collisions
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    abs_x = piece_x + x
                    abs_y = piece_y + y
                    # Check for collisions with walls or existing blocks
                    if (abs_x < 0 or abs_x >= GRID_WIDTH or
                        abs_y >= GRID_HEIGHT or
                        (abs_y >= 0 and self.player2_grid[abs_y][abs_x])):
                        return True
        return False

    def lock_player2_piece(self):
        """
        Lock player 2's piece in place.
        """
        # Iterate over each cell in the piece's shape
        for y, row in enumerate(self.player2_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    abs_y = self.player2_piece.y + y
                    if abs_y < 0:
                        continue
                    # Lock the piece in the grid
                    self.player2_grid[abs_y][self.player2_piece.x + x] = self.player2_piece.color
        
        # Clear completed lines for player 2
        self.clear_player2_lines()
        # Spawn a new piece for player 2
        self.spawn_player2_piece()

    def clear_player2_lines(self):
        """
        Clear completed lines for player 2 and update score.
        """
        # Initialize lines cleared counter
        lines_cleared = 0
        # Start from the bottom of the grid
        y = GRID_HEIGHT - 1
        while y >= 0:
            # Check if the line is filled
            if all(cell is not None for cell in self.player2_grid[y]):
                # Increment lines cleared counter
                lines_cleared += 1
                # Move lines down
                for move_y in range(y, 0, -1):
                    self.player2_grid[move_y] = self.player2_grid[move_y - 1][:]
                # Clear the top line
                self.player2_grid[0] = [None] * GRID_WIDTH
            else:
                # Move up to the next line
                y -= 1
        
        # Update player 2's score
        if lines_cleared > 0:
            self.player2_score += lines_cleared * 100 * lines_cleared

    def draw(self):
        """
        Draw both player and AI grids.
        """
        # Draw player's grid
        super().draw()
        # Draw player 2's grid on the right side
        for y, row in enumerate(self.player2_grid):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(self.screen, color,
                                   (GRID_OFFSET_X + GRID_WIDTH * BLOCK_SIZE + 100 + x * BLOCK_SIZE,
                                    GRID_OFFSET_Y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        # Draw player 2's current piece
        if self.player2_piece:
            for y, row in enumerate(self.player2_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.player2_piece.color,
                                       (GRID_OFFSET_X + GRID_WIDTH * BLOCK_SIZE + 100 + 
                                        (self.player2_piece.x + x) * BLOCK_SIZE,
                                        GRID_OFFSET_Y + (self.player2_piece.y + y) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))
