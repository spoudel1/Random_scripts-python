#this script will count the total number of interactions given a schema generated contact files
import sys
#import matplotlib.pyplot as plt


degrees={}
outputfile=open(sys.argv[2],'w')
with open(sys.argv[1],'r') as inputfile:
    for line in inputfile:
        if not line.startswith('#'):
            line_split=line.strip().split('\t')
#            print(line_split)

            #getting source and finding it's interaction
            if line_split[3] in degrees:
                degrees[line_split[3]] +=1
            else:
                degrees[line_split[3]]=1

            #getting target and finding it's interaction
            if line_split[4] in degrees:
                degrees[line_split[4]] +=1
            else:
                degrees[line_split[4]]=1


for key,value in degrees.items():
    outputfile.write(str(key)+'\t'+str(value)+'\n')
#plt.plot(degrees.keys(),degrees.values())
#plt.xticks(range(min((degrees.keys())), max((degrees.values()))+1, 5), rotation=45)
#plt.tight_layout()
#plt.xlabel('position')
#plt.ylabel('Total # of interactions')
#plt.title('PS04')

#plt.show()
#plt.savefig(sys.argv[3])



