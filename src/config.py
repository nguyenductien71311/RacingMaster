# from future.moves import tkinter
from functools import partial
from typing import TextIO
from pygame.locals import *
from tkinter import *
from pygame import mixer as sounds, FULLSCREEN
import random
import time
import tkinter.messagebox
import tkinter.simpledialog
import pygame
import pygame_menu
from pygame_menu.themes import Theme
import os, sys
from tkinter import *
from pygame import mixer as sounds

background_sound = 0

tk = Tk()
sounds.init()

tk.title('HG')
tk.attributes("-fullscreen", True)
# tk.config(cursor='none')
tk.update()

screen_width = tk.winfo_width()
screen_height = tk.winfo_height()   # 720
print("Screen: " + str(screen_width) + " by " + str(screen_height))

NumberofPunters = 0
keypressed = False
numberofLines = 32
numberofCols = 25  # 30

row_spacing = screen_height/numberofLines  # 55  #75

myfont = ("Fixedsys", str(int(row_spacing)))

# make empty lists
horselist = []
punterlist = []

# sounds
gunSound = sounds.Sound("gun.wav")
hoovesSound = sounds.Sound("hooves.wav")
brokeSound = sounds.Sound("broke.wav")

finish_pos = 200

horse_step = (screen_width - 400)/numberofCols  # 50
horse_wait = 0.4

# setup a canvas to draw on (Must be public)
global canvas
canvas = Canvas(tk, width=screen_width,
                height=screen_height, highlightthickness=0)
