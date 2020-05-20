import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *


def bigOne(path,dataname,mostlyD,allH):
    # coords, weights, metadata, size = concatenatenpz(path + 'FullDataset/')
    data=np.load(path+dataname+'.npz')
    coords=data['coords']
    weights=data['weights']
    # simulation=data['simulation']

    # data = np.load(path + dataname)
    # # make a large matrix
    # coords = data['coords']
    # origins = data['origin']
    counter=0

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

    if allH==True:
        waterzero = 15
        waterone = 6
        watertwo = 3
        waterthree = 0
        waterfour = 9
        waterfive = 12
        deuterium = 18
        length = coords.shape[0]
    elif simulation == 6 or (simulation == 4 and mostlyD == True):
        waterzero = 12
        waterone = 3
        watertwo = 0
        waterthree = 15
        waterfour = 6
        waterfive = 9
        deuterium = 3
        length = coords.shape[0]
    elif (simulation == 5 and mostlyD==False) or (simulation == 3 and mostlyD == True):
        waterzero = 12
        waterone = 3
        watertwo = 15
        waterthree = 0
        waterfour = 6
        waterfive = 9
        deuterium = 2
        length = coords.shape[0]
    elif simulation == 4 or (simulation == 2 and mostlyD == True):
        waterzero = 12
        waterone = 15
        watertwo = 3
        waterthree = 0
        waterfour = 6
        waterfive = 9
        deuterium = 1
        length = coords.shape[0]
    elif simulation == 3 or (simulation == 5 and mostlyD == True):
        waterzero = 15
        waterone = 6
        watertwo = 3
        waterthree = 0
        waterfour = 9
        waterfive = 12
        deuterium = 0
        length = coords.shape[0]
    elif simulation == 2:
        waterzero = 12
        waterone = 6
        watertwo = 3
        waterthree = 0
        waterfour = 9
        waterfive = 15
        deuterium = 5
        length = coords.shape[0]
    elif simulation == 1:
        waterzero = 12
        waterone = 6
        watertwo = 3
        waterthree = 0
        waterfour = 15
        waterfive = 9
        deuterium = 4
        length = coords.shape[0]
    print('complete')
    #numpy indexing
    results = {
        'oneToThreeCount': 0,
        'fourToSixCount': 0,
        'fiveToNineCount': 0,
        'sevenToNineCount': 0,
        'tenToTwelveCount': 0,
        'thirteenToFifteenCount': 0,
        'fourteenToZeroCount': 0,
        'sixteenToZeroCount': 0,
        'seventeenToSixCount': 0,
        'confusedCount': 0,
        'doubleCount':0,
        'tripleCount':0,
        'quadplusCount':0,
        'cAndGCorrelation':0,
        'cAndBCorrelation':0,
        'cAndHCorrelation':0,
        'bAndGCorrelation':0,
        'bAndHCorrelation':0,
        'gAndHCorrelation':0,
        'sillyCheck':0}

    resultsFile = open('Results/' + f"{dataname}_results.txt", 'w')
    count = 0
    reference = []
    problemcount=0

    for a in np.arange(0, length):
        weight = weights[a]
        haserror = 0
        problemresults = {
            'oneToThreeCount': 0,
            'fourToSixCount': 0,
            'fiveToNineCount': 0,
            'sevenToNineCount': 0,
            'tenToTwelveCount': 0,
            'thirteenToFifteenCount': 0,
            'fourteenToZeroCount': 0,
            'sixteenToZeroCount': 0,
            'seventeenToSixCount': 0,
            'confusedCount': 0}
        if whichwaterpointer(coords[a], 1) != 3:
            results['oneToThreeCount'] += weight
            problemresults['oneToThreeCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 1, 3) > 3:
            results['oneToThreeCount'] += weight
            problemresults['oneToThreeCount'] += weight
            haserror += 1
        if whichwaterpointer(coords[a], 4) != 6:
            results['fourToSixCount'] += weight
            problemresults['fourToSixCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 4, 6) > 3:
            results['fourToSixCount'] += weight
            problemresults['fourToSixCount'] += weight
            haserror += 1
        if whichwaterpointer(coords[a], 5) != 9:
            results['fiveToNineCount'] += weight
            problemresults['fiveToNineCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 5, 9) > 3:
            results['fiveToNineCount'] += weight
            problemresults['fiveToNineCount'] += weight
            haserror += 1
        if whichwaterpointer(coords[a], 7) != 9:
            results['sevenToNineCount'] += weight
            problemresults['sevenToNineCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 7, 9) > 3:
            results['sevenToNineCount'] += weight
            problemresults['sevenToNineCount'] += weight
            haserror += 1
        if whichwaterpointer(coords[a], 10) != 12:
            results['tenToTwelveCount'] += weight
            problemresults['tenToTwelveCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 10, 12) > 3:
            results['tenToTwelveCount'] += weight
            problemresults['tenToTwelveCount'] += weight
            haserror += 1
        if whichwaterpointer(coords[a], 13) != 15:
            results['thirteenToFifteenCount'] += weight
            problemresults['thirteenToFifteenCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 13, 15) > 3:
            results['thirteenToFifteenCount'] += weight
            problemresults['thirteenToFifteenCount'] += weight
            haserror += 1
        if whichwaterpointer(coords[a], 14) != 0:
            results['fourteenToZeroCount'] += weight
            problemresults['fourteenToZeroCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 14, 0) > 3:
            results['fourteenToZeroCount'] += weight
            problemresults['fourteenToZeroCount'] += weight
            haserror += 1
        if whichwaterpointer(coords[a], 16) != 0:
            results['sixteenToZeroCount'] += weight
            problemresults['sixteenToZeroCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 16, 0) > 3:
            results['sixteenToZeroCount'] += weight
            problemresults['sixteenToZeroCount'] += weight
            haserror += 1
        if whichwaterpointer(coords[a], 17) != 6:
            results['seventeenToSixCount'] += weight
            problemresults['seventeenToSixCount'] += weight
            haserror += 1
        elif checkdistance(coords[a], 17, 6) > 3:
            results['seventeenToSixCount'] += weight
            problemresults['seventeenToSixCount'] += weight
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
        if haserror > 3:
            results['quadplusCount']+= weight
        if problemresults['fiveToNineCount']>0 and problemresults['fourToSixCount']>0:
            results['cAndBCorrelation']+=weight
            counter+=1
            # writeMeAnXYZFile(coords[a], path + f'{simulation}now{a}.xyz', 15)
            # if counter==5:
            #     exit()
        if problemresults['fiveToNineCount']>0 and problemresults['fourteenToZeroCount']>0:
            results['cAndGCorrelation']+=weight
        if problemresults['fiveToNineCount']>0 and problemresults['seventeenToSixCount']>0:
            results['cAndHCorrelation']+=weight
        if problemresults['fourToSixCount']>0 and problemresults['fourteenToZeroCount']>0:
            results['bAndGCorrelation']+=weight
        if problemresults['fourToSixCount']>0 and problemresults['sixteenToZeroCount']>0:
            results['bAndHCorrelation']+=weight
        if problemresults['fourteenToZeroCount']>0 and problemresults['sixteenToZeroCount']>0:
            results['gAndHCorrelation']+=weight
        if problemresults['seventeenToSixCount']>0 and problemresults['sixteenToZeroCount']>0:
            results['sillyCheck']+=weight
        # writeMeAnXYZFile(coords[a],'path'+f'Prism{a}.xyz',0)
    # totalcount=sum(results.values())
    totalcount = count + results['confusedCount']
    # totalcount=oneToThreeCount+fourToSixCount+fiveToNineCount+sevenToNineCount+tenToTwelveCount+thirteenToFifteenCount+fourteenToZeroCount+sixteenToZeroCount+seventeenToSixCount+confusedCount
    print(totalcount)
    if allH==True:
        resultsFile.write('Results for homogeneous:' + "\n")
    elif mostlyD==True:
        resultsFile.write('Hydrogen Position is: ' + str(deuterium) + "\n")
    else:
        resultsFile.write('Deuterium Position is: ' + str(deuterium) + "\n")
    for name, value in results.items():
        resultsFile.write(name + "\n")
        resultsFile.write(str(value / totalcount) + "\n")
        resultsFile.write(str(value / problemcount) + "\n")
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
bigOne(path,dataname,mostlyD,allH)
path = f'SortedData/'
dataname = 'd2o6_prism'
mostlyD = False
allH=True
bigOne(path,dataname,mostlyD,allH)

#simulation