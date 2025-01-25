"""
Module containing UI elements for the game.
"""

import pygame
import logging
from .constants import COLORS, GameState

# Initialize logger
logger = logging.getLogger(__name__)

class Button:
    """Class representing a clickable button."""
    
    def __init__(self, x, y, width, height, text, color=COLORS["WHITE"], hover_color=COLORS["BLUE"]):
        """Initialize a new button."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        # Cache text surfaces
        self._normal_text = self.font.render(text, True, color)
        self._hover_text = self.font.render(text, True, hover_color)

    def draw(self, screen):
        """Draw the button on the screen."""
        text_surface = self._hover_text if self.is_hovered else self._normal_text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle mouse events for the button."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click only
            return self.is_hovered
        return False

class Menu:
    """Class managing game menus."""
    
    def __init__(self, screen, settings, high_scores):
        """Initialize the menu system."""
        self.screen = screen
        self.settings = settings
        self.high_scores = high_scores
        self.state = GameState.MAIN_MENU
        self.previous_state = None
        self.selected_setting = None
        # Cache fonts
        self.title_font = pygame.font.Font(None, 74)
        self.text_font = pygame.font.Font(None, 36)
        self.cached_title = self.title_font.render("TETRIS", True, COLORS["WHITE"])
        self.create_buttons()

    def create_buttons(self):
        """Create all menu buttons."""
        button_width = 200
        button_height = 50
        start_y = self.screen.get_height() // 3
        spacing = 70
        center_x = self.screen.get_width() // 2 - button_width // 2

        # Main Menu Buttons
        self.main_menu_buttons = [
            Button(center_x, start_y, button_width, button_height, "Play Game"),
            Button(center_x, start_y + spacing, button_width, button_height, "High Scores"),
            Button(center_x, start_y + spacing * 2, button_width, button_height, "Settings"),
            Button(center_x, start_y + spacing * 3, button_width, button_height, "Quit")
        ]

        # Game Mode Buttons
        self.mode_buttons = [
            Button(center_x, start_y, button_width, button_height, "Classic Mode"),
            Button(center_x, start_y + spacing, button_width, button_height, "Speed Mode"),
            Button(center_x, start_y + spacing * 2, button_width, button_height, "Battle Mode"),
            Button(center_x, start_y + spacing * 3, button_width, button_height, "Back")
        ]

        # Settings Buttons
        self.settings_buttons = [
            Button(center_x, start_y, button_width, button_height, 
                  f"Music: {int(self.settings.music_volume * 100)}%"),
            Button(center_x, start_y + spacing, button_width, button_height, 
                  f"SFX: {int(self.settings.sfx_volume * 100)}%"),
            Button(center_x, start_y + spacing * 2, button_width, button_height, 
                  f"Difficulty: {self.settings.difficulty}"),
            Button(center_x, start_y + spacing * 3, button_width, button_height, "Back")
        ]

        # Back button for high scores
        self.back_button = Button(center_x, self.screen.get_height() - 100,
                                button_width, button_height, "Back")

    def draw(self):
        """Draw the current menu screen."""
        self.screen.fill(COLORS["BLACK"])
        
        # Draw title
        title_rect = self.cached_title.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(self.cached_title, title_rect)

        # Draw buttons based on current state
        if self.state == GameState.MAIN_MENU:
            for button in self.main_menu_buttons:
                button.draw(self.screen)
        elif self.state == GameState.MODE_SELECTION:
            for button in self.mode_buttons:
                button.draw(self.screen)
        elif self.state == GameState.SETTINGS:
            for button in self.settings_buttons:
                button.draw(self.screen)
        elif self.state == GameState.HIGH_SCORES:
            self.draw_high_scores()
            self.back_button.draw(self.screen)

        pygame.display.flip()

    def draw_high_scores(self):
        """Draw the high scores screen."""
        font = pygame.font.Font(None, 36)
        y = self.screen.get_height() // 4
        
        # Draw header
        header = font.render("HIGH SCORES", True, COLORS["WHITE"])
        header_rect = header.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(header, header_rect)
        
        y += 50
        for score in self.high_scores.scores:
            score_text = f"{score['score']:,} - {score['mode']} - {score['date']}"
            text = font.render(score_text, True, COLORS["WHITE"])
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += 40

    def draw_game_over(self, current_game, last_game_snapshot):
        """Draw the GAME OVER screen over the last snapshot of the game."""
        # Draw the last game snapshot
        self.screen.blit(last_game_snapshot, (0, 0))
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0, 0, 0))  # Fill with black
        overlay.set_alpha(128)  # Set transparency level (0-255)
        self.screen.blit(overlay, (0, 0))  # Draw the overlay
        
        # Draw GAME OVER text
        game_over_text = "GAME OVER"
        font = pygame.font.Font(None, 74)
        text_surface = font.render(game_over_text, True, COLORS["WHITE"])
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        self.screen.blit(text_surface, text_rect)
        
        # Draw restart and quit buttons
        center_x = self.screen.get_width() // 2 - 100
        start_y = self.screen.get_height() // 2
        spacing = 70
        button_width = 200
        button_height = 50
        self.restart_button = Button(center_x, start_y + spacing, button_width, button_height, "Restart")
        self.quit_button = Button(center_x, start_y + spacing * 2, button_width, button_height, "Quit")
        self.restart_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        
        pygame.display.flip()

    def handle_back(self):
        """Handle back button navigation."""
        if self.state == GameState.MODE_SELECTION:
            self.state = GameState.MAIN_MENU
        elif self.state == GameState.SETTINGS:
            self.state = GameState.MAIN_MENU
        elif self.state == GameState.HIGH_SCORES:
            self.state = GameState.MAIN_MENU
        elif self.state == GameState.PAUSE:
            self.state = GameState.MAIN_MENU
            return GameState.MAIN_MENU
        return None

    def handle_events(self, events):
        """Handle menu events."""
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if self.state == GameState.GAME_OVER:
                # Ignore arrow key events
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.state != GameState.MAIN_MENU:
                    return self.handle_back()

            if self.state == GameState.MAIN_MENU:
                for i, button in enumerate(self.main_menu_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Play Game
                            self.state = GameState.MODE_SELECTION
                        elif i == 1:  # High Scores
                            self.state = GameState.HIGH_SCORES
                        elif i == 2:  # Settings
                            self.state = GameState.SETTINGS
                        elif i == 3:  # Quit
                            return GameState.QUIT
        
            elif self.state == GameState.MODE_SELECTION:
                # First check back button
                if self.back_button.handle_event(event):
                    print("Back button clicked in mode selection.")  # Debugging output
                    self.state = GameState.MAIN_MENU
                    return None
            
                # Then check mode buttons
                for i, button in enumerate(self.mode_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Classic Mode
                            self.state = GameState.CLASSIC_GAME
                            return GameState.CLASSIC_GAME
                        elif i == 1:  # Speed Mode
                            self.state = GameState.SPEED_GAME
                            return GameState.SPEED_GAME
                        elif i == 2:  # Battle Mode
                            self.state = GameState.BATTLE_GAME
                            return GameState.BATTLE_GAME
        
            elif self.state == GameState.SETTINGS:
                # First check back button
                if self.back_button.handle_event(event):
                    print("Back button clicked in settings.")  # Debugging output
                    self.state = GameState.MAIN_MENU
                    return None
            
                # Then check settings buttons
                for i, button in enumerate(self.settings_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Music Volume
                            self.selected_setting = "music"
                        elif i == 1:  # SFX Volume
                            self.selected_setting = "sfx"
                        elif i == 2:  # Difficulty
                            self.selected_setting = "difficulty"
                        elif i == 3:  # Back
                            self.state = GameState.MAIN_MENU
                            return None
        
            elif self.state == GameState.HIGH_SCORES:
                if self.back_button.handle_event(event):
                    self.state = GameState.MAIN_MENU

            elif self.state == GameState.GAME_OVER:
                # Check restart and quit buttons
                if self.restart_button.handle_event(event):
                    print("Restart button clicked.")  # Debugging output
                    self.state = GameState.CLASSIC_GAME  # Or whatever mode you want to restart
                    return None
                elif self.quit_button.handle_event(event):
                    print("Quit button clicked.")  # Debugging output
                    self.state = GameState.MAIN_MENU
                    return None

        return None
