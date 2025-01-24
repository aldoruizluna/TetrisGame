"""Module for managing game settings and high scores."""

import json
from datetime import datetime
from .constants import (
    DEFAULT_MUSIC_VOLUME,
    DEFAULT_SFX_VOLUME,
    DEFAULT_DIFFICULTY,
    DEFAULT_CONTROLS
)

class Settings:
    """Class for managing game settings."""
    
    def __init__(self):
        """Initialize settings with default values."""
        self.music_volume = DEFAULT_MUSIC_VOLUME
        self.sfx_volume = DEFAULT_SFX_VOLUME
        self.difficulty = DEFAULT_DIFFICULTY
        self.controls = DEFAULT_CONTROLS.copy()
        self.load_settings()

    def save_settings(self):
        """Save current settings to a JSON file."""
        settings_dict = {
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "difficulty": self.difficulty,
            "controls": {k: v for k, v in self.controls.items()}
        }
        with open("settings.json", "w") as f:
            json.dump(settings_dict, f)

    def load_settings(self):
        """Load settings from JSON file."""
        try:
            with open("settings.json", "r") as f:
                settings_dict = json.load(f)
                self.music_volume = settings_dict.get("music_volume", self.music_volume)
                self.sfx_volume = settings_dict.get("sfx_volume", self.sfx_volume)
                self.difficulty = settings_dict.get("difficulty", self.difficulty)
                self.controls.update(settings_dict.get("controls", {}))
        except FileNotFoundError:
            self.save_settings()

class HighScores:
    """Class for managing high scores."""
    
    def __init__(self):
        """Initialize high scores list."""
        self.scores = []
        self.max_scores = 10
        self.load_scores()

    def add_score(self, score, mode):
        """Add a new score to the high scores list.
        
        Args:
            score (int): The score to add
            mode (str): The game mode in which the score was achieved
        """
        date = datetime.now().strftime("%Y-%m-%d")
        self.scores.append({"score": score, "date": date, "mode": mode})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:self.max_scores]
        self.save_scores()

    def save_scores(self):
        """Save high scores to a JSON file."""
        with open("highscores.json", "w") as f:
            json.dump(self.scores, f)

    def load_scores(self):
        """Load high scores from JSON file."""
        try:
            with open("highscores.json", "r") as f:
                self.scores = json.load(f)
        except FileNotFoundError:
            self.save_scores()

    def get_high_scores(self, mode=None):
        """Get high scores, optionally filtered by mode.
        
        Args:
            mode (str, optional): Game mode to filter by. Defaults to None.
        
        Returns:
            list: List of high scores
        """
        if mode is None:
            return self.scores
        return [score for score in self.scores if score["mode"] == mode]
