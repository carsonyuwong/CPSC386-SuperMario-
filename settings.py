class Settings():

    def __init__(self, game):
        self.game = game
        self.game_active = False

        self.bg_color = (107, 140, 255)

        self.level_map = [
        '                            ',
        '       XXXXX                ',
        '                            ',
        '                 XXXXX      ',
        '                            ',
        '                            ',
        '                    XXXX    ',
        '           XX               ',
        '                            ',
        '  P                         ',
        'XXXXXXXX  XXXXXX  XX  XXXX  ']

        self.tile_size = 64
        self.screen_width = 744
        self.screen_height = len(self.level_map) * self.tile_size