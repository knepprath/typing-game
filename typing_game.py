#!/usr/bin/env python3

from tkinter import *
import PIL.Image
import PIL.ImageTk
import os

# Size of MacBook Air
# TODO make this dynamic
WIDTH=1366
HEIGHT=768

# Consective Magic Keystroke Count to Quit
QUIT=4

class MainWindow():
    
    def __init__(self, main):
        self.quit_counter = 1
        
        # canvas for image
        self.canvas = Canvas(main, width=WIDTH, height=HEIGHT, highlightthickness=0, bg="black")
        self.canvas.grid(row=1, column=0)

        # images
        self.my_images_dict = dict()

        # get all images, ignoring hidden files
        letter_dirs = next(os.walk('images'))[1]
        for letter_dir in letter_dirs:
            images = filter( lambda f: not f.startswith('.'), os.listdir('images/' + letter_dir))
            for image in images:
                if letter_dir in self.my_images_dict:
                    self.my_images_dict[letter_dir].append(PIL.ImageTk.PhotoImage(PIL.Image.open("images/" + letter_dir + "/" + image)))
                else:
                    self.my_images_dict[letter_dir] = [PIL.ImageTk.PhotoImage(PIL.Image.open("images/" + letter_dir + "/" + image))]
                    
        self.my_image_number = 0

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(WIDTH/2, HEIGHT/2, anchor = CENTER, image = self.my_images_dict["b"][self.my_image_number])

        # key press
        root.bind("<Key>", self.onKey)
        root.bind("<Escape>", self.quit)

    def quit(self, event=None):
            if self.quit_counter == QUIT:
                root.destroy()
            else:
                self.quit_counter += 1

    def onKey(self, event=None):
        # reset quit_counter so that accidental esc clicks don't accrue
        self.quit_counter = 1 
        
        if event.char in self.my_images_dict:
            # next image
            # BUG when changing between letters if my_image_number from previous letter is greater than what new letter contains
            self.my_image_number += 1

            # return to first image
            if self.my_image_number == len(self.my_images_dict[event.char]):
                self.my_image_number = 0

            # change image
            self.canvas.itemconfig(self.image_on_canvas, image = self.my_images_dict[event.char][self.my_image_number])


root = Tk()
root.wm_attributes('-fullscreen', 1)
root.configure(background='black')
root.config(cursor="none")

MainWindow(root)
root.mainloop()
