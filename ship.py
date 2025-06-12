import pygame # type: ignore

class Ship:
    '''A class to manage the ship'''

    # ai_game: reference to the current instance of AI class
    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position'''
        # assign the screen to an attribute of Ship
        self.screen = ai_game.screen
        # access screen's rect (or rectangle) attribute
        # -> later can place the ship in the correct location on the screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect -> return a surface representing the ship
        self.image = pygame.image.load('images/ship.bmp')
        # access the ship surface's rect attribute -> later use to place the ship
        self.ship_rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.ship_rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        '''Draw the ship at its current location'''
        self.screen.blit(self.image, self.ship_rect)