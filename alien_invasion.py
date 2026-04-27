"""
Main module for AlienInvasion_milzyb14.
Author: Myles Buchanan
Purpose: Main game loop and initialization for Alien Invasion game.
Starter code from: https://github.com/RedBeard41/alien_Invasion_starter.git
Date: 04/26/2026

Asset Attribution:
- Laser sound: "Short Laser Gun Shot" from Mixkit
  https://mixkit.co/free-sound-effects/laser/
- Impact sound: "Arcade Space Shooter Dead Notification" from Mixkit
  https://mixkit.co/free-sound-effects/game/
- Font: VT323 by Peter Hull (Google Fonts)
  https://fonts.google.com/specimen/VT323
- Background image: NASA Artemis II mission imagery
  https://images-assets.nasa.gov/image/art002e009301/art002e009301~medium.jpg
- Background music: "Space Ambient" by Leberch
  https://pixabay.com/music/ambient-space-ambient-509783/
"""

import sys
from time import sleep

import pygame
from pathlib import Path
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")
        
        # Create an instance to store game statistics
        #        create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

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

        # Load custom sound effects
        self.laser_sound = pygame.mixer.Sound(
            Path('Assets/sound/mixkit-short-laser-gun-shot-1670.wav')
        )
        self.impact_sound = pygame.mixer.Sound(
            Path('Assets/sound/mixkit-arcade-space-shooter-dead-notification-272.wav')
        )
        self.laser_sound.set_volume(0.3)
        self.impact_sound.set_volume(0.2)
        # Load background music
        pygame.mixer.music.load(
            Path('Assets/sound/leberch-space-ambient-509783.mp3')
        )
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # -1 means loop forever

        # Start Alien Invasion in an inactive state. 
        self.game_active = False
         # Make play button.
        self.play_button = Button(self, "Play")
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
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

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.laser_sound.play()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.impact_sound.play()
            self.sb.prep_score()
            self.sb.check_high_score()

        # If all aliens gone, start a new level. 
        if not self.aliens:
        # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

        # Increase level. 
            self.stats.level += 1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_aliens(self):
        """Update positions of all aliens and check ship collisions."""
        self.aliens.update()
        # Check alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Check for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
        # Decrement ships left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
        # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
        # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            self._show_game_over()

    def _show_game_over(self):
        """Display a game over message."""
        font_path = Path('Assets/Fonts/VT323/VT323-Regular.ttf')
        game_over_font = pygame.font.Font(font_path, 120)
        text = game_over_font.render("GAME OVER", True,(255, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.screen_rect.center
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        sleep(1.5)
        

    def _create_fleet(self):
        """Create a custom cross shaped fleet of aliens."""
        center_x = self.settings.screen_width // 2
        center_y = 150 
        spacing = 70

        # Horizonatal arm of the cross (5 aliens) 
        for i in range(-2, 3):
            self._create_alien(center_x + (i * spacing), center_y)

        # Vertical arm of the cross (4 aliens, skip center - already placed)
        for i in range(-2, 3):
            if i != 0:
                self._create_alien(center_x, center_y + (i * spacing))

    def _create_alien(self, x, y):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self, x, y)
        self.aliens.add(new_alien)

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.blit(self.background, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()
        # Draw the play button if the game is inactive. 
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()