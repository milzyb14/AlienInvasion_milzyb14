import pygame 
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        
        # Load the alien image and set its rect attribute.
        alien_path = Path('Assets/images/alien.bmp')
        self.image = pygame.image.load(alien_path)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = x
        self.rect.y = y

        # Store the alien's exact horizontal position.
    
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the alien right or left."""
        self.y += self.settings.alien.speed
        self.rect.y = self.y
