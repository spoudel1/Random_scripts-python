#this program will extract all the genomes that contains user specified phylum from ncbi - database based on 05/05/2020 
#python extractgenomes_fromncbi.py assembly_summary_refseq_completegenomesonly_filtered.txt fullnamelineage.dmp
#Here, the code takes two files: 1) summary file that contains all the complete genome ftp and 2) file that contains taxonomic information (i.e., Firmicutes etc)
#This code will create three main things: 1) directory called "Firmicutesonly" - this will contain all the complete genomes, 2) "Firmicutes_flanking_gene.txt" - this will contain all the protein id of all the extracted genome and 3) "Taxonomy_firmicutes.txt" - this will contain the entire lineage information (e.g., family, order, class etc.)
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
#firmicutes=open("Taxonomy_firmicutes.txt","w")
#flankingene=open("Firmicutes_flanking_gene.txt","w")
firmpath=os.path.join(os.getcwd(),"Firmicutesonly")
if os.path.isdir(firmpath):
    firmicutes=open("Taxonomy_firmicutes.txt","a")
    flankingene=open("Firmicutes_flanking_gene.txt","a")
else:
    os.mkdir(firmpath) #creates a directory
    firmicutes=open("Taxonomy_firmicutes.txt","w")
    flankingene=open("Firmicutes_flanking_gene.txt","w")

_checkpoint=[]
if os.path.isfile(os.path.join(os.getcwd(),"checkpoint.txt")):
        tcheckpoint=open("checkpoint.txt","r")
        for cline in tcheckpoint:
            _checkpoint.append(cline.strip())
        tcheckpoint.close()
        checkpoint=open("checkpoint.txt","w")
else:
    checkpoint=open("checkpoint.txt","w")
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
                                        os.chdir(firmpath)
					subprocess.call(["wget",new])
                                        new_split=new.split('/')
                                        newgenomefile=new_split[-1][:new_split[-1].index(".gz")]
                                        if os.path.isfile(firmpath+"/"+newgenomefile+".gz"):
                                            inf=gzip.GzipFile(firmpath+"/"+newgenomefile+".gz",'rb')
                                            s=inf.read()
					    inf.close()
					    outf=file(firmpath+"/"+newgenomefile,'wb')
					    outf.write(s)
					    outf.close()
					    os.remove(firmpath+"/"+newgenomefile+".gz")
					    os.chdir('../')
					    _newwork=''
                                            if os.path.isfile(firmpath+"/"+newgenomefile):
                                                _file=open(firmpath+"/"+newgenomefile).readlines()
						scount=0
                                                tpresent=1
                                                flankingene.write(newgenomefile[:newgenomefile.index('_protein')])
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
#reads the entire assembly report file]
for line in assemblyfile:
    line_strip=line.strip()
    if (not 'assembly_accession' in line_strip):
        line_split=line_strip.split('\t')
        wpresent=0
        for dgen in _checkpoint:
            if line_split[0].strip()==dgen:
                wpresent=1
                break
        if wpresent==0:
            apresent,temp_line=checkphylum(line_split[1])
            if (apresent==1):
                if findgenome(line_split[4],'1')==1:
                    firmicutes.write(line_strip+'\t'+temp_line+'\n')
                else:
                    print "phylum not found",line_split[0]
            else:
                print "not Firmicutes", line_split[0]
            checkpoint.write(line_split[0]+"\n")
