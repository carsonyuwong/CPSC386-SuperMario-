import pygame as pg
from tiles import Tile
from settings import Settings
from mario import Mario


class Level:
    def __init__(self, level_data, surface):
        self.settings = Settings(game=self)

        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pg.sprite.Group()
        self.mario = pg.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * self.settings.tile_size
                y = row_index * self.settings.tile_size

                if cell == 'X':
                    tile = Tile((x, y), self.settings.tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    mario_sprite = Mario((x, y))
                    self.mario.add(mario_sprite)

    def scroll_x(self):
        mario = self.mario.sprite
        mario_x = mario.rect.centerx
        direction_x = mario.direction.x

        if mario_x < self.settings.screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            mario.speed = 0
        elif mario_x > self.settings.screen_width - (self.settings.screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            mario.speed = 0
        else:
            self.world_shift = 0
            mario.speed = 8

    def horizontal_movement_collision(self):
        mario = self.mario.sprite
        mario.rect.x += mario.direction.x * mario.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(mario.rect):
                if mario.direction.x < 0:
                    mario.rect.left = sprite.rect.right
                elif mario.direction.x > 0:
                    mario.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        mario = self.mario.sprite
        mario.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(mario.rect):
                if mario.direction.y > 0:
                    mario.rect.bottom = sprite.rect.top
                    mario.direction.y = 0
                elif mario.direction.y < 0:
                    mario.rect.top = sprite.rect.bottom
                    mario.direction.y = 0

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        self.mario.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.mario.draw(self.display_surface)