"""Tests for UI components."""

import unittest
import pygame
from tetris.ui import Button, Menu
from tetris.settings import Settings, HighScores
from tetris.constants import COLORS, GameState, SCREEN_DIMENSIONS

class TestButton(unittest.TestCase):
    """Test cases for the Button class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        pygame.init()
        cls.screen = pygame.display.set_mode((SCREEN_DIMENSIONS['WIDTH'], SCREEN_DIMENSIONS['HEIGHT']))

    def setUp(self):
        """Set up test cases."""
        self.button = Button(100, 100, 200, 50, "Test Button")

    def test_initialization(self):
        """Test button initialization."""
        self.assertEqual(self.button.rect.x, 100)
        self.assertEqual(self.button.rect.y, 100)
        self.assertEqual(self.button.rect.width, 200)
        self.assertEqual(self.button.rect.height, 50)
        self.assertEqual(self.button.text, "Test Button")
        self.assertEqual(self.button.color, COLORS["WHITE"])
        self.assertEqual(self.button.hover_color, COLORS["BLUE"])
        self.assertFalse(self.button.is_hovered)
        # Test cached text surfaces
        self.assertIsNotNone(self.button._normal_text)
        self.assertIsNotNone(self.button._hover_text)

    def test_hover_state(self):
        """Test button hover state."""
        # Simulate mouse movement outside button
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (0, 0)})
        self.button.handle_event(event)
        self.assertFalse(self.button.is_hovered)

        # Simulate mouse movement over button
        event = pygame.event.Event(pygame.MOUSEMOTION, 
                                 {'pos': (self.button.rect.centerx, 
                                        self.button.rect.centery)})
        self.button.handle_event(event)
        self.assertTrue(self.button.is_hovered)

    def test_click_event(self):
        """Test button click event."""
        # Simulate click outside button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (0, 0), 'button': 1})
        result = self.button.handle_event(event)
        self.assertFalse(result)

        # Simulate click on button
        self.button.is_hovered = True
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, 
                                 {'pos': (self.button.rect.centerx, 
                                        self.button.rect.centery),
                                  'button': 1})
        result = self.button.handle_event(event)
        self.assertTrue(result)

        # Test right click (should not trigger)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, 
                                 {'pos': (self.button.rect.centerx, 
                                        self.button.rect.centery),
                                  'button': 3})
        result = self.button.handle_event(event)
        self.assertFalse(result)

class TestMenu(unittest.TestCase):
    """Test cases for the Menu class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        pygame.init()
        cls.screen = pygame.display.set_mode((SCREEN_DIMENSIONS['WIDTH'], SCREEN_DIMENSIONS['HEIGHT']))

    def setUp(self):
        """Set up test cases."""
        self.settings = Settings()
        self.high_scores = HighScores()
        self.menu = Menu(self.screen, self.settings, self.high_scores)

    def test_initialization(self):
        """Test menu initialization."""
        self.assertEqual(self.menu.state, GameState.MAIN_MENU)
        self.assertIsNone(self.menu.previous_state)
        self.assertIsNotNone(self.menu.main_menu_buttons)
        self.assertIsNotNone(self.menu.mode_buttons)
        self.assertIsNotNone(self.menu.settings_buttons)
        self.assertIsNotNone(self.menu.back_button)
        # Test cached fonts
        self.assertIsNotNone(self.menu.title_font)
        self.assertIsNotNone(self.menu.text_font)
        self.assertIsNotNone(self.menu.cached_title)

    def test_main_menu_navigation(self):
        """Test main menu navigation."""
        # Simulate clicking "Play Game"
        event = self._create_click_event(self.menu.main_menu_buttons[0])
        self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.MODE_SELECTION)

        # Go back to main menu
        self.menu.state = GameState.MAIN_MENU

        # Simulate clicking "High Scores"
        event = self._create_click_event(self.menu.main_menu_buttons[1])
        self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.HIGH_SCORES)

        # Go back to main menu
        self.menu.state = GameState.MAIN_MENU

        # Simulate clicking "Settings"
        event = self._create_click_event(self.menu.main_menu_buttons[2])
        self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.SETTINGS)

    def test_game_mode_selection(self):
        """Test game mode selection."""
        # First, navigate to mode selection
        self.menu.state = GameState.MODE_SELECTION
        
        # Test Classic Mode
        event = self._create_click_event(self.menu.mode_buttons[0])
        # Add mouse motion event to trigger hover
        hover_event = pygame.event.Event(pygame.MOUSEMOTION, {
            'pos': (self.menu.mode_buttons[0].rect.centerx, 
                   self.menu.mode_buttons[0].rect.centery)
        })
        self.menu.handle_events([hover_event, event])
        self.assertEqual(self.menu.state, GameState.CLASSIC_GAME)
        
        # Reset to mode selection
        self.menu.state = GameState.MODE_SELECTION
        
        # Test Speed Mode
        event = self._create_click_event(self.menu.mode_buttons[1])
        # Add mouse motion event to trigger hover
        hover_event = pygame.event.Event(pygame.MOUSEMOTION, {
            'pos': (self.menu.mode_buttons[1].rect.centerx, 
                   self.menu.mode_buttons[1].rect.centery)
        })
        self.menu.handle_events([hover_event, event])
        self.assertEqual(self.menu.state, GameState.SPEED_GAME)
        
        # Reset to mode selection
        self.menu.state = GameState.MODE_SELECTION
        
        # Test Battle Mode
        event = self._create_click_event(self.menu.mode_buttons[2])
        # Add mouse motion event to trigger hover
        hover_event = pygame.event.Event(pygame.MOUSEMOTION, {
            'pos': (self.menu.mode_buttons[2].rect.centerx, 
                   self.menu.mode_buttons[2].rect.centery)
        })
        self.menu.handle_events([hover_event, event])
        self.assertEqual(self.menu.state, GameState.BATTLE_GAME)

    def test_back_navigation(self):
        """Test back button functionality."""
        # Test mode selection back button
        self.menu.state = GameState.MODE_SELECTION
        event = self._create_click_event(self.menu.back_button)  
        self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.MAIN_MENU)

        # Test settings back button
        self.menu.state = GameState.SETTINGS
        event = self._create_click_event(self.menu.back_button)  
        self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.MAIN_MENU)

        # Test high scores back button
        self.menu.state = GameState.HIGH_SCORES
        event = self._create_click_event(self.menu.back_button)
        self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.MAIN_MENU)

    def _create_click_event(self, button):
        """Helper method to create click events."""
        button.is_hovered = True
        return pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            'pos': (button.rect.centerx, button.rect.centery),
            'button': 1
        })

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
