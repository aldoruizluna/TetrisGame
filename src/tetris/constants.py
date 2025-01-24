"""Constants used throughout the Tetris game."""

import enum
import pygame

# Screen dimensions
SCREEN_DIMENSIONS = {
    "WIDTH": 800,
    "HEIGHT": 600,
    "BLOCK_SIZE": 30,
    "GRID_WIDTH": 10,
    "GRID_HEIGHT": 20,
    "GRID_OFFSET_X": (800 - 10 * 30) // 2,
    "GRID_OFFSET_Y": (600 - 20 * 30) // 2
}

# Colors
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "CYAN": (0, 255, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "ORANGE": (255, 165, 0),
    "PURPLE": (128, 0, 128),
    "GRAY": (128, 128, 128),
    "DARK_GRAY": (64, 64, 64)
}

# Game States
class GameState(enum.Enum):
    """Enum for different game states."""
    MAIN_MENU = 1  # Main menu screen
    MODE_SELECTION = 2  # Mode selection screen
    CLASSIC_GAME = 3  # Classic game mode
    SPEED_GAME = 4  # Speed game mode
    BATTLE_GAME = 5  # Battle game mode
    SETTINGS = 6  # Settings screen
    HIGH_SCORES = 7  # High scores screen
    PAUSE = 8  # Game paused
    QUIT = 9  # Quit game

# Tetrimino shapes and their colors
SHAPES = [
    {'shape': [[1, 1, 1, 1]], 'color': COLORS["CYAN"]},    # I
    {'shape': [[1, 1], [1, 1]], 'color': COLORS["YELLOW"]},  # O
    {'shape': [[0, 1, 1], [1, 1, 0]], 'color': COLORS["GREEN"]},  # S
    {'shape': [[1, 1, 0], [0, 1, 1]], 'color': COLORS["RED"]},    # Z
    {'shape': [[1, 1, 1], [0, 0, 1]], 'color': COLORS["BLUE"]},   # L
    {'shape': [[1, 1, 1], [1, 0, 0]], 'color': COLORS["ORANGE"]}, # J
    {'shape': [[1, 1, 1], [0, 1, 0]], 'color': COLORS["PURPLE"]}  # T
]

# Default settings
DEFAULT_SETTINGS = {
    "FALL_SPEED": 500,
    "MUSIC_VOLUME": 0.7,
    "SFX_VOLUME": 1.0,
    "DEFAULT_SFX_VOLUME": 1.0,
    "DIFFICULTY": "Normal",
    "DEFAULT_DIFFICULTY": "Normal",
    "CONTROLS": {
        "MOVE_LEFT": pygame.K_LEFT,
        "MOVE_RIGHT": pygame.K_RIGHT,
        "ROTATE": pygame.K_UP,
        "SOFT_DROP": pygame.K_DOWN,
        "HARD_DROP": pygame.K_SPACE
    },
    "DEFAULT_CONTROLS": {
        "MOVE_LEFT": pygame.K_LEFT,
        "MOVE_RIGHT": pygame.K_RIGHT,
        "ROTATE": pygame.K_UP,
        "SOFT_DROP": pygame.K_DOWN,
        "HARD_DROP": pygame.K_SPACE
    }
}
