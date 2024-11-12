import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """initialize ship and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image and rect
        self.image = pygame.image.load('images/spaceship.png')
        self.rect = self.image.get_rect()

        # Start each new ship at botoom center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a float value for ships horizontal position
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """update the ships postions based on movement flag"""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        # update recet object from self.x
        self.rect.x = self.x

    def center_ship(self):
        """recenter ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)