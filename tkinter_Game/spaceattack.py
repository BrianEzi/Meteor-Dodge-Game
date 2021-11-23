import random 
from tkinter import *

#sets the window dimensions and creates the window
def setWindowDimensions(w,h,t):
	window=Tk()
	window.title(t)
	ws=window.winfo_screenwidth()
	hs=window.winfo_screenheight()
	x =(ws/2) - (w/2)
	y=(hs/2)-(h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y)) # window size

	return window
	

#Creates the window and canvas
width = 1280
height =  720
title="Snake Game"
window=setWindowDimensions(width,height,title)
canvas=Canvas(window, width=width, height=height)


#stores the background image in a local variable and sets the canvas background
background=PhotoImage(file="GameBackground.png")
canvas.create_image(0,0,image=background,anchor='nw')
canvas.pack()


window.mainloop()
