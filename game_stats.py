"""
Game stats module for AlienInvasion_milzyb14.
Author: Myles Buchanan
Purpose: Stores all stats for Alien Invasion game.
Starter code from: https://github.com/RedBeard41/alien_Invasion_starter.git
Date: 04/26/2026
"""

from pathlib import Path


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__ (self,ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.high_score_path = Path('Assets/file/high_score.txt')
        self.reset_stats()
        # Load high score from file if it exits, otherwise set to 0
        if self.high_score_path.exists():
            with self.high_score_path.open('r') as f:
                self.high_score = int(f.read())
        else:
            self.high_score = 0


    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        
    def _load_high_score(self):
        """Load high score from file."""
        try:
            with open(self.high_score_path, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0 
        
    def _save_high_score(self):
        """Save high score to file."""
        with open(self.high_score_path, 'w') as f:
            f.write(str(self.high_score))