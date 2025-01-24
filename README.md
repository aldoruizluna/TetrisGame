# Tetris Game

## Overview
This is a classic Tetris game implemented in Python using the Pygame library. The game includes various modes, including Classic, Speed, and Battle modes, and features a modular design for easy extensibility.

## Features
- Classic Tetris gameplay mechanics
- Multiple game modes:
  - **Classic Mode**: Traditional Tetris gameplay
  - **Speed Mode**: Increased difficulty with faster piece movement
  - **Battle Mode**: Competitive gameplay mode (under development)
- Difficulty settings (Easy, Normal, Hard)
- Score tracking and high score management
- User-friendly controls
- Debug logging for development and testing

## Game Modes
### Classic Mode
- Traditional Tetris gameplay
- Clear lines to score points
- Difficulty increases based on settings

### Speed Mode
- Enhanced version of Classic Mode
- Faster piece movement
- Higher scoring potential

### Battle Mode (Coming Soon)
- Competitive gameplay
- Special features and power-ups
- Head-to-head competition

## File Structure
The project is organized in a way that separates different components of the game for better maintainability and readability:

```
TetrisGame/
├── src/
│   ├── tetris/
│   │   ├── game.py         # Main game logic and classes
│   │   ├── constants.py    # Game constants (colors, dimensions)
│   │   ├── settings.py     # Game settings management
│   │   └── ui.py          # User interface components
│   ├── main.py            # Game entry point
│   ├── settings.json      # User settings configuration
│   └── highscores.json    # High scores storage
├── tests/
│   └── test_game.py       # Unit tests for game logic
└── README.md
```

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/aldoruizluna/TetrisGame.git
   cd TetrisGame
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game
1. Navigate to the src directory:
   ```bash
   cd src
   ```

2. Run the game:
   ```bash
   python main.py
   ```

## Controls
- **Left Arrow**: Move piece left
- **Right Arrow**: Move piece right
- **Down Arrow**: Move piece down
- **Up Arrow**: Rotate piece
- **ESC**: Exit game/Return to menu

## Development Status
- [x] Basic game mechanics
- [x] Classic Mode implementation
- [x] Score tracking
- [x] Multiple difficulty levels
- [ ] Speed Mode refinements
- [ ] Battle Mode implementation
- [ ] Power-ups and special features

## Recent Updates
- Added debugging capabilities for development
- Fixed grid initialization and piece spawning
- Improved game state management
- Relocated configuration files to src directory
- Enhanced error handling and logging

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
