import sys
import pygame # type: ignore

from settings import Settings

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

        # Create a display window, (1200,800) is the dimensions of game window
        # 1200 pixels wide by 800 pixels high
        # the object we assign to self.screen is a surface - game elements can be display
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Set background color, black as default
        # colors in Pygame are specified as RGB colors (red-green-blue), ranging from 0 to 255
        self.bg_color = (230, 230, 230)

    def run_game(self):
        '''Start the main loop for the game'''

        while True:
            # Watch for key board and mouse events
            # event = an action that user performs while playing (press a key or mouse moving)
            # the for loop below is an event loop
            # pygame.event.get() -> access the events that Pygame detects
            # -> returns list of events that was done since last time function was called
            for event in pygame.event.get():
                # pygame.QUIT = player clicks the window's close button
                if event.type == pygame.QUIT:
                    # call sys.exit() to exit the game
                    sys.exit()

            # Redraw the screen during each pass through the loop
            # .fill() -> fill the screen with background color, acts on a surface and takes one arg (a color)
            self.screen.fill(self.settings.bg_color)

            # Make the most recently drawn screen visible
            # continually updates display to show new positions of game elements & hide old ones
            # -> create illusion of smooth movement
            pygame.display.flip()

            # make the clock tick at the end of a while loop
            # frame rate for the game <- Python makes the loop run 60 times per second
            self.clock.tick(60)

if __name__ == '__main__':
    # Make a game instance and run the game
    # if block: it only runs if the file is called directly
    ai = AlienInvasion()
    ai.run_game()