import pygame # type: ignore
from pygame.sprite import Sprite # type: ignore

class Ship(Sprite):
    '''A class to manage the ship'''

    # ai_game: reference to the current instance of AI class
    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position'''
        super().__init__()
        # assign the screen to an attribute of Ship
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # access screen's rect (or rectangle) attribute
        # -> later can place the ship in the correct location on the screen
        # ai_game: instance - connect with main.py when this instance is created in main file
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect -> return a surface representing the ship
        self.image = pygame.image.load('images/ship2.bmp')
        # access the ship surface's rect attribute -> later use to place the ship
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)

        # Movement flag - default value = ship is not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update the ship's position based on the movement flag'''
        # Update the ship x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.x += 1
            self.x += self.settings.ship_speed
        # use if instead of elif: avoid right key being prioritized
        # top left corner of screen has coordinate of (0,0), increase as you move down or right
        if self.moving_left and self.rect.left > 0:
            # self.rect.x -= 1
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        # self.rect.x will only keep the integer part of the position (ie. 1.5 -> 1)
        # self.x is there for the record of the float position (ie. 1.5)
        self.rect.x = self.x

    def blitme(self):
        '''Draw the ship at its current location'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center the ship on the screen'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)