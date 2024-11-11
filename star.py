import pygame 
from pygame.sprite import Sprite

from random import randint

class Star(Sprite):
    """a class to manage bullets"""

    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.star_color



        randnumsize = randint(1,3)
        randx = randint(0, self.settings.screen_width)
        randy = randint(0, self.settings.screen_height)
        self.rect = pygame.Rect(randx,randy, randnumsize, randnumsize)

    def draw_star(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

