import random 
from tkinter import *
#calculates the velocity of the asteroid (speed and direction)
def Asteroid_Velocity(i,targetpos,speed):
	global velocity
	global targets
	startpos=canvas.coords(asteroids[i])
	if shot[i]==False :
		if firstshot==True:
			targetpos=targets[i]
		#print(targetpos)
		distance_x= targetpos[0]-startpos[0]
		distance_y=targetpos[1]-startpos[1]
		speed_x=distance_x/speed
		speed_y=distance_y/speed
		#print(speed_x,speed_y)
		velocity[i]=[speed_x,speed_y]
		targets[i]=canvas.coords(player) #store the current target relating to the current available asteroid
		shot[i]=True
#function to move all asteroids that have been shot
def shoot(velocity):
	global firstshot
	for i in range(10):
		if shot[i]==True:
			canvas.move(asteroids[i],velocity[i][0],velocity[i][1])
#resets all asteroids back to their original position where they are following the spaceship
def resetAsteroids():
	global direction
	invaderpos=canvas.coords(invader)
	for i in range(10):
		asteroidpos=canvas.coords(asteroids[i])		
		if shot[i]==False :
			if direction=="left":
				canvas.move(asteroids[i],-10,0)
			else:
				canvas.move(asteroids[i],10,0)
		if asteroidpos[0]+50<0 or asteroidpos[0]>width or asteroidpos[1]+50> height or  asteroidpos[1]< 0:
			window.after(50,canvas.move(asteroids[i],invaderpos[0]+spaceship.width()/2-asteroidpos[0],spaceship.height()-30 - asteroidpos[1]))
			shot[i]=False

#checks which keys are currently being pressed then adjusts the characters direction accordingly
#active keys are stored in external file called prevkey.txt
def pressing(event):
	canvas.pack()
	with open("prevkey.txt","r") as f:
		lastkey=f.read()
	if event.char not in lastkey:
		with open("prevkey.txt","a") as f:
			f.write(event.char)
		lastkey+=event.char
	global x,y
	if lastkey!="":
		for letter in lastkey:
			if letter=="w":
				y-=10
				canvas.itemconfigure(player,image=astronaut_turbo)
				with open("lastpos.txt","w") as f:
					f.write("1")
			elif letter=="a":
				x-=10
				canvas.itemconfigure(player,image=astronaut_turbo_left)
				with open("lastpos.txt","w") as f:
					f.write("2")
			elif letter=="s":
				y+=10
				canvas.itemconfigure(player,image=astronaut_turbo_down)
				with open("lastpos.txt","w") as f:
					f.write("3")
			elif letter=="d":
				x+=10
				canvas.itemconfigure(player,image=astronaut_turbo_right)
				with open("lastpos.txt","w") as f:
					f.write("4")
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

#prevents the player from moving off screen 
def SetBorders():
	position=(canvas.coords(player))
	if position[0]<0:
		canvas.coords(player,0,position[1])
	elif position[0]+90>width:
		canvas.coords(player,width-90,position[1])
	elif position[1]+90 > height:
		canvas.coords(player,position[0], height-90)
	elif position[1] < 0:
		canvas.coords(player,position[0],0)
	position.clear()

def click(event):
	x, y = event.x, event.y
	print('{}, {}'.format(x, y))

#function to move the spaceship from left to right at the top of the screen
def moveSpaceship():
	position=canvas.coords(invader)
	invaderwidth = spaceship.width()
	x=0
	global direction
	if position[0]<0:
		direction="right"
	if position[0]+invaderwidth>1280:
		direction="left"
	if direction=="left":
		x=-20
	elif direction=="right":
		x=20
	canvas.move(invader,x,0)

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

#function to play the game once it started
def Play_Game():
	canvas.pack()
	global x,y
	global direction
	global buffer
	global speed
	global firstshot
	global score
	score+=1
	txt="\nScore:"+str(score)
	canvas.itemconfigure(scoreText,text=txt)
	if buffer==10:
		buffer=0
		firstshot=False
	canvas.move(player,x,y)
	#print(x,y)
	x,y=0,0
	SetBorders()
	moveSpaceship()
	resetAsteroids()
	Asteroid_Velocity(buffer,canvas.coords(player),speed)
	window.after(50,shoot(velocity))#shoots the asteroid after 2 seconds wait
	# print(shot,velocity,targets)
	with open("lastpos.txt","r") as f:
		coordskey=f.read()
	playercoords=""
	if coordskey=="1":
		playercoords=Coordinates(player,astronaut_turbo.width(),astronaut_turbo.height())
	elif coordskey=="2":
		playercoords=Coordinates(player,astronaut_turbo_left.width(),astronaut_turbo_left.height())
	elif coordskey=="3":
		playercoords=Coordinates(player,astronaut_turbo_down.width(),astronaut_turbo_down.height())
	elif coordskey=="4":
		playercoords=Coordinates(player,astronaut_turbo_right.width(),astronaut_turbo_right.height())
	for i in range(10):
		asteroidcoords=Coordinates(asteroids[i], asteroid.width(), asteroid.height())
		if collision(asteroidcoords,playercoords):
			print("OW!")







	if 'endgame' not in locals():
		buffer+=1
		speed=speed*0.999
		window.after(90,Play_Game)
def collision(a,b):
	if a[0][0]<b[1][0] and a[1][0]>b[0][0] and a[0][1]<b[1][1] and a[1][1]>b[0][1]:
		return True
	return False

def Coordinates(o,width,height):
	size=[]
	size.append(canvas.coords(o))
	topleft=canvas.coords(o)
	size.append([topleft[0]+width,topleft[1]+height])
	return size
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
spaceship=PhotoImage(file="spaceship_asteroid.png")
spaceship_beam=PhotoImage(file="spaceship_beam1.png")
asteroid=PhotoImage(file="asteroid.png")
spacedust=PhotoImage(file="spacedust.png")


gamestart=False
#stores the background image in a local variable and sets the canvas background
background=PhotoImage(file="GameBackground.png")
canvas.create_image(0,0,image=background,anchor='nw')

#creates the character as a movign image
player=canvas.create_image(100,150,image=astronaut_turbo,anchor='nw')

#creates ten asteroids as well as arrays to store different values relating to each asteroid
asteroids=[]
shot=[]
targets=[]
velocity=[]
for i in range(10):
	asteroids.append(canvas.create_image(width/2 -20, + spaceship.height() - 30,image=asteroid,anchor='nw'))
	shot.append(False)
	targets.append([i*128,i*72])
	velocity.append([])
invader=canvas.create_image(width/2-spaceship.width()/2,0,image=spaceship,anchor='nw')
with open("lastpos.txt","w") as f:
	f.write("1")
canvas.create_image(0,0,image=spacedust,anchor='nw')



x,y=0,0
direction="left"
buffer=0
speed=100
firstshot=True

score=0
txt="\n Score:"+str(score)
scoreText = canvas.create_text( width/2 , 10 , fill="white" , font="Times 20 italic bold", text=txt)

#binds the control for the character
canvas.bind("<KeyPress>",pressing)
canvas.bind("<KeyRelease>",released)
canvas.bind("<Button-1>",click)
canvas.focus_set()


menu=Toplevel(window)
menu.geometry("300x300")
menu.title("")
newgame=Button(menu, text="New game")
newgame.pack()
scoreboards=Button(menu, text="Scoreboard")
scoreboards.pack()
menu.attributes("-topmost",1)



canvas.pack()

#SetBorders()

Play_Game()
window.mainloop()




#clears the file storing all active keys

with open("prevkey.txt","w") as f:

	f.write("")