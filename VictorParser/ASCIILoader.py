import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *
def DeuteriumChecker(coords):
    #find  OH distances, determine which are shortest
    coords=coords*0.529177
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
    sorted=np.sort(distances[:,5])
    sorth1=np.sort(distances[10])
    sorth2 = np.sort(distances[11])
    blue=sorth1[1]
    red=sorth2[1]
    if blue<red:
        return sorted[3],red
    else:
        return sorted[3],blue

f=open('simulation1Broken/optimized_sim1_coords.dat','r')
weird=[]
eight=[]
coords=[]
origin=[]
for line in f:
    oranges=line.strip()
    france=oranges.split()
    weird.append(france)
weird=np.array(weird)
print(np.int(weird[0][0]))
for i in np.arange(1,np.int(weird[0][0])+1):
    eight.append(weird[i])
eight=np.array(eight)
# for i in np.arange(0,2):
for i in np.arange(0,np.int(weird[0][0])):
    layer=[]
    originLayer=[]
    originLayer.append([eight[i][54],eight[i][55]])
    for j in np.arange(0,18):
        h=j*3
        layer.append([np.float(eight[i][h]),np.float(eight[i][h+1]),np.float(eight[i][h+2])])
    coords.append(layer)
    origin.append(originLayer)
coords=np.array(coords)
origin=np.array(origin)
count=0
count2=0
# print(coords[26587]*0.529177)
# exit()
# for i in np.arange(0,2):

# for i in np.arange(0,np.int(weird[0][0])):
#     acceptorlength,donorlength=DeuteriumChecker(coords[i])
#     if acceptorlength < 2.5:
#         count=count+1
#     if donorlength <2.5:
#         count2=count2+1
#         print(i)
# print(count/np.int(weird[0][0]))
# print(count2)
np.savez('simulation1Broken/PythonData/data',coords=coords,origin=origin)



