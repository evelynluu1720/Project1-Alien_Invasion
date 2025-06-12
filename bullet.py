import pygame # type: ignore
from pygame.sprite import Sprite # type: ignore

class Bullet(Sprite):
    '''A class to manage bullets fired from the ship'''

    def __init__(self, ai_game):
        '''Create a bullet object at the ship's current position'''
        # inherit attributes from Sprite - module that helps group related elements ...
        # ... in your game and act on all grouped elements at once
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0,0) and then set correct position
        # Build a rect from scratch using the pygame.Rect() class ...
        # ... which requires x and y coord of top left corner of the rect & width and height of rect
        self.rect = pygame.Rect(0, 0, 
                                self.settings.bullet_width, 
                                self.settings.bullet_height)
        
        # bullet will emerge from top of the ship
        self.rect.midtop = ai_game.ship.ship_rect.midtop

        # Store the bullet's position as a float - bullet will be shot upwards
        self.y = float(self.rect.y)

    def update(self):
        '''Move the bullet up the screen = decreasing y coord of the bullet'''
        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
    
    def draw_bullet(self):
        '''Draw the bullet to the screen'''
        # draw.rect(): fills the part of screen defined by the bullet's rect ...
        # ... with the color stored in self.color 
        pygame.draw.rect(self.screen, self.color, self.rect)