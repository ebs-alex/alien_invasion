import sys

import pygame # type: ignore

from settings import Settings # type: ignore
from ship import Ship # type: ignore
from bullet import Bullet # type: ignore
from alien import Alien # type: ignore

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
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

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
    
    def _create_fleet(self):
        """create alien fleet"""
        # creae an alien and find the number of aliens in a row. 
        # spacing between each alien is equal to one alien width. 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        # determine the number of alein rows that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_rows = available_space_y // (2*alien_height)

        #create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        '''create an alien and place it in the row'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
         
    def _update_screen(self):
            # redraw the screen during each pass through the loop
            self.screen.fill(self.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                 bullet.draw_bullet()
            self.aliens.draw(self.screen)
            # Make most recently drawn screen visible
            pygame.display.flip()


         
if __name__ == '__main__':
    # Make a game instance and run game
    ai = AlienInvasion()
    ai.run_game()