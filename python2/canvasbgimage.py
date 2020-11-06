from Tkinter import *
from PIL import Image, ImageTk

root = Tk()
w = Canvas(root, width=300, height=300)

im = Image.open("Lenna.png")

photo = ImageTk.PhotoImage(im)
w.create_image(100, 100, image=photo, anchor=CENTER)
w.create_text(100, 240, font=("Arial",16), text="Hello", fill="red")
w.create_text(100, 270,  font=("Arial",16), text="world!", fill="blue")
w.pack()
root.mainloop()
