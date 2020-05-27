import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *


def bigOne(path,dataname,mostlyD,allH,deuterium):

    # simulation=data['simulation']
    # data = np.load(path + dataname)
    # # make a large matrix
    # coords = data['coords']
    # origins = data['origin']

    # for i in np.arange(0,6):
    #     writeMeAnXYZFile(coords[0], path + f'simulation{simulation}_{i}.xyz', 15)
    # writeMeAnXYZFile(coords[0],path+f'{simulation}MostlyD.xyz',15)
    # exit()
    def whichwaterpointer(walkercoords, currentHydrogen):
        water = np.arange(0, 6) * 3
        list = []
        for i in water:
            list.append(np.sqrt(np.sum(np.square(walkercoords[currentHydrogen] - walkercoords[i]))))
        sort = np.argsort(list)[1]
        nextwater = sort * 3
        return nextwater

    def checkdistance(walkercoords, particleOne, particleTwo):
        return np.sqrt(np.sum(np.square(walkercoords[particleOne] - walkercoords[particleTwo]))) * 0.529177

    coordsdict, weightsdict= concatenateseparatenpz(path)
    dictionarycount=0
    filenumbers=[]
    allresults=[]
    for coordsnumber,coords in coordsdict.items():
        dictionarycount+=1
        filenumbers.append(coordsnumber)
        weights=weightsdict[f'{coordsnumber}']
        length = coords.shape[0]
        #numpy indexing
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
            'confusedCount': 0,
            'doubleCount':0,
            'tripleCount':0,
            'quadplusCount':0,
            '4to6and1to3Count':0,
            '4to5and4to6Count':0,
            '4to6and2to5Count':0,
            '4to5and1to3Count':0,
            '4to5and2to3Count':0,
            '1to3and2to3Count':0,
            '2to5and2to3Count':0,
            '4to5and2to5Count':0,
            '4to6and2to3Count':0}
        # 4to5 and 2to3,4to5 and 2to5, 4to6 and 2to3, 4to6 and 2to3
        resultsFile = open(f'/Users/nicholasvetterli/PycharmProjects/WaterHexamer/VictorParser/Results/PrismBreaks/{dataname}/individual/' + f"{dataname}_results{dictionarycount}.txt", 'w')
        count = 0
        reference = []
        problemcount=0
        print('why')
        for a in np.arange(0, length):
            weight = weights[a]
            haserror = 0
            problemresults = {
                '3to4Count': 0,
                '4to5Count': 0,
                '4to6Count': 0,
                '5to6Count': 0,
                '6to1Count': 0,
                '1to2Count': 0,
                '1to3Count': 0,
                '2to3Count': 0,
                '2to5Count': 0,
                'confusedCount': 0}
            if whichwaterpointer(coords[a], 1) != 3:
                results['3to4Count'] += weight
                problemresults['3to4Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 1, 3) > 3:
                results['3to4Count'] += weight
                problemresults['3to4Count'] += weight
                haserror += 1
            if whichwaterpointer(coords[a], 4) != 6:
                results['4to5Count'] += weight
                problemresults['4to5Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 4, 6) > 3:
                results['4to5Count'] += weight
                problemresults['4to5Count'] += weight
                haserror += 1
            if whichwaterpointer(coords[a], 5) != 9:
                results['4to6Count'] += weight
                problemresults['4to6Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 5, 9) > 3:
                results['4to6Count'] += weight
                problemresults['4to6Count'] += weight
                haserror += 1
            if whichwaterpointer(coords[a], 7) != 9:
                results['5to6Count'] += weight
                problemresults['5to6Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 7, 9) > 3:
                results['5to6Count'] += weight
                problemresults['5to6Count'] += weight
                haserror += 1
            if whichwaterpointer(coords[a], 10) != 12:
                results['6to1Count'] += weight
                problemresults['6to1Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 10, 12) > 3:
                results['6to1Count'] += weight
                problemresults['6to1Count'] += weight
                haserror += 1
            if whichwaterpointer(coords[a], 13) != 15:
                results['1to2Count'] += weight
                problemresults['1to2Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 13, 15) > 3:
                results['1to2Count'] += weight
                problemresults['1to2Count'] += weight
                haserror += 1
            if whichwaterpointer(coords[a], 14) != 0:
                results['1to3Count'] += weight
                problemresults['1to3Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 14, 0) > 3:
                results['1to3Count'] += weight
                problemresults['1to3Count'] += weight
                haserror += 1
            if whichwaterpointer(coords[a], 16) != 0:
                results['2to3Count'] += weight
                problemresults['2to3Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 16, 0) > 3:
                results['2to3Count'] += weight
                problemresults['2to3Count'] += weight
                haserror += 1
            if whichwaterpointer(coords[a], 17) != 6:
                results['2to5Count'] += weight
                problemresults['2to5Count'] += weight
                haserror += 1
            elif checkdistance(coords[a], 17, 6) > 3:
                results['2to5Count'] += weight
                problemresults['2to5Count'] += weight
                haserror += 1
            if haserror == 0:
                results['confusedCount'] += weight
            else:
                count += weight
                problemcount +=weight
            if haserror == 2:
                results['doubleCount']+= weight
            if haserror == 3:
                results['tripleCount']+= weight
                print('triple problem')
                print(problemresults)
            if haserror > 3:
                results['quadplusCount']+= weight
            if problemresults['4to6Count']>0 and problemresults['4to5Count']>0and haserror==2:
                results['4to5and4to6Count']+=weight
                results['4to6Count']-=weight
                results['4to5Count'] -= weight
                haserror-=1
                # writeMeAnXYZFile(coords[a], path + f'{simulation}now{a}.xyz', 15)
                # if counter==5:
                #     exit()
            if problemresults['4to6Count']>0 and problemresults['1to3Count']>0 and haserror==2:
                results['4to6and1to3Count']+=weight
                results['4to6Count'] -= weight
                results['1to3Count'] -= weight
                haserror-=1
            if problemresults['4to6Count']>0 and problemresults['2to5Count']>0 and haserror==2:
                results['4to6and2to5Count']+=weight
                results['4to6Count'] -= weight
                results['2to5Count'] -= weight
                haserror-=1
            if problemresults['4to5Count']>0 and problemresults['1to3Count']>0 and haserror==2:
                results['4to5and1to3Count']+=weight
                results['4to5Count'] -= weight
                results['1to3Count'] -= weight
                haserror-=1
            if problemresults['4to5Count']>0 and problemresults['2to3Count']>0 and haserror==2:
                results['4to5and2to3Count']+=weight
                results['4to5Count'] -= weight
                results['2to3Count'] -= weight
                haserror-=1
            if problemresults['1to3Count']>0 and problemresults['2to3Count']>0 and haserror==2:
                results['1to3and2to3Count']+=weight
                results['2to3Count'] -= weight
                results['1to3Count'] -= weight
                haserror-=1
            if problemresults['2to5Count']>0 and problemresults['2to3Count']>0 and haserror==2:
                results['2to5and2to3Count']+=weight
                results['2to5Count'] -= weight
                results['2to3Count'] -= weight
                haserror-=1
            if problemresults['4to5Count']>0 and problemresults['2to5Count']>0 and haserror==2:
                results['4to5and2to5Count']+=weight
                results['2to5Count'] -= weight
                results['4to5Count'] -= weight
                haserror-=1
            if problemresults['4to6Count']>0 and problemresults['2to3Count']>0 and haserror==2:
                results['4to6and2to3Count']+=weight
                results['2to3Count'] -= weight
                results['4to6Count'] -= weight
                haserror-=1
            if haserror==2:
                print('still a double problem')
                print(problemresults)
            # writeMeAnXYZFile(coords[a],'path'+f'Prism{a}.xyz',0)
        # totalcount=sum(results.values())
        totalcount = count + results['confusedCount']
        # totalcount=oneToThreeCount+4to5Count+4to6Count+5to6Count+6to1Count+1to2Count+1to3Count+2to3Count+2to5Count+confusedCount
        print(totalcount)
        if allH==True:
            resultsFile.write('Results for homogeneous:' + "\n")
        elif mostlyD==True:
            resultsFile.write('Hydrogen Position is: ' + str(deuterium) + "\n")
        else:
            resultsFile.write('Deuterium Position is: ' + str(deuterium) + "\n")
        temporaryresults=[]
        for name, value in results.items():
            resultsFile.write(name + "\n")
            resultsFile.write(str(value / totalcount) + "\n")
            resultsFile.write(str(value / problemcount) + "\n")
            temporaryresults.append(value/totalcount)
        resultsFile.close()
        allresults.append(temporaryresults)
        print()
        #makefile
    resultsFile = open(f'Results/PrismBreaks/{dataname}/' + f"{dataname}_full_results.txt",
                           'w')
    if allH==True:
        resultsFile.write('Results for homogeneous:' + "\n")
    elif mostlyD==True:
        resultsFile.write('Hydrogen Position is: ' + str(deuterium) + "\n")
    else:
        resultsFile.write('Deuterium Position is: ' + str(deuterium) + "\n")
    # for dictionario in allresults:
        #get keys as a list, loop over list,
    #make 2d array, use axis keyword to get everything at once
    resultsFile.write('Format is value then stdev.' + "\n")
    n=0
    allresults=np.array(allresults)
    for name, value in results.items():
        resultsFile.write(name + "\n")
        resultsFile.write(str(np.average(allresults[:,n])) + "\n")
        resultsFile.write(str(np.std(allresults[:,n])) + "\n")
        n+=1
    resultsFile.close()

# for simulation in np.arange(1, 7):
#     path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
#     # path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
#     # path = f'h2o6_prism/PythonData/'
#     dataname = f'h2o5_d2o_prism_{simulation}'
#     mostlyD = False
#     allH=False
#     bigOne(path,dataname,mostlyD,allH,simulation)
# for simulation in np.arange(1, 6):
#     #path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
#     path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
#     # path = f'h2o6_prism/PythonData/'
#     dataname = f'h2o_d2o5_prism_{simulation}'
#     mostlyD = True
#     allH=False
#     bigOne(path,dataname,mostlyD,allH,simulation)




# for number in np.arange(0,6):
#     path=f'SortedData/'
#     dataname=f'h2o5_d2o_prism_{number}'
#     mostlyD = False
#     allH=False
#     bigOne(path,dataname,mostlyD,allH)
# for number in np.arange(0,5):
#     path=f'SortedData/'
#     dataname=f'h2o_d2o5_prism_{number}'
#     mostlyD = True
#     allH=False
#     bigOne(path,dataname,mostlyD,allH)
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
#4to5 and 2to3,4to5 and 2to5, 4to6 and 2to3, 4to6 and 2to3
#simulation

# def bigOne(path,dataname,mostlyD,allH):
#     # coords, weights, metadata, size = concatenatenpz(path + 'FullDataset/')
#     data=np.load(path+dataname+'.npz')
#     coords=data['coords']
#     weights=data['weights']
#     # simulation=data['simulation']
#
#     # data = np.load(path + dataname)
#     # # make a large matrix
#     # coords = data['coords']
#     # origins = data['origin']
#     counter=0
#
#     # for i in np.arange(0,6):
#     #     writeMeAnXYZFile(coords[0], path + f'simulation{simulation}_{i}.xyz', 15)
#     # writeMeAnXYZFile(coords[0],path+f'{simulation}MostlyD.xyz',15)
#     # exit()
#     def whichwaterpointer(walkercoords, currentHydrogen):
#         water = np.arange(0, 6) * 3
#         list = []
#         for i in water:
#             list.append(np.sqrt(np.sum(np.square(walkercoords[currentHydrogen] - walkercoords[i]))))
#         sort = np.argsort(list)[1]
#         nextwater = sort * 3
#         return nextwater
#
#     def checkdistance(walkercoords, particleOne, particleTwo):
#         return np.sqrt(np.sum(np.square(walkercoords[particleOne] - walkercoords[particleTwo]))) * 0.529177
#
#     if allH==True:
#         waterzero = 15
#         waterone = 6
#         watertwo = 3
#         waterthree = 0
#         waterfour = 9
#         waterfive = 12
#         deuterium = 18
#         length = coords.shape[0]
#     elif simulation == 6 or (simulation == 4 and mostlyD == True):
#         waterzero = 12
#         waterone = 3
#         watertwo = 0
#         waterthree = 15
#         waterfour = 6
#         waterfive = 9
#         deuterium = 3
#         length = coords.shape[0]
#     elif (simulation == 5 and mostlyD==False) or (simulation == 3 and mostlyD == True):
#         waterzero = 12
#         waterone = 3
#         watertwo = 15
#         waterthree = 0
#         waterfour = 6
#         waterfive = 9
#         deuterium = 2
#         length = coords.shape[0]
#     elif simulation == 4 or (simulation == 2 and mostlyD == True):
#         waterzero = 12
#         waterone = 15
#         watertwo = 3
#         waterthree = 0
#         waterfour = 6
#         waterfive = 9
#         deuterium = 1
#         length = coords.shape[0]
#     elif simulation == 3 or (simulation == 5 and mostlyD == True):
#         waterzero = 15
#         waterone = 6
#         watertwo = 3
#         waterthree = 0
#         waterfour = 9
#         waterfive = 12
#         deuterium = 0
#         length = coords.shape[0]
#     elif simulation == 2:
#         waterzero = 12
#         waterone = 6
#         watertwo = 3
#         waterthree = 0
#         waterfour = 9
#         waterfive = 15
#         deuterium = 5
#         length = coords.shape[0]
#     elif simulation == 1:
#         waterzero = 12
#         waterone = 6
#         watertwo = 3
#         waterthree = 0
#         waterfour = 15
#         waterfive = 9
#         deuterium = 4
#         length = coords.shape[0]
#     print('complete')
#     #numpy indexing
#     results = {
#         'oneToThreeCount': 0,
#         '4to5Count': 0,
#         '4to6Count': 0,
#         '5to6Count': 0,
#         '6to1Count': 0,
#         '1to2Count': 0,
#         '1to3Count': 0,
#         '2to3Count': 0,
#         '2to5Count': 0,
#         'confusedCount': 0,
#         'doubleCount':0,
#         'tripleCount':0,
#         'quadplusCount':0,
#         '4to6and1to3Count':0,
#         '4to5and4to6Count':0,
#         '4to6and2to5Count':0,
#         '4to5and1to3Count':0,
#         '4to5and2to3Count':0,
#         '1to3and2to3Count':0,
#         '2to5and2to3Count':0}
#
#     resultsFile = open('Results/' + f"{dataname}_results.txt", 'w')
#     count = 0
#     reference = []
#     problemcount=0
#
#     for a in np.arange(0, length):
#         weight = weights[a]
#         haserror = 0
#         problemresults = {
#             'oneToThreeCount': 0,
#             '4to5Count': 0,
#             '4to6Count': 0,
#             '5to6Count': 0,
#             '6to1Count': 0,
#             '1to2Count': 0,
#             '1to3Count': 0,
#             '2to3Count': 0,
#             '2to5Count': 0,
#             'confusedCount': 0}
#         if whichwaterpointer(coords[a], 1) != 3:
#             results['oneToThreeCount'] += weight
#             problemresults['oneToThreeCount'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 1, 3) > 3:
#             results['oneToThreeCount'] += weight
#             problemresults['oneToThreeCount'] += weight
#             haserror += 1
#         if whichwaterpointer(coords[a], 4) != 6:
#             results['4to5Count'] += weight
#             problemresults['4to5Count'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 4, 6) > 3:
#             results['4to5Count'] += weight
#             problemresults['4to5Count'] += weight
#             haserror += 1
#         if whichwaterpointer(coords[a], 5) != 9:
#             results['4to6Count'] += weight
#             problemresults['4to6Count'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 5, 9) > 3:
#             results['4to6Count'] += weight
#             problemresults['4to6Count'] += weight
#             haserror += 1
#         if whichwaterpointer(coords[a], 7) != 9:
#             results['5to6Count'] += weight
#             problemresults['5to6Count'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 7, 9) > 3:
#             results['5to6Count'] += weight
#             problemresults['5to6Count'] += weight
#             haserror += 1
#         if whichwaterpointer(coords[a], 10) != 12:
#             results['6to1Count'] += weight
#             problemresults['6to1Count'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 10, 12) > 3:
#             results['6to1Count'] += weight
#             problemresults['6to1Count'] += weight
#             haserror += 1
#         if whichwaterpointer(coords[a], 13) != 15:
#             results['1to2Count'] += weight
#             problemresults['1to2Count'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 13, 15) > 3:
#             results['1to2Count'] += weight
#             problemresults['1to2Count'] += weight
#             haserror += 1
#         if whichwaterpointer(coords[a], 14) != 0:
#             results['1to3Count'] += weight
#             problemresults['1to3Count'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 14, 0) > 3:
#             results['1to3Count'] += weight
#             problemresults['1to3Count'] += weight
#             haserror += 1
#         if whichwaterpointer(coords[a], 16) != 0:
#             results['2to3Count'] += weight
#             problemresults['2to3Count'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 16, 0) > 3:
#             results['2to3Count'] += weight
#             problemresults['2to3Count'] += weight
#             haserror += 1
#         if whichwaterpointer(coords[a], 17) != 6:
#             results['2to5Count'] += weight
#             problemresults['2to5Count'] += weight
#             haserror += 1
#         elif checkdistance(coords[a], 17, 6) > 3:
#             results['2to5Count'] += weight
#             problemresults['2to5Count'] += weight
#             haserror += 1
#         if haserror == 0:
#             results['confusedCount'] += weight
#         else:
#             count += weight
#             problemcount +=weight
#         if haserror == 2:
#             results['doubleCount']+= weight
#         if haserror == 3:
#             results['tripleCount']+= weight
#         if haserror > 3:
#             results['quadplusCount']+= weight
#         if problemresults['4to6Count']>0 and problemresults['4to5Count']>0:
#             results['4to5and4to6Count']+=weight
#             counter+=1
#             # writeMeAnXYZFile(coords[a], path + f'{simulation}now{a}.xyz', 15)
#             # if counter==5:
#             #     exit()
#         if problemresults['4to6Count']>0 and problemresults['1to3Count']>0:
#             results['4to6and1to3Count']+=weight
#         if problemresults['4to6Count']>0 and problemresults['2to5Count']>0:
#             results['4to6and2to5Count']+=weight
#         if problemresults['4to5Count']>0 and problemresults['1to3Count']>0:
#             results['4to5and1to3Count']+=weight
#         if problemresults['4to5Count']>0 and problemresults['2to3Count']>0:
#             results['4to5and2to3Count']+=weight
#         if problemresults['1to3Count']>0 and problemresults['2to3Count']>0:
#             results['1to3and2to3Count']+=weight
#         if problemresults['2to5Count']>0 and problemresults['2to3Count']>0:
#             results['2to5and2to3Count']+=weight
#         # writeMeAnXYZFile(coords[a],'path'+f'Prism{a}.xyz',0)
#     # totalcount=sum(results.values())
#     totalcount = count + results['confusedCount']
#     # totalcount=+4to5Count+4to6Count+5to6Count+6to1Count+1to2Count+1to3Count+2to3Count+2to5Count+confusedCount
#     print(totalcount)
#     if allH==True:
#         resultsFile.write('Results for homogeneous:' + "\n")
#     elif mostlyD==True:
#         resultsFile.write('Hydrogen Position is: ' + str(deuterium) + "\n")
#     else:
#         resultsFile.write('Deuterium Position is: ' + str(deuterium) + "\n")
#     for name, value in results.items():
#         resultsFile.write(name + "\n")
#         resultsFile.write(str(value / totalcount) + "\n")
#         resultsFile.write(str(value / problemcount) + "\n")
#     resultsFile.close()