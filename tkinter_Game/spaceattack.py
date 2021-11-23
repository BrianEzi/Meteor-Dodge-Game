import random 
from tkinter import *
#checks which keys are currently being pressed then adjusts the characters direction accordingly
#active keys are stored in external file called prevkey.txt
def pressing(event):
	x=0
	y=0
	with open("prevkey.txt","r") as f:
		lastkey=f.read()
	if event.char not in lastkey:
		with open("prevkey.txt","a") as f:
			f.write(event.char)
		lastkey+=event.char
	if lastkey!="":
		for letter in lastkey:
			if letter=="w":
				y-=10
				canvas.itemconfigure(player,image=astronaut_turbo)
			elif letter=="a":
				x-=10
				canvas.itemconfigure(player,image=astronaut_turbo_left)
			elif letter=="s":
				y+=10
				canvas.itemconfigure(player,image=astronaut_turbo_down)
			elif letter=="d":
				x+=10
				canvas.itemconfigure(player,image=astronaut_turbo_right)
	canvas.move(player,x,y)

#checks when a key has been released then removes it from the currently active keys
def released(event):
	lastkey=""
	with open("prevkey.txt","r") as f:
		lastkey=f.read()
	for letter in lastkey:
		if event.keysym==letter:
			lastkey=lastkey.replace(event.keysym,"")
	with open("prevkey.txt","w") as f:
		f.write(lastkey)

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


#stores the different images the player can have in different variables
astronaut=PhotoImage(file="Astronaut.png")
astronaut_turbo=PhotoImage(file="turbo_astronaut.png")
astronaut_turbo_down=PhotoImage(file="turbo_astronaut_down.png")
astronaut_turbo_left=PhotoImage(file="turbo_astronaut_left.png")
astronaut_turbo_right=PhotoImage(file="turbo_astronaut_right.png")
spaceship=PhotoImage(file="Spaceship.png")

#stores the background image in a local variable and sets the canvas background
background=PhotoImage(file="GameBackground.png")
canvas.create_image(0,0,image=background,anchor='nw')

#creates the character as a movign image
player=canvas.create_image(100,150,image=astronaut_turbo,anchor='nw')
invader=canvas.create_image(250,0,image=spaceship,anchor='nw')

#binds the control for the character
canvas.bind("<KeyPress>",pressing)
canvas.bind("<KeyRelease>",released)
canvas.focus_set()

canvas.pack()

window.mainloop()

#clears the file storing all active keys
with open("prevkey.txt","w") as f:
	f.write("")