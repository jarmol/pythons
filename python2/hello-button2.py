#!/usr/bin/python

from Tkinter import *
import tkMessageBox

class App:

    def __init__(self, master):

        master.geometry("250x100+50+50")
        master.title("Otsikko")
        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

#    def say_hi(self):
#        print "hi there, everyone!"

    def say_hi(self):
        tkMessageBox.showinfo( "Hello Python", "Hello World")

root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
