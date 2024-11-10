import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall Class to manage game assets and resources"""

    def __init__(self):
        """initialize game and create game reosurces"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # set the background color
        self.bg_color = (self.settings.bg_color)

    def run_game(self):
        """Start main game loop"""
        while True:
            self._check_events()
            self._update_screen()
            self.ship.update()
            self._update_bullets()
             


    def _check_events(self):
           #watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                     
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """respond to =key releases"""
        if event.key == pygame.K_RIGHT:
            # Move ship to the right
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            # Move ship to the left
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """respond to =key releases"""
        if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False     
        if event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    def _fire_bullet(self):
         """create a new bullet and add it to the bullets group"""
         if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update postion of bullets and get rid of old bullets"""
        self.bullets.update()

        # Get rid of bullets that have dissapeared
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                        self.bullets.remove(bullet)
        #print(len(self.bullets))         
         

    def _update_screen(self):
            # redraw the screen during each pass through the loop
            self.screen.fill(self.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                 bullet.draw_bullet()
            # Make most recently drawn screen visible
            pygame.display.flip()


         
if __name__ == '__main__':
    # Make a game instance and run game
    ai = AlienInvasion()
    ai.run_game()