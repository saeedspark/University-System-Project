#Import tkinter library
from tkinter import *

#Create an instance of tkinter frame
win = Tk()

#Set the geometry of tkinter window
win.geometry("750x250")

#Create an Entry Widget
entry= Entry(win, width= 25)
entry.insert(0,"ttk Entry widget")
entry.pack()

#Set the focus to Entry widget
entry.focus_set()
win.mainloop()