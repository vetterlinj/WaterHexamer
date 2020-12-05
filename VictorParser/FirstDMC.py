import numpy as np
import argparse
import matplotlib.pyplot as plt
# import sys
# sys.path.insert(0, 'FixingThingsWithRyan')
# print('This is the old file')
# from VictorParser.FixingThingsWithRyan import h2o_pot
# #
# # h2o_pot.calc_hoh_pot([[[0,0,0],[2,0,0],[0,0,1]]],1)
# # exit()
#Harmonic to Morse to 2*1D to 6D

amutoelectron=1.000000000000000000/6.02213670000e23/9.10938970000e-28
massH=1.00794*amutoelectron
massO=15.9994*amutoelectron
m=(massH*massO)/(massH+massO)
#omega=1
omega=3700*(4.5563e-6)
k=m*(omega**2)
dimensions=1
numWalkers=20000
numTimeSteps=40000
deltaTau=1
sigma=np.sqrt(deltaTau/m)
alpha=1/(2*deltaTau)
bunchofjobs=False
if bunchofjobs == True:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', help='<Required> File Name', required=True)
    parser.add_argument('-l', '--list', nargs='+', help='<Required> Set flag', required=True)
    args = parser.parse_args()
    fnameExtension = args.string
    numWalkers = int(args.list[0])
    deltaTau = int(args.list[2])
    numTimeSteps = int(args.list[1]) / deltaTau
    namedeltaTau = str(deltaTau).replace(".", "point")
    sigma = np.sqrt(deltaTau / m)
    alpha = 1 / (2 * deltaTau)
    filename = "Results/Multiple/Harmonic/" + fnameExtension# + f"_{namedeltaTau}"
    resultsfilename = "Results/Multiple/Harmonic/npzFiles/" + fnameExtension #+ f"_{namedeltaTau}"
# V=h2o_pot.calc_hoh_pot
#first is array, second is length of the array
#mass for each coord
def randommovement(coords,sigma):
    for walker in np.arange(0,len(coords)):
        coords[walker]+=np.random.normal(0,sigma)
    return coords

def getDemEnergies(coords):
    energies=0.5*k*(np.square(coords))
    return energies


def birthandDeath(coords, energies, alpha, numWalkers, weights, deltaTau):
    averageEnergy = np.average(energies)
    # print('averageEnergy:')
    # print(averageEnergy)
    #Vref = averageEnergy - (alpha / numWalkers * (len(coords) - numWalkers))
    Vref = averageEnergy - (alpha *np.log(np.sum(weights)/numWalkers))
    # print(len(coords[:,0]))
    # print()
    birthlist = []
    deathlist = []
    deathweights = []
    deathcount = 0
    for walker in np.arange(0, int(len(coords))):
        expon = np.exp(-deltaTau * (energies[walker] - Vref))
        weights[walker] *= expon
        if weights[walker] < (0.01):
            actualwalker = walker * 1
            deathlist.append(actualwalker)
            deathweights.append(walker)
            deathcount += 1
    deathlist = np.array(deathlist)
    deathweights = np.array(deathweights)
    deletedcoords = np.delete(coords, deathlist, 0)
    deletedcoords = np.array(deletedcoords)
    deletedweights = np.delete(weights, deathweights, 0)
    if len(weights) - len(deathweights) != len(deletedweights):
        print('issue')
    appendlist = []
    if deathcount > 0:
        for neededwalker in np.arange(0, deathcount):
            walker = np.argmax(deletedweights)
            actualwalker = walker * 1
            birthlist.append(deletedcoords[actualwalker])
            deletedweights[walker] /= 2
            # deletedweights.append(deletedweights[walker])
            appendlist.append(deletedweights[walker])
    deletedweights = np.array(deletedweights)
    birthlist = np.array(birthlist)
    appendlist = np.array(appendlist)
    if len(birthlist) == 0:
        #print('empty')
        birthedcoords = deletedcoords
        birthedweights = deletedweights
    else:
        birthedcoords = np.append(deletedcoords, birthlist)
        birthedweights = np.append(deletedweights, appendlist)
    return birthedcoords, birthedweights
superlist=[]
# for run in np.arange(0,10):
#     if run %2==0:
#         deltaTau = 10
#         sigma = np.sqrt(deltaTau / m)
#         alpha = 1 / (2 * deltaTau)
#         print(deltaTau)
#     else:
#         deltaTau = 1
#         sigma = np.sqrt(deltaTau / m)
#         alpha = 1 / (2 * deltaTau)
#         print(deltaTau)

coords=np.zeros((numWalkers,dimensions))
weights=np.zeros((numWalkers))
weights+=1
# print(len(coords[:,0]))
count=0
fullEnergies=[]
for i in np.arange(0,numTimeSteps):
    if count%100==0:
        print(count)
    count+=1
    coords=randommovement(coords,sigma)
    energies=getDemEnergies(coords)
    averageEnergy=np.average(energies)
    # Vref = averageEnergy - (alpha / numWalkers * (len(coords) - numWalkers))
    Vref = averageEnergy - (alpha * np.log(np.sum(weights) / numWalkers))
    fullEnergies.append([i,Vref,np.std(energies)])
    coords,weights=birthandDeath(coords, energies,alpha,numWalkers,weights,deltaTau)
    # print(count)
    # print(len(coords))
fullEnergies=np.array(fullEnergies)
# plt.errorbar(fullEnergies[:,0],fullEnergies[:,1],yerr=fullEnergies[:,2])
# plt.plot(fullEnergies[:,0],fullEnergies[:,1]/(4.5563e-6))
averageEnergy=np.average(fullEnergies[int(len(fullEnergies)/2):,1])
print(averageEnergy/(4.5563e-6))
np.savez(resultsfilename+"Data",energies=fullEnergies,coords=coords,iwalkers=numWalkers,deltatau=deltaTau,timesteps=numTimeSteps,weights=weights)




