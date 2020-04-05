import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *
coords, weights, metadata=concatenatenpz('NickFiles/VictorData/h2o6_book/PythonData/')
#coords, weights, metadata=concatenatenpz('h2o6_bookPythonData/')
oranges=len(weights)

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
    if currentwater==0:
        return sorth1*3,1
    elif listh1[sorth1] < listh2[sorth2]:
        if currentwater-3==sorth1*3:
            print('thefirstone')
            return sorth2*3,2
        else:
            return sorth1*3,1
    elif listh2[sorth2] < listh1[sorth1]:
        if currentwater-3==sorth2*3:
            print('thesecondone')
            return sorth1*3,1
        else:
            return sorth2*3,2
    else:
        print('problem found')
        print(a)
def initialoxygen(coords):
    #find  OH distances, determine which are shortest
    oxygen = [coords[0, :], coords[3, :], coords[6, :], coords[9, :], coords[12, :], coords[15, :]]
    # Oxygen is (6,walkers,3)
    h1 = [coords[1, :], coords[4, :], coords[7, :], coords[10, :], coords[13, :], coords[16, :]]
    h2 = [coords[2, :], coords[5, :], coords[8, :], coords[11, :], coords[14, :], coords[17, :]]
    h1 = np.array(h1)
    h2 = np.array(h2)
    oxygen = np.array(oxygen)
    distances=[]
    for hydrogenatom in np.arange(0,6):
        listh1=[]
        listh2=[]
        for oxygenatom in np.arange(0,6):
            listh1.append(np.sqrt(np.sum(np.square(h1[hydrogenatom]-oxygen[oxygenatom]))))
            listh2.append(np.sqrt(np.sum(np.square(h2[hydrogenatom]-oxygen[oxygenatom]))))
        distances.append(listh1)
        distances.append(listh2)
    distances=np.array(distances)
    sorted=np.sort(distances)
    bondeddistances=[]
    for i in np.arange(0,6):
        list=[]
        list.append(sorted[i*2,1])
        list.append(sorted[i*2+1,1])
        bondeddistances.append(list)
    bondeddistances=np.array(bondeddistances)
    sortedbondeddistances=np.sort(bondeddistances)
    print(distances)


    # roh1 = np.square(oxygen - h1)
    # roh1 = np.sqrt(np.sum(roh1, 1))
    # print(roh1)
    # # roh is (6,walkers)
    # roh2 = np.square(oxygen - h2)
    # roh2 = np.sqrt(np.sum(roh2, 1))
    # print(roh2)
    # print('this is an orange')
    return [12,0]
problems=[]
for a in np.arange(0,oranges):

    candidates=oxygendistance(coords[a])
    # candidates=initialoxygen(coords[a])
    c1=candidates[0]
    c2=candidates[1]
    # print(coords[a])
    theone, theonehydrogen=whichisitthough(coords[a],c1,c2)
    #print(f"the first water is {theone}")
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
        #print(f"the current water is {w} and the next water is {nextoxygen}")
        if nextoxygen < w:
            print('problem: switching with locked in waters')
            print(a)
            print(w)
            problems.append(a)
            break
        coords[a][[w+3, nextoxygen]] = coords[a][[nextoxygen, w+3]]
        coords[a][[w + 4, nextoxygen+1]] = coords[a][[nextoxygen+1, w + 4]]
        coords[a][[w + 5, nextoxygen+2]] = coords[a][[nextoxygen+2, w + 5]]
    lastw=15
    nextoxygen, changehydrogen = whichoxygenisnext(coords[a], lastw)
    if nextoxygen != 0:
        print('Problem: cycle is incomplete')
        print(a)
        print(lastw)

    if changehydrogen == 2:
        coords[a][[lastw + 1, lastw + 2]] = coords[a][[lastw + 1, lastw + 2]]
    #print('layercomplete')
    print(a)
print(problems)
reversedProblems=problems[::-1]
#[43, 45, 437, 527, 679, 805, 895, 1024, 1241, 1487, 2284, 2305, 2347, 2416, 3233, 3342, 3601, 3966, 4099, 4165, 5343, 5364, 5791, 6013, 8748, 8787, 9102, 9199, 9353, 9450, 10275, 10707, 10890, 11000, 11284, 11885, 12103, 12335, 13517, 13584, 13600, 14158, 14234, 14506, 16571, 17439, 17923, 18022, 18203, 18308, 18397, 18510, 18529, 18963, 18998, 19029, 20885, 21201, 21477, 23427, 24133, 24187, 24876, 25044, 25993, 26408, 26971, 27788, 28362, 31347, 31487, 32930, 33829, 34008, 36096, 37367, 37781, 38881, 40454, 41164, 41167, 43795, 48807, 49378]

newcoords=coords
for problem in reversedProblems:
    newcoords = np.delete(newcoords, problem, 0)
    weights = np.delete(weights, problem)
np.savez('NickFiles/VictorData/h2o6_book/SortedWithoutProblems',coords=newcoords,weights=weights,metadata=metadata,problems=problems)