import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *

for simulation in np.arange(1, 6):
    # path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
    path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
    dataname = 'uncategorized.npz'
    mostlyD = True
    coords, weights, metadata, size = concatenatenpz(path + 'FullDataset/')
    # data = np.load(path + dataname)
    # # make a large matrix
    # coords = data['coords']
    # origins = data['origin']


    # for i in np.arange(0,6):
    #     writeMeAnXYZFile(coords[0], path + f'simulation{simulation}_{i}.xyz', 15)
    # writeMeAnXYZFile(coords[0],path+'simulation3.xyz',15)
    # exit()
    def whichwaterpointer(walkercoords, currentHydrogen):
        water = np.arange(0, 6) * 3
        list = []
        for i in water:
            list.append(np.sqrt(np.sum(np.square(walkercoords[currentHydrogen] - walkercoords[i]))))
        sort = np.argsort(list)[1]
        nextwater = sort * 3
        return nextwater


    def doublewatertime(walkercoords, currentwater):
        water = np.arange(0, 6) * 3
        listh1 = []
        listh2 = []
        for i in water:
            listh1.append(np.sqrt(np.sum(np.square(walkercoords[currentwater + 1] - walkercoords[i]))))
            listh2.append(np.sqrt(np.sum(np.square(walkercoords[currentwater + 2] - walkercoords[i]))))
        sorth1 = np.argsort(listh1)[1]
        sorth2 = np.argsort(listh2)[1]
        return sorth1 * 3, sorth2 * 3


    def watertrader(walkercoords, currentwater, watertotrade, hydrogenpointer):
        walkercoords[[currentwater, watertotrade]] = walkercoords[[watertotrade, currentwater]]
        walkercoords[[currentwater + 1, watertotrade + hydrogenpointer]] = walkercoords[
            [watertotrade + hydrogenpointer, currentwater + 1]]
        if hydrogenpointer == 1:
            walkercoords[[currentwater + 2, watertotrade + 2]] = walkercoords[[watertotrade + 2, currentwater + 2]]
        elif hydrogenpointer == 2:
            walkercoords[[currentwater + 2, watertotrade + 1]] = walkercoords[[watertotrade + 1, currentwater + 2]]
        return walkercoords


    def checkdistance(walkercoords, particleOne, particleTwo):
        return np.sqrt(np.sum(np.square(walkercoords[particleOne] - walkercoords[particleTwo]))) * 0.529177


    if simulation == 6 or (simulation == 4 and mostlyD == True):
        waterzero = 12
        waterone = 3
        watertwo = 0
        waterthree = 15
        waterfour = 6
        waterfive = 9
        deuterium = 3
        length = coords.shape[0]
    elif simulation == 5 or (simulation == 3 and mostlyD == True):
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
    waterlist = [waterzero, waterone, watertwo, waterthree, waterfour, waterfive]
    frencharray = np.zeros((length, 18, 3))
    valuecounter = 0
    for b in waterlist:
        for c in np.arange(0, 3):
            frencharray[:, valuecounter, :] = coords[:, b + c, :]
            valuecounter = valuecounter + 1
    frencharray = np.array(frencharray)
    coords = frencharray
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
        'confusedCount': 0}
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
    resultsFile = open(path + "FullResults.txt", 'w')
    count = 0
    reference = []
    problemcount=0
    for a in np.arange(0, length):
        weight = weights[a]
        haserror = 0
        for b in np.arange(0, 6):
            b = b * 3
            if checkdistance(coords[a], b + 1, (b + 3) % 18) > checkdistance(coords[a], b + 2, (b + 3) % 18):
                coords[a][[b + 1, b + 2]] = coords[a][[b + 2, b + 1]]
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
        # writeMeAnXYZFile(coords[a],'path'+f'Prism{a}.xyz',0)
    # totalcount=sum(results.values())
    totalcount = count + results['confusedCount']
    # totalcount=oneToThreeCount+fourToSixCount+fiveToNineCount+sevenToNineCount+tenToTwelveCount+thirteenToFifteenCount+fourteenToZeroCount+sixteenToZeroCount+seventeenToSixCount+confusedCount
    print(totalcount)
    if mostlyD==True:
        resultsFile.write('Hydrogen Position is: ' + str(deuterium) + "\n")
    else:
        resultsFile.write('Deuterium Position is: ' + str(deuterium) + "\n")
    for name, value in results.items():
        resultsFile.write(name + "\n")
        resultsFile.write(str(value / totalcount) + "\n")
        resultsFile.write(str(value / problemcount) + "\n")
    resultsFile.close()

