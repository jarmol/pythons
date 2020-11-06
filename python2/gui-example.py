from Tkinter import *

def onclick():
   pass

root = Tk()
text = Text(root)
text.insert(INSERT, "Hello.....")
text.insert(END, "\nBye Bye.....")
text.pack()

text.tag_add("here", "1.0", "1.5")
text.tag_add("start", "2.0", "2.3")
text.tag_add("toinen", "2.4", "2.7")
text.tag_config("here", background="yellow", foreground="blue")
text.tag_config("start", background="black", foreground="red")
text.tag_config("toinen", background="blue", foreground="white")
root.mainloop()
