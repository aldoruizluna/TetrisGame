"""Tests for UI components."""

import unittest
import pygame
from tetris.ui import Button, Menu
from tetris.settings import Settings, HighScores
from tetris.constants import WHITE, BLUE, GameState

class TestButton(unittest.TestCase):
    """Test cases for the Button class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

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
        self.assertEqual(self.button.color, WHITE)
        self.assertEqual(self.button.hover_color, BLUE)
        self.assertFalse(self.button.is_hovered)

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
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (0, 0)})
        result = self.button.handle_event(event)
        self.assertFalse(result)

        # Simulate click on button
        self.button.is_hovered = True
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, 
                                 {'pos': (self.button.rect.centerx, 
                                        self.button.rect.centery)})
        result = self.button.handle_event(event)
        self.assertTrue(result)

class TestMenu(unittest.TestCase):
    """Test cases for the Menu class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

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

    def test_main_menu_navigation(self):
        """Test main menu navigation."""
        # Simulate clicking "Play Game"
        event = self._create_click_event(self.menu.main_menu_buttons[0])
        new_state = self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.MODE_SELECTION)

        # Simulate clicking "High Scores"
        event = self._create_click_event(self.menu.main_menu_buttons[1])
        new_state = self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.HIGH_SCORES)

        # Simulate clicking "Settings"
        event = self._create_click_event(self.menu.main_menu_buttons[2])
        new_state = self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.SETTINGS)

    def test_back_navigation(self):
        """Test back button navigation."""
        # Go to mode selection
        self.menu.state = GameState.MODE_SELECTION
        
        # Test ESC key
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        new_state = self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.MAIN_MENU)

        # Go to settings
        self.menu.state = GameState.SETTINGS
        
        # Test back button
        event = self._create_click_event(self.menu.settings_buttons[-1])
        new_state = self.menu.handle_events([event])
        self.assertEqual(self.menu.state, GameState.MAIN_MENU)

    def test_settings_changes(self):
        """Test settings modifications."""
        self.menu.state = GameState.SETTINGS
        
        # Test music volume change
        initial_volume = self.settings.music_volume
        event = self._create_click_event(self.menu.settings_buttons[0])
        self.menu.handle_events([event])
        self.assertNotEqual(self.settings.music_volume, initial_volume)
        
        # Test difficulty change
        initial_difficulty = self.settings.difficulty
        event = self._create_click_event(self.menu.settings_buttons[2])
        self.menu.handle_events([event])
        self.assertNotEqual(self.settings.difficulty, initial_difficulty)

    def _create_click_event(self, button):
        """Helper method to create click event for a button."""
        button.is_hovered = True
        return pygame.event.Event(pygame.MOUSEBUTTONDOWN, 
                                {'pos': (button.rect.centerx, button.rect.centery)})

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
