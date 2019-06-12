#this script will extract sequences with specific residues given a file containing list of positions
#input: residue position file and clustal file
#output: aligned sequences with specific residues

import sys

posfile=open(sys.argv[1]).readlines()
alignfile=open(sys.argv[2]).readlines()
outputfile=open(sys.argv[3],'w')
_store=[]
_store_align=[]
for line in posfile:
    line_strip=line.strip()
    line_split=line_strip.split(' ')
    _store.append(line_split[1][:line_split[1].index('.')])
seqid=''
sequence=''
count=0
for word in alignfile:
    word_strip=word.strip()
    if word_strip.startswith('>'):
        if count>0:
            outputfile.write('\n'+seqid+'\n')
            if 'AAF81681' in seqid:
                gcount=0
                scount=0
                for ts in sequence:
                    if not '-' in ts:
                        scount+=1
                        for x in _store:
                            if scount == int(x):
                                _store_align.append(gcount)
                                outputfile.write(ts)
                    gcount+=1
            else:
                for tst in _store_align:
                    outputfile.write(sequence[tst])
        else:
            count+=1
        sequence=''
        seqid=word_strip
    else:
        sequence+=word_strip
