# Tetris Game

## Overview
This is a classic Tetris game implemented in Python using the Pygame library. The game includes various modes, including single-player and battle modes, and features a modular design for easy extensibility.

## Features
- Classic Tetris gameplay mechanics
- Multiple game modes (BaseGame, SpeedGame, BattleGame)
- Collision detection and line clearing logic
- Score tracking and high score management
- User-friendly controls
- Logging for debugging and testing

## File Structure
The project is organized in a way that separates different components of the game for better maintainability and readability. Below is an overview of the main files and directories:

```
TetrisGame/
├── src/
│   ├── tetris/
│   │   ├── game.py          # Contains the main game logic and classes
│   │   ├── game_objects.py   # Defines the Tetrimino class and other game objects
│   │   ├── constants.py      # Contains game constants such as colors and dimensions
│   └── main.py               # Entry point for the game, initializes and runs the game loop
├── tests/
│   ├── test_game.py         # Unit tests for the game logic
│   ├── test_game_objects.py  # Unit tests for game objects
├── README.md                 # Project documentation
└── requirements.txt          # List of dependencies
```

### Main Files
- **`main.py`**: This is the entry point of the game. It initializes Pygame, sets up the game window, and starts the game loop.
- **`game.py`**: Contains the `BaseGame` class and other game modes. This file handles the core game logic, including piece movement, collision detection, and game state management.
- **`game_objects.py`**: Defines the `Tetrimino` class and other game objects. This file is responsible for creating and managing the different shapes used in Tetris.
- **`constants.py`**: Holds constant values used throughout the game, such as screen dimensions, colors, and game settings.
- **`test_game.py`**: Contains unit tests for the game logic, ensuring that the core functionalities work as intended.
- **`test_game_objects.py`**: Contains unit tests for the game objects, verifying their behaviors and interactions.

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd TetrisGame
   ```

2. Install the required dependencies:
   ```bash
   pip install pygame
   ```

## Usage
To start the game, run the following command:
```bash
python main.py
```

### Controls
- **Arrow Keys**: Move and rotate the Tetrimino
- **Escape**: Exit the game

## Testing
To run the test suite, ensure you have `pytest` installed and run:
```bash
pytest tests/
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bugs.

## License
This project is licensed under the MIT License.
