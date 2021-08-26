# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Simpletest demo for MacroPad. Prints the key pressed, the relative position of the rotary
encoder, and the state of the rotary encoder switch to the serial console.
"""
import time
import math
from rainbowio import colorwheel
from adafruit_macropad import MacroPad


macropad = MacroPad()

player_turn = 1
color_counter = 0

keys = [None] * 3
for i in range(3):
    keys[i] = [None] * 3

key_colors = [None] * 3
for i in range(3):
    key_colors[i] = [None] * 3

def key_to_grid(key):
    x = (key - 3) % 3
    y = math.floor((key - 3) / 3)
    return (x, y)


def grid_to_key(x, y):
    key = (y * 3) + x + 3
    return key

def is_winner():
    winning_player = None
    if keys[0][0] == keys[1][1] and keys[1][1] == keys[2][2] and keys[1][1] != None:
        key_colors[0][0] = keys[0][0] + 10
        key_colors[1][1] += keys[1][1] + 10
        key_colors[2][2] += keys[2][2] + 10
        winning_player = keys[2][2]

    if keys[2][0] == keys[1][1] and keys[1][1] == keys[0][2] and keys[1][1] != None:
        key_colors[2][0] = keys[2][0] + 10
        key_colors[1][1] = keys[1][1] + 10
        key_colors[0][2] = keys[0][2] + 10
        winning_player = keys[1][1]

    for i in range(0, 3):
        if keys[0][i] == keys[1][i] and keys[1][i] == keys[2][i] and keys[1][i] != None:
            key_colors[0][i] = keys[0][i] + 10
            key_colors[1][i] = keys[1][i] + 10
            key_colors[2][i] = keys[2][i] + 10
            winning_player = keys[1][i]
        if keys[i][0] == keys[i][1] and keys[i][1] == keys[i][2] and keys[i][1] != None:
            key_colors[i][0] = keys[i][0] + 10
            key_colors[i][1] = keys[i][1] + 10
            key_colors[i][2] = keys[i][2] + 10
            winning_player = keys[i][1]



#for i in range(3, 12):
#    x, y = key_to_grid(i)
#    print("{} {},{}".format(i, x, y))

def update_grid():
    global color_counter
    color_counter = color_counter + 1
    for y in range(0, 3):
        for x in range(0, 3):
            key = grid_to_key(x, y)
            player = key_colors[x][y]
            if player == None:
                color = 170
            elif player == 1:
                color = 0
            elif player == 2:
                color = 340
            elif player > 10:
                color = color_counter % 255
            else:
                color = 170
            macropad.pixels[key] = colorwheel(color)


update_grid()
while True:
    key_event = macropad.keys.events.get()
    if key_event and key_event.pressed:
        key = key_event.key_number
        x, y = key_to_grid(key)
        if keys[x][y] == None and key > 3:
            keys[x][y] = player_turn
            key_colors[x][y] = player_turn
            print("{} {},{}".format(key, x, y))
            if player_turn == 1:
                player_turn = 2
            else:
                player_turn = 1

        is_winner()
    update_grid()

