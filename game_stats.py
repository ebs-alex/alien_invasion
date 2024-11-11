class GameStats:
    """track statistics for game"""

    def __init__(self, ai_game):
        """initalize stats"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        """inital stats"""
        self.ships_left = self.settings.ship_limit