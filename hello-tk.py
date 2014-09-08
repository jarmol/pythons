#!/usr/bin/python

from Tkinter import *

root = Tk()
root.geometry("200x100+40+40")
root.title("Otsikko")
w = Label(root, text="Hello, world!")
w.pack()

root.mainloop()
