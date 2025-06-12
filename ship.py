import pygame # type: ignore

class Ship:
    '''A class to manage the ship'''

    # ai_game: reference to the current instance of AI class
    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position'''
        # assign the screen to an attribute of Ship
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # access screen's rect (or rectangle) attribute
        # -> later can place the ship in the correct location on the screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect -> return a surface representing the ship
        self.image = pygame.image.load('images/ship2.bmp')
        # access the ship surface's rect attribute -> later use to place the ship
        self.ship_rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.ship_rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position
        self.x = float(self.ship_rect.x)

        # Movement flag - default value = ship is not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update the ship's position based on the movement flag'''
        # Update the ship x value, not the rect
        if self.moving_right and self.ship_rect.right < self.screen_rect.right:
            # self.ship_rect.x += 1
            self.x += self.settings.ship_speed
        # use if instead of elif: avoid right key being prioritized
        # top left corner of screen has coordinate of (0,0), increase as you move down or right
        if self.moving_left and self.ship_rect.left > 0:
            # self.ship_rect.x -= 1
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        # self.ship_rect.x will only keep the integer part of the position (ie. 1.5 -> 1)
        # self.x is there for the record of the float position (ie. 1.5)
        self.ship_rect.x = self.x

    def blitme(self):
        '''Draw the ship at its current location'''
        self.screen.blit(self.image, self.ship_rect)