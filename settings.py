class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """initialize game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)

        # Ship Settings
        self.ship_speed = 2.0
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 9.0
        self.bullet_width = 2
        self.bullet_height = 45
        self.bullet_color = (8,96,168)
        self.bullets_allowed = 1

        #alien settings
        self.alien_speed = 1.0
        self.fleet_dropSpeed = 10
        #fleet_direction of 1 represents rightward movement, -1 leftward
        self.fleet_direction = 1

        #star settings
        self.star_color = (230,230,230)
        self.number_stars = 40