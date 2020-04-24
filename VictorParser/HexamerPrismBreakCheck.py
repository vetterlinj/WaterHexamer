import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *
path='h2o5_d2o_prismPythonData/Uncategorized/minimum6_wfns/PythonData/'
dataname='uncategorized.npz'
data = np.load(path+dataname)
# make a large matrix
coords =data['coords']
def whichwaterpointer(walkercoords,currentHydrogen):
    water = np.arange(0, 6) * 3
    list=[]
    for i in water:
        list.append(np.sqrt(np.sum(np.square(walkercoords[currentHydrogen]-walkercoords[i]))))
    sort=np.argsort(list)[1]
    nextwater=sort*3
    return nextwater
def doublewatertime(walkercoords, currentwater):
    water = np.arange(0, 6) * 3
    listh1=[]
    listh2=[]
    for i in water:
        listh1.append(np.sqrt(np.sum(np.square(walkercoords[currentwater+1]-walkercoords[i]))))
        listh2.append(np.sqrt(np.sum(np.square(walkercoords[currentwater + 2] - walkercoords[i]))))
    sorth1=np.argsort(listh1)[1]
    sorth2=np.argsort(listh2)[1]
    return sorth1*3,sorth2*3
def watertrader(walkercoords, currentwater, watertotrade, hydrogenpointer):
    walkercoords[[currentwater, watertotrade]] = walkercoords[[watertotrade, currentwater]]
    walkercoords[[currentwater+1, watertotrade+hydrogenpointer]] = walkercoords[[watertotrade+hydrogenpointer, currentwater+1]]
    if hydrogenpointer ==1:
        walkercoords[[currentwater+2, watertotrade+2]] = walkercoords[[watertotrade+2, currentwater+2]]
    elif hydrogenpointer ==2:
        walkercoords[[currentwater+2, watertotrade+1]] = walkercoords[[watertotrade+1, currentwater+2]]
    return walkercoords
def checkdistance(walkercoords,particleOne,particleTwo):
    return np.sqrt(np.sum(np.square(walkercoords[particleOne]-walkercoords[particleTwo])))*0.529177
waterzero=15
waterone=6
watertwo=3
waterthree=0
waterfour=9
waterfive=12
#deuterium is 15>0
waterlist=[waterzero,waterone,watertwo,waterthree,waterfour,waterfive]
frencharray=np.zeros((56242,18,3))
valuecounter=0
for b in waterlist:
    for c in np.arange(0,3):
        frencharray[:,valuecounter,:]=coords[:,b+c,:]
        valuecounter=valuecounter+1
frencharray=np.array(frencharray)
coords=frencharray

results={
'oneToThreeCount':0,
'fourToSixCount':0,
'fiveToNineCount':0,
'sevenToNineCount':0,
'tenToTwelveCount':0,
'thirteenToFifteenCount':0,
'fourteenToZeroCount':0,
'sixteenToZeroCount':0,
'seventeenToSixCount':0,
'confusedCount':0}
resultsFile=open(path+"Results.txt",'w')
for a in np.arange(0,56242):
    weight=1
    for b in np.arange(0,6):
        b=b*3
        if checkdistance(coords[a], b + 1, (b+3)%18) > checkdistance(coords[a], b + 2, (b+3)%18):
                coords[a][[b + 1, b + 2]] = coords[a][[b + 2, b + 1]]
    if whichwaterpointer(coords[a],1)!=3:
        results['oneToThreeCount']+=weight
        continue
    elif checkdistance(coords[a],1,3)>3:
        results['oneToThreeCount'] += weight
        continue
    if whichwaterpointer(coords[a],4)!=6:
        results['fourToSixCount']+=weight
        continue
    elif checkdistance(coords[a],4,6)>3:
        results['fourToSixCount'] += weight
        continue
    if whichwaterpointer(coords[a],5)!=9:
        results['fiveToNineCount']+=weight
        continue
    elif checkdistance(coords[a],5,9)>3:
        results['fiveToNineCount'] += weight
        continue
    if whichwaterpointer(coords[a],7)!=9:
        results['sevenToNineCount']+=weight
        continue
    elif checkdistance(coords[a],7,9)>3:
        results['sevenToNineCount'] += weight
        continue
    if whichwaterpointer(coords[a], 10) != 12:
        results['tenToTwelveCount']+=weight
        continue
    elif checkdistance(coords[a],10,12)>3:
        results['tenToTwelveCount'] += weight
        continue
    if whichwaterpointer(coords[a], 13) != 15:
        results['thirteenToFifteenCount']+=weight
        continue
    elif checkdistance(coords[a],13,15)>3:
        results['thirteenToFifteenCount'] += weight
        continue
    if whichwaterpointer(coords[a], 14) != 0:
        results['fourteenToZeroCount']+=weight
        continue
    elif checkdistance(coords[a],14,0)>3:
        results['fourteenToZeroCount'] += weight
        continue
    if whichwaterpointer(coords[a], 16) != 0:
        results['sixteenToZeroCount']+=weight
        continue
    elif checkdistance(coords[a],16,0)>3:
        results['sixteenToZeroCount'] += weight
        continue
    if whichwaterpointer(coords[a], 17) != 6:
        results['seventeenToSixCount']+=weight
        continue
    elif checkdistance(coords[a],17,6)>3:
        results['seventeenToSixCount'] += weight
        continue
    print(a)
    results['confusedCount'] += weight
    # writeMeAnXYZFile(coords[a],'path'+f'Prism{a}.xyz',0)
totalcount=sum(results.values())
# totalcount=oneToThreeCount+fourToSixCount+fiveToNineCount+sevenToNineCount+tenToTwelveCount+thirteenToFifteenCount+fourteenToZeroCount+sixteenToZeroCount+seventeenToSixCount+confusedCount
print(totalcount)
for name,value in results.items():
    resultsFile.write(name+"\n")
    resultsFile.write(str(value/totalcount)+"\n")
resultsFile.close()