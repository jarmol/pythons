from Tkinter import *
import tkMessageBox
import Tkinter

top = Tkinter.Tk()
top.title('Raksi ruutuun')
top.geometry("200x240+100+100")

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()

C1 = Checkbutton(top, text = "Musiikkia", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C2 = Checkbutton(top, text = "Videoita", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C3 = Checkbutton(top, text = "Facebook", variable = CheckVar3, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C1.pack()
C2.pack()
C3.pack()
top.mainloop()
