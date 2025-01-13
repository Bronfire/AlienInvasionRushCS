import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''This is a line comment'''

    def __init__(self):
        '''Initialize the game, and create game resources.'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #self.screen = pygame.display.set_mode((1800,800)) # change this later, this is my default windowed mode
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height 
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Set the background colour.
        self.bg_color = (230, 230, 230)

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")
    
    def _ship_hit(self):
        '''Respond to the ship being hit by an alien.'''
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any bullets and aliens left over.
            self.bullets.empty()
            self.aliens.empty()

            # Create new aliens and new ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else: 
            self.game_active = False

    def _create_fleet(self):
        '''Create the fleet of aliens.'''
        # Make an alien.
        # Create aliens and keep adding aliens until there's no room left
        # Spacing between aliens is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        #self.aliens.add(alien)

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width): 
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        '''create an alien and place it in a fleet.'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        #current_x += 2 * alien_width

    def _check_alien_bottom(self):
        '''Check if any alien have reached the bottom of the screen.'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def run_game(self):
        '''Start the main loop for the game.'''
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _update_aliens(self):
        '''Update the positions of all aliens in the fleet, check if fleet is at edge, update positions.'''
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Ship hit!!!")

        # Look for aliens hitting the bottom of the screen.
        self._check_alien_bottom()

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check for any bullets that hit aliens, if so get rid of bullet and alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()


    def _check_events(self):
        '''respond to keypresses and mouse events'''
        # Watch for the keyboard and mouse events.
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

    def _check_play_button(self, mouse_pos):
        '''Start a new game when Player clicks play.'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics
            self.stats.reset_stats()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()


    def _check_keydown_events(self, event):
        '''Respond to keypresses.'''
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
            #self.ship.rect.x += 1
        elif event.key == pygame.K_LEFT:
            #self.ship.rect.x -= 1
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        '''Respond to key releases.'''
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group.'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_screen(self):
        '''update images on screen and flip to the new screen'''
        # Redraw the screen during each pass through the loop.
        #self.screen.fill(self.bg_color)
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_fleet_edges(self):
        '''Respond appriopriately if any aliens have reached an edge.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        ''' Drop the entire fleet and change the fleet's direction.'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


if __name__ == '__main__':
    # Make the game instance, run the game
    ai = AlienInvasion()
    ai.run_game()
