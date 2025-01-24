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
        """Initialize a new button.
        
        Args:
            x (int): X position
            y (int): Y position
            width (int): Button width
            height (int): Button height
            text (str): Button text
            color (tuple, optional): Normal color. Defaults to WHITE.
            hover_color (tuple, optional): Color when hovered. Defaults to BLUE.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        """Draw the button on the screen.
        
        Args:
            screen: Pygame screen surface
        """
        color = self.hover_color if self.is_hovered else self.color
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle mouse events for the button.
        
        Args:
            event: Pygame event
            
        Returns:
            bool: True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Menu:
    """Class managing game menus."""
    
    def __init__(self, screen, settings, high_scores):
        """Initialize the menu system.
        
        Args:
            screen: Pygame screen surface
            settings: Game settings instance
            high_scores: High scores instance
        """
        self.screen = screen
        self.settings = settings
        self.high_scores = high_scores
        self.state = GameState.MAIN_MENU
        self.previous_state = None
        self.selected_setting = None
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
        font = pygame.font.Font(None, 74)
        title = font.render("TETRIS", True, COLORS["WHITE"])
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title, title_rect)

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
        """Handle menu events.
        
        Args:
            events: List of pygame events
            
        Returns:
            GameState or None: New game state if changed, None otherwise
        """
        print("\nMenu handling events, current state:", self.state)
        for event in events:
            if event.type == pygame.QUIT:
                print("Menu: Quit event received")
                return GameState.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.state != GameState.MAIN_MENU:
                    print("Menu: Back event (ESC) received")
                    return self.handle_back()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Menu: Mouse click at", event.pos)

            if self.state == GameState.MAIN_MENU:
                for i, button in enumerate(self.main_menu_buttons):
                    if button.handle_event(event):
                        print(f"Menu: Main menu button {i} clicked ({button.text})")
                        if i == 0:  # Play Game
                            self.state = GameState.MODE_SELECTION
                            print("Menu: Transitioning to MODE_SELECTION")
                        elif i == 1:  # High Scores
                            self.state = GameState.HIGH_SCORES
                            print("Menu: Transitioning to HIGH_SCORES")
                        elif i == 2:  # Settings
                            self.state = GameState.SETTINGS
                            print("Menu: Transitioning to SETTINGS")
                        elif i == 3:  # Quit
                            print("Menu: Quit button clicked")
                            return GameState.QUIT
            
            elif self.state == GameState.MODE_SELECTION:
                for i, button in enumerate(self.mode_buttons):
                    if button.handle_event(event):
                        print(f"Menu: Mode selection button {i} clicked ({button.text})")
                        if i == 0:  # Classic Mode
                            print("Menu: Classic Mode selected, returning CLASSIC_GAME state")
                            return GameState.CLASSIC_GAME
                        elif i == 1:  # Speed Mode
                            print("Menu: Speed Mode selected")
                            return GameState.SPEED_GAME
                        elif i == 2:  # Battle Mode
                            print("Menu: Battle Mode selected")
                            return GameState.BATTLE_GAME
                        elif i == 3:  # Back
                            self.state = GameState.MAIN_MENU
                            print("Menu: Returning to main menu")

            elif self.state == GameState.SETTINGS:
                for i, button in enumerate(self.settings_buttons):
                    if button.handle_event(event):
                        print(f"Menu: Settings button {i} clicked ({button.text})")
                        if i < len(self.settings_buttons) - 1:  # Not the back button
                            self.selected_setting = i
                        else:  # Back button
                            self.state = GameState.MAIN_MENU
                            print("Menu: Returning to main menu from settings")

            elif self.state == GameState.HIGH_SCORES:
                if self.back_button.handle_event(event):
                    print("Menu: Back from high scores")
                    self.state = GameState.MAIN_MENU

        return None
