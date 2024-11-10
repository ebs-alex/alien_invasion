import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """a class representing a single alien in the fleet"""

    def __init__(self,ai_game):
        """initialize the alien and set its starting postion"""
        super().__init__()
        self.screen = ai_game.screen

        #load the alein image and set rect attributes
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #start new alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the aleins exact horizontal postion
        self.x = float(self.rect.x)

