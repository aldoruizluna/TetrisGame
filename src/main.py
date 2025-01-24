"""Main entry point for the Tetris game."""

import pygame
from tetris.game import BaseGame, SpeedGame, BattleGame
from tetris.settings import Settings, HighScores
from tetris.ui import Menu
from tetris.constants import SCREEN_DIMENSIONS, GameState


def main():
    """Main game function."""
    print("Initializing game...")
    pygame.init()
    # Initialize display with proper flags
    screen = pygame.display.set_mode((SCREEN_DIMENSIONS['WIDTH'], SCREEN_DIMENSIONS['HEIGHT']), 
                                   pygame.SHOWN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Tetris")
    print("Display initialized with dimensions:", SCREEN_DIMENSIONS['WIDTH'], "x", SCREEN_DIMENSIONS['HEIGHT'])
    
    settings = Settings()
    high_scores = HighScores()
    menu = Menu(screen, settings, high_scores)
    clock = pygame.time.Clock()
    current_game = None
    running = True
    print("Game components initialized")

    while running:
        clock.tick(60)
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                print("Quit event received")
            # Handle window focus events
            elif event.type == pygame.ACTIVEEVENT:
                print("Window focus event:", event.gain)
                if event.gain:  # Window gained focus
                    if current_game:
                        pygame.event.set_grab(True)
                        pygame.display.flip()
                        print("Window focus gained, display updated")

        if current_game is None:
            new_state = menu.handle_events(events)
            if new_state:
                print("New state received:", new_state)
                if new_state == GameState.QUIT:
                    running = False
                elif new_state == GameState.CLASSIC_GAME:
                    print("Creating new Classic Game instance...")
                    current_game = BaseGame(screen, settings, high_scores)
                    current_game.current_state = GameState.PLAYING
                    print("Classic Game instance created, state:", current_game.current_state)
                elif new_state == GameState.SPEED_GAME:
                    current_game = SpeedGame(screen, settings, high_scores)
                    current_game.current_state = GameState.PLAYING
                    print("Speed Game instance created")
                elif new_state == GameState.BATTLE_GAME:
                    current_game = BattleGame(screen, settings, high_scores)
                    current_game.current_state = GameState.PLAYING
                    print("Battle Game instance created")
            menu.draw()
        else:
            print("Game state:", current_game.current_state)
            current_game.handle_input(events)
            if current_game.current_state == GameState.PAUSE:
                print("Game paused, returning to menu")
                current_game = None
                pygame.event.set_grab(False)
            else:
                current_game.update()
                current_game.draw()
                pygame.display.flip()
                if current_game.game_over:
                    print("Game over, returning to menu")
                    current_game = None
                    pygame.event.set_grab(False)

        # Ensure the display is always updated
        pygame.display.flip()

    print("Game shutting down...")
    pygame.quit()

if __name__ == '__main__':
    main()
