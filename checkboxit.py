import Tkinter
from Tkinter import *
import tkMessageBox

top = Tkinter.Tk()
top.title('Raksi ruutuun')
top.geometry("200x240+100+100")

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()

C1 = Checkbutton(top, text = "Musiikkia", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 16, activebackground = 'lightyellow')
C2 = Checkbutton(top, text = "Videoita ", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 16, activebackground = 'lightgreen')
C3 = Checkbutton(top, text = "Facebook ", variable = CheckVar3, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 16, activebackground = 'lightblue')
C4 = Checkbutton(top, text = "Grillimakkaraa", variable = CheckVar4, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 16, activebackground = 'pink')

C1.pack()
C2.pack()
C3.pack()
C4.pack()
top.mainloop()
