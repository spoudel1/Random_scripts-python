#this script will match the protein sequence id given two files that might contain genes from same organism
#input: two tab delimited files with protein id and organisms name
#output: file that contains both sequence ids

import sys
outputfile=open(sys.argv[1],'w')
_store1={}
_store2={}

with open(sys.argv[1],'r') as file1:
    for t1 in file1:
        t1_split=t1.split('\t')
        _store1[t1_split[0][:t1_split[0].index('.')].strip()]=t1_split[1].strip()
        _store2[t1_split[2][:t1_split[2].index('.')].strip()]=t1_split[3].strip()

#with open(sys.argv[2],'r') as file2:
#    for t2 in file2:
#        t2_split=t2.split('\t')
#        _store2[t2_split[0].strip()]=t2_split[1].strip()

for key,value in _store1.items():
    for tkey,tvalue in _store2.items():
        if tvalue in value:
            if tkey[:-5]==key[:-5] and int(tkey[-5:])+10<int(key[-5:]) or int(tkey[-5:])-10<int(key[-5:]):
                outputfile.write(key+'\t'+tkey+'\t'+value+'\n')

