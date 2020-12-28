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

pygame.init()


# DISPLAYSURF = pygame.display.set_mode((s_w, s_h), FULLSCREEN)
DISPLAYSURF = pygame.display.set_mode((1280 , 900))
pygame.display.set_caption("Race Master")



MyTheme = Theme(
    #background_color=(56, 4, 75),
    background_color=(151, 255, 255),
    scrollbar_shadow=True,
    scrollbar_slider_color=(0, 191, 255),
    scrollbar_slider_pad=2,
    scrollbar_thick=14,
    selection_color=(200, 46, 49),
    title_background_color=(0, 191, 255),
    title_font_color=(220, 20, 60),
    title_shadow=True,
    widget_font_color=(0, 178, 191),
)

bg = []
sl = []
cast = []
help = []
try:
    f = open("shopping2.txt", "r")
    for line in f:
        sl.append(line.strip())
    f.close()
except:
    pass

try:
    g = open("cast.txt", "r")
    for m in g:
        cast.append(m.strip())
    g.close()
except:
    pass

try:
    h = open("help.txt", "r")
    for n in h:
        help.append(n.strip())
    h.close()
except:
    pass

try:
    b = open("LOGO.txt", "r")
    for i in b:
        bg.append(i.strip())
    b.close()
except:
    pass

def saveList(file):
    f = open(file, "w")
    for item in sl:
        f.write(item + "\n")
    f.close()
'''
class Player(object):
    def __init__(self, name, money, fast, slow, finishline, startline, stop, returncar):
        self.name = name
        self.money = money
        self.fast = fast
        self.slow = slow
        self.finishline = finishline
        self.startline = startline
        self.stop = stop
        self.returncar = returncar


playerlist = []
try:
    with open("saveplayerlist.txt", "r") as f:
        for line in f:
            data = line.strip().split()
            playerlist.append(Player(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
        f.close()
except:
    pass
'''
def draw_background(surface):
    anime = pygame.image.load('./assets/animebg.png')
    #background_image.draw(surface),background_image = pygame_menu.baseimage.BaseImage(image_path='nen.png')
    surface.fill((255,255,255))
    font = pygame.font.SysFont('consolas', 22)
    y = 80
    for line in bg:
        LINE = font.render(line, True, (0,250,154))
        surface.blit(LINE, (120, y))
        y = y + 10
    surface.blit(anime,(50,200))


def draw_backgroundshop(surface):
    surface.fill((255, 255, 255))
    animeshop1 = pygame.image.load('./assets/shopbg.png')
    animeshop2 = pygame.image.load('./assets/shopbg2.png')
    surface.blit(animeshop1, (0, 350))
    surface.blit(animeshop2, (1040, 350))

def draw_backgroundhelp(surface):
    surface.fill((255, 255, 255))
    animehelp = pygame.image.load('./assets/helpbg.jpg')
    surface.blit(animehelp, (950, 250))

def start_the_game():
    # Horse Race Betting game by Paul and Ben Barber
    # Based on an original game for the BBC model B, by John Barber of Ipswich Town
    # March 2016

    # Python3, can be run from IDLE or at the command line, developed under version 3.2 with pygame for sound

    # Press Esc once or maybe more to exit the game early

    # TODO

    tk = Tk()
    sounds.init()

    # make the window and canvas to draw on
    tk.title("Horse Game")
    # tk.resizable(False, False)
    # tk.attributes("-topmost", True)
    tk.attributes("-fullscreen", True)
    #tk.config(cursor='none')
    tk.update()

    screen_width = tk.winfo_width()  # 1280
    screen_height = tk.winfo_height()  # 720
    print("Screen: " + str(screen_width) + " by " + str(screen_height))

    NumberofPunters = 0
    keypressed = False
    numberofLines = 32
    numberofCols = 25  # 30

    row_spacing = screen_height / numberofLines  # 55  #75
    # start_pos = screen_width - 200  # 1000
    finish_pos = 200
    horse_step = (screen_width - 400) / numberofCols  # 50
    horse_wait = 0.4

    myfont = ("Fixedsys", str(int(row_spacing)))  # ("Arial", "32")

    # make empty lists
    horselist = []
    punterlist = []

    # sounds
    gunSound = sounds.Sound("gun.wav")
    hoovesSound = sounds.Sound("hooves.wav")
    brokeSound = sounds.Sound("broke.wav")

    # make a horse class so it is easy to make many of them
    class HorseSprite:
        def __init__(self, canvas, number, name, colour):
            self.canvas = canvas
            self.images = [PhotoImage(file="./assets/legsin.gif"), PhotoImage(file="./assets/legsout.gif")]
            # make the image bigger
            zoom_factor = 5
            self.images[0] = self.images[0].zoom(zoom_factor, zoom_factor)
            self.images[1] = self.images[1].zoom(zoom_factor, zoom_factor)
            # position it in the correct row
            self.number = number
            self.name = name
            self.colour = colour
            self.pos = 0  # start_pos
            self.current_image = 0
            self.price = 0

        def prepare_to_race(self):
            self.pos = finish_pos + (numberofCols - 6 + self.price / 5) * horse_step  # start_pos
            self.current_image = 0
            row = self.number * row_spacing * 2
            self.image = canvas.create_image(self.pos, row, image=self.images[0])
            self.bib = canvas.create_rectangle(self.pos - 10, row - 5, self.pos + 10, row + 5, fill=self.colour)

        def move(self):
            # change the image to make the horse gallop
            if self.current_image == 0:
                self.current_image = 1
            else:
                self.current_image = 0
            self.canvas.itemconfig(self.image, image=self.images[self.current_image])
            # move some amount
            self.canvas.move(self.image, -horse_step, 0)
            self.canvas.move(self.bib, -horse_step, 0)
            self.pos -= horse_step
            hoovesSound.play()

    # make a punter (player) class, there will be a few of those
    class Punter:
        def __init__(self, name):
            self.name = name
            self.total = 100  # how much money they have left # random.randint(0,100) #
            self.pick = -1  # which horse they have picked, 0-6, -1=not made a pick
            self.stake = 0  # how much they have bet on the horse+row_spacing
            self.totalwinnings = 0  # running total of all winnings
            self.numberofturns = 0  # count of how many turns this punter has

    # keypress callback, just update some global variables
    def KeyPress(event):
        global keypressed, keyevent
        keypressed = True
        keyevent = event

    # Wait for any keypress
    def WaitForKeyPress(canvas):
        global keypressed
        wait_text = canvas.create_text(screen_width / 2, screen_height - 50, text="Press any key to continue...",
                                       fill="cyan", font=myfont, justify="center")
        canvas.pack()
        keypressed = False
        while (keypressed == False):
            # wait for KeyPress to be called
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
        if (keyevent.keysym == 'Escape'):
            exit(0)
        canvas.delete(wait_text)

    # Wait for integer number to be typed, textitem is where it will be echoed as you type
    def WaitForInteger(canvas, textitem):
        global keypressed, keyevent
        string = ""
        keypressed = False
        escape_press = 0
        while True:
            while (keypressed == False):
                # wait for KeyPress to be called
                tk.update_idletasks()
                tk.update()
                time.sleep(0.01)
            # print (keyevent.char)
            if (keyevent.keysym == 'Return'):
                if (len(string) > 0):
                    return int(string)
            elif (keyevent.keysym == 'BackSpace'):
                if (len(string) > 0):
                    string = string[:-1]
                    canvas.itemconfig(textitem, text=string)
            elif (keyevent.char.isdigit()):
                string = string + keyevent.char
                # print (string)
                canvas.itemconfig(textitem, text=string)
            elif (keyevent.keysym == 'Escape'):
                escape_press = escape_press + 1
            if escape_press > 1:
                exit(0)
            keypressed = False

    # Wait for string to be typed, textitem is where it will be echoed as you type
    def WaitForString(canvas, textitem):
        global keypressed, keyevent
        string = ""
        keypressed = False
        escape_press = 0
        while True:
            while (keypressed == False):
                # wait for KeyPress to be called
                tk.update_idletasks()
                tk.update()
                time.sleep(0.01)
            if (keyevent.keysym == 'Return'):
                return string
            elif (keyevent.keysym == 'BackSpace'):
                if (len(string) > 0):
                    string = string[:-1]
                    canvas.itemconfig(textitem, text=string)
            elif (keyevent.keysym == 'Escape'):
                escape_press = escape_press + 1
            else:
                # print (keyevent.char)
                string = string + keyevent.char
                # print (string)
                canvas.itemconfig(textitem, text=string)
            if escape_press > 1:
                exit(0)
            keypressed = False

    def Initialize_characters_variables(canvas):
        # create some horse sprites
        horse = HorseSprite(canvas, 1, "Red Wold", "red")
        horselist.append(horse)
        horse = HorseSprite(canvas, 2, "Black Jet", "black")
        horselist.append(horse)
        horse = HorseSprite(canvas, 3, "Yellow Dog", "yellow")
        horselist.append(horse)
        horse = HorseSprite(canvas, 4, "Super Blue", "blue")
        horselist.append(horse)
        horse = HorseSprite(canvas, 5, "Hot Magenta", "magenta")
        horselist.append(horse)
        horse = HorseSprite(canvas, 6, "Cyan Runner", "cyan")
        horselist.append(horse)
        horse = HorseSprite(canvas, 7, "Green Flash", "green")
        horselist.append(horse)

    def DisplayCash(canvas, title="LEADER BOARD", wait=False):
        Broke = 0  # Count how many punters are broke
        # clear the scene
        canvas.delete("all")
        # draw the scene
        canvas.create_rectangle(0, 0, screen_width, screen_height, fill="white")
        canvas.create_text(screen_width / 2, row_spacing, text="--------------------------------", fill="cyan",
                           font=myfont, justify="center")
        canvas.create_text(screen_width / 2, row_spacing * 2, text="* " + title + " *", fill="magenta", font=myfont,
                           justify="center")
        canvas.create_text(screen_width / 2, row_spacing * 3, text="--------------------------------", fill="cyan",
                           font=myfont, justify="center")
        pos = row_spacing * 5
        for punter in sorted(punterlist, key=lambda punter: punter.total, reverse=True):
            message = punter.name + " has £" + str(punter.total)
            canvas.create_text(screen_width / 2, pos, text=message, fill="Yellow", font=myfont, justify="center")
            pos = pos + row_spacing * 2
            if (punter.total <= 0):
                Broke = Broke + 1
        canvas.pack()
        tk.update()
        if (wait):
            WaitForKeyPress(canvas)
        return Broke

    def Punters(canvas):
        DisplayCash(canvas, title="HORSE RACING GAME")
        question = canvas.create_text(screen_width / 2, screen_height - row_spacing * 4, text="How many punters?",
                                      fill="red", font=myfont, justify="center")
        answer = canvas.create_text(screen_width / 2, screen_height - row_spacing * 2, text="", fill="orange",
                                    font=myfont, justify="center")
        n = 0
        while (n < 1 or n > 8):  # minimum 1 and maximum 8 players
            n = WaitForInteger(canvas, answer)
            canvas.itemconfig(answer, text="")
        canvas.delete(question, answer)

        for i in range(1, n + 1):
            question = canvas.create_text(screen_width / 2, screen_height - row_spacing * 4,
                                          text="Punter " + str(i) + ", what is your name?", fill="red", font=myfont,
                                          justify="center")
            answer = canvas.create_text(screen_width / 2, screen_height - row_spacing * 2, text="", fill="orange",
                                        font=myfont, justify="center")
            name = WaitForString(canvas, answer)
            punter = Punter(name)
            punterlist.append(punter)
            canvas.delete(question, answer)
            DisplayCash(canvas, title="HORSE RACING GAME")

    def StartingPrices(canvas):
        # clear the scene
        canvas.delete("all")
        # draw the scene
        canvas.create_rectangle(0, 0, screen_width, screen_height, fill="white")
        canvas.create_text(screen_width / 2, row_spacing, text="--------------------------------", fill="red",
                           font=myfont, justify="center")
        canvas.create_text(screen_width / 2, row_spacing * 2, text="* STARTING PRICES *", fill="yellow", font=myfont,
                           justify="center")
        canvas.create_text(screen_width / 2, row_spacing * 3, text="--------------------------------", fill="red",
                           font=myfont, justify="center")
        pos = row_spacing * 5
        i = 1
        for horse in horselist:
            horse.price = random.randint(1, 6) * 5
            message = str(i) + ") " + horse.name + " " + str(horse.price) + "/1"
            canvas.create_text(screen_width / 2, pos, text=message, fill=horse.colour, font=myfont, justify="center")
            pos = pos + row_spacing * 2
            i = i + 1
        canvas.create_text(screen_width / 2, pos, text="================================", fill="red", font=myfont,
                           justify="center")
        canvas.create_text(screen_width / 2, pos + row_spacing, text="PLACE YOUR BETS", fill="yellow", font=myfont,
                           justify="center")
        canvas.create_text(screen_width / 2, pos + row_spacing * 2, text="================================", fill="red",
                           font=myfont, justify="center")
        canvas.pack()
        tk.update()

        # ask punters one by one for their bets
        for punter in punterlist:
            if punter.total <= 0:
                sorry = canvas.create_text(screen_width / 2, pos + row_spacing * 4,
                                           text=punter.name + ", you are BROKE. NO BETS!!!!", fill="dark red",
                                           font=myfont, justify="center")
                punter.pick = -1
                punter.stake = 0
                tk.update()
                brokeSound.play()
                time.sleep(3)
                canvas.delete(sorry)
            else:
                punter.numberofturns = punter.numberofturns + 1
                punter.pick = -1
                punter.stake = -1
                question1 = canvas.create_text(screen_width / 2, pos + row_spacing * 4,
                                               text=punter.name + ", you have £" + str(
                                                   punter.total) + ". Pick a horse 1-7", fill="blue", font=myfont,
                                               justify="center")
                while (punter.pick < 0 or punter.pick > 6):
                    answer1 = canvas.create_text(screen_width / 2, pos + row_spacing * 5.2, text="", fill="orange",
                                                 font=myfont, justify="center")
                    punter.pick = WaitForInteger(canvas, answer1) - 1
                    canvas.delete(answer1)
                question2 = canvas.create_text(screen_width / 2, pos + row_spacing * 7,
                                               text="How much on " + horselist[punter.pick].name + "?", fill="blue",
                                               font=myfont, justify="center")
                while (punter.stake < 0 or punter.stake > punter.total):
                    answer2 = canvas.create_text(screen_width / 2, pos + row_spacing * 8.2, text="", fill="orange",
                                                 font=myfont, justify="center")
                    punter.stake = WaitForInteger(canvas, answer2)
                    if punter.stake > punter.total:
                        sorry = canvas.create_text(screen_width / 2, pos + row_spacing * 10, text="SORRY NO CREDIT!",
                                                   fill="dark blue", font=myfont, justify="center")
                        tk.update()
                        time.sleep(1)
                        canvas.delete(sorry)
                    canvas.delete(answer2)
                canvas.delete(question1, question2)
                punter.total = punter.total - punter.stake
                print(punter.name + " placed £" + str(punter.stake) + " on " + horselist[
                    punter.pick].name + " and now has £" + str(punter.total))

    def Race(canvas):
        global keypressed, keyevent
        # clear the scene
        canvas.delete("all")
        # draw the scene
        canvas.create_rectangle(0, 0, screen_width, 7 * 2 * row_spacing + 65, fill="gray")

        canvas.create_line(finish_pos - horse_step, 1 * 2 * row_spacing - 30, finish_pos - horse_step,
                           7 * 2 * row_spacing + 65, width=5, fill="black")
        canvas.create_oval(finish_pos - horse_step - 8, 0, finish_pos - horse_step + 8, 16, width=5, fill="",
                           outline="gold")
        canvas.create_line(finish_pos - horse_step, 16, finish_pos - horse_step, 1 * 2 * row_spacing - 20, width=5,
                           fill="gold")
        canvas.create_oval(finish_pos - horse_step - 8, 7 * 2 * row_spacing + 30, finish_pos - horse_step + 8,
                           7 * 2 * row_spacing + 30 + 16, width=5, fill="", outline="gold")
        canvas.create_line(finish_pos - horse_step, 7 * 2 * row_spacing + 30 + 16, finish_pos - horse_step,
                           7 * 2 * row_spacing + 65, width=5, fill="gold")

        canvas.create_rectangle(0, 8 * 2 * row_spacing, screen_width, screen_height, fill="light green")
        pos = row_spacing * 17
        canvas.create_text(screen_width / 2, pos, text="================================", fill="red", font=myfont,
                           justify="center")
        canvas.create_text(screen_width / 2, pos + row_spacing, text="LET'S RACE", fill="yellow", font=myfont,
                           justify="center")
        canvas.create_text(screen_width / 2, pos + row_spacing * 2, text="================================", fill="red",
                           font=myfont, justify="center")
        pos = pos + row_spacing * 3
        for punter in punterlist:
            if punter.pick > -1:
                canvas.create_text(screen_width / 2, pos,
                                   text=punter.name + " bet £" + str(punter.stake) + " on " + horselist[
                                       punter.pick].name + " at " + str(horselist[punter.pick].price) + "/1",
                                   fill=horselist[punter.pick].colour, font=myfont, justify="center")
                pos = pos + row_spacing * 1.2

        for h in horselist:
            h.prepare_to_race()

        canvas.pack()
        tk.update()
        random.seed()

        WaitForKeyPress(canvas)
        gunSound.play()
        time.sleep(0.5)
        keypressed = False
        esc_pressed = 0

        # main race loop
        while True:
            # pick a random horse
            h = random.randint(0, 6)
            horse = horselist[h]
            # move that horse
            horse.move()
            # print("Horse ", horse.number, " pos ", horse.pos)
            # update the screen
            tk.update_idletasks()
            tk.update()
            # check for the winner, break from the race loop if we have one
            if horse.pos < finish_pos:
                break
            # Check for Esc
            if keypressed == True:
                if (keyevent.keysym == 'Escape'):
                    esc_pressed = esc_pressed + 1
                    keypressed = False
                if esc_pressed > 1:
                    exit(0)
                    # wait for some time
            time.sleep(horse_wait)

        # announce the winner
        winner_text = horse.name + " is the winner!"
        canvas.create_text(screen_width / 2, (h + 1) * row_spacing * 2, text=winner_text, fill=horse.colour,
                           font=myfont, justify="center")
        WaitForKeyPress(canvas)

        # return the number of the winning horse so we can calculate punter winnings next
        return h

    def Results(canvas, winning_horse_index):
        # clear the scene
        canvas.delete("all")
        # draw the scene
        canvas.create_rectangle(0, 0, screen_width, screen_height, fill="dark green")
        canvas.create_text(screen_width / 2, row_spacing, text="--------------------------------", fill="red",
                           font=myfont, justify="center")
        canvas.create_text(screen_width / 2, row_spacing * 2, text="* RESULTS *", fill="yellow", font=myfont,
                           justify="center")
        canvas.create_text(screen_width / 2, row_spacing * 3, text="--------------------------------", fill="red",
                           font=myfont, justify="center")
        pos = row_spacing * 5
        i = 0
        winning_horse = horselist[winning_horse_index]
        for punter in punterlist:
            # print("Horse index " + str(winning_horse_index) + " punter pick " + str(punter.pick))
            if punter.pick == winning_horse_index:
                winnings = punter.stake * winning_horse.price
                punter.total = punter.total + winnings + punter.stake
                punter.totalwinnings = punter.totalwinnings + winnings
                message = punter.name + " wins £" + str(winnings) + " on " + winning_horse.name
                canvas.create_text(screen_width / 2, pos, text=message, fill=winning_horse.colour, font=myfont,
                                   justify="center")
                pos = pos + row_spacing * 2
                i = i + 1

        if i == 0:
            canvas.create_text(screen_width / 2, pos, text="No winners this race...", fill=winning_horse.colour,
                               font=myfont, justify="center")

        sounds.music.load("yankee.mp3")
        sounds.music.play()
        WaitForKeyPress(canvas)
        # sounds.music.fadeout(2000)

    def Broke(canvas):
        # clear the scene
        canvas.delete("all")
        # draw the scene
        canvas.create_rectangle(0, 0, screen_width, screen_height, fill="white")
        canvas.create_text(screen_width / 2, row_spacing, text="--------------------------------", fill="cyan",
                           font=myfont, justify="center")
        canvas.create_text(screen_width / 2, row_spacing * 2, text="* GAME OVER *", fill="magenta", font=myfont,
                           justify="center")
        canvas.create_text(screen_width / 2, row_spacing * 3, text="--------------------------------", fill="cyan",
                           font=myfont, justify="center")
        pos = row_spacing * 5
        for punter in sorted(punterlist, key=lambda punter: punter.totalwinnings, reverse=True):
            bet_text = " bet" if punter.numberofturns == 1 else " bets"
            message = punter.name + " won a total of £" + str(punter.totalwinnings) + " in " + str(
                punter.numberofturns) + bet_text
            canvas.create_text(screen_width / 2, pos, text=message, fill="yellow", font=myfont, justify="center")
            pos = pos + row_spacing * 2
        canvas.create_text(screen_width / 2, screen_height - 100, text="Press any key to play again or Esc to exit.",
                           fill="blue", font=myfont, justify="center")
        sounds.music.load("yankee_slow.mp3")
        sounds.music.play()
        WaitForKeyPress(canvas)

    # HORSE-RACE MAIN CODE

    # setup a callback on any keypress for keyboard entry
    tk.bind_all('<Key>', KeyPress)

    # setup a canvas to draw on
    canvas = Canvas(tk, width=screen_width, height=screen_height, highlightthickness=0)

    # setup horses and punters
    Initialize_characters_variables(canvas)

    while True:
        Punters(canvas)

        # main game loop
        while True:
            numberbroke = DisplayCash(canvas, wait=True)
            print(str(numberbroke) + " punters are broke out of " + str(len(punterlist)))
            if numberbroke == len(punterlist):  # if everyone broke, end the game by breaking out of the game loop
                break
            StartingPrices(canvas)
            winning_horse = Race(canvas)
            print("Horse index ", winning_horse, " ", horselist[winning_horse].name, " is the winner.")
            Results(canvas, winning_horse)

        Broke(canvas)
        punterlist = []


def minigame():
    # ham
    pass


def rank():
    pass

def shop():
    y1 = 120
    y2 = 120
    #y3 = 400
    yellow = (192,255,62)
    font = pygame.font.SysFont('consolas', 30)
    textSurface = font.render("Welcome to my shop", True, yellow)
    quitshop = font.render("Press ESC to get out", True, yellow)
    draw_backgroundshop(DISPLAYSURF)
    DISPLAYSURF.blit(textSurface, (600, 50))
    DISPLAYSURF.blit(quitshop, (600, 700))
    for item in sl:
        ITEM = font.render(item, True, yellow)
        DISPLAYSURF.blit(ITEM, (400, y1))
        y1 = y1 + 40
    for money in cast:
        CAST = font.render(money, True, yellow)
        DISPLAYSURF.blit(CAST, (100, y2))
        y2 = y2 + 40
    '''for i in playerlist:
        I = font.render(i, True, yellow)
        DISPLAYSURF.blit(I, (1200, y3))
        y3 = y3 + 40'''
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    drawmenu()
                if event.key == K_1:
                    pass
                if event.key == K_2:
                    pass
                if event.key == K_3:
                    pass
                if event.key == K_4:
                    pass
                if event.key == K_5:
                    pass
                if event.key == K_6:
                    pass
        pygame.display.update()



def helping():
    y = 30
    green = (0, 250, 154)
    font = pygame.font.SysFont('consolas', 20)
    draw_backgroundhelp(DISPLAYSURF)
    for a in help:
        HELP = font.render(a, True, green)
        DISPLAYSURF.blit(HELP, (50, y))
        y = y + 40
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    drawmenu()

        pygame.display.update()



'''
MyTheme.set_background_color_opacity(0.5)
help = pygame_menu.Menu(800, 1500, 'Help', menu_position=(50, 50), theme=MyTheme)
help.add_label('_______HUONG DAN GAME RACE MASTER_______')
help.add_label('*Ban co 5,000,000VND de dat cuoc, so tien cuoc it nhat la 500,000VND, nhieu nhat la so tien ban dang co.')
help.add_label('*Khi het tien, ban co the tham gia mini game do vui de co them tien, 1 cau dung ban duoc 1,000,000VND.')
help.add_label('*Tren duong dua se co nhung chuong ngai vat nhu da hoac o ga gay can tro trong qua trinh dua.')
help.add_label('*Se co cac loai bua giup hoac gay can tro trong qua trinh choi:')
help.add_label('1: Bua nhanh-giup xe ban chay nhanh len')
help.add_label('2: Bua cham-khien xe ban chay cham lai')
help.add_label('3: Bua choang-ban se bi bat dong trong 1 vai giay')
help.add_label('4: Bua quay lui-xe ban se quay dau va chay nguoc lai trong mot vai giay va quay lai dung huong')
help.add_label('5: Bua quay ve-xe ban se quay lai vi tri xuat phat')
help.add_label('6: Bua ve dich-xe ban se lap tuc ve dich va gianh chien thang')
'''

def option():
    #
    pass


def drawmenu():
    #MyTheme.set_background_color_opacity(0.5)
    menu = pygame_menu.Menu(500, 500, 'RACING', menu_position=(90, 70), theme=MyTheme)

    #menu.add_text_input('Player:', default=' ')
    menu.get_input_data(recursive=True)
    menu.add_button('Play game', start_the_game)
    menu.add_button("Mini Game", minigame)
    menu.add_button("Ranking", rank)
    menu.add_button("Shop", shop)
    menu.add_button("Option", option)
    menu.add_button("Help", helping)
    #menu.add_button(help.get_title(), help)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.center_content()
    sounds.music.load("menu.wav")
    sounds.music.play()
    menu.mainloop(surface=DISPLAYSURF, bgfun=partial(draw_background, DISPLAYSURF), fps_limit=120)



def main():

    drawmenu()



main()
