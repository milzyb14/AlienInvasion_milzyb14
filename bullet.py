"""
Bullet module for AlienInvasion_milzyb14.
Author: Myles Buchanan
Purpose: Manages the bullets fired from the ship using a custom laser image.
Starter code from: https://github.com/RedBeard41/alien_Invasion_starter.git
Date: 04/26/2026

Asset Attribution:
- Bullet image: from Kenney.nl Space Shooter Remastered Pack
  https://kenney.nl/assets/space-shooter-remastered
"""

import pygame
from pathlib import Path

class Bullet(pygame.sprite.Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load custom laser image
        laser_path = Path('Assets/images/laser.png')
        self.image = pygame.image.load(laser_path)
        self.rect = self.image.get_rect()

        # Start bullet at top of ship
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store exact position
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)