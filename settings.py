class Settings:
    '''A class to store all settings for Alien Invasion'''

    def __init__(self):
        '''Initialize the game settings'''
        
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800

        # Set background color, black as default
        # colors in Pygame are specified as RGB colors (red-green-blue), ranging from 0 to 255
        self.bg_color = (230,230,230)

        # Ship settings
        self.ship_speed = 1.5 # 1.5 pixels on each pass through the loop

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3