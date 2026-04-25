"""
Game stats module for AlienInvasion_milzyb14.
Author: Myles Buchanan
Purpose: Stores all stats for Alien Invasion game.
Starter code from: https://github.com/RedBeard41/alien_Invasion_starter.git
Date: 04/25/2026
"""

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__ (self,ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit