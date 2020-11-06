import Tkinter
from Tkinter import *
import tkMessageBox

top = Tkinter.Tk()
top.title('Raksi ruutuun')
top.geometry("200x240+100+100")

def dosomething3():
   tkMessageBox.showinfo( "Task 3", "OK Task 3")

def dosomething4():
   tkMessageBox.showinfo( "Task 4", "OK Task 4")

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()

C1 = Checkbutton(top, text = "Musiikkia", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 16, activebackground = 'lightyellow')
C2 = Checkbutton(top, text = "Videoita ", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 16, activebackground = 'cyan')
C3 = Checkbutton(top, text = "Facebook ", variable = CheckVar3, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 16, activebackground = 'lightblue', bg = 'green', \
                 command = dosomething3 )
C4 = Checkbutton(top, text = "Grillimakkaraa", variable = CheckVar4, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 16, activebackground = 'pink', bg = 'yellow', \
                 command = dosomething4 )

C1.pack(side=TOP)
C2.pack(side=TOP)
C3.pack(side=TOP)
C4.pack()
top.mainloop()
