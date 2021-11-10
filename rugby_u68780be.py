import sys
import os 

directory = sys.argv[1]
filecount=0
for entry in os.scandir(directory):
	if entry.path.endswith(".txt") and entry.is_file():
		filecount+=1
for entry in os.scandir(directory):
	if entry.path.endswith(".txt") and entry.is_file():
		with open(entry.path, 'r') as f:
		    rugbyscores = f.read()
		teamone=0
		teamtwo=0
		team=False
		for x in range(len(rugbyscores)):
			if rugbyscores[x]=="1":
				if rugbyscores[x+1]=="t":
					teamone+=5
				elif rugbyscores[x+1]=="c":
					teamone+=2
				elif rugbyscores[x+1]=="p":
					teamone+=3
				elif rugbyscores[x+1]=="d":
					teamone+=3
			elif rugbyscores[x]=="2":	
				if rugbyscores[x+1]=="t":
					teamtwo+=5
				elif rugbyscores[x+1]=="c":
					teamtwo+=2
				elif rugbyscores[x+1]=="p":
					teamtwo+=3
				elif rugbyscores[x+1]=="d":
					teamtwo+=3
		solutionlocation=""
		for i in range(filecount):
			currentpath=str(i+1)+".txt"
			if entry.path.endswith(currentpath):
				filename="test_file"+str(i+1)+"_u68780be.txt"
				solutionlocation=os.path.join(sys.argv[2],filename)			
		with open(solutionlocation, 'a') as f:
			totalscore = str(teamone)+":"+str(teamtwo)
			f.write(totalscore)
