import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, 'FixingThingsWithRyan')
# from FixingThingsWithRyan \
import h2o_pot
exit()


amutoelectron=1.000000000000000000/6.02213670000e23/9.10938970000e-28
massH=1.008*amutoelectron
massO=16*amutoelectron
m=(massH*massO)/(massH+massO)
#omega=1
omega=3000*(4.5563e-6)
k=m*(omega**2)
dimensions=1
numWalkers=1000
numTimeSteps=1000
deltaTau=1
sigma=np.sqrt(deltaTau/m)
alpha=1/(2*deltaTau)
# V=h2o_pot.calc_hoh_pot
#first is array, second is length of the array
#mass for each coord
def randommovement(coords,sigma):
    for walker in np.arange(0,len(coords[:,0])):
        coords[walker]+=np.random.normal(0,sigma)
    return coords

def getDemEnergies(coords):
    energies=0.5*k*(np.square(coords))
    return energies

def birthandDeath(coords,energies,alpha,numWalkers):
    averageEnergy=np.average(energies)
    # print('averageEnergy:')
    # print(averageEnergy)
    Vref=averageEnergy-(alpha/numWalkers*(len(coords[:,0])-numWalkers))

    # print(len(coords[:,0]))
    # print()
    birthlist=[]
    deathlist=[]
    for walker in np.arange(0,len(coords[:,0])):
        random=np.random.random()
        if energies[walker]<Vref:
            prob=np.exp(-deltaTau*(energies[walker]-Vref))-1
            if random<prob:
                birthlist.append(coords[walker])
        elif energies[walker]>Vref:
            prob=1-np.exp(-deltaTau*(energies[walker]-Vref))
            # print('probability')
            # print(prob)
            # print(np.exp(-deltaTau*(energies[walker]-Vref)))
            # exit()
            if random<prob:
                deathlist.append(walker)
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

coords=np.zeros((numWalkers,dimensions))
# print(len(coords[:,0]))
count=0
fullEnergies=[]
for i in np.arange(0,numTimeSteps):
    count+=1
    coords=randommovement(coords,sigma)
    energies=getDemEnergies(coords)
    fullEnergies.append([i,np.average(energies),np.std(energies)])
    coords=birthandDeath(coords, energies,alpha,numWalkers)
    # print(count)
    # print(len(coords))
fullEnergies=np.array(fullEnergies)
# plt.errorbar(fullEnergies[:,0],fullEnergies[:,1],yerr=fullEnergies[:,2])
plt.plot(fullEnergies[:,0],fullEnergies[:,1]/(4.5563e-6))
plt.show()




