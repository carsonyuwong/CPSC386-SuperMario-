import pygame as pg
from tiles import Tile
from settings import Settings


class Level:
    def __init__(self, level_data, surface):
        self.settings = Settings(game=self)

        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = -1

    def setup_level(self, layout):
        self.tiles = pg.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index * self.settings.tile_size
                    y = row_index * self.settings.tile_size
                    tile = Tile((x, y), self.settings.tile_size)
                    self.tiles.add(tile)

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)