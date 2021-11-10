import sys
import os

directory = sys.argv[2] 
filecount=0

for entry in os.scandir(directory):
    if entry.path.endswith(".txt") and entry.is_file():
        filecount+=1
for entry in os.scandir(directory):
    if entry.path.endswith(".txt") and entry.is_file():
        punc_count=0
        num_count=0
        upper_count=0
        word_count=0
        correctwords=0
        punctuation=[".","?","!",",",":",";","-","(",")","{","}","[","]","'","\"","...",]
        englishwordslist=[]
        with open(sys.argv[1], 'r') as f:
            englishwords = f.read()
        englishwordslist=englishwords.split("\n")
        with open(entry.path, 'r') as f:
            inputfile = f.read()
        words=inputfile.split()
        for x in range(len(words)):
            temp=words[x]
            for y in range(len(temp)):
                asc=ord(temp[y])
                if (asc>=33 and asc<=47) or (asc>=58 and asc<=64) or (asc>=91 and asc<=96) or (asc>=123 and asc<=126):
                    punc_count+=words[x].count(temp[y])
                    words[x]=words[x].replace(temp[y],"")
            for y in range(len(temp)):
                asc=ord(temp[y])    
                if (asc>=48 and asc<=57):
                    num_count+=words[x].count(temp[y])
                    words[x]=words[x].replace(chr(asc),"")
            if temp.lower() != temp:
                words[x]=words[x].lower()
                upper_count+=1
            if len(words[x])<1:
                pass
            else:
                word_count+=1

            for z in range(len(englishwordslist)):
                if words[x]==englishwordslist[z]:
                    correctwords+=1
                    break
        solutionlocation=""
        for i in range(filecount):
            currentpath=str(i+1)+".txt"
            if entry.path.endswith(currentpath):
                filename="test_file"+str(i+1)+"_u68780be.txt"
                solutionlocation=os.path.join(sys.argv[3],filename)         
        with open(solutionlocation, 'a') as f:
            f.write("u68780be")
            f.write("\nFormatting ###################")
            f.write("\nNumber of upper case words transformed: "+str(upper_count))
            f.write("\nNumber of punctuation’s removed: "+str(punc_count))
            f.write("\nNumber of numbers removed: "+str(num_count))
            f.write("\nSpellchecking ###################")
            f.write("\nNumber of words in file: "+str(word_count))
            f.write("\nNumber of correct words in file: "+str(correctwords))
            f.write("\nNumber of incorrect words in file: "+str(word_count-correctwords))