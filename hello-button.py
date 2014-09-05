#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://www.tutorialspoint.com/python/tk_button.htm

import Tkinter
import tkMessageBox

top = Tkinter.Tk()
top.geometry("300x200+50+200")
 
def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
top.mainloop()
