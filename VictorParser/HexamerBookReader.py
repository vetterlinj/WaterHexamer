import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *
#coords, weights, metadata=concatenatenpz('NickFiles/VictorData/h2o6_book/PythonData/')
coords, weights, metadata=concatenatenpz('h2o6_bookPythonData/')
def oxygendistance(walkercoords):
    water=np.arange(0,6)*3
    distances=np.zeros((6,6))
    for i in water:
        water=np.delete(water,0)
        for j in water:
            entry=walkercoords[i,:]-walkercoords[j,:]
            entry = np.square(entry)
            entry = np.sqrt(np.sum(entry))
            distances[int(i/3),int(j/3)]=entry
            distances[int(j/3),int(i/3)]=entry
    sorted=np.sort(distances)
    candidates=np.array(np.argsort(sorted[:,3])[0:2])
    candidates=candidates*3
    return candidates
def whichisitthough(walkercoords,c1,c2):
    list=[]
    list.append(np.sqrt(np.sum(np.square(walkercoords[c1+1]-walkercoords[c2]))))
    list.append(np.sqrt(np.sum(np.square(walkercoords[c1+2]-walkercoords[c2]))))
    list.append(np.sqrt(np.sum(np.square(walkercoords[c2+1]-walkercoords[c1]))))
    list.append(np.sqrt(np.sum(np.square(walkercoords[c2 + 2] - walkercoords[c1]))))
    list=np.argsort(list)
    if list[0] == 2:
        return c2, 1
    if list[0]== 3:
        return c2, 2
    if list[0]==0:
        return c1, 1
    if list[0]==1:
        return c1, 2

def whichoxygenisnext(walkercoords, currentwater):
    water = np.arange(0, 6) * 3
    listh1=[]
    listh2=[]
    for i in water:
        listh1.append(np.sqrt(np.sum(np.square(walkercoords[currentwater+1]-walkercoords[i]))))
        listh2.append(np.sqrt(np.sum(np.square(walkercoords[currentwater + 2] - walkercoords[i]))))
    sorth1=np.argsort(listh1)[1]
    sorth2=np.argsort(listh2)[1]
    print(listh1)
    print(listh2)
    print(sorth1)
    print(sorth2)
    if listh1[sorth1] < listh2[sorth2]:
        return sorth1*3,1
    elif listh2[sorth2] < listh1[sorth1]:
        return sorth2*3,2
    else:
        print('problem found')
        print(a)


for a in np.arange(3,4):
    candidates=oxygendistance(coords[a])
    c1=candidates[0]
    c2=candidates[1]
    theone, theonehydrogen=whichisitthough(coords[a],c1,c2)
    #swaps the 0th row with what we want to be oxygen 0
    coords[a][[0,theone]] = coords[a][[theone,0]]
    #ensures that the second hydrogen (coords[2]) is the one pointing to the middle, so that hydrogen 1 points to the next oxygen in the cycle.
    if theonehydrogen == 2:
        coords[a][[1,theone+1]] = coords[a][[theone+1,1]]
        coords[a][[2,theone+2]] = coords[a][[theone+2,2]]
    else:
        coords[a][[2,theone+1]] = coords[a][[theone+1,2]]
        coords[a][[1,theone+2]] = coords[a][[theone+2,1]]
    for w in np.arange(0,5)*3:
        nextoxygen, changehydrogen=whichoxygenisnext(coords[a],w)
        if changehydrogen==2 and w!=0:
            coords[a][[w+1, w+2]] = coords[a][[w+2, w+1]]
        print(nextoxygen)
        print(w)
        if nextoxygen < w:
            print('problem: switching with locked in waters')
            print(a)
            print(w)
            exit()
        coords[a][[w+3, nextoxygen]] = coords[a][[nextoxygen, w+3]]
        coords[a][[w + 4, nextoxygen+1]] = coords[a][[nextoxygen+1, w + 4]]
        coords[a][[w + 5, nextoxygen+2]] = coords[a][[nextoxygen+2, w + 5]]
    lastw=15
    nextoxygen, changehydrogen = whichoxygenisnext(coords[a], lastw)
    if nextoxygen != 0:
        print('Problem: cycle is incomplete')
        print(a)
        print(lastw)
        exit()
    if changehydrogen == 2:
        coords[a][[lastw + 1, lastw + 2]] = coords[a][[lastw + 1, lastw + 2]]
    print('layercomplete')
