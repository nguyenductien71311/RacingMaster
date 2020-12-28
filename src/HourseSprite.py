from tkinter import *
from config import *

# make a horse class so it is easy to make many of them
class HorseSprite:
       def __init__(self, canvas, number, name, colour):
            self.canvas = canvas
            self.images = [PhotoImage(file="legsin.gif"),
                           PhotoImage(file="legsout.gif")]
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
            self.pos = finish_pos + \
                (numberofCols - 6 + self.price / 5) * horse_step  # start_pos
            self.current_image = 0
            row = self.number * row_spacing * 2
            self.image = canvas.create_image(
                self.pos, row, image=self.images[0])
            self.bib = canvas.create_rectangle(
                self.pos - 10, row - 5, self.pos + 10, row + 5, fill=self.colour)

        def move(self):
            # change the image to make the horse gallop
            if self.current_image == 0:
                self.current_image = 1
            else:
                self.current_image = 0
            self.canvas.itemconfig(
                self.image, image=self.images[self.current_image])
            # move some amount
            self.canvas.move(self.image, -horse_step, 0)
            self.canvas.move(self.bib, -horse_step, 0)
            self.pos -= horse_step
            hoovesSound.play()
