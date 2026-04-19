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
from bullet import Bullet
from alien import Alien

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

        self.ship = Ship(ai_game=self)

        # Load background image
        bg_path = Path('Assets/images/background.png')
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(
            self.background,
            (self.settings.screen_width, self.settings.screen_height)
        )

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self._update_aliens()


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
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_alien_collisions(self):
        """Respond to bullet alien collisions."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        # If all aliens gone, respwan the fleet. 
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Update positions of all aliens and check ship collisions."""
        self.aliens.update()
        # Check alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.rect.midbottom = self.screen.get_rect().midbottom
        self.ship.x = float(self.ship.rect.x)

    

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.blit(self.background, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()

    

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()