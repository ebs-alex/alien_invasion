import sys
from time import sleep

import pygame # type: ignore

from random import randint
from settings import Settings # type: ignore
from ship import Ship # type: ignore
from bullet import Bullet # type: ignore
from alien import Alien # type: ignore
from star import Star # type: ignore
from game_stats import GameStats # type: ignore
from button import Button # type: ignore
from scoreboard import Scoreboard # type: ignore



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

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.play_button = Button(self, "Play")
        self.sb = Scoreboard(self)

        self._create_fleet()
        

        # set the background color
        self.bg_color = (self.settings.bg_color)
        self.counter = 0

    def run_game(self):
        """Start main game loop"""
        while True:
            self._check_events()
            self._update_screen()
            if self.stats.game_active:
                self._update_bullets()
                self.ship.update()
                self._update_aliens()
            # else:
                #  self.game_over()
             


    def _check_events(self):
           #watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                     
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     mouse_pos = pygame.mouse.get_pos()
                     self._check_play_button(mouse_pos)

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

        self._check_bullet_alien_collisions()     
    
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
             for aliens in collisions.values():
                  self.stats.score += self.settings.alien_points * len(aliens)
             self.sb.prep_score()
             self.sb.check_high_score()
        if not self.aliens:
             self.bullets.empty()
             self._create_fleet()
             self.settings.increase_speed()
             self.stats.level += 1
         
    
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

    def _create_stars(self):
          for star in range(self.settings.number_stars):
            new_star = Star(self)
            self.stars.add(new_star)

    def _destroy_stars(self):
        for star in self.stars.copy():
            self.stars.remove(star)         
         
    def _render_stars(self):
        if self.counter == 1:
            self._create_stars()
        elif self.counter <= 39:
            for star in self.stars.sprites():
                star.draw_star()    
        elif self.counter == 40:
            self._destroy_stars()
            self.counter = 0

        self.counter += 1


    def _check_fleet_edges(self):
         """respond if aliens have reached edges"""
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
              
    def _change_fleet_direction(self):
        """drop entire fleet and change direciton"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_dropSpeed
        self.settings.fleet_direction *= -1
          
    def _update_aliens(self):
         """analyze and update position of all aliens"""
         self._check_fleet_edges()
         self.aliens.update()
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
              self._ship_hit()
         self._check_aliens_bottom()

    def _check_aliens_bottom(self):
         screen_rect = self.screen.get_rect()
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= screen_rect.bottom:
                   self._ship_hit()
                   break
    
    def _ship_hit(self):
         """respond to ship hit by alien"""
         #decrement ships left
         if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #reset aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            #pause for game reset
            sleep(0.5)
         else:
            self.stats.game_active = False    
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_pos):
         button_clicked = self.play_button.rect.collidepoint(mouse_pos)
         if button_clicked and not self.stats.game_active:            
            self.reset_game()
            self.stats.game_active = True
            pygame.mouse.set_visible(False)
            
    def reset_game(self):
        self.stats.reset_stats()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.settings.initialize_dynamic_settings()
        self.sb.prep_ships()
                 
    def _update_screen(self):
        # redraw the screen during each pass through the loop
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
                bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self._render_stars()
        self.sb.prep_score()
        self.sb.show_score()
        

        if not self.stats.game_active:
             self.play_button.draw_button()
        
        # Make most recently drawn screen visible
        pygame.display.flip()

    def game_over(self):
         sys.exit()

         
if __name__ == '__main__':
    # Make a game instance and run game
    ai = AlienInvasion()
    ai.run_game()