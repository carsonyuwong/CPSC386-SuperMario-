import pygame as pg


class Button():
    def __init__(self, game, msg):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 250, 50
        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 48)

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.msg_image, self.msg_image_rect)