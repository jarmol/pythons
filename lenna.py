# -*- coding: utf-8 -*-

import Tkinter as tk
from PIL import Image
from PIL import ImageTk

try:
    original = Image.open("Lenna.png")
except:
    print "Unable to load image"

original = original.resize((160, 160), Image.ANTIALIAS)

master = tk.Tk()
master.title("Python Imaging")

tk.Label(text="LENNA", fg="red", pady=5).pack()

photo = ImageTk.PhotoImage(original)
tk.Label(image=photo).pack()

separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=5)

tk.Label(text='\"Lenna\" by Original full portrait: \
        \n\"Playmate of the Month\". \
        \nPlayboy Magazine. November 1972, photographed by Dwight Hooker.\n \
        This 512x512 electronic/mechanical scan of a section of the full portrait: \
        \nAlexander Sawchuk and two others[1] \
        \nThe USC-SIPI image database. Via Wikipedia \
        \nhttp://en.wikipedia.org/wiki/File:Lenna.png', fg="blue").pack()

tk.mainloop()
