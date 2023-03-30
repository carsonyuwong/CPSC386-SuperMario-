import sys
import pygame as pg
from settings import Settings
from sound import Sound
from button import Button
from level import Level
from game_data import level_0


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings(game=self)
        self.clock = pg.time.Clock()

        size = self.settings.screen_width, self.settings.screen_height
        self.screen = pg.display.set_mode(size=size)
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Super Mario Bros.")

        self.play_button = Button(game=self, msg="1 PLAYER GAME")
        self.sound = Sound(bg_music="sounds/theme.wav")

        self.level = Level(level_0, self.screen)

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_over()
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_q:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.check_play_button(mouse_x, mouse_y)

    def check_play_button(self, mouse_x, mouse_y):
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.settings.game_active:
            #pg.mouse.set_visible(False)
            self.settings.game_active = True

            self.sound.start_bg()
            self.sound.play_bg()

    def main_menu(self):
        image = pg.transform.scale(pg.image.load('images/main_menu.png'), (self.settings.screen_width, self.settings.screen_height))

        if not self.settings.game_active:
            image_rect = image.get_rect()
            image_rect.centerx = self.screen_rect.centerx
            self.screen.blit(image, image_rect)
            self.play_button.draw_button()

    def game_over(self):
        self.sound.gameover()
        self.sound.stop_bg()
        pg.mouse.set_visible(True)

    def play(self):
        while True:
            self.screen.fill(self.settings.bg_color)
            self.event_handler()

            self.main_menu()

            if self.settings.game_active:
                self.level.run()

            pg.display.flip()
            pg.display.update()
            self.clock.tick(60)


def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()
