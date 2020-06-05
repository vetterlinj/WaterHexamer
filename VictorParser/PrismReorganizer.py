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

def bigOne2(path,dataname,mostlyD,allH,simulation, resultspath):
    coordsdict, weightsdict= concatenateseparatesimulationnpz(path)
    dictionarycount=0
    filenumbers=[]
    for coordsnumber,coords in coordsdict.items():
        dictionarycount+=1
        filenumbers.append(coordsnumber)
        weights=weightsdict[f'{coordsnumber}']
        # writeMeAnXYZFile(coords[0],dataname+'.xyz',simulation)
        # continue
        # print(oranges)
        # exit()
        if allH==True:
            waterzero = 15
            waterone = 6
            watertwo = 3
            waterthree = 0
            waterfour = 9
            waterfive = 12
            deuterium = 18
            length = coords.shape[0]
        elif simulation == 1:
            waterzero = 12
            waterone = 6
            watertwo = 3
            waterthree = 0
            waterfour = 15
            waterfive = 9
            deuterium = 15
            length = coords.shape[0]
        elif simulation == 2:
            waterzero = 12
            waterone = 6
            watertwo = 3
            waterthree = 0
            waterfour = 9
            waterfive = 15
            deuterium = 15
            length = coords.shape[0]
        elif simulation == 3:
            waterzero = 15
            waterone = 6
            watertwo = 3
            waterthree = 0
            waterfour = 9
            waterfive = 12
            deuterium = 15
            length = coords.shape[0]
        elif simulation == 4:
            waterzero = 12
            waterone = 15
            watertwo = 3
            waterthree = 0
            waterfour = 6
            waterfive = 9
            deuterium = 15
            length = coords.shape[0]
        elif simulation == 5:
            waterzero = 12
            waterone = 3
            watertwo = 15
            waterthree = 0
            waterfour = 6
            waterfive = 9
            deuterium = 15
            length = coords.shape[0]
        elif simulation == 6:
            waterzero = 12
            waterone = 3
            watertwo = 0
            waterthree = 15
            waterfour = 6
            waterfive = 9
            deuterium = 15
            length = coords.shape[0]
        # elif simulation == 6 or (simulation == 4 and mostlyD == True):
        #     waterzero = 12
        #     waterone = 3
        #     watertwo = 0
        #     waterthree = 15
        #     waterfour = 6
        #     waterfive = 9
        #     deuterium = 3
        #     length = coords.shape[0]
        # elif (simulation == 5 and mostlyD==False) or (simulation == 3 and mostlyD == True):
        #     waterzero = 12
        #     waterone = 3
        #     watertwo = 15
        #     waterthree = 0
        #     waterfour = 6
        #     waterfive = 9
        #     deuterium = 2
        #     length = coords.shape[0]
        # elif simulation == 4 or (simulation == 2 and mostlyD == True):
        #     waterzero = 12
        #     waterone = 15
        #     watertwo = 3
        #     waterthree = 0
        #     waterfour = 6
        #     waterfive = 9
        #     deuterium = 1
        #     length = coords.shape[0]
        # elif simulation == 3 or (simulation == 5 and mostlyD == True):
        #     waterzero = 15
        #     waterone = 6
        #     watertwo = 3
        #     waterthree = 0
        #     waterfour = 9
        #     waterfive = 12
        #     deuterium = 0
        #     length = coords.shape[0]
        # elif simulation == 2:
        #     waterzero = 12
        #     waterone = 6
        #     watertwo = 3
        #     waterthree = 0
        #     waterfour = 9
        #     waterfive = 15
        #     deuterium = 5
        #     length = coords.shape[0]
        # elif simulation == 1:
        #     waterzero = 12
        #     waterone = 6
        #     watertwo = 3
        #     waterthree = 0
        #     waterfour = 15
        #     waterfive = 9
        #     deuterium = 4
        #     length = coords.shape[0]
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
        np.savez(f'{resultspath}' + dataname+f'_{coordsnumber}', coords=coords, weights=weights)


for simulation in np.arange(1, 7):
    path=f'UpdatedPrism/Parsed/h2o5_d2o/D{simulation}/'
    resultspath = f'UpdatedPrism/Reorganized/h2o5_d2o/D{simulation}/'
    # path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
    # path = f'h2o6_prism/PythonData/'
    dataname = f'D{simulation}'
    mostlyD = False
    allH=False
    bigOne2(path,dataname,mostlyD,allH,simulation,resultspath)
for simulation in np.arange(1, 7):
    #path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
    resultspath = f'UpdatedPrism/Reorganized/h2o_d2o5/H{simulation}/'
    path = f'UpdatedPrism/Parsed/h2o_d2o5/H{simulation}/'
    # path = f'h2o6_prism/PythonData/'
    dataname = f'H{simulation}'
    mostlyD = True
    allH=False
    bigOne2(path,dataname,mostlyD,allH,simulation,resultspath)

