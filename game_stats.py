class GameStats:
    '''Track statistics for Alien Invasion'''

    def __init__(self, ai_game):
        '''Initialize stats'''
        self.settings = ai_game.settings
        # call reset_stats() whenever player starts a new game.
        self.reset_stats()

        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        '''Initialize stats that can change during the game'''
        self.ships_left = self.settings.ship_limit
        # Track game's score in real time -> display high score, level, number of ships remaining
        # Reset score each time new game starts
        self.score = 0
        self.level = 1