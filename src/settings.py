import pygame as pg

from src.contants import DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT

pg.init()
global_screen = pg.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pg.RESIZABLE)
