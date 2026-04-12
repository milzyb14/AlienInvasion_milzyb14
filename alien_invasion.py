"""
Main module for AlienInvasion_milzyb14.
Author: Myles Buchanan
Purpose: Main game loop and initialization for Alien Invasion game.
Starter code from: https://github.com/RedBeard41/alien_Invasion_starter.git
Date: 04/12/2026
"""

import sys
import pygame
from pathlib import Path
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))
        pygame.display.set_caption("Alien Invasion")

        # Load background image
        bg_path = Path('Assets/images/background.png')
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(
            self.background,
            (self.settings.screen_width, self.settings.screen_height)
        )

        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_q:
                    sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.blit(self.background, (0, 0))
        self.ship.blitme()
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()