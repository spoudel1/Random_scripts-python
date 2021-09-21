#this script will calculate the average charge of a column in MSA
#input: 1) excel file containing MSA position, protein index 2) file containing the user interested index
#output: average charge for each user defined index

import sys
datafile=open(sys.argv[1]).readlines()
queryfile=open(sys.argv[2]).readlines()
fastafile=open(sys.argv[3]).readlines()
outputfile=open(sys.argv[4],'w')
_store=[]
_index={}
_charge={}
for line in queryfile:
    line_strip=line.strip()
    if not 'Nif-AB-H' in line_strip:
        _store.append(int(line_strip[line_strip.index('#')+1:line_strip.index('-')]))
_store.sort()
for word in datafile:
    word_strip=word.strip()
    word_split=word_strip.split(',')
    if not 'Aligned' in word_strip:
        for x in _store:
            if x == int(word_split[2]):
                _index[x]=word_split[0]
print _index
seqcount=1
for seq in fastafile:
    seq_strip=seq.strip()
    if not seq_strip.startswith('>'):
        count=1
        for y in seq_strip:
            for xt_k,xt in _index.items():
                if count==int(xt):
                    if y=='H' or y=='K' or y=='R':
                        if not _charge.has_key(xt_k):
                            _charge[xt_k]=1
                        else:
                            _charge[xt_k]+=1
                    elif y=='E' or y=='D':
                        if _charge.has_key(xt_k):
                            _charge[xt_k]=_charge[xt_k]-1
                        else:
                            _charge[xt_k]=-1
                    else:
                        if not _charge.has_key(xt_k):
                            _charge[xt_k]=0
            count+=1
        seqcount+=1
print _charge,'charge'
for key,value in _charge.items():
    outputfile.write(str(key)+'\t'+str(int(value)/float(seqcount))+'\n')
print seqcount


