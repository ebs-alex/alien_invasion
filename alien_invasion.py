import sys

import pygame

from settings import Settings

class AlienInvasion:
    """Overall Class to manage game assets and resources"""

    def __init__(self):
        """initialize game and create game reosurces"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # set the background color
        self.bg_color = (self.settings.bg_color)

    def run_game(self):
        """Start main game loop"""
        while True:
            #watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # redraw the screen during each pass through the loop
            self.screen.fill(self.bg_color)

            #Make most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run game
    ai = AlienInvasion()
    ai.run_game()