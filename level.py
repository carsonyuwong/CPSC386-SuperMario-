import pygame as pg
from support import import_csv_layout, import_cut_graphics
from settings import Settings
from tiles import Tile, StaticTile
from mario import Mario
from enemy import Enemy


class Level():
    def __init__(self, level_data, surface):
        self.settings = Settings(game=self)
        self.tile_size = self.settings.tile_size
        self.display_surface = surface
        self.world_shift = 0

        mario_layout = import_csv_layout(level_data['player'])
        self.mario = pg.sprite.GroupSingle()
        self.mario_setup(mario_layout)

        blocks_layout = import_csv_layout(level_data['blocks'])
        self.blocks_sprites = self.create_tile_group(blocks_layout, 'blocks')

        deco_layout = import_csv_layout(level_data['deco'])
        self.deco_sprites = self.create_tile_group(deco_layout, 'deco')

        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

        boundry_layout = import_csv_layout(level_data['boundry'])
        self.boundry_sprites = self.create_tile_group(boundry_layout, 'boundry')

        player_layout = import_csv_layout(level_data['player'])
        self.player_sprites = self.create_tile_group(player_layout, 'player')

    def create_tile_group(self, layout, type):
        sprite_group = pg.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size

                    if type == 'blocks':
                        blocks_tile_list = import_cut_graphics('images\\blocks.png')
                        tile_surface = blocks_tile_list[int(val)]
                        sprite = StaticTile(self.tile_size, x, y, tile_surface)

                    if type == 'deco':
                        deco_tile_list = import_cut_graphics('images\\deco.png')
                        tile_surface = deco_tile_list[int(val)]
                        sprite = StaticTile(self.tile_size, x, y, tile_surface)

                    if type == 'coins':
                        coins_tile_list = import_cut_graphics('images\\coins.png')
                        tile_surface = coins_tile_list[int(val)]
                        sprite = StaticTile(self.tile_size, x, y, tile_surface)

                    if type == 'enemies':
                        sprite = Enemy(self.tile_size, x, y)

                    if type == 'boundry':
                        sprite = Tile(self.tile_size, x, y)

                    if type == 'player':
                        player_tile_list = import_cut_graphics('images\\player.png')
                        tile_surface = player_tile_list[int(val)]
                        sprite = StaticTile(self.tile_size, x, y, tile_surface)
                    
                    sprite_group.add(sprite)

        return sprite_group
    
    def mario_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if val == '0':
                    sprite = Mario((x, y))
                    self.mario.add(sprite)

    def scroll_x(self):
        mario = self.mario.sprite
        mario_x = mario.rect.centerx
        direction_x = mario.direction.x

        if mario_x < self.settings.screen_width / 2 and direction_x < 0:
            self.world_shift = 4
            mario.current_speed = 0
        elif mario_x > self.settings.screen_width - (self.settings.screen_width / 2) and direction_x > 0:
            self.world_shift = -4
            mario.current_speed = 0
        else:
            self.world_shift = 0
            mario.current_speed = mario.default_speed
    
    def horizontal_movement_collision(self):
        mario = self.mario.sprite
        mario.rect.x += mario.direction.x * mario.current_speed

        for sprite in self.blocks_sprites.sprites():
            if sprite.rect.colliderect(mario.rect):
                if mario.direction.x < 0:
                    mario.rect.left = sprite.rect.right
                    mario.on_left = True
                    self.current_x = mario.rect.left
                elif mario.direction.x > 0:
                    mario.rect.right = sprite.rect.left
                    mario.on_right = True
                    self.current_x = mario.rect.right

        if mario.on_left and (mario.rect.left < self.current_x or mario.direction.x >= 0):
            mario.on_left = False
        if mario.on_right and (mario.rect.right > self.current_x or mario.direction.x <= 0):
            mario.on_right = False

    def vertical_movement_collision(self):
        mario = self.mario.sprite
        mario.apply_gravity()

        for sprite in self.blocks_sprites.sprites():
            if sprite.rect.colliderect(mario.rect):
                if mario.direction.y > 0:
                    mario.rect.bottom = sprite.rect.top
                    mario.direction.y = 0
                    mario.on_ground = True
                elif mario.direction.y < 0:
                    mario.rect.top = sprite.rect.bottom
                    mario.direction.y = 0
                    mario.on_ceiling = True

            if mario.on_ground and mario.direction.y < 0 or mario.direction.y > 1:
                mario.on_ground = False
            if mario.on_ceiling and mario.direction.y > 0:
                mario.on_ceiling = False

    def enemy_collision_reverse(self):
        for enemy in self.enemies_sprites.sprites():
            if pg.sprite.spritecollide(enemy, self.boundry_sprites, False):
                enemy.reverse()

    def check_enemy_collision(self):
        enemy_collisions = pg.sprite.spritecollide(self.mario.sprite, self.enemies_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                mario_bottom = self.mario.sprite.rect.bottom
                if enemy_top < mario_bottom < enemy_center and self.mario.sprite.direction.y >= 0:
                    self.mario.sprite.direction.y = -10
                    enemy.kill()
                else:
                    print("touch")
    
    def run(self):
        self.deco_sprites.update(self.world_shift)
        self.deco_sprites.draw(self.display_surface)

        self.blocks_sprites.update(self.world_shift)
        self.blocks_sprites.draw(self.display_surface)

        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        self.player_sprites.update(self.world_shift)
        self.player_sprites.draw(self.display_surface)

        self.enemies_sprites.update(self.world_shift)
        self.boundry_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.check_enemy_collision()
        self.enemies_sprites.draw(self.display_surface)

        self.mario.update()
        self.mario.draw(self.display_surface)

        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()