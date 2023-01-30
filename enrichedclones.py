#this script will selected enriched clones at each rounds
#input: list of EVmutations.tsv files
#output: last round mutationtsv file with average diff

import sys
import pandas as pd
import numpy as np
import subprocess
from sklearn.linear_model import LinearRegression

_store=[]
with open (sys.argv[1],'r') as inputfile:
    for line in inputfile:
        _store.append(line.strip())
lastfile=pd.read_csv(_store[-1], sep='\t')
dflast=lastfile[["Position", "Mutation", "Enrichment Value"]]
dflast=dflast[dflast["Enrichment Value"]>1]
df1=lastfile[lastfile["Enrichment Value"]>1]

for k in range(0, len(_store)-1):
    dftemp=pd.read_csv(_store[k], sep='\t')
    df2=dftemp[["Position", "Mutation", "Enrichment Value"]]
    df2=df2[df2["Enrichment Value"]>-50]
    df2=df2.rename(columns={"Enrichment Value": "Enrichment Value_"+str(k)})
    dflast=dflast.merge(df2)
#column_to_move=dflast.pop("Enrichment Value")
dflast.insert(len(dflast.columns)-1, "Enrichment value", dflast.pop("Enrichment Value"))
tcount=0
for index, row in dflast.iterrows():
    temp=((dflast.iloc[index,2:(2+len(_store))])).values.reshape(len(_store), 1)
    tempx=(pd.Series(range(0, len(_store)))).values.reshape(len(_store), 1)
    model=LinearRegression().fit(tempx,temp)
    r_sq=model.score(tempx,temp)
    if tcount==0:
        dflast.insert(len(_store)+2, "r square value", r_sq)
        dflast.insert(len(_store)+3, "slope",model.coef_[0][0])
        tcount=1
    else:
        dflast.at[index,'r square value']=r_sq
        dflast.at[index,'slope']=model.coef_[0][0]
dflast=dflast.sort_values(by=['r square value'], ascending=False)
print (dflast)
dflast.to_csv('testing.tsv', sep="\t")
    
'''
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--list")
'''
