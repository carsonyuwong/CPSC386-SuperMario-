class Settings():

    def __init__(self, game):
        self.game = game
        self.game_active = False

        self.bg_color = (92, 148, 252)

        self.vertical_tile_number = 30
        self.tile_size = 16

        self.screen_height = self.vertical_tile_number * self.tile_size
        self.screen_width = 320