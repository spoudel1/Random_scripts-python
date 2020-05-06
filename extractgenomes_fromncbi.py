#this program will extract all the genomes that contains user specified phylum from ncbi - database based on 05/05/2020 
#input: assembly summary refseq file and fullname lineage.dmp taxonomy file
#output: All genomes, tabulated sequence id, file with flanking genes

import sys
import shutil
import urllib
import os
import gzip
import subprocess

assemblyfile=open(sys.argv[1]).readlines()
taxonomyfile=open(sys.argv[2]).readlines()
phylum='Firmicutes'
firmicutes=open("Taxonomy_firmicutes.txt","w")
flankingene=open("Firmicutes_flanking_gene.txt","w")
firmpath=os.path.join(os.getcwd(),"Firmicutesonly")
os.mkdir(firmpath) #creates a directory
#function extracts the genome from the ncbi site
def findgenome(tname,tseq):
	tpresent=0
	f=urllib.urlopen(tname)
	for fline in f:
		if '.faa' in fline:
			fline_strip=fline.strip()
			fline_split=fline_strip.split(' ')
			for tj in fline_split:
				if 'protein.faa.gz' in tj:
					new=tname.strip()+'/'+tj.strip()
					path_1="test/"
                                        os.chdir(firmpath)
					subprocess.call(["wget",new])		
					for dirs in os.listdir('.'):
						if '.gz' in dirs:
							inf=gzip.GzipFile(dirs,'rb')
							s=inf.read()
							inf.close()
							_tempfile=dirs[:dirs.index("g")-1]
							outf=file(_tempfile,'wb')
							outf.write(s)
							outf.close()
							os.remove(dirs)
							os.chdir('../')
							_newwork=''
							for root, dirs, files in os.walk(firmpath):#workfile=[f for f in os.listdir('.') if os.path.isfile(f)]
								for work in files:#workfile:
                                                                    if 'protein.faa' in work:# or 'GCA' in work:
										_file=open(firmpath+"/"+work).readlines()
										_newwork=work
										scount=0
                                                                                tpresent=1
                                                                                flankingene.write(work)
										for sline in _file:
											sline_strip=sline.strip()
											if sline_strip.startswith('>'):
                                                                                            sline_split=sline_strip.split(' ')
                                                                                            if scount==0:
                                                                                                flankingene.write("\t"+sline_split[0][1:])
                                                                                                scount+=1
                                                                                            else:
                                                                                                flankingene.write(","+sline_split[0][1:])

							flankingene.write("\n")
                                                        os.chdir(firmpath)
							outf.close()
							break
	return tpresent
									
#this function will check for phylum firmicutes
def checkphylum(name):
    tpresent=0
    temp_tax=''
    for word in taxonomyfile:
        word_strip=word.strip()
        word_split=word_strip.split('|')
        if (name.strip()==word_split[0].strip()):
            if ('Firmicutes' in word_strip):
                temp_tax=word_split[2]
                tpresent=1
                break
    return tpresent,temp_tax
#reads the entire assembly report file
for line in assemblyfile:
	line_strip=line.strip()
        if (not 'assembly_accession' in line_strip):
            line_split=line_strip.split('\t')
            apresent,temp_line=checkphylum(line_split[1])
            if (apresent==1):
              #  if findgenome(line_split[4],'1')==0:
	#	    print 'not found',line_split[0]
                firmicutes.write(line_strip+'\t'+temp_line+'\n')
        #    else:
         #       print "phylum not found",line_split[0]
