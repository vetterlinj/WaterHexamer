import numpy as np
import matplotlib.pyplot as plt
from VictorParser.Constants import *
# import sys
# sys.path.insert(0, 'FixingThingsWithRyan')
print('This one is new')
import sys
import os
# sys.path.insert(0, "/Users/nicholasvetterli/PycharmProjects/WaterHexamer/VictorParser/FixingThingsWithRyan")
import h2o_pot
# amutoelectron=1.000000000000000000/6.02213670000e23/9.10938970000e-28
# massH=1.008*amutoelectron
# massO=16*amutoelectron
# m=(massH*massO)/(massH+massO)
#omega=1
# omega=3000*(4.5563e-6)
# k=m*(omega**2)
dimensions=3
numWalkers=1000
numTimeSteps=1000
deltaTau=1
# sigma=np.sqrt(deltaTau/m)
alpha=1/(2*deltaTau)
# V=h2o_pot.calc_hoh_pot
#first is array, second is length of the array
#mass for each coord
def randommovement(coords,dimensions,deltaTau):
    count=0
    amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
    for walker in np.arange(0,len(coords[:,0])):
        count +=1
        if count % 3==0:
            #Oxygen
            m = 15.9994 * amutoelectron
        else:
            #Hydrogen
            m = 1.00794 * amutoelectron
        sigma = np.sqrt(deltaTau / m)
        randomCoord = np.zeros((dimensions))
        for coord in np.arange(0, dimensions):
            randomCoord[coord] += np.random.normal(0, sigma)
        coords[walker]+=randomCoord
    return coords

def getDemEnergies(coords):
    # energies=[]
    #
    # for a in np.arange(0,len(coords[:,0])/3):
    #
    #     a=int(a*3)
    #     walkercoords=[]
    #     walkercoords.append(coords[a])
    #     walkercoords.append(coords[a+1])
    #     walkercoords.append(coords[a+2])
    #     # walkercoords.append([0,0,0])
    #     # walkercoords.append([1,0,0])
    #     # walkercoords.append([0,0,2])
    #     energies.append(h2o_pot.calc_hoh_pot([walkercoords],1))
    reshapedcoords=np.reshape(coords,(len(coords)//3,3,3))
    energies=h2o_pot.calc_hoh_pot(reshapedcoords,len(coords)//3)
    return energies

def birthandDeath(coords,energies,alpha,numWalkers):
    averageEnergy=np.average(energies)
    # print('averageEnergy:')
    # print(averageEnergy)
    Vref=averageEnergy-(alpha/numWalkers*(len(coords[:,0])/3-numWalkers))

    # print(len(coords[:,0]))
    # print()
    birthlist=[]
    deathlist=[]
    for walker in np.arange(0,int(len(coords[:,0])/3)):
        random=np.random.random()
        if energies[walker]<Vref:
            prob=np.exp(-deltaTau*(energies[walker]-Vref))-1
            if random<prob:
                actualwalker=walker*3
                birthlist.append(coords[actualwalker])
                birthlist.append(coords[actualwalker+1])
                birthlist.append(coords[actualwalker + 2])
        elif energies[walker]>Vref:
            prob=1-np.exp(-deltaTau*(energies[walker]-Vref))
            # print('probability')
            # print(prob)
            # print(np.exp(-deltaTau*(energies[walker]-Vref)))
            # exit()
            if random<prob:
                actualwalker=walker*3
                deathlist.append(actualwalker)
                deathlist.append(actualwalker+1)
                deathlist.append(actualwalker+2)
        else:
            print('I am confuse destroyer of work')
    birthlist=np.array(birthlist)
    deathlist=np.array(deathlist)
    deletedcoords=np.delete(coords,deathlist,0)
    deletedcoords=np.array(deletedcoords)
    if len(birthlist)==0:
        print('empty')
        birthedcoords=deletedcoords
    else:
        birthedcoords=np.append(deletedcoords,birthlist,axis=0)
    return birthedcoords
angstr=0.529177
startingGeo=np.array([[0.9578400,0.0000000,0.0000000],
                     [-0.2399535,0.9272970,0.0000000],
             [0.0000000,0.0000000,0.0000000]])/angstr * 1.01
coords=np.zeros((numWalkers*3,dimensions))
for i in np.arange(0,numWalkers):
    coords[i*3]+= startingGeo[0]
    coords[i*3+1]+= startingGeo[1]
    coords[i*3+2]+=startingGeo[2]
# print(len(coords[:,0]))
count=0
fullEnergies=[]
for i in np.arange(0,numTimeSteps):
    count+=1
    coords=randommovement(coords,dimensions,deltaTau)
    energies=getDemEnergies(coords)
    fullEnergies.append([i,np.average(energies),np.std(energies)])
    coords=birthandDeath(coords, energies,alpha,numWalkers)
    # print(count)
    # print(len(coords))
fullEnergies=np.array(fullEnergies)
# plt.errorbar(fullEnergies[:,0],fullEnergies[:,1],yerr=fullEnergies[:,2])
plt.plot(fullEnergies[:,0],fullEnergies[:,1]/(4.5563e-6))
plt.show()
print('done')




