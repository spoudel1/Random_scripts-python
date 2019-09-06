#this program will extract upstream and downstream sequences as required
#input file:seq id file
#outputfile: file that contains all 10 up and downstream files

import os
import sys

keyfile=open(sys.argv[1]).readlines()
_num=sys.argv[2]
#genomedir="path to the genomes"
justseqfile=open(sys.argv[4],'w') #this file contains only the sequence if of all the sequences
#csvfile=open(sys.argv[4],'w') # this file contains the matrix for entire database

def findid(name):  #this function will pull the upand downstream seqeunces
	present=0;count=0;tcount=0;_newseq='';_initial=0;temp='';seqname='';_store=[]
	downstream=0
	with open(sys.argv[3],'r') as _infile:
		for word in _infile:
			word_strip=word.strip()
			if word_strip.startswith('>'):
				if count>0:
					if name in seqname and downstream==0: #look for the genes
						if len(_store)==0:
#							justseqfile.write('>'+seqname+'\n')
							_parseseq=seqname.split(' ')
							temp='found'
							present=1
						else:
							for ij in range(0,len(_store)): #copies the # upstream sequences
#								justseqfile.write('>'+_store[ij][0]+'\n'+_store[ij][1]+'\n')
								_parseseq=_store[ij][0].split(' ')
								temp='found'
								present=1
#	        	        		justseqfile.write('>'+seqname+'\n')
					elif (_initial)==int(_num)+1 and not temp=='found':
						_store.pop(0)
						_initial=_initial-1
						_store.append([seqname,_newseq])
					elif not temp=='found':
						_store.append([seqname,_newseq])
				if not temp=='found':
					seqname=word_strip[1:]
					count=count+1	
					_initial=_initial+1
				else:
					if tcount<int(_num): #prints the # downstream sequences
						downstream=1
#						justseqfile.write(_newseq+'\n'+word_strip+'\n')
						justseqfile.write(word_strip+'\n')
						tcount=tcount+1
					elif tcount==int(_num):
						justseqfile.write(_newseq)
						break
					count=count+1
					_initial=_initial+1
				_newseq=''
			else:
				_newseq=_newseq+word_strip
		if not present==1 and downstream==0:
			if downstream==1:
				print 'something wrong'
			if name in seqname: #if the sequences match is at last than prints the first # upstream and prints this
				for ij in range(0,len(_store)):
					justseqfile.write('>'+_store[ij][0]+'\n'+_store[ij][1]+'\n')
					_parseseq=_store[ij][0].split(' ')
					justseqfile.write('>'+seqname+'\n')
					present=1
		if present==1:
			justseqfile.write('\n'+'\n'+'\n'+'\n')
		#	break
	return present
for line in keyfile: #this will open the key file
	line_strip=line.strip()
	if findid(line_strip)==0:
		print 'sequence not found',line_strip

