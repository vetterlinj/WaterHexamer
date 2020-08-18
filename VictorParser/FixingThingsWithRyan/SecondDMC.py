import numpy as np
import matplotlib.pyplot as plt
import sys
import h2o_pot
import os
# from VictorParser.Constants import *
# import sys
# sys.path.insert(0, 'FixingThingsWithRyan')
numWalkers=3000
numTimeSteps=1000
deltaTau=1
bunchofjobs=False
print('running')
filename='DMCResult'
if bunchofjobs == True:
    fnameExtension=sys.argv[1]
    arg2=sys.argv[2]
    numWalkers=int(arg2)
    arg3 = sys.argv[3]
    numTimeSteps=int(arg3)
    arg4= sys.argv[4]
    deltaTau=int(arg4)
    filename="Result/"+fnameExtension

# sys.path.insert(0, "/Users/nicholasvetterli/PycharmProjects/WaterHexamer/VictorParser/FixingThingsWithRyan")

# amutoelectron=1.000000000000000000/6.02213670000e23/9.10938970000e-28
# massH=1.008*amutoelectron
# massO=16*amutoelectron
# m=(massH*massO)/(massH+massO)
#omega=1
# omega=3000*(4.5563e-6)
# k=m*(omega**2)
dimensions=3
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
            #COMMENT PLEASE
            randomCoord[coord] += np.random.normal(0, sigma)
        # print(randomCoord)
        coords[walker]+=randomCoord
    return coords

def getDemEnergies(coords):
    reshapedcoords=np.reshape(coords,(len(coords)//3,3,3))
    energies=h2o_pot.calc_hoh_pot(reshapedcoords,len(coords)//3)
    return energies

def birthandDeath(coords,energies,alpha,numWalkers):
    averageEnergy=np.average(energies)
    # print('averageEnergy:')
    # print(averageEnergy)
    Vref=averageEnergy-(alpha/numWalkers*(len(coords[:,0])/3-numWalkers))
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
def getVref(energies, alpha, weights, numWalkers, coords):
    Vref = np.average(energies) - (alpha / numWalkers * ((len(coords)/3) - numWalkers))
    return Vref
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
print('initalized')
count=0
fullEnergies=[]
weights=[]
for i in np.arange(0,numTimeSteps):
    if i%100==0:
        print(i)
    count+=1
    coords=randommovement(coords,dimensions,deltaTau)
    energies=getDemEnergies(coords)
    Vref = getVref(energies, alpha, weights, numWalkers, coords)
    fullEnergies.append([i, Vref / (4.5563e-6)])
    # if i==0:
        #do VREF right
    coords=birthandDeath(coords, energies,alpha,numWalkers)
    #real vref for time
    # print(count)
    # print(len(coords))
energies = getDemEnergies(coords)
Vref=getVref(energies,alpha,weights,numWalkers,coords)
fullEnergies.append([numTimeSteps, Vref / (4.5563e-6)])
fullEnergies=np.array(fullEnergies)
# plt.errorbar(fullEnergies[:,0],fullEnergies[:,1],yerr=fullEnergies[:,2])
plt.plot(fullEnergies[:,0],fullEnergies[:,1])
plt.savefig(filename)
np.save(filename+"Data",fullEnergies)
averageEnergy=np.average(fullEnergies[int(len(fullEnergies)/2):-1,1])
resultsFile = open(f"{filename}Energy.txt", 'w')
# 4638.39 cm^-1 for Pschwenk
resultsFile.write(str(averageEnergy) + '\n')
resultsFile.close()
exit()



