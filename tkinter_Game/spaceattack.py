import random 
import sys
if "Tkinter" not in sys.modules:
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
	global direction, impact, shot, velocity, asteroids
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
			impact[i]=False
		if impact[i]==True:
			canvas.move(player,5*velocity[i][0], 5*velocity[i][1])
			canvas.move(asteroids[i],-10*velocity[i][0],-10*velocity[i][1])
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
	movePlayer(lastkey)
def movePlayer(lastkey):
	global x,y
	if lastkey!="":
		print("moveplayer",lastkey)
		for letter in lastkey:
			if letter==up:
				y-=10
				canvas.itemconfigure(player,image=astronaut_turbo)
				with open("lastpos.txt","w") as f:
					f.write("1")
			elif letter==left:
				x-=10
				canvas.itemconfigure(player,image=astronaut_turbo_left)
				with open("lastpos.txt","w") as f:
					f.write("2")
			elif letter==down:
				y+=10
				canvas.itemconfigure(player,image=astronaut_turbo_down)
				with open("lastpos.txt","w") as f:
					f.write("3")
			elif letter==right:
				x+=10
				canvas.itemconfigure(player,image=astronaut_turbo_right)
				with open("lastpos.txt","w") as f:
					f.write("4")
			print(letter)
#checks when a key has been released then removes it from the currently active keys
def released(event):
	lastkey=""
	with open("prevkey.txt","r") as f:
		lastkey=f.read()
	for letter in lastkey:
		if event.keysym==letter:
			print(event.keysym)
			lastkey=lastkey.replace(event.keysym,"")
	with open("prevkey.txt","w") as f:
		f.write(lastkey)
	movePlayer(lastkey)
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
def PlaceSpacedust():
	global spacedustimg, spacedust, spacedustx,spacedusty
	spacedust = canvas.create_image(0,0,image=spacedustimg,anchor='nw')
	spacedustx = random.randint(0,width- spacedustimg.width())
	spacedusty = random.randint(0,height- spacedustimg.height())
	canvas.move(spacedust, spacedustx, spacedusty)
def MoveSpacedust():
	global spacedustimg, spacedust, spacedustx,spacedusty
	canvas.move(spacedust,spacedustx*-1,spacedusty*-1)
	spacedustx = random.randint(0,width- spacedustimg.width())
	spacedusty = random.randint(0,height- spacedustimg.height())
	canvas.move(spacedust, spacedustx, spacedusty)
def CreateAsteroids():
	global asteroids, shot, targets, velocity, impact
	asteroids=[]
	shot=[]
	targets=[]
	velocity=[]
	impact=[]
	for i in range(10):
		asteroids.append(canvas.create_image(width/2 -20, + spaceship.height() - 30,image=asteroid,anchor='nw'))
		shot.append(False)
		targets.append([i*128,i*72])#sets the initial targets of each asteroid
		velocity.append([])
		impact.append(False)
def Bosskey(event):
	canvas.create_image(0,0,image=bossimg, anchor="nw")
#function to play the game once it started
def Play_Game():
	canvas.pack()
	global x,y,direction,buffer,speed,firstshot,score,lives, impact, shot
	score+=1
	txt="\nScore:"+str(score)
	canvas.itemconfigure(scoreText,text=txt)
	if buffer==10:
		buffer=0
		firstshot=False
	canvas.move(player,x,y)
	canvas.move(hitbox,x,y)
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
			if impact[i]==False:
				print("OW!")
				lives-=1
				livetxt="\n Lives:"+str(lives)
				canvas.itemconfigure(livesText,text=livetxt)
				resetAsteroids()
				impact[i]=True
	spacedustcoords=Coordinates(spacedust,spacedustimg.width(),spacedustimg.height())
	invadercoords=Coordinates(invader,spaceship.width(),spaceship.height())
	if collision(invadercoords,playercoords):
		lives=0
	if collision(spacedustcoords,playercoords):
		score+=50
		MoveSpacedust()
	if lives==0:
		endgame=True
	if 'endgame' not in locals():
		buffer+=1
		speed=speed*0.999
		window.after(90,Play_Game)
	else:
		canvas.create_text(width/2,height/2,fill="white",font="Times 20 italic bold", text="Game Over!")
		CreateMenu()		
def collision(a,b):
	if a[0][0]<b[1][0] and a[1][0]>b[0][0] and a[0][1]<b[1][1] and a[1][1]>b[0][1]:
		return True
	return False

def Coordinates(o,width,height):
	size=[]
	size.append(canvas.coords(o))
	global hitbox
	if o==player:
		with open("lastpos.txt","r") as f:
			lastpos=f.read()
		if lastpos=="1":
			size.append([size[0][0]+32,size[0][1]+65])
			size[0][0]+=8
		elif lastpos=="2":
			size.append([size[0][0]+65,size[0][1]+31])
			size[0][1]+=7
		elif lastpos=="3":
			size.append([size[0][0]+31,size[0][1]+height])
			size[0][0]+=7
			size[0][1]+=25
		elif lastpos=="4":
			size.append([size[0][0]+width,size[0][1]+32])
			size[0][0]+=25
			size[0][1]+=8
		canvas.coords(hitbox,size[0][0],size[0][1],size[1][0],size[1][1])
	elif o==invader:
		size[0][0]+=30
		size[0][1]+=0
		size.append([size[0][0]+width-65,size[0][1]+height-20])
		canvas.coords(invaderhitbox,size[0][0],size[0][1],size[1][0],size[1][1])
	else:
		size[0][0]+=5
		size[0][1]+=5
		size.append([size[0][0]+width-5,size[0][1]+height-5])

	return size
#Creates the window and canvas
width = 1280
height =  720
title="Astronauts and Asteroids"
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
spacedustimg=PhotoImage(file="spacedust.png")
bossimg=PhotoImage(file="boss.png")

gamestart=False
#stores the background image in a local variable and sets the canvas background
background=PhotoImage(file="GameBackground.png")
canvas.create_image(0,0,image=background,anchor='nw')

#creates the character as a movign image
player=canvas.create_image(100,600,image=astronaut_turbo,anchor='nw')

#creates ten asteroids as well as arrays to store different values relating to each asteroid

invader=canvas.create_image(width/2-spaceship.width()/2,0,image=spaceship,anchor='nw')
with open("lastpos.txt","w") as f:
	f.write("1")

x,y=0,0
direction="left"
buffer=0
speed=100
firstshot=True

invaderhitbox=canvas.create_rectangle(canvas.coords(invader)[0],canvas.coords(invader)[1],canvas.coords(invader)[0]+1,canvas.coords(invader)[1]+1)

score=0
txt="\n Score:"+str(score)
scoreText = canvas.create_text( width/2 , 10 , fill="white" , font="Times 20 italic bold", text=txt)

lives=5
livetxt="\n Lives:"+str(lives)
livesText = canvas.create_text( width/10 , 10 , fill="white" , font="Times 20 italic bold", text=livetxt)

#binds the control for the character
canvas.bind("<KeyPress>",pressing)
canvas.bind("<KeyRelease>",released)
canvas.bind("<Button-1>",click)
canvas.bind("b",Bosskey)
canvas.focus_set()

hitbox=canvas.create_rectangle(canvas.coords(player)[0]+8,canvas.coords(player)[1],canvas.coords(player)[0]+32,canvas.coords(player)[1]+65)
def Setdefaultcontrols():
	global up, down, left, right
	up="w"
	left="a"
	right="d"
	down="s"
def CreateMenu():
	global menu, menuw,menuh
	menu=Toplevel(window)
	menu.configure(bg="#212121")
	ws=window.winfo_screenwidth()
	hs=window.winfo_screenheight()
	menuw=300
	menuh=300
	x =(ws/2) - (menuw/2)
	y=(hs/2)-(menuh/2)
	menu.geometry('%dx%d+%d+%d' % (menuw, menuh, x, y)) # window size
	newgame=Button(menu, text="New game", font=("Arial", 30),command=lambda:Newgame(),bg="#222121", fg = "white")
	newgame.pack(pady="10")
	scoreboards=Button(menu, text="Scoreboard", font=("Arial",30),bg="#212121", fg="white", command=lambda:ShowScores())
	scoreboards.pack(pady="10")
	controls=Button(menu,text="Controls", font=("Arial",30,), bg="#212121", fg="white", command=lambda:Controls())
	controls.pack(pady="10")
	#menu.attributes("-topmost",1)
	menu.overrideredirect(True)

def Newgame():
	menu.destroy()
	Play_Game()
def ShowScores():
	#scoreboard=setWindowDimensions(250,250,"Scoreboard")
	global menuh, menuw
	scoreboard=Toplevel(menu)
	ws=window.winfo_screenwidth()
	hs=window.winfo_screenheight()
	x =(ws/2) - (menuw/2)
	y=(hs/2)-(menuh/2)
	scoreboard.geometry('%dx%d+%d+%d' % (menuw, menuh, x, y)) # window size
	scoreboard.configure(bg="#212121")
	with open("scores.txt","r") as f:
		temp=f.read()
	print(temp)
	scores=Label(scoreboard, text=temp)
	scores.configure(fg="white",bg="#212121")
	# scores.place(x=50,y=50)
	scores.pack()
	backbutton=Button(scoreboard,text="Back", font=("Arial",20), bg="#212121", fg="white", command=lambda:scoreboard.destroy())
	backbutton.pack(side="bottom")
	scoreboard.overrideredirect(True)

def Controls():
	global menuh, menuw
	controls=Toplevel(menu)
	ws=window.winfo_screenwidth()
	hs=window.winfo_screenheight()
	x =(ws/2) - (menuw/2)
	y=(hs/2)-(menuh/2)
	controls.geometry('%dx%d+%d+%d' % (menuw, menuh, x, y)) # window size
	controls.configure(bg="#212121")
	uplbl=Label(controls,text="UP",fg="white",bg="#212121",font=("Arial",20))
	uplbl.pack()
	upentry=Text(controls,height="1",width="5")
	upentry.pack()
	leftlbl=Label(controls,text="LEFT",fg="white",bg="#212121",font=("Arial",20))
	leftlbl.pack()
	leftentry=Text(controls,height="1",width="5")
	leftentry.pack()
	downlbl=Label(controls,text="DOWN",fg="white",bg="#212121",font=("Arial",20))
	downlbl.pack()
	downentry=Text(controls,height="1",width="5")
	downentry.pack()
	rightlbl=Label(controls,text="RIGHT",fg="white",bg="#212121",font=("Arial",20))
	rightlbl.pack()
	rightentry=Text(controls,height="1",width="5")
	rightentry.pack()
	upentry.insert("end-1c",up)
	downentry.insert("end-1c",down)
	leftentry.insert("end-1c",left)
	rightentry.insert("end-1c",right)
	savebutton=Button(controls, text="Save and Return", font=("Arial",20), bg="#212121", fg="white", command=lambda:setcontrols(upentry.get(1.0,"end-1c"),leftentry.get(1.0,"end-1c"),rightentry.get(1.0,"end-1c"),downentry.get(1.0,"end-1c"),controls))
	savebutton.pack()
	controls.overrideredirect(True)
def setcontrols(u,l,r,d,controls): 
	print(u,l,r,d)
	global up,down,left,right
	errorfound=False
	if len(u)==1:
		up=u
	else:
		errorfound=True
		error=Toplevel(controls)
		ws=window.winfo_screenwidth()
		hs=window.winfo_screenheight()
		x =(ws/2) - (menuw/4)
		y=(hs/2)-(menuh/4)
		error.geometry('%dx%d+%d+%d' % (menuw, menuh/3, x*1.3, y)) # window size
		error.configure(bg="#212121")
		errorlbl=Label(error,text="Up Key must be \n only one character",fg="blue",bg="#212121",font=("Arial",20))
		errorlbl.pack()
		#error.overrideredirect(True)
		#window.after(1000,error.destroy())
	if len(l)==1:
		left=l
	else:
		errorfound=True
		error=Toplevel(controls)
		ws=window.winfo_screenwidth()
		hs=window.winfo_screenheight()
		x =(ws/2) - (menuw/4)
		y=(hs/2)-(menuh/4)
		error.geometry('%dx%d+%d+%d' % (menuw, menuh/3,  x*1.3, y)) # window size
		error.configure(bg="#212121")
		errorlbl=Label(error,text="Left Key must be \nonly one character",fg="blue",bg="#212121",font=("Arial",20))
		errorlbl.pack()
		#error.overrideredirect(True)
		#window.after(1000,error.destroy())
	if len(r)==1:
		right=r
	else:
		errorfound=True
		error=Toplevel(controls)
		ws=window.winfo_screenwidth()
		hs=window.winfo_screenheight()
		x =(ws/2) - (menuw/4)
		y=(hs/2)-(menuh/4)
		error.geometry('%dx%d+%d+%d' % (menuw, menuh/3, x*1.3, y)) # window size
		error.configure(bg="#212121")
		errorlbl=Label(error,text="Right Key must be \nonly one character",fg="blue",bg="#212121",font=("Arial",20))
		errorlbl.pack()
		#error.overrideredirect(True)
		#window.after(1000,error.destroy())
	if len(d)==1:
		down=d 
	else:
		errorfound=True
		error=Toplevel(controls)
		ws=window.winfo_screenwidth()
		hs=window.winfo_screenheight()
		x =(ws/2) - (menuw/4)
		y=(hs/2)-(menuh/4)
		error.geometry('%dx%d+%d+%d' % (menuw, menuh/3, x*1.3, y)) # window size
		error.configure(bg="#212121")
		errorlbl=Label(error,text="Down Key must be \nonly one character",fg="blue",bg="#212121",font=("Arial",20))
		errorlbl.pack()
		#error.overrideredirect(True)
		#window.after(1000,error.destroy())
	if not errorfound:
		controls.destroy()
canvas.pack()

#SetBorders()
Setdefaultcontrols()
CreateMenu()
PlaceSpacedust()
CreateAsteroids()
window.mainloop()




#clears the file storing all active keys

with open("prevkey.txt","w") as f:

	f.write("")