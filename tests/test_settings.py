"""Tests for settings and high scores."""

import unittest
import os
import json
from datetime import datetime
from tetris.settings import Settings, HighScores
from tetris.constants import (
    DEFAULT_MUSIC_VOLUME, DEFAULT_SFX_VOLUME,
    DEFAULT_DIFFICULTY, DEFAULT_CONTROLS
)

class TestSettings(unittest.TestCase):
    """Test cases for the Settings class."""

    def setUp(self):
        """Set up test cases."""
        # Remove settings file if it exists
        if os.path.exists("settings.json"):
            os.remove("settings.json")
        self.settings = Settings()

    def test_default_values(self):
        """Test default settings values."""
        self.assertEqual(self.settings.music_volume, DEFAULT_MUSIC_VOLUME)
        self.assertEqual(self.settings.sfx_volume, DEFAULT_SFX_VOLUME)
        self.assertEqual(self.settings.difficulty, DEFAULT_DIFFICULTY)
        self.assertEqual(self.settings.controls, DEFAULT_CONTROLS)

    def test_save_load_settings(self):
        """Test saving and loading settings."""
        # Modify settings
        test_settings = {
            "music_volume": 0.5,
            "sfx_volume": 0.8,
            "difficulty": "Hard",
            "controls": {
                "MOVE_LEFT": 97,  # 'a' key
                "MOVE_RIGHT": 100,  # 'd' key
                "ROTATE": 119,  # 'w' key
                "SOFT_DROP": 115,  # 's' key
                "HARD_DROP": 32  # space key
            }
        }
        
        self.settings.music_volume = test_settings["music_volume"]
        self.settings.sfx_volume = test_settings["sfx_volume"]
        self.settings.difficulty = test_settings["difficulty"]
        self.settings.controls = test_settings["controls"].copy()
        self.settings.save_settings()

        # Create new settings instance to load saved values
        new_settings = Settings()
        self.assertEqual(new_settings.music_volume, test_settings["music_volume"])
        self.assertEqual(new_settings.sfx_volume, test_settings["sfx_volume"])
        self.assertEqual(new_settings.difficulty, test_settings["difficulty"])
        self.assertEqual(new_settings.controls, test_settings["controls"])

    def test_volume_bounds(self):
        """Test volume settings bounds."""
        # Test upper bound
        self.settings.music_volume = 1.5
        self.settings.save_settings()
        new_settings = Settings()
        self.assertLessEqual(new_settings.music_volume, 1.0)

        # Test lower bound
        self.settings.sfx_volume = -0.5
        self.settings.save_settings()
        new_settings = Settings()
        self.assertGreaterEqual(new_settings.sfx_volume, 0.0)

    def test_difficulty_values(self):
        """Test difficulty setting values."""
        valid_difficulties = ["Easy", "Normal", "Hard"]
        
        # Test valid difficulties
        for difficulty in valid_difficulties:
            self.settings.difficulty = difficulty
            self.settings.save_settings()
            new_settings = Settings()
            self.assertEqual(new_settings.difficulty, difficulty)

        # Test invalid difficulty
        self.settings.difficulty = "Invalid"
        self.settings.save_settings()
        new_settings = Settings()
        self.assertEqual(new_settings.difficulty, DEFAULT_DIFFICULTY)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists("settings.json"):
            os.remove("settings.json")

class TestHighScores(unittest.TestCase):
    """Test cases for the HighScores class."""

    def setUp(self):
        """Set up test cases."""
        # Remove high scores file if it exists
        if os.path.exists("highscores.json"):
            os.remove("highscores.json")
        self.high_scores = HighScores()

    def test_add_score(self):
        """Test adding scores."""
        test_score = {
            "score": 1000,
            "mode": "Classic",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.high_scores.add_score(test_score["score"], test_score["mode"])
        self.assertEqual(len(self.high_scores.scores), 1)
        self.assertEqual(self.high_scores.scores[0]["score"], test_score["score"])
        self.assertEqual(self.high_scores.scores[0]["mode"], test_score["mode"])
        self.assertEqual(self.high_scores.scores[0]["date"], test_score["date"])

    def test_score_sorting(self):
        """Test score sorting."""
        test_scores = [
            {"score": 500, "mode": "Classic"},
            {"score": 1000, "mode": "Speed"},
            {"score": 750, "mode": "Battle"}
        ]
        
        for score in test_scores:
            self.high_scores.add_score(score["score"], score["mode"])

        self.assertEqual(len(self.high_scores.scores), 3)
        self.assertEqual(self.high_scores.scores[0]["score"], 1000)
        self.assertEqual(self.high_scores.scores[1]["score"], 750)
        self.assertEqual(self.high_scores.scores[2]["score"], 500)

    def test_max_scores(self):
        """Test maximum scores limit."""
        # Add more scores than the maximum limit
        for i in range(self.high_scores.max_scores + 5):
            self.high_scores.add_score(i * 100, "Classic")

        self.assertEqual(len(self.high_scores.scores), self.high_scores.max_scores)
        self.assertEqual(self.high_scores.scores[0]["score"], 
                        (self.high_scores.max_scores + 4) * 100)

    def test_get_high_scores_by_mode(self):
        """Test getting scores filtered by mode."""
        test_scores = [
            {"score": 1000, "mode": "Classic"},
            {"score": 800, "mode": "Speed"},
            {"score": 600, "mode": "Classic"},
            {"score": 900, "mode": "Battle"},
            {"score": 700, "mode": "Speed"}
        ]
        
        for score in test_scores:
            self.high_scores.add_score(score["score"], score["mode"])

        classic_scores = self.high_scores.get_high_scores("Classic")
        speed_scores = self.high_scores.get_high_scores("Speed")
        battle_scores = self.high_scores.get_high_scores("Battle")

        self.assertEqual(len(classic_scores), 2)
        self.assertEqual(len(speed_scores), 2)
        self.assertEqual(len(battle_scores), 1)
        
        self.assertEqual(classic_scores[0]["score"], 1000)
        self.assertEqual(speed_scores[0]["score"], 800)
        self.assertEqual(battle_scores[0]["score"], 900)

    def test_save_load_scores(self):
        """Test saving and loading scores."""
        test_scores = [
            {"score": 1000, "mode": "Classic"},
            {"score": 800, "mode": "Speed"},
            {"score": 600, "mode": "Battle"}
        ]
        
        for score in test_scores:
            self.high_scores.add_score(score["score"], score["mode"])
        
        self.high_scores.save_scores()

        # Create new high scores instance to load saved values
        new_high_scores = HighScores()
        self.assertEqual(len(new_high_scores.scores), len(test_scores))
        self.assertEqual(new_high_scores.scores[0]["score"], 1000)
        self.assertEqual(new_high_scores.scores[1]["score"], 800)
        self.assertEqual(new_high_scores.scores[2]["score"], 600)

    def test_invalid_scores(self):
        """Test handling of invalid scores."""
        # Test negative score
        self.high_scores.add_score(-100, "Classic")
        self.assertEqual(len(self.high_scores.scores), 0)

        # Test zero score
        self.high_scores.add_score(0, "Classic")
        self.assertEqual(len(self.high_scores.scores), 0)

        # Test invalid mode
        self.high_scores.add_score(100, "Invalid")
        self.assertEqual(len(self.high_scores.scores), 0)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists("highscores.json"):
            os.remove("highscores.json")

if __name__ == '__main__':
    unittest.main()
