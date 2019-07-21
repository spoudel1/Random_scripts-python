#this sequence will extract all or user specified number of sequences
#to know how to run this script please use -h flag 

import sys
import argparse

#this function will extract the required sequences
def extractseq(_b1store,d1file):
    for key,value in _b1store.items():
        tcount=0
        for kkey in _b1store.keys():
            f=open(kkey,'w')
            for tvalue in _b1store[kkey]:
             #   print kkey,'and',_b1store[kkey],tvalue
             #   raw_input()
                with open(d1file, 'r') as datafile:
                    copying=False
                    for dline in datafile:
                        dline_strip=dline.strip()
                        if dline_strip.startswith('>'):
                             copying=False
                             if tvalue in dline_strip:
                                 f.write('\n'+dline_strip+'\n')
                                 copying=True
                        elif copying:
                             f.write(dline_strip)
        f.close()
       #     tcount+=1
#this function will pull out the required number of sequences
def findid(n,_q2store,bfile,dfile):
    _bstore={}
    for ts in _q2store:
        count=0
        with open(bfile, 'r') as blastfile:
            for bline in blastfile:
                bline_strip=bline.strip()
                bline_split=bline_strip.split('-')
               # if ts in _bstore.keys():
                #    _bstore.setdefault(ts,[]).append(bline_split[0])
                 #   count=0
               # else:
                if ts in bline_strip:
                    if n>0:
                        if count<int(n):
                            _bstore.setdefault(ts,[]).append(bline_split[0].strip())
                            count+=1
                    else:
                        _bstore.setdefault(ts,[]).append(bline_split[0].strip())
    extractseq(_bstore,dfile)

#this function reads queryfile and stores the seqid in an array
def queryseq(n,qfile,bfile,dfile):
    queryfile=open(qfile).readlines()
    _q1store=[]
    for qline in queryfile:
        if qline.startswith('>'):
            qline_strip=qline.strip()
            qline_split=qline_strip.split(' ')
            _q1store.append(qline_split[0][1:])
    findid(n,_q1store,bfile,dfile)

#main function
if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Extracts all or user specified number of sequences. This script will require files: file that contains the reference sequences (queryfile), blast (hmmer) result file and the subject fasta file against which the query sequence was blasted against")
    parser.add_argument('-n',type=int, default=0, help='provide the number of sequences you wish to want to extract. Default is set to extract all')
    parser.add_argument('-q',metavar="queryfile", required=True,help="queryfile that contains the query reference sequences")
    parser.add_argument('-b',metavar="blastfile",required=True,help="blast result file obtained from hmmer")
    parser.add_argument('-d',metavar="fastadatafile",required=True,help="original fasta file that contains all the protein sequences")
  #  parser.add_argument('-o',metavar="outputfile",type=argparse.FileType('w'),required=True,help="outputfile")
    args=parser.parse_args()
    queryseq(args.n,args.q,args.b,args.d)
    


