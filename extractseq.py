#this program will extract sequences given blast tabulated file
#input file: blast file,sequencefile
#output: hit sequences

import sys

blastfile=open(sys.argv[1]).readlines()
proteinfile=open(sys.argv[2]).readlines()
outputfile=open(sys.argv[3],'w')
_store=[]
def dupcheck(name):
	present=0
	for ts in _store:
		if name == ts:
			present=1
	return present
def findid(name):
	present=0
	copying=False
	for word in proteinfile:
		word_strip=word.strip()
		if word_strip.startswith('>'):
			if copying==True:
				break
			copying=False
			if name in word_strip[1:word_strip.index(' ')]:
				copying=True
				outputfile.write('\n'+word_strip+'\n')
				present=1
		elif copying:
			outputfile.write(word_strip)
	return present
for line in blastfile:
	line_strip=line.strip()
	line_split=line_strip.split(',')
#	line_split=line_strip.split('\t')
#	if 'gi|' in line_strip and not 'Query:' in line_strip and float(line_split[2])>=30 and float(line_split[12])>=60:
#	if not '%iden' in line_strip and float(line_split[2])>=30 and float(line_split[12])>=60:
#	if dupcheck(line_strip)==0:
#		_store.append(line_strip)
	if findid(line_split[0])==0:
		print 'not found',line_strip
