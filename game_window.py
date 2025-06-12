import sys
import pygame # type: ignore

from settings import Settings
from ship import Ship

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

        # Call the ship - arg self refers to the current instance of AI
        # -> give access to the game's resources (ie. screen object)
        self.ship = Ship(self)

        # Set background color, black as default
        # colors in Pygame are specified as RGB colors (red-green-blue), ranging from 0 to 255
        self.bg_color = (230, 230, 230)

    def run_game(self):
        '''Start the main loop for the game'''

        while True:
            # adding a helper method
            self._check_events()
            self.ship.update()
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

    def _check_keyup_events(self, event):
        '''Respond to key releases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        '''Update images on the screen and flip to the new screen'''
        # Redraw the screen during each pass through the loop
        # .fill() -> fill the screen with background color, acts on a surface and takes one arg (a color)
        self.screen.fill(self.settings.bg_color)

        # Call blitme() -> draw image of ship at bottom center of screen
        self.ship.blitme()

        # Make the most recently drawn screen visible
        # continually updates display to show new positions of game elements & hide old ones
        # -> create illusion of smooth movement
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    # if block: it only runs if the file is called directly
    ai = AlienInvasion()
    ai.run_game()