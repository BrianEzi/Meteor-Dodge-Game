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
			inputfile=f.read()
		decrypted=""
		encrypted=inputfile.split(":")
		if encrypted[0].lower()=="hex":
			decrypted=bytes.fromhex(encrypted[1]).decode('utf-8').lower()
		elif encrypted[0].count("+3")>0:
			for letter in encrypted[1]:
				asc=ord(letter.lower())
				if asc!=32: asc-=3
				if asc < 97 and asc!=32: asc+=26
				decrypted+=chr(asc)
		else:
			MORSE_CODE_DICT = { 'A':'.-', 'B':'-...','C':'-.-.', 'D':'-..', 'E':'.','F':'..-.', 'G':'--.', 'H':'....','I':'..', 'J':'.---', 'K':'-.-','L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-','R':'.-.', 'S':'...', 'T':'-','U':'..-', 'V':'...-', 'W':'.--','X':'-..-', 'Y':'-.--', 'Z':'--..','1':'.----', '2':'..---', '3':'...--','4':'....-', '5':'.....', '6':'-....','7':'--...', '8':'---..', '9':'----.','0':'-----', ', ':'--..--', '.':'.-.-.-','?':'..--..', '/':'-..-.', '-':'-....-','(':'-.--.', ')':'-.--.-'}
			encrypted=encrypted[1].split()
			for letter in encrypted:
				if letter=="/":
					decrypted+=" "
				else:
					decrypted+=list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(letter)].lower()
		for i in range(filecount):
			currentpath=str(i+1)+".txt"
			if entry.path.endswith(currentpath):
				filename="test_file"+str(i+1)+"_u68780be.txt"
				solutionlocation=os.path.join(sys.argv[2],filename)	

		with open(solutionlocation, 'a') as f:
			f.write(decrypted)
