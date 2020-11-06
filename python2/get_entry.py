from Tkinter import *
import string

# This program  shows how to make a typein box shadow a program variable.

class App(Frame):
    def __init__(self, master=None):
	Frame.__init__(self, master)
	self.pack()

	self.entrythingy = Entry(self)
	self.entrythingy.pack()

	self.button = Button(self, text="Uppercase The Entry",
			     command=self.upper)
	self.button.pack()

	self.contents = StringVar()
	self.contents.set("this is a variable")
	self.entrythingy.config(textvariable=self.contents)

	self.entrythingy.bind('<Key-Return>', self.print_contents)

    def upper(self):


	str = string.upper(self.contents.get())
	self.contents.set(str)

    def print_contents(self, event):
	print "hi. contents of entry is now ---->", self.contents.get()

root = App()
root.master.title("Foo")
root.mainloop()
