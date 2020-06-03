import numpy as np
import matplotlib.pyplot as plt
import itertools as it
from VictorParser.loadnpz import *







def bigOne(path,dataname,mostlyD,allH,deuterium):
    coordsdict, weightsdict = concatenateseparatenpz(path)
    dictionarycount = 0
    filenumbers = []
    allresults = []
    for coordsnumber, coords in coordsdict.items():
        dictionarycount += 1
        filenumbers.append(coordsnumber)
        weights = weightsdict[f'{coordsnumber}'].T
        totalweight=np.sum(weights)
        distances = {
            '3to4Count': [1,3],
            '4to5Count': [4,6],
            '4to6Count': [5,9],
            '5to6Count': [7,9],
            '6to1Count': [10,12],
            '1to2Count': [13,15],
            '1to3Count': [14,0],
            '2to3Count': [16,0],
            '2to5Count': [17,6]}
        results = {
            '3to4Count': 0,
            '4to5Count': 0,
            '4to6Count': 0,
            '5to6Count': 0,
            '6to1Count': 0,
            '1to2Count': 0,
            '1to3Count': 0,
            '2to3Count': 0,
            '2to5Count': 0,
            "3to4Countand4to5CountCount": 0,
            "3to4Countand4to6CountCount": 0,
            "3to4Countand5to6CountCount": 0,
            "3to4Countand6to1CountCount": 0,
            "3to4Countand1to2CountCount": 0,
            "3to4Countand1to3CountCount": 0,
            "3to4Countand2to3CountCount": 0,
            "3to4Countand2to5CountCount": 0,
            "4to5Countand4to6CountCount": 0,
            "4to5Countand5to6CountCount": 0,
            "4to5Countand6to1CountCount": 0,
            "4to5Countand1to2CountCount": 0,
            "4to5Countand1to3CountCount": 0,
            "4to5Countand2to3CountCount": 0,
            "4to5Countand2to5CountCount": 0,
            "4to6Countand5to6CountCount": 0,
            "4to6Countand6to1CountCount": 0,
            "4to6Countand1to2CountCount": 0,
            "4to6Countand1to3CountCount": 0,
            "4to6Countand2to3CountCount": 0,
            "4to6Countand2to5CountCount": 0,
            "5to6Countand6to1CountCount": 0,
            "5to6Countand1to2CountCount": 0,
            "5to6Countand1to3CountCount": 0,
            "5to6Countand2to3CountCount": 0,
            "5to6Countand2to5CountCount": 0,
            "6to1Countand1to2CountCount": 0,
            "6to1Countand1to3CountCount": 0,
            "6to1Countand2to3CountCount": 0,
            "6to1Countand2to5CountCount": 0,
            "1to2Countand1to3CountCount": 0,
            "1to2Countand2to3CountCount": 0,
            "1to2Countand2to5CountCount": 0,
            "1to3Countand2to3CountCount": 0,
            "1to3Countand2to5CountCount": 0,
            "2to3Countand2to5CountCount": 0,
            "3to4Countand4to5Countand4to6CountCount": 0,
            "3to4Countand4to5Countand5to6CountCount": 0,
            "3to4Countand4to5Countand6to1CountCount": 0,
            "3to4Countand4to5Countand1to2CountCount": 0,
            "3to4Countand4to5Countand1to3CountCount": 0,
            "3to4Countand4to5Countand2to3CountCount": 0,
            "3to4Countand4to5Countand2to5CountCount": 0,
            "3to4Countand4to6Countand5to6CountCount": 0,
            "3to4Countand4to6Countand6to1CountCount": 0,
            "3to4Countand4to6Countand1to2CountCount": 0,
            "3to4Countand4to6Countand1to3CountCount": 0,
            "3to4Countand4to6Countand2to3CountCount": 0,
            "3to4Countand4to6Countand2to5CountCount": 0,
            "3to4Countand5to6Countand6to1CountCount": 0,
            "3to4Countand5to6Countand1to2CountCount": 0,
            "3to4Countand5to6Countand1to3CountCount": 0,
            "3to4Countand5to6Countand2to3CountCount": 0,
            "3to4Countand5to6Countand2to5CountCount": 0,
            "3to4Countand6to1Countand1to2CountCount": 0,
            "3to4Countand6to1Countand1to3CountCount": 0,
            "3to4Countand6to1Countand2to3CountCount": 0,
            "3to4Countand6to1Countand2to5CountCount": 0,
            "3to4Countand1to2Countand1to3CountCount": 0,
            "3to4Countand1to2Countand2to3CountCount": 0,
            "3to4Countand1to2Countand2to5CountCount": 0,
            "3to4Countand1to3Countand2to3CountCount": 0,
            "3to4Countand1to3Countand2to5CountCount": 0,
            "3to4Countand2to3Countand2to5CountCount": 0,
            "4to5Countand4to6Countand5to6CountCount": 0,
            "4to5Countand4to6Countand6to1CountCount": 0,
            "4to5Countand4to6Countand1to2CountCount": 0,
            "4to5Countand4to6Countand1to3CountCount": 0,
            "4to5Countand4to6Countand2to3CountCount": 0,
            "4to5Countand4to6Countand2to5CountCount": 0,
            "4to5Countand5to6Countand6to1CountCount": 0,
            "4to5Countand5to6Countand1to2CountCount": 0,
            "4to5Countand5to6Countand1to3CountCount": 0,
            "4to5Countand5to6Countand2to3CountCount": 0,
            "4to5Countand5to6Countand2to5CountCount": 0,
            "4to5Countand6to1Countand1to2CountCount": 0,
            "4to5Countand6to1Countand1to3CountCount": 0,
            "4to5Countand6to1Countand2to3CountCount": 0,
            "4to5Countand6to1Countand2to5CountCount": 0,
            "4to5Countand1to2Countand1to3CountCount": 0,
            "4to5Countand1to2Countand2to3CountCount": 0,
            "4to5Countand1to2Countand2to5CountCount": 0,
            "4to5Countand1to3Countand2to3CountCount": 0,
            "4to5Countand1to3Countand2to5CountCount": 0,
            "4to5Countand2to3Countand2to5CountCount": 0,
            "4to6Countand5to6Countand6to1CountCount": 0,
            "4to6Countand5to6Countand1to2CountCount": 0,
            "4to6Countand5to6Countand1to3CountCount": 0,
            "4to6Countand5to6Countand2to3CountCount": 0,
            "4to6Countand5to6Countand2to5CountCount": 0,
            "4to6Countand6to1Countand1to2CountCount": 0,
            "4to6Countand6to1Countand1to3CountCount": 0,
            "4to6Countand6to1Countand2to3CountCount": 0,
            "4to6Countand6to1Countand2to5CountCount": 0,
            "4to6Countand1to2Countand1to3CountCount": 0,
            "4to6Countand1to2Countand2to3CountCount": 0,
            "4to6Countand1to2Countand2to5CountCount": 0,
            "4to6Countand1to3Countand2to3CountCount": 0,
            "4to6Countand1to3Countand2to5CountCount": 0,
            "4to6Countand2to3Countand2to5CountCount": 0,
            "5to6Countand6to1Countand1to2CountCount": 0,
            "5to6Countand6to1Countand1to3CountCount": 0,
            "5to6Countand6to1Countand2to3CountCount": 0,
            "5to6Countand6to1Countand2to5CountCount": 0,
            "5to6Countand1to2Countand1to3CountCount": 0,
            "5to6Countand1to2Countand2to3CountCount": 0,
            "5to6Countand1to2Countand2to5CountCount": 0,
            "5to6Countand1to3Countand2to3CountCount": 0,
            "5to6Countand1to3Countand2to5CountCount": 0,
            "5to6Countand2to3Countand2to5CountCount": 0,
            "6to1Countand1to2Countand1to3CountCount": 0,
            "6to1Countand1to2Countand2to3CountCount": 0,
            "6to1Countand1to2Countand2to5CountCount": 0,
            "6to1Countand1to3Countand2to3CountCount": 0,
            "6to1Countand1to3Countand2to5CountCount": 0,
            "6to1Countand2to3Countand2to5CountCount": 0,
            "1to2Countand1to3Countand2to3CountCount": 0,
            "1to2Countand1to3Countand2to5CountCount": 0,
            "1to2Countand2to3Countand2to5CountCount": 0,
            "1to3Countand2to3Countand2to5CountCount": 0,
            "3to4Countand4to5Countand4to6Countand5to6CountCount": 0,
            "3to4Countand4to5Countand4to6Countand6to1CountCount": 0,
            "3to4Countand4to5Countand4to6Countand1to2CountCount": 0,
            "3to4Countand4to5Countand4to6Countand1to3CountCount": 0,
            "3to4Countand4to5Countand4to6Countand2to3CountCount": 0,
            "3to4Countand4to5Countand4to6Countand2to5CountCount": 0,
            "3to4Countand4to5Countand5to6Countand6to1CountCount": 0,
            "3to4Countand4to5Countand5to6Countand1to2CountCount": 0,
            "3to4Countand4to5Countand5to6Countand1to3CountCount": 0,
            "3to4Countand4to5Countand5to6Countand2to3CountCount": 0,
            "3to4Countand4to5Countand5to6Countand2to5CountCount": 0,
            "3to4Countand4to5Countand6to1Countand1to2CountCount": 0,
            "3to4Countand4to5Countand6to1Countand1to3CountCount": 0,
            "3to4Countand4to5Countand6to1Countand2to3CountCount": 0,
            "3to4Countand4to5Countand6to1Countand2to5CountCount": 0,
            "3to4Countand4to5Countand1to2Countand1to3CountCount": 0,
            "3to4Countand4to5Countand1to2Countand2to3CountCount": 0,
            "3to4Countand4to5Countand1to2Countand2to5CountCount": 0,
            "3to4Countand4to5Countand1to3Countand2to3CountCount": 0,
            "3to4Countand4to5Countand1to3Countand2to5CountCount": 0,
            "3to4Countand4to5Countand2to3Countand2to5CountCount": 0,
            "3to4Countand4to6Countand5to6Countand6to1CountCount": 0,
            "3to4Countand4to6Countand5to6Countand1to2CountCount": 0,
            "3to4Countand4to6Countand5to6Countand1to3CountCount": 0,
            "3to4Countand4to6Countand5to6Countand2to3CountCount": 0,
            "3to4Countand4to6Countand5to6Countand2to5CountCount": 0,
            "3to4Countand4to6Countand6to1Countand1to2CountCount": 0,
            "3to4Countand4to6Countand6to1Countand1to3CountCount": 0,
            "3to4Countand4to6Countand6to1Countand2to3CountCount": 0,
            "3to4Countand4to6Countand6to1Countand2to5CountCount": 0,
            "3to4Countand4to6Countand1to2Countand1to3CountCount": 0,
            "3to4Countand4to6Countand1to2Countand2to3CountCount": 0,
            "3to4Countand4to6Countand1to2Countand2to5CountCount": 0,
            "3to4Countand4to6Countand1to3Countand2to3CountCount": 0,
            "3to4Countand4to6Countand1to3Countand2to5CountCount": 0,
            "3to4Countand4to6Countand2to3Countand2to5CountCount": 0,
            "3to4Countand5to6Countand6to1Countand1to2CountCount": 0,
            "3to4Countand5to6Countand6to1Countand1to3CountCount": 0,
            "3to4Countand5to6Countand6to1Countand2to3CountCount": 0,
            "3to4Countand5to6Countand6to1Countand2to5CountCount": 0,
            "3to4Countand5to6Countand1to2Countand1to3CountCount": 0,
            "3to4Countand5to6Countand1to2Countand2to3CountCount": 0,
            "3to4Countand5to6Countand1to2Countand2to5CountCount": 0,
            "3to4Countand5to6Countand1to3Countand2to3CountCount": 0,
            "3to4Countand5to6Countand1to3Countand2to5CountCount": 0,
            "3to4Countand5to6Countand2to3Countand2to5CountCount": 0,
            "3to4Countand6to1Countand1to2Countand1to3CountCount": 0,
            "3to4Countand6to1Countand1to2Countand2to3CountCount": 0,
            "3to4Countand6to1Countand1to2Countand2to5CountCount": 0,
            "3to4Countand6to1Countand1to3Countand2to3CountCount": 0,
            "3to4Countand6to1Countand1to3Countand2to5CountCount": 0,
            "3to4Countand6to1Countand2to3Countand2to5CountCount": 0,
            "3to4Countand1to2Countand1to3Countand2to3CountCount": 0,
            "3to4Countand1to2Countand1to3Countand2to5CountCount": 0,
            "3to4Countand1to2Countand2to3Countand2to5CountCount": 0,
            "3to4Countand1to3Countand2to3Countand2to5CountCount": 0,
            "4to5Countand4to6Countand5to6Countand6to1CountCount": 0,
            "4to5Countand4to6Countand5to6Countand1to2CountCount": 0,
            "4to5Countand4to6Countand5to6Countand1to3CountCount": 0,
            "4to5Countand4to6Countand5to6Countand2to3CountCount": 0,
            "4to5Countand4to6Countand5to6Countand2to5CountCount": 0,
            "4to5Countand4to6Countand6to1Countand1to2CountCount": 0,
            "4to5Countand4to6Countand6to1Countand1to3CountCount": 0,
            "4to5Countand4to6Countand6to1Countand2to3CountCount": 0,
            "4to5Countand4to6Countand6to1Countand2to5CountCount": 0,
            "4to5Countand4to6Countand1to2Countand1to3CountCount": 0,
            "4to5Countand4to6Countand1to2Countand2to3CountCount": 0,
            "4to5Countand4to6Countand1to2Countand2to5CountCount": 0,
            "4to5Countand4to6Countand1to3Countand2to3CountCount": 0,
            "4to5Countand4to6Countand1to3Countand2to5CountCount": 0,
            "4to5Countand4to6Countand2to3Countand2to5CountCount": 0,
            "4to5Countand5to6Countand6to1Countand1to2CountCount": 0,
            "4to5Countand5to6Countand6to1Countand1to3CountCount": 0,
            "4to5Countand5to6Countand6to1Countand2to3CountCount": 0,
            "4to5Countand5to6Countand6to1Countand2to5CountCount": 0,
            "4to5Countand5to6Countand1to2Countand1to3CountCount": 0,
            "4to5Countand5to6Countand1to2Countand2to3CountCount": 0,
            "4to5Countand5to6Countand1to2Countand2to5CountCount": 0,
            "4to5Countand5to6Countand1to3Countand2to3CountCount": 0,
            "4to5Countand5to6Countand1to3Countand2to5CountCount": 0,
            "4to5Countand5to6Countand2to3Countand2to5CountCount": 0,
            "4to5Countand6to1Countand1to2Countand1to3CountCount": 0,
            "4to5Countand6to1Countand1to2Countand2to3CountCount": 0,
            "4to5Countand6to1Countand1to2Countand2to5CountCount": 0,
            "4to5Countand6to1Countand1to3Countand2to3CountCount": 0,
            "4to5Countand6to1Countand1to3Countand2to5CountCount": 0,
            "4to5Countand6to1Countand2to3Countand2to5CountCount": 0,
            "4to5Countand1to2Countand1to3Countand2to3CountCount": 0,
            "4to5Countand1to2Countand1to3Countand2to5CountCount": 0,
            "4to5Countand1to2Countand2to3Countand2to5CountCount": 0,
            "4to5Countand1to3Countand2to3Countand2to5CountCount": 0,
            "4to6Countand5to6Countand6to1Countand1to2CountCount": 0,
            "4to6Countand5to6Countand6to1Countand1to3CountCount": 0,
            "4to6Countand5to6Countand6to1Countand2to3CountCount": 0,
            "4to6Countand5to6Countand6to1Countand2to5CountCount": 0,
            "4to6Countand5to6Countand1to2Countand1to3CountCount": 0,
            "4to6Countand5to6Countand1to2Countand2to3CountCount": 0,
            "4to6Countand5to6Countand1to2Countand2to5CountCount": 0,
            "4to6Countand5to6Countand1to3Countand2to3CountCount": 0,
            "4to6Countand5to6Countand1to3Countand2to5CountCount": 0,
            "4to6Countand5to6Countand2to3Countand2to5CountCount": 0,
            "4to6Countand6to1Countand1to2Countand1to3CountCount": 0,
            "4to6Countand6to1Countand1to2Countand2to3CountCount": 0,
            "4to6Countand6to1Countand1to2Countand2to5CountCount": 0,
            "4to6Countand6to1Countand1to3Countand2to3CountCount": 0,
            "4to6Countand6to1Countand1to3Countand2to5CountCount": 0,
            "4to6Countand6to1Countand2to3Countand2to5CountCount": 0,
            "4to6Countand1to2Countand1to3Countand2to3CountCount": 0,
            "4to6Countand1to2Countand1to3Countand2to5CountCount": 0,
            "4to6Countand1to2Countand2to3Countand2to5CountCount": 0,
            "4to6Countand1to3Countand2to3Countand2to5CountCount": 0,
            "5to6Countand6to1Countand1to2Countand1to3CountCount": 0,
            "5to6Countand6to1Countand1to2Countand2to3CountCount": 0,
            "5to6Countand6to1Countand1to2Countand2to5CountCount": 0,
            "5to6Countand6to1Countand1to3Countand2to3CountCount": 0,
            "5to6Countand6to1Countand1to3Countand2to5CountCount": 0,
            "5to6Countand6to1Countand2to3Countand2to5CountCount": 0,
            "5to6Countand1to2Countand1to3Countand2to3CountCount": 0,
            "5to6Countand1to2Countand1to3Countand2to5CountCount": 0,
            "5to6Countand1to2Countand2to3Countand2to5CountCount": 0,
            "5to6Countand1to3Countand2to3Countand2to5CountCount": 0,
            "6to1Countand1to2Countand1to3Countand2to3CountCount": 0,
            "6to1Countand1to2Countand1to3Countand2to5CountCount": 0,
            "6to1Countand1to2Countand2to3Countand2to5CountCount": 0,
            "6to1Countand1to3Countand2to3Countand2to5CountCount": 0,
            "1to2Countand1to3Countand2to3Countand2to5CountCount": 0}
        distanceskeys=[]
        for key in distances.keys():
            distanceskeys.append(key)
        # quads=list(it.combinations(distanceskeys,4))
        # for quad in quads:
        #     print('"'+quad[0]+'and'+quad[1]+'and'+quad[2]+'and'+quad[3]+'Count'+'"'+' :0,')
        # exit()
        # for a in np.arange(1,4):
        #     print(list(it.combinations(distances.values(),a)))
        # for x in distances.values():
        #     print(x)
        atoms_0= coords[:, tuple(x[0] for x in distances.values())]
        atoms_1 = coords[:, tuple(x[1] for x in distances.values())]
        diffs = atoms_1 - atoms_0
        bondLengths = np.linalg.norm(diffs, axis=2).T
        keycount=0
        # oranges=weights[bondLengths[1]>(3.0/0.529177)]
        oranges=np.argwhere(bondLengths > 3.0/0.529177)
        moleculenumbers=oranges[:,1]
        hi = np.array(np.unique(oranges[:, 1], return_counts=True, return_index=True))
        for a in np.arange(0,len(hi[1])):

            if hi[2,a]==1:
                #do 1 stuff
                results[distanceskeys[oranges[hi[1,a],0]]]+=weights[hi[0,a]]
            if hi[2,a]==2:
                positions=np.where(moleculenumbers==hi[0,a])[0]
                onenum=distanceskeys[oranges[positions[0],0]]
                twonum=distanceskeys[oranges[positions[1],0]]
                results[onenum+'and'+twonum+'Count']+=weights[hi[0,a]]
            if hi [2,a]==3:
                positions=np.where(moleculenumbers==hi[0,a])[0]
                onenum = distanceskeys[oranges[positions[0],0]]
                twonum = distanceskeys[oranges[positions[1],0]]
                threenum=distanceskeys[oranges[positions[2],0]]
                results[onenum + 'and' + twonum +'and'+threenum+ 'Count'] += weights[hi[0, a]]
            if hi[2, a] == 4:
                positions=np.where(moleculenumbers==hi[0,a])[0]
                onenum = distanceskeys[oranges[positions[0],0]]
                twonum = distanceskeys[oranges[positions[1],0]]
                threenum=distanceskeys[oranges[positions[2],0]]
                fournum=distanceskeys[oranges[positions[3],0]]
                results[onenum + 'and' + twonum + 'and' + threenum +'and'+fournum+ 'Count'] += weights[hi[0, a]]

        results={k:v/totalweight for k,v in results.items()}
        # returns the unique indices, also count
        resultsFile = open(f'Results/Test/' + f"{dataname}_full_results.txt",
                           'w')
        if allH == True:
            resultsFile.write('Results for homogeneous:' + "\n")
        elif mostlyD == True:
            resultsFile.write('Hydrogen Position is: ' + str(deuterium) + "\n")
        else:
            resultsFile.write('Deuterium Position is: ' + str(deuterium) + "\n")
        # for dictionario in allresults:
        # get keys as a list, loop over list,
        # make 2d array, use axis keyword to get everything at once
        #np.argwhere(bondLengths>3.0)
        #if x,
        for key in results.keys():
            resultsFile.write(key+'\n')
            resultsFile.write(str(results[key])+'\n')
            # resultsFile.write(str((np.sum(weights[bondLengths[keycount]>(3.0/0.529177)]))/totalweight)+'\n')
            keycount+=1
        resultsFile.close()


        # seconds=list(it.combinations(distanceskeys,2))
        # for second in seconds:
        #     print('"'+second[0]+'and'+second[1]+'Count'+'"'+' :0,')

        # triples = list(it.combinations(distanceskeys, 3))
        # for triple in triples:
        #     print('"' + triple[0] + 'and' + triple[1] + 'and' + triple[2] + 'Count' + '"' + ' :0,')

        # quads = list(it.combinations(distanceskeys, 4))
        # for quad in quads:
        #     print('"' + quad[0] + 'and' + quad[1] + 'and' + quad[2] + 'and' + quad[3] + 'Count' + '"' + ' :0,')
path = f'SortedData/'
dataname = 'h2o6_prism'
mostlyD = False
allH=True
deuterium=18
bigOne(path+dataname+'/',dataname,mostlyD,allH,deuterium)
path = f'SortedData/'
dataname = 'd2o6_prism'
mostlyD = False
allH=True
deuterium=18
bigOne(path,dataname,mostlyD,allH,deuterium)