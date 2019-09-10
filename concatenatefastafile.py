#this script will concatenate two aligned fasta file
#input: two fasta file, id file
#output: concatenated fasta file

import sys

nfnafile=open(sys.argv[1]).readlines()
nfnbfile=open(sys.argv[2]).readlines()
idfile=open(sys.argv[3]).readlines()
outputfile=open(sys.argv[4],'w')

def findnfnb(tname):
	tpresent=0
	copying=False
	_tempbseq=''
	for word in nfnbfile:
		word_strip=word.strip()
		if word_strip.startswith('>'):
			copying=False
			if not _tempbseq=='':
				tpresent=1
				break
			if tname in word_strip:
				copying=True
		elif copying:
			_tempbseq=_tempbseq+word_strip
	if not _tempbseq=='':
		tpresent=1
	return tpresent,_tempbseq
def findid(name):
	present=0
	sequence=''
	for ts in idfile:	
		ts_strip=ts.strip()
		ts_split=ts_strip.split('\t')
		if name == ts_split[1]:
			bpresent,bseq=findnfnb(ts_split[2])
			if bpresent==1:
				sequence=bseq
				present=1
	return present,sequence	
count=0
sequence_1=''
for line in nfnafile:
	line_strip=line.strip()
	if line_strip.startswith('>'):
		if count>0:
			seq_split=seq.split(' ')
			_temp=seq_split[0]
			abpresent,nfnbseq= findid(_temp[1:])
			if abpresent==1:
				outputfile.write(seq+'\n'+sequence_1+nfnbseq+'\n')
				sequence_1=''
			else:
				print 'what the hell',seq
				sequence_1=''
			seq=line_strip
		else:
			count=1
			seq=line_strip
	else:
		sequence_1=sequence_1+line_strip
seq_split=seq.split(' ')
_temp=seq_split[0]
abpresent,nfnbseq=findid(_temp[1:])
if abpresent==1:
	outputfile.write(seq+'\n'+sequence_1+nfnbseq+'\n')
else:
	print 'what the hell outside',seq
