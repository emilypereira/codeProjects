#!/opt/bin/python3
   
#mtfcoding.py
#Emily Pereira V00728841
#Created Mar.1,2015
#Input: is either a .txt or a .mtf file
#Output: is a .mtf or .txt respectively
   
import sys
import os
  
encoded_words = 0
encode_table = []
words = []
decode_table = []
decoded_words = 0
 
def tokenize(lines):
# This function splits the lines read in from the file into individual words 20     
	global words
	words  = []
    words = lines.split(' ')
def insert(fout):
#This function determines if a word is in the encode_table or not and then either adds it to t
he table or moves the word in the table to the end of the list
	global encoded_words
    global words
    global encode_table
  
    if len(words) > 0:
    	s1 = ""
        if words[0] == '\n':
    		fout.write('\n')
     	else:
     		for i in range(len(words)):
            	if i == len(words) - 1:
                #handles '\n' at the end of a word    
                	temp = words.pop()
                    tSize = len(temp)
                    if temp[tSize - 1] == '\n':
                          s1='\n'
                          temp = temp[:-1]
                          temp = "".join(temp)
                          words.append(temp)
                    else:
                    	s1 = ""
                        temp ="".join(temp)
                        words.append(temp)
  
                if words[i] in encode_table:
                #word already in table
                	y = encoded_words - encode_table.index(words[i])
                	encode_table.append(words[i])
                    encode_table.remove(words[i])
                    fout.write(chr(y + 128))
  
                    if s1 == '\n':
                          fout.write(s1)
                else:
            	#word wasn't in the table
                	encode_table.append(words[i])
                    insertToFile(words[i],s1,fout)
                    encoded_words = encoded_words + 1
def insertToFile(s1,s2,fout):
#writes the word that was added to the word table into the file with it's code number
	global encoded_words
    x = len(s1)
    y = encoded_words + 1 + 128
    fout.write(chr(y))
    fout.write(s1)
    if s2 == '\n':
    	fout.write(s2)
  
def mtfEncode():
#encodes a .txt file into a .mtf file    
	if len(sys.argv)!= 1:
    	filename = sys.argv[1]
        n = len(filename)
  
        li = list(sys.argv[1])
        li[n-3] = 'm'
        li[n-2] = 't'
        li[n-1] = 'f'
        li = "".join(li)
  
        fout = open(li, "w",encoding = "latin-1")
        fout.write(chr(0xfa))
        fout.write(chr(0xce))
        fout.write(chr(0xfa))
        fout.write(chr(0xde))
  
        with open(filename,"r") as fin:
        	for line in fin:
                tokenize(line)
                insert(fout)
  
        fin.close()
        fout.close()

def makeWord(char,w):
#forms a word in the list w from the .mtf file
	w.append(char)
    return w

def makeTable(w,code,fout):
#adds the word derived from the .mtf file to the word table
	global decode_table
    global decoded_words
    temp = "".join(w)
    decode_table.append(temp)
    writeTextFile(fout,temp)
    decoded_words = decoded_words + 1
 
def updateTable(code,fout):
#if updates word table if a code from the .mtf file is read in that corresponds to a pre-existingword
    global decode_table
    global decoded_words
 
    val = decoded_words - code
    if decoded_words == 1:
        writeTextFile(fout,decode_table[val])
    else:
        cur = decode_table.pop(val)
        decode_table.append(cur)
        writeTextFile(fout,cur)

def writeTextFile(fout,st):
#prints a word to the .txt file
    fout.write(st)                    

def mtfDecode():
#decodes a .mtf file and makes a .txt file with the result of the decoding
    if len(sys.argv) != 1:
        filename = sys.argv[1]
        li = list(filename)
        n = len(li)
        li[n-3] = 't'
        li[n-2] = 'x'
        li[n-1] = 't'
        li = "".join(li)
        fout = open(li,"w")
 
        with open(filename,"rb") as fin:
             byte1 = bytes(fin.read(1))
             byte2 = bytes(fin.read(1))
             byte3 = bytes(fin.read(1))
             byte4 = bytes(fin.read(1))
             #checks for magic numbers, does nothing if they're not found
             if byte1 and byte3 == b'\xfa' and byte2 == b'\xce' and byte4 == b'\xde':
                w = []
                byte = bytes(fin.read(1))
                code = 1
                #reads in file byte by byte until there are no more bytes
                while True:
                    byte = bytes(fin.read(1))
                    ls = list(byte)
                    if len(ls) > 0:
                        temp = int(ls[0])
 
                        #checks if code value corresponds to pre-existing word in table
                        if temp  < code + 128 and temp > 128:
                            temp = temp - 128
                            updateTable(temp,fout)
                            last_pos = fin.tell()
                            val = fin.read(1)
                            val = list(val)
                            # prints a space if the next character isn't EOF or a new line
                            if len(val) > 0:
                                val = int(val[0])
                                if val != 10:
                                    fout.write(" ")
                            fin.seek(last_pos)
                            continue

                        #forms a word from values in file
                        if temp < 128:
                            letter = chr(ls[0])
                            #doesn't add new line characters to words
                            if letter != '\n':
                                w = makeWord(letter,w)
                            last_pos = fin.tell()
                            val = fin.read(1)
                            val = list(val)
                            if len(val) > 0:
                                cur = int(val[0])
                                #if the next character is a newline or a code value
                                #this will add the word to the word table
                                if cur > 128 or cur == 10:
                                    if w != []:
                                        makeTable(w,code,fout)
                                        w = []
                                        code = code + 1
                                        #write a space if next character isn't a new line
                                        if cur != 10:
                                            fout.write(" ")
                            fin.seek(last_pos)
                        #if the w list isn't empty and there are no more values to be read
                        #in, will add word to the word table
                        if w != []:
                            last_pos = fin.tell()
                            val = fin.read(1)
                            val = list(val)
                            if val == []:
                                makeTable(w,code,fout)
                                w = []
                            fin.seek(last_pos)

                        #writes a new line character if one is read in    
                        if temp == 10:
                            fout.write('\n')
                    if not byte:
                        break
        fin.close()
        fout.close()
        
command = os.path.basename(__file__)
if __name__ == "__main__" and command == "mtfencode.py":
    mtfEncode()
elif __name__ == "__main__" and command ==  "mtfdecode.py":
    mtfDecode()
                                                                           
