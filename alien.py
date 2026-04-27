"""Alien module for AlienInvasion_milzyb14.
Author: Myles Buchanan
Purpose: Manages individual alien sprites using a custom alien image.
Starter code from: https://github.com/RedBeard41/alien_Invasion_starter.git
Date: 04/19/2026

Asset Attribution:
- Alien image: from Kenney.nl Space Shooter Remastered Pack
  https://kenney.nl/assets/space-shooter-remastered
"""


import pygame
from pathlib import Path

class Alien(pygame.sprite.Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game, x, y):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        alien_path = Path('Assets/images/alien.png')
        self.image = pygame.image.load(alien_path)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the alien down the screen."""
        self.y += self.settings.alien_speed
        self.rect.y = self.y