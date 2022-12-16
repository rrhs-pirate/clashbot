import cv2
import pyautogui
import keyboard
import mss
import os
import numpy as np
from random import choice, randint
import time

state = 'home'

def get_screen_loc():
    print('Move mouse to top left and press a')
    keyboard.wait('a')
    mouse_pos = pyautogui.position()
    return {
        'left': mouse_pos[0],
        'top': mouse_pos[1],
        'width': 450,
        'height': 700
    }

def move_mouse_to(screen, coord):
    origx = screen['left']
    origy = screen['top']

    pyautogui.moveTo((origx + coord[0], origy + coord[1]))


def play():
    global state
    screen = get_screen_loc()

    with mss.mss() as sct:
        screen_shot = sct.grab(screen)

    screen_shot = np.array(screen_shot)

    screen_shot = screen_shot[:,:,:3]
    screen_shot = screen_shot.copy()

    while state == 'home':
        needle = cv2.imread(os.path.join('.', 'images', 'start.png'))

        height, width = needle.shape[:2]

        match = cv2.matchTemplate(screen_shot, needle, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(match)

        if max_val >= 0.8:
            move_mouse_to(screen, (max_loc[0] + width // 2, max_loc[1] + height // 2))
            pyautogui.click()
            print('[ + ] Battle Button Found...')
            state = 'loading'

    while state == 'loading':
        needle = cv2.imread(os.path.join('.', 'images', 'searching.png'))
        match = cv2.matchTemplate(screen_shot, needle, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(match)

        if max_val < 0.5:
            state = 'playing'
        else:
            print('[ - ] Loading...')

    while state == 'playing':
        choices = ['1', '2', '3', '4']
        needle = cv2.imread(os.path.join('.', 'images', 'elixer.png'))
        match = cv2.matchTemplate(screen_shot, needle, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(match)

        if max_val > 0.5:
            print('[ + ] Battling')

            pyautogui.press(choice(choices))
            pyautogui.moveTo((randint(1450, 1550), randint(550, 600)))
            time.sleep(0.1)
            pyautogui.click()
        else:
            print('[ + ] GAME OVER')
            return

play()