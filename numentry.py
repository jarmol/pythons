from Tkinter import *
from PIL import Image, ImageTk
import datetime

def cdegtofdeg():
    content3.set(datetime.datetime.now())
    text = content.get()
    try:
        if text:
            value = 9.0*float(text)/5.0 +32.0
            content2.set("%.2f" % value)
    except ValueError:
        content2.set("Virhe!")
        return None

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

Label(topframe, text="C degr", fg="red").place(relx=0, rely=0, relwidth=0.25)
Label(midframe, text="F degr", fg="red").place(relx=0, rely=0.1, relwidth=0.25)
Label(botframe, text="Time", fg="red").place(relx=0, rely=0.2, relwidth=0.25)

content = StringVar()
content.set("12.34")
e1 = Entry(topframe, textvariable=content).place(relx=0.3, rely=0)

content2 = StringVar()
e2 = Entry(midframe, textvariable=content2).place(relx=0.3, rely=0.1)

content3 = StringVar()
e3 = Entry(botframe, textvariable=content3).place(relx=0.3, rely=0.2)

button1 = Button(root, text="C -> F", command=cdegtofdeg).pack(side=BOTTOM)

root.mainloop()
