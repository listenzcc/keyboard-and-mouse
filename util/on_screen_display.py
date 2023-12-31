"""
File: on_screen_display.py
Author: Chuncheng Zhang
Date: 2023-12-09
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2023-12-09 ------------------------
# Requirements and constants
import os
import time
import random
import win32api
import win32con
import win32gui
import pygame as pg

from datetime import datetime
from string import ascii_letters
from rich import print, inspect
from pathlib import Path

from . import LOGGER


# %% ---- 2023-12-09 ------------------------
# Function and class
def rnd_color():
    return tuple(random.randint(100, 255) for _ in ['r', 'g', 'b'])


def now_str():
    now = datetime.now()
    lst = datetime.isoformat(now).split('.', 1)
    return '.'.join([lst[0], lst[1]])


folder = Path(__file__).parent
font_path = folder.joinpath('agave regular Nerd Font Complete Mono.ttf')


class OnScreenDisplay(object):
    pg.init()
    width = 600
    height = 400
    transparency_background = (0, 0, 0)
    framerate = 20

    clock = pg.time.Clock()

    content = dict(
        h1='h1',
        p='p1\np2',
        time='time',
        mouse_pos=(0, 0)
    )

    content_options = dict(
        default=dict(
            font=pg.font.Font(None, 45),
            color=rnd_color()
        ),
        h1=dict(
            font=pg.font.Font(font_path, 45),
            color=rnd_color()
        ),
        p=dict(
            font=pg.font.Font(font_path, 30),
            color=rnd_color()
        ),
        time=dict(
            font=pg.font.Font(font_path, 20),
            color=rnd_color()
        )
    )

    running = False

    def __init__(self):
        self._init_screen()
        LOGGER.debug(f'Initialized {self.__class__}')

    def loop(self, screen=None):
        if screen is None:
            screen = self.screen

        screen_rect = screen.get_rect()

        rect1 = pg.Rect(screen_rect.width-400,
                        screen_rect.height-300, 400, 200)

        self.running = True
        LOGGER.debug('Starts displaying loop')
        while self.running:
            self.update_content(dict(time=now_str()))

            for event in pg.event.get():
                LOGGER.debug(f'Got event: {event}')

            screen.fill(self.transparency_background)

            # ----------------------------------------
            # Render rect1
            # Render h1
            txt = self._mk_txt('h1')
            screen.blit(txt, txt.get_rect(center=rect1.midtop))

            # Render p
            txt = self._mk_txt('p')
            screen.blit(txt, txt.get_rect(center=rect1.center))

            # Render time
            txt = self._mk_txt('time')
            screen.blit(txt, txt.get_rect(center=rect1.midbottom))

            # ----------------------------------------
            pg.draw.rect(
                screen,
                (255, 0, 0),
                pg.Rect([e-50 for e in self.content['mouse_pos']], (100, 100)),
                2,
                1)

            # ----------------------------------------
            # Refresh
            pg.display.flip()
            self.clock.tick(self.framerate)

        LOGGER.debug('Stopped displaying loop')

    def update_content(self, mapping: dict = None):
        if mapping is None:
            mapping = {}
        self.content.update(mapping)

    def _mk_txt(self, name: str):
        if name not in self.content:
            LOGGER.error(f'Invalid content name: {name}.')
            return

        txt = self.content[name]

        if name in self.content_options:
            option = self.content_options[name]
        else:
            option = self.content_options['default']
            LOGGER.warning(
                f'Invalid content option name: {name}, using default instead.')

        return option['font'].render(txt, True, option['color'])

    def quit(self):
        pg.quit()

    def _init_screen(self):
        info = pg.display.Info()
        inspect(info)

        # Put my screen to the ES corner of the screen
        x = info.current_w - self.width
        y = info.current_h - self.height
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

        # screen = pg.display.set_mode((self.width, self.height), pg.NOFRAME, 32)
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.NOFRAME, 8)

        # Create layered window
        hwnd = pg.display.get_wm_info()["window"]
        l_ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        l_ex_style |= win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, l_ex_style)

        # Always on top
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd,
                                            win32api.RGB(*self.transparency_background), 0, win32con.LWA_COLORKEY)

        self.screen = screen
        LOGGER.debug(f'Initialized screen: {screen}')
        return screen


# %% ---- 2023-12-09 ------------------------
# Play ground


# %% ---- 2023-12-09 ------------------------
# Pending


# %% ---- 2023-12-09 ------------------------
# Pending
