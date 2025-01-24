"""Main entry point for the Tetris game."""

import pygame
from tetris.game import BaseGame, SpeedGame, BattleGame
from tetris.settings import Settings, HighScores
from tetris.ui import Menu
from tetris.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GameState

def main():
    """Main game function."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    settings = Settings()
    high_scores = HighScores()
    menu = Menu(screen, settings, high_scores)
    clock = pygame.time.Clock()
    current_game = None
    running = True

    while running:
        clock.tick(60)
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if current_game is None:
            new_state = menu.handle_events(events)
            if new_state:
                if new_state == GameState.QUIT:
                    running = False
                elif new_state == GameState.CLASSIC_GAME:
                    current_game = BaseGame(screen, settings, high_scores)
                elif new_state == GameState.SPEED_GAME:
                    current_game = SpeedGame(screen, settings, high_scores)
                elif new_state == GameState.BATTLE_GAME:
                    current_game = BattleGame(screen, settings, high_scores)
            menu.draw()
        else:
            current_game.handle_input(events)
            if current_game.current_state == GameState.PAUSE:
                current_game = None
            else:
                current_game.update()
                current_game.draw()
                if current_game.game_over:
                    current_game = None

    pygame.quit()

if __name__ == '__main__':
    main()
