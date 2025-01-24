"""Constants used throughout the Tetris game."""

import enum
import pygame

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Game States
class GameState(enum.Enum):
    """Enum for different game states."""
    MAIN_MENU = 1
    MODE_SELECTION = 2
    CLASSIC_GAME = 3
    SPEED_GAME = 4
    BATTLE_GAME = 5
    SETTINGS = 6
    HIGH_SCORES = 7
    PAUSE = 8

# Tetrimino shapes and their colors
SHAPES = [
    {'shape': [[1, 1, 1, 1]], 'color': CYAN},    # I
    {'shape': [[1, 1], [1, 1]], 'color': YELLOW},  # O
    {'shape': [[0, 1, 1], [1, 1, 0]], 'color': GREEN},  # S
    {'shape': [[1, 1, 0], [0, 1, 1]], 'color': RED},    # Z
    {'shape': [[1, 1, 1], [0, 0, 1]], 'color': BLUE},   # L
    {'shape': [[1, 1, 1], [1, 0, 0]], 'color': ORANGE}, # J
    {'shape': [[1, 1, 1], [0, 1, 0]], 'color': PURPLE}  # T
]

# Default settings
DEFAULT_FALL_SPEED = 500
DEFAULT_MUSIC_VOLUME = 0.7
DEFAULT_SFX_VOLUME = 1.0
DEFAULT_DIFFICULTY = "Normal"
DEFAULT_CONTROLS = {
    "MOVE_LEFT": pygame.K_LEFT,
    "MOVE_RIGHT": pygame.K_RIGHT,
    "ROTATE": pygame.K_UP,
    "SOFT_DROP": pygame.K_DOWN,
    "HARD_DROP": pygame.K_SPACE
}
