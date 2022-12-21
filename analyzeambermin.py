#this script will sort the mmpbsa energyscores by ranking complex energy and binding energy
#input: amber combos csv file or any csv file that follows amber combos csv file pattern
#this script will sort the mmpbsa energyscores by ranking complex energy and binding energy
#input: amber combos csv file or any csv file that follows amber combos csv file pattern

import sys
import pandas as pd
import argparse
from collections import Counter
#be_index=int(sys.argv[2]) #index for complex energy. count from 0
#ce_index=int(sys.argv[3]) #index for binding energy. count from 0

def get_most_frequent_combination(combination_length, lists, number):
  # Flatten the list of lists into a single list
  flat_list = [item for sublist in lists for item in sublist]

  # Get all combinations of the specified length from the flattened list
  combinations = [tuple(flat_list[i:i+combination_length]) for i in range(len(flat_list)-combination_length+1)]

  # Count the frequency of each combination
  combination_counts = Counter(combinations)
  for k in combination_counts:
      combination_counts[k]=round(((combination_counts[k]/float(len(lists)))*100),2)
#  print(combination_counts.most_common((number)))
  # Return the most frequent combination
  return combination_counts.most_common(number)

#main loop
def main(argv):
    #Parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--datafile", type=str, help="mmpbsa datafile to sort", required=True, action='store')
    parser.add_argument("-l", "--toplistfile", type=str, help="file containing the top n candidates", required=False, action='store')
    parser.add_argument("-n", "--totalcan", type=str, help="total number of candidates user wants", required=False, action='store')
    parser.add_argument("-tv", "--threshold", type=str, help="specify the threshold value to filter the data", required=False, action='store')
    parser.add_argument("-cn", "--combo_length", type=str, help="specify the length of combinations you want for frequency calculation", required=False,action='store')
    parser.add_argument("-fn", "--topcombo", type=int, help="specify the total number of most frequent combinations you want to print", default=50, action='store')
    parser.add_argument("-c", "--combination", action='store_true')
    parser.add_argument("-tl", "--toplist", action='store_true')
    parser.add_argument("-o", "--outputfile", type=str, help="outputfile", required=True,action='store')

    args = parser.parse_args()
    topcombo = args.topcombo
    df = pd.read_csv(args.datafile,sep=",", skipinitialspace =True, header=None)
    if args.threshold:
        threshold=float(args.threshold)
    else:
        threshold=float(df[df[1] == 'WT'][6].iloc[0])
    outputfile=open(args.outputfile,'w')
    # Load the dataset
    if not args.combination:
    #    df = pd.read_csv(args.datafile,sep=",", skipinitialspace =True, header=None)
#        outputfile=open(args.datafile[:args.datafile.index('.')]+'_sorted.csv','w')
        df_data=df.iloc[:, 3:5] #make sure third, fourth and fifth column is complex energy, binder energy and peptide energy
        # Calculate the interquartile range (IQR)
        Q1 = df_data.quantile(0.25)
        Q3 = df_data.quantile(0.75)
        IQR = Q3 - Q1
        
        # Filter the dataset to only include values within the IQR
        df1 = df_data[~((df_data < (Q1 - 3 * IQR)) | (df_data > (Q3 + 3 * IQR))).any(axis=1)]
        #df1 = df_data[~((df_data.lt(Q1 - 3 * IQR)) | (df_data.gt (Q3 + 3 * IQR)))]
        
        #Sort the dataset based on binding energy
        #df2=(df.loc[df1.index]).sort_values('be')
        df2=(df.loc[df1.index]).sort_values(by=df.columns[6])

        #print the data to file_sorted.csv file
        outputfile.write('Sorted list: '+'\n')
        outputfile.write('binder,mutations,peptide,complexEnergy,binderEnergy,peptideEnergy,bindingEnergy'+'\n')
        df2.to_csv(outputfile,index=False, header=False)
        
        #selecting user specified number of candidates based on the threshold 
        if args.toplist:
            df4=[]
            totalcandidates=int(args.totalcan)
    #        threshold=float(args.threshold)
            df3=df2.to_numpy()
            for x in range(0, len(df3)):
                if df3[x][6]< threshold:
                    df4.append(df3[x])
            finaldf=(pd.DataFrame(df4)).head(totalcandidates)
            if args.toplistfile:
                listfile=open(args.toplistfile, 'w')
                finaldf.to_csv(listfile,index=False, header=False)
            else:
                outputfile.write('\n\n\n\n'+"Top "+str(totalcandidates)+" or maximum possible candidates"+'\n')
                outputfile.write('binder,mutations,peptide,complexEnergy,binderEnergy,peptideEnergy,bindingEnergy'+'\n')
                finaldf.to_csv(outputfile, mode="a", index=False, header=False)

            #print the result
         #   df_select=[list(df.iloc[:, 1][x].split('_')) for x in range(0, len(df.iloc[:, 1]))]
            df_select=[list(finaldf.iloc[:, 1][x].split('_')) for x in range(0, len(finaldf.iloc[:, 1]))]
            outputfile.write('\n\n\n\n'+"Most "+str(topcombo)+" frequnent combination(s)"+'\n')
            for i in range(1,5):
                most_frequent_combination = get_most_frequent_combination(i,df_select, topcombo)
                pd.DataFrame(most_frequent_combination).to_csv(outputfile, mode="a", index=False, header=False)
    #  print(most_frequent_combination)  # Output: [3, 4]
    elif args.combination:
        combo_length=int(args.combo_length)
     #   df = pd.read_csv(args.datafile,sep=",", skipinitialspace =True, header=None)
        df_select=[list(df.iloc[:, 1][x].split('_')) for x in range(0, len(df.iloc[:, 1]))]
        most_frequent_combination = get_most_frequent_combination(combo_length,df_select, topcombo)
#        print(combo_length)


#    print(df2)
if __name__ =="__main__":
    main(sys.argv[1:])



    




    
