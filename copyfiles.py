#this script will copy select files present in your key files 
#input:keyfile,folder path
#output: folder with select files

import sys
import os
import shutil 

path='test1' #source directory
pathd='dest' #destination directory
def findfile(name):
	present=0
        for root,dirs,files in os.walk(path):
	    for tfile in files:
		if name in tfile:
                    shutil.copy2(path+'/'+tfile,pathd+'/')
                    present=1
                    break
        return present
			 
with open (sys.argv[1],'r') as keyfile: #tab delimited file that contains pdb name in column 1 and group in column 2
	for line in keyfile:
		line_strip=line.strip()
		line_split=line_strip.split('\t')
                print line_strip
		if line_split[1]=='0' or line_split[1]=='7':
                        print 'came'
			if findfile(line_split[0]+'.pdb')==0:
				print 'not found',line_split[0]	
