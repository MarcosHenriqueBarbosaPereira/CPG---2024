import os

import pygame as pg

from src.game import WeedReaper

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window
screen = pg.display.set_mode((1270, 720), pg.RESIZABLE)  # Set the screen size
bg = pg.image.load("src/assets/img/menu-background.png")  # Load the background image


def load_options(opt: list):
    for i, option in enumerate(opt):
        button = pg.Rect(screen.get_width() / 2, 300 + i * 100, 0, 0)
        pg.draw.rect(screen, (0, 0, 0), button)
        font = pg.font.Font("src/assets/fonts/EaseOfUse.ttf", 50)
        text = font.render(option, True, (255, 255, 255))
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

    mouse_pos = pg.mouse.get_pos()
    for i, option in enumerate(opt):
        button = pg.Rect(screen.get_width() / 2 - 100, 300 + i * 100, 200, 50)
        if button.collidepoint(mouse_pos):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            break
    else:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


def main_menu():
    """ Main Menu Screen """
    pg.display.set_caption("Menu")
    menu_options = ['Start Game', 'Options', 'Quit']

    while True:
        screen.blit(bg, (0, 0))
        logo = pg.image.load("src/assets/img/weedreaper-logo.png")
        screen.blit(logo, (screen.get_width() / 2 - logo.get_width() / 2, 100))

        load_options(menu_options)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # Check for left mouse button click
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                for i, option in enumerate(menu_options):
                    button = pg.Rect(screen.get_width() / 2 - 100, 300 + i * 100, 200, 50)
                    if button.collidepoint(mouse_pos):
                        if option == 'Start Game':
                            start_game()
                        elif option == 'Options':
                            pass
                        elif option == 'Quit':
                            pg.quit()
                            quit()

        pg.display.update()


def start_game():
    """ Start the game """
    game = WeedReaper("Weed Reaper", 600, 800)
    game.main_loop()



if __name__ == '__main__':
    main_menu()
