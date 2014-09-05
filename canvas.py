import Tkinter
import tkMessageBox

top = Tkinter.Tk()
top.title("Canvas")

C = Tkinter.Canvas(top, bg="blue", height=250, width=300)

coord = 10, 50, 240, 210
arc = C.create_arc(coord, start=-30, extent=120, fill="white")
arc = C.create_arc(coord, start=30, extent=120, fill="red")
arc = C.create_arc(coord, start=-30, extent=-120, fill="yellow")
arc = C.create_arc(coord, start=150, extent=60, fill="black")

C.pack()
top.mainloop()
