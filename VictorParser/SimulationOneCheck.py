import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *

data = np.load('simulation1Broken/PythonData/FullPythonData/data.npz')
# make a large matrix
coords =data['coords']
def whichisnextwater(walkercoords,currentwater):
    water = np.arange(0, 6) * 3
    list=[]
    for i in water:
        list.append(np.sqrt(np.sum(np.square(walkercoords[currentwater+1]-walkercoords[i]))))
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
count=0
count1=0
weird=0
countsixtonine=0
count15to1=0
count14to16=0
count17to7=0
count18to1=0
confused=0
for a in np.arange(0,56242):
    # print(coords[a]*0.529177)
    coords[a]=watertrader(coords[a],0,15,1)
    nextwater=whichisnextwater(coords[a],0)
    if nextwater != 6:
        print(nextwater)
        print(a)
        continue
    coords[a]=watertrader(coords[a],3,nextwater,2)
    if doublewatertime(coords[a],3) !=(6,6) and doublewatertime(coords[a],3) != (15,15) and doublewatertime(coords[a],3) != (6,15)and doublewatertime(coords[a],3) != (0,15)and doublewatertime(coords[a],3) != (15,0)and doublewatertime(coords[a],3) != (6,0)and doublewatertime(coords[a],3) != (0,6):

        weird=weird+1
        continue
    elif doublewatertime(coords[a],3) == (6,6) or doublewatertime(coords[a],3)==(6,0) or doublewatertime(coords[a],3)==(0,6):
        count=count+1
        #5to7?
        continue
    elif doublewatertime(coords[a],3) == (15,15) or doublewatertime(coords[a],3)==(0,15) or doublewatertime(coords[a],3)==(15,0):
        count1=count1+1
        #6to10?
        continue
    coords[a][[7, 8]] = coords[a][[8, 7]]
    nextwater=whichisnextwater(coords[a],6)
    if nextwater != 15 and nextwater!= 12 and nextwater!=3:
        print('weird')
        print(a)
        print(nextwater)
        print(coords[a]*0.529177)
    elif nextwater == 12 or nextwater == 3:
        countsixtonine=countsixtonine+1
        continue
    coords[a]=watertrader(coords[a],9,15,1)
    nextwater=whichisnextwater(coords[a],9)
    if nextwater!=15:
        print('weird')
        print(a)
        print(nextwater)
        print(coords[a] * 0.529177)
        continue
    coords[a]=watertrader(coords[a],12,nextwater,1)
    #check 12 to 1, and then the others
    if doublewatertime(coords[a],12) == (15,15) or doublewatertime(coords[a],12) == (15,9) or doublewatertime(coords[a],12) == (9,15):
        count15to1=count15to1+1
        continue
    if doublewatertime(coords[a],12) == (9,0) or doublewatertime(coords[a],12) == (0,0):
        count14to16=count14to16+1
        continue
    if doublewatertime(coords[a],12) != (15,0):
        print(doublewatertime(coords[a],12))
        print(coords[a] * 0.529177)
    if doublewatertime(coords[a],15) == (6,12)or doublewatertime(coords[a],15) == (6,6)or doublewatertime(coords[a],15) == (12,6):
        count18to1=count18to1+1
        continue
    if doublewatertime(coords[a],15) == (12,0) or doublewatertime(coords[a],15) == (0,0):
        count17to7=count17to7+1
        continue
    if doublewatertime(coords[a],15) != (6,0) and doublewatertime(coords[a],15) != (0,6):
        print(doublewatertime(coords[a],15))
        print(coords[a] * 0.529177)
    #check distances:
    if doublewatertime(coords[a], 15) == (6, 0):
        if checkdistance(coords[a],16,6) >3:
            count17to7=count17to7+1
            continue
        if checkdistance(coords[a],17,0) >3:
            count18to1=count18to1+1
            continue
    if doublewatertime(coords[a], 15) == (0, 16):
        if checkdistance(coords[a],17,6) >3:
            count17to7=count17to7+1
            continue
        if checkdistance(coords[a],16,0) >3:
            count18to1=count18to1+1
            continue
    if doublewatertime(coords[a],12) == (15,0):
        if checkdistance(coords[a],13,15)>3:
            count14to16=count14to16+1
            continue
        if checkdistance(coords[a], 14, 0) > 3:
            count15to1=count15to1+1
            continue
    print('oranges')
    print(a)
    confused=confused+1
totalcounted=count+count1+weird+countsixtonine+count15to1+count14to16+count17to7+count18to1
print('6 to 10')
print(count/(totalcounted+confused))
print('5 to 7')
print(count1/(totalcounted+confused))
print('the number of weirdy ones for our first double donor')
print(weird/(totalcounted+confused))
print('6 to 10')
print(countsixtonine/(totalcounted+confused))
print('15to1')
print(count15to1/(totalcounted+confused))
print('14 to 16')
print(count14to16/(totalcounted+confused))
print('17 to 7')
print(count17to7/(totalcounted+confused))
print('18 to 1')
print(count18to1/(totalcounted+confused))
print('the number that have no problems?')
print(confused/(confused+totalcounted))
print(confused+totalcounted)

