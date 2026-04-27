"""
Button module for AlienInvasion_milzyb14.
Author: Myles Buchanan
Purpose: Manages the play button for the game.
Starter code from: https://github.com/RedBeard41/alien_Invasion_starter.git
Date: 04/12/2026


Asset Attribution:
- Font: VT323 by The VT323 Project Authors
Source: https://fonts.google.come/specimen/VT323
License: Open Font License (OFL)
"""
import pygame.font
from pathlib import Path

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 250, 80 
        self.button_color = (20, 20, 60)
        self.border_color = (0, 255, 255)
        self.text_color = (255, 255, 255)
        font_path = 'Assets/Fonts/VT323/VT323-Regular.ttf'
        self.font = pygame.font.Font(font_path, 48)

        # Use custom VT323 font
        font_path = Path('Assets/Fonts/VT323/VT323-Regular.ttf')
        self.font = pygame.font.Font(font_path, 64)

        # Build the button's rect object and center it. 
        self.rect = pygame.Rect(0, 0, self.width + 8, self.height + 8)
        self.rect.center = self.screen_rect.center

        # Create the border rect (slightly bigger than button)
        self.border_rect = pygame.Rect(0, 0, self.width, self.height)
        self.border_rect.center = self.rect.center

        # The button message needs to be prepped only once. 
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center   

    def draw_button(self):
        """Draw blank button and then draw message."""
        # Draw outter border
        self.screen.fill(self.border_color, self.border_rect)
        # Draw inner button
        self.screen.fill(self.button_color, self.rect)
        # Draw message
        self.screen.blit(self.msg_image, self.msg_image_rect)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 3)
