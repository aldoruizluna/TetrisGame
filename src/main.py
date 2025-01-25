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
        clock.tick(60)  # Limit to 60 FPS
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                print("Quit event received")
            elif event.type == pygame.ACTIVEEVENT and event.gain and current_game:
                pygame.event.set_grab(True)
                print("Window focus gained")

        if current_game is None:
            new_state = menu.handle_events(events)
            if new_state:
                print("New state received:", new_state)
                if new_state == GameState.QUIT:
                    running = False
                elif new_state == GameState.CLASSIC_GAME:
                    current_game = BaseGame(screen, settings, high_scores)
                elif new_state == GameState.SPEED_GAME:
                    current_game = SpeedGame(screen, settings, high_scores)
                elif new_state == GameState.BATTLE_GAME:
                    current_game = BattleGame(screen, settings, high_scores)
                
                if current_game:
                    current_game.current_state = GameState.PLAYING
                    print(f"Created new {new_state} instance")
            menu.draw()
            pygame.display.flip()
        else:
            game_state = current_game.handle_input(events)
            
            if game_state == GameState.QUIT:
                running = False
            elif game_state == GameState.PAUSE:
                current_game = None
                pygame.event.set_grab(False)
            else:
                current_game.update()
                current_game.draw()
                
                if current_game.current_state == GameState.GAME_OVER:
                    print("Game Over reached!")
                    # Keep the game instance to show the game over screen
                    pygame.event.set_grab(False)
                
                # Only flip the display if the game is initialized
                if pygame.get_init():
                    pygame.display.flip()

    print("Game shutting down...")
    pygame.quit()

if __name__ == '__main__':
    main()
