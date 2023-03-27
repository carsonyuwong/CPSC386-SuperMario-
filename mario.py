import pygame as pg


class Mario(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        
    
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_height = -16

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_d]:
            self.direction.x = 1
        elif keys[pg.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pg.K_SPACE]:
            self.jump()
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_height

    def update(self):
        self.get_input()