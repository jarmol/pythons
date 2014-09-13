# http://www.tutorialspoint.com/python/tk_entry.htm

from Tkinter import *
import tkMessageBox

def callback():
    s = E1.get()
    tkMessageBox.showinfo( "User", s)

top = Tk()
top.geometry('250x100+40+40')
top.title('Text entry field')
b = Button(top, text="get", command=callback)
b.pack(side = TOP)

L1 = Label(top, text="User Name")
L1.pack( side = LEFT)
E1 = Entry(top, bd =5)
E1.pack(side = RIGHT)
E1.insert(0, "User name")

top.mainloop()
