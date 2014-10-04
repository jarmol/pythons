from Tkinter import *
from PIL import Image, ImageTk
import time

def cdegtofdeg():
    s = time.strftime("%d.%m.%Y %T",time.localtime())
    content3.set(s)
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
root.title("Numeric entries")
w = Canvas(root, width=300, height=300)

im = Image.open("Lenna.png")

photo = ImageTk.PhotoImage(im)
w.create_image(100, 100, image=photo, anchor=CENTER)
w.create_text(100, 200, font=("Arial",16), text="Hello", fill="red")
w.create_text(100, 220,  font=("Arial",16), text="world!", fill="blue")
w.place(anchor=NW, relwidth=1, relheight=1)

w1 = 0.26
rh1 = 0.07

Label(root, text="C degr", fg="red").place(relx=0.03, rely=0.02, relwidth=w1, relheight=rh1)
Label(root, text="F degr", fg="red").place(relx=0.03, rely=0.1, relwidth=w1, relheight=rh1)
Label(root, text="Local time", fg="red").place(relx=0.03, rely=0.18, relwidth=w1, relheight=rh1)

content = StringVar()
content.set("-25.0")
e1 = Entry(root, textvariable=content).place(relx=0.3, rely=0.02)

content2 = StringVar()
e2 = Entry(root, textvariable=content2).place(relx=0.3, rely=0.1)

content3 = StringVar()
e3 = Entry(root, textvariable=content3).place(relx=0.3, rely=0.18)

button1 = Button(root, text="C -> F", command=cdegtofdeg).pack(side=BOTTOM)

root.mainloop()
