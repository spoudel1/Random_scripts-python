import pandas as pd
import sys
import csv
#read the file

def getpenalty(inputf,difference,mutation):
    count=0
    aaorder=[]
    totalsum=0
    with open(inputf) as inputfile:
        matrix = csv.reader(inputfile, delimiter=' ')
        for row in matrix:
            if not row[0].startswith('#'):
                aaorder.append(list(filter(None,row)))
        aaorder[0].insert(0,'aa')
    mutation_split=mutation.strip().split(',')
    for mut in mutation_split:
        pos=[y for y in range(0,len(aaorder[0]))  if mut[:1]==aaorder[0][y]]
        for x in aaorder:
            if mut[-1:] == x[0]:
                totalsum+=(int(x[pos[0]])+difference)
    print(totalsum, 'totalsum ')
    return totalsum
getpenalty(sys.argv[1],int(sys.argv[2]),sys.argv[3])
