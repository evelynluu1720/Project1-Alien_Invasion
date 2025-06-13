import sys
from time import sleep

import pygame # type: ignore

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize the game, create game resources'''

        # Initialize the background settings Pygame needs to work properly
        pygame.init()

        # create an instance of the class Clock, to control frame rate of the game
        # ensure clock ticks once on each pass through main loop
        # -> calculate amount of time to pause so that game runs at consistent rate
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Full screen mode
        # pygame.FULLSCREEN: figure out a window size that will fill the screen
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Create a display window, (1200,800) is the dimensions of game window
        # 1200 pixels wide by 800 pixels high
        # the object we assign to self.screen is a surface - game elements can be display

        # Custom mode
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height)
        # )
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics & create scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Call the ship - arg self refers to the current instance of AI
        # -> give access to the game's resources (ie. screen object)
        self.ship = Ship(self)

        # create a group that holds the bullets & fleet of aliens
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Start Alien Invasion in active state
        self.game_active = True

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # Make the Play button
        self.play_button = Button(self, 'Play')

    def run_game(self):
        '''Start the main loop for the game'''

        while True:
            # adding a helper method
            self._check_events()

            if self.game_active: # is True
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            # make the clock tick at the end of a while loop
            # frame rate for the game <- Python makes the loop run 60 times per second
            self.clock.tick(60)

    def _check_events(self):
        '''Respond to keypresses and mouse events'''
        # event = an action that user performs while playing (press a key or mouse moving)
        # the for loop below is an event loop
        # pygame.event.get() -> access the events that Pygame detects
        # -> returns list of events that was done since last time function was called
        for event in pygame.event.get():
            # pygame.QUIT = player clicks the window's close button
            if event.type == pygame.QUIT:
                # call sys.exit() to exit the game
                sys.exit()
            # press key - this pair will allow continuous motion
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # release key
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # detect when player clicks anywhere on the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # return mouse cursor's x and y coord
                mouse_pos = pygame.mouse.get_pos() 
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''Start a new game when player clicks Play'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        # check whether point of mouse click overlaps region defined by Play button's rect
        # clicks to Play button only works when Play button is visible
        if button_clicked and not self.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_settings()

            # Reset game statistics
            self.stats.reset_stats()
            self.sb.prep_score() # reset to 0
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Get rid of remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        '''Respond to key presses'''
        # check whether key pressed is right arrow key
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        # can use elif here because each event is connected to only one key - keydown
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # press Q for quit
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''Respond to key releases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''Create a new bullet and ad it to the bullets group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            # add() is similar to append() but specifically for Pygame groups
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''Update position of bullets and get rid of old bullets'''
        # Update bullet positions - when calls update() on a group 
        # -> automatically calls update() for each sprite in the group
        self.bullets.update()
        # Get rid of bullets that have disappeared
        # we can't remove items from a list or group within a for loop -> have to loop over a copy
        # -> free to modify the bullet group
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # check for number of bullets on screen
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check for any bullets that have hit aliens -> get rid of bullet and alien
        # this code compares positions of all bullets & aliens -> identifies overlap
        # if an overlap exists -> a key-value pair added to dictionary it returns
        # False True = after collision, bullet doesn't disappear (False) alien disappears (True)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

        # collisions is a dict: {bullet_hit: [alien 1, alien 2, alien 3]}
        if collisions:
            # loop through list of values, add points for each alien hit
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # When current alien fleet destroyed -> destroy existing bullets and create a new fleet
        # Check if alien group is empty
        if not self.aliens:
            # remove bullets
            self.bullets.empty()
            # fills screen with new alien fleet
            self._create_fleet()
            # Increase game speed when last alien been shot down
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        '''Check if the fleet is at an edge, then update positions'''
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        # function takes 2 arg: a sprite and a group, 
        # - looking for any member of group colliding with the sprite
        # - stop looping through the group as soon as it finds one collision
        # - if no collisions -> return None -> if block doesnt get executed
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting bottom of screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        '''Create the fleet of aliens'''
        # Create an alien and keep adding until there's no room left
        # Spacing between aliens is one alien width and one alien height
        # Make an alien
        alien = Alien(self)

        # grab alien's width and height from size attribute of an alien rect
        alien_width, alien_height = alien.rect.size # tuple (w,h)
        # set xy coord for first alien
        current_x, current_y = alien_width, alien_height

        # as long as space left is larger than one alien width -> can add 1 more
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finished a row, starting to draw first alien of next row
            # Hence, x coord returns to initial position, y coord move 1 row down
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        '''Create an alien and place it in the row'''
        new_alien = Alien(self)
        new_alien.x = x_position
        # position new alien's rect at this same x value
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        # add new alien to the fleet
        self.aliens.add(new_alien)
        
    def _check_fleet_edges(self):
        '''Respond appropriately if any aliens have reached an edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Drop the fleet and change its direction'''
        for alien in self.aliens.sprites():
            # Move down so y coord increase
            alien.rect.y += self.settings.fleet_drop_speed
        # Change direction -> multiple by (-1)
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        '''Respond to the ship being hit by an alien'''
        if self.stats.ships_left > 0:
            # Player loses one life -> Decrement ships_left & update scoreboard
            self.stats.ships_left -= 1
            # update display of ship images when player loses a ship
            self.sb.prep_ships()

            # Get rid of remaining bullets and aliens
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause game for (second) when ship is hit
            sleep(0.5)
        else:
            self.game_active = False
            # set_visible() -> tell Pygame to hide / show cursor
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        '''Check if any aliens have reached the bottom of the screen'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        '''Update images on the screen and flip to the new screen'''
        # Redraw the screen during each pass through the loop
        # .fill() -> fill the screen with background color, acts on a surface and takes one arg (a color)
        self.screen.fill(self.settings.bg_color)

        # each bullet is drawn to the screen
        # bullets.sprites(): return a list of all sprites in the group bullets
        # to draw all bullets -> loop through the sprites in <bullets> ...
        # ... and call draw_bullet() on each one
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Call blitme() -> draw image of ship at bottom center of screen
        self.ship.blitme()

        # draw() on a group -> each element is drawn at the position defined by its rect attribute
        # draw() requires a surface on which to draw the elements
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        # continually updates display to show new positions of game elements & hide old ones
        # -> create illusion of smooth movement
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    # if block: it only runs if the file is called directly
    ai = AlienInvasion()
    ai.run_game()