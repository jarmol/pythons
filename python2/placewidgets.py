from Tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.geometry("250x300+200+200")
root.title("Python Background Image")
wi = 240 
w = Canvas(root, width=300, height=300)

im = Image.open("Lenna.png")

photo = ImageTk.PhotoImage(im)
w.create_image(100, 100, image=photo, anchor=CENTER)
w.create_text(100, 200, font=("Arial",16), text="Hello", fill="red")
w.create_text(100, 220,  font=("Arial",16), text="world!", fill="blue")
#w.pack(fill=BOTH)
w.place(anchor=NW, relwidth=1, relheight=1)
topframe = Frame(root).place(rely=0, relheight=0.1, relwidth=1)
midframe = Frame(root).place(rely=0.1, relheight=0.1, relwidth=1)
botframe = Frame(root).place(rely=0.2, relheight=0.1, relwidth=1)

Label(topframe, text="Label 1 ", fg="red").place(relx=0, rely=0, relwidth=0.25)
Label(midframe, text="Label 2 ", fg="red").place(relx=0, rely=0.1, relwidth=0.25)
Label(botframe, text="Label 3 ", fg="red").place(relx=0, rely=0.2, relwidth=0.25)
e1 = Entry(topframe).place(relx=0.3, rely=0)
e2 = Entry(midframe).place(relx=0.3, rely=0.1)
e3 = Entry(botframe).place(relx=0.3, rely=0.2)

button1 = Button(root, text="nappula").pack(side=BOTTOM)

root.mainloop()
