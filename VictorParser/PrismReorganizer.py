import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *

def watertrader(walkercoords, currentwater, watertotrade, hydrogenpointer):
    walkercoords[[currentwater, watertotrade]] = walkercoords[[watertotrade, currentwater]]
    walkercoords[[currentwater + 1, watertotrade + hydrogenpointer]] = walkercoords[
        [watertotrade + hydrogenpointer, currentwater + 1]]
    if hydrogenpointer == 1:
        walkercoords[[currentwater + 2, watertotrade + 2]] = walkercoords[[watertotrade + 2, currentwater + 2]]
    elif hydrogenpointer == 2:
        walkercoords[[currentwater + 2, watertotrade + 1]] = walkercoords[[watertotrade + 1, currentwater + 2]]
    return walkercoords

def singleatomtrader(walkercoords):
    hydrogenzero = 0
    hydrogenone = 1
    hydrogentwo = 0
    hydrogenthree = 0
    hydrogenfour = 0
    hydrogenfive = 1
    walkercoords[:,[4, 5]] = walkercoords[:,[5, 4]]
    walkercoords[:,[16, 17]] = walkercoords[:,[17, 16]]
    return walkercoords

def checkdistance(walkercoords, particleOne, particleTwo):
    return np.sqrt(np.sum(np.square(walkercoords[particleOne] - walkercoords[particleTwo]))) * 0.529177

def bigOne(path,dataname,mostlyD,allH,simulation):
    coords, weights, metadata, size = concatenatenpz(path + 'FullDataset/')
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
    print('reorg')
#    writeMeAnXYZFile(coords[1],path+dataname+'.xyz',deuterium)


    waterlist = [waterzero, waterone, watertwo, waterthree, waterfour, waterfive]
    frencharray = np.zeros((length, 18, 3))
    valuecounter = 0
    for b in waterlist:
        for c in np.arange(0, 3):
            frencharray[:, valuecounter, :] = coords[:, b + c, :]
            valuecounter = valuecounter + 1
    frencharray = np.array(frencharray)
    coords = frencharray
    coords=singleatomtrader(coords)
    if deuterium==18:
        np.savez('SortedData/' + dataname, coords=coords, weights=weights, metadata=metadata)
    else:
        np.savez('SortedData/' + dataname+f'_{deuterium}', coords=coords, weights=weights, metadata=metadata,simulation=simulation)


for simulation in np.arange(1, 7):
    path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
    # path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
    # path = f'h2o6_prism/PythonData/'
    dataname = f'h2o5_d2o_prism'
    mostlyD = False
    allH=False
    bigOne(path,dataname,mostlyD,allH,simulation)
for simulation in np.arange(1, 6):
    #path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
    path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
    # path = f'h2o6_prism/PythonData/'
    dataname = f'h2o_d2o5_prism'
    mostlyD = True
    allH=False
    bigOne(path,dataname,mostlyD,allH,simulation)

path = f'h2o6_prism/PythonData/'
dataname = 'h2o6_prism'
mostlyD = False
allH=True
simulation=0
bigOne(path,dataname,mostlyD,allH,simulation)
path = f'd2o6_prism/PythonData/'
dataname = 'd2o6_prism'
mostlyD = False
allH=True
bigOne(path,dataname,mostlyD,allH,simulation)