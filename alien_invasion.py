import sys

import pygame

class AlienInvasion:
    """Overall Class to manage game assets and resources"""

    def __init__(self):
        """initialize game and create game reosurces"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start main game loop"""
        while True:
            #watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Make most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run game
    ai = AlienInvasion()
    ai.run_game()