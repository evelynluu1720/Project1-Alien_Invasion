class GameStats:
    '''Track statistics for Alien Invasion'''

    def __init__(self, ai_game):
        '''Initialize stats'''
        self.settings = ai_game.settings
        # call reset_stats() whenever player starts a new game.
        self.reset_stats()

    def reset_stats(self):
        '''Initialize stats that can change during the game'''
        self.ships_left = self.settings.ship_limit