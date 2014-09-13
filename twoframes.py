# -*- coding: utf-8 -*-
import Tkinter as tk

master = tk.Tk()
master.geometry("250x150+50+50")
master.title("Frame-erotin")

tk.Label(text="Yläosa", fg="red", pady=15).pack()

separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=5)

tk.Label(text="Alaosa", fg="blue").pack()

tk.mainloop()
