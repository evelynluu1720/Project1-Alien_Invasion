import pygame.font # type: ignore

class Button:
    '''A class to build buttons for the game'''

    def __init__(self, ai_game, msg):
        '''Initialize button attributes'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0,135,0)
        self.text_color = (255,255,255)
        # pygame render text to screen
        # None -> use default font, 48 = size of text
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''Turn msg into a rendered image and center text on the button'''
        # font.render() turns text stored in msg into an image -> store in self.msg_image
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        '''Draw blank button and then draw message'''
        # screen.fill() draw the rectangular portion of the button
        self.screen.fill(self.button_color, self.rect)
        # screen.blit() draw the text image to the screen -> pass it an image -> rect associates with the image
        self.screen.blit(self.msg_image, self.msg_image_rect)