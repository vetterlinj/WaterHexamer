import numpy as np
import argparse
import matplotlib.pyplot as plt
import sys
import h2o_pot
from pyvibdmc import potential_manager as pm
TryUncorrPot=False
if TryUncorrPot==True:
    import h2o_uncorr_pot
import os

pot_dir = 'legacy_mbpol/'  # this directory is part of the one you copied that is outside of pyvibdmc.
py_file = 'callmbpol.py'
pot_func = 'call_a_cpot'  # def water_pot(cds) in h2o_potential.py
# The Potential object assumes you have already made a .so file and can successfully call it from Python
hex_pot = pm.Potential(potential_function=pot_func,
                         python_file=py_file,
                         potential_directory=pot_dir,
                         num_cores=8)
# exit()
# from VictorParser.Constants import *
# import sys
# sys.path.insert(0, 'FixingThingsWithRyan')
for weirdsimthingy in np.arange(0,1):
    amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
    dimensions = 3
    watersperwalker=1
    numWalkers = 20000
    numTimeSteps = 5
    deltaTau = 1
    alpha = 1 / (2 * deltaTau)
    ContWeights=False
    debut=False
    atomicMass=True
    CarringtonPot=False
    primecup=0
    print('running')
    filename='DMCResult'
    energieslist=[]
    for i in np.arange(0,1):
        # filename = f"Results/Multiple/{foldername}/" + fnameExtension #+ f"_{namedeltaTau}_{i}"
            # print(filename)
        # resultsfilename = f"Results/Multiple/{foldername}/npzFiles/" + fnameExtension #+ f"_{namedeltaTau}_{i}"
        #first is array, second is length of the array
        #mass for each coord
        def randommovement(coords,dimensions,deltaTau):
            #check
            initialcoords=np.copy(coords)
            for atom in np.arange(0, len(coords)/18):
                actualcoord=atom*18
                countmove = 0
                #FIX THIS
                for actualatom in np.arange(0,3):

                    if countmove % 3 == 0:
                        # Oxygen
                        # print("O")
                        m = 15.9994 * amutoelectron
                    # elif countmove %3 == 1:
                    else:
                        # print("H")
                        # Hydrogen
                        m = 1.00794 * amutoelectron

                    # elif countmove %3 == 2:
                    #     # Deuterium
                    #     m = 2.014102 * amutoelectron
                    sigma = np.sqrt(deltaTau / m)
                    randomCoord = np.zeros((dimensions))
                    for coordinate in np.arange(0, dimensions):
                        randomCoord[coordinate] += np.random.normal(0, sigma)
                    coords[int(actualcoord+actualatom)] += randomCoord
                    countmove += 1
            diffcoords=coords-initialcoords
            return coords
        if CarringtonPot==False:
            def getDemEnergies(coords,watersperwalker):
                #check
                #################
                reshapedcoords = np.reshape(coords, (len(coords) // 18, 18, 3))
                # reshapedcoords=reshapedcoords[:,0:3,:]
                # initialcage=np.reshape(initialcage, (len(initialcage) // 18, 18, 3))
                # listenergies = h2o_pot.calc_hoh_pot(reshapedcoords, len(reshapedcoords))#/627.5094740631
                listenergies = hex_pot.getpot(reshapedcoords)/627.5094740631
                #numwalkersx18x3
                #hex_pot.getpot(coords)
                # energies = np.add.reduceat(listenergies, np.arange(0, len(listenergies), 1))
                return listenergies
        if ContWeights==False:
            def getVref(energies,alpha,weights,numWalkers,coords,watersperwalker):
                Vref = np.average(energies) - (alpha / numWalkers * (len(coords)/(18) - numWalkers))
                if len(coords)/(18*watersperwalker)!= len(energies):
                    print("BIG PROBLEM")
                #check len coords (modified) is the same as energies
                return Vref
            def birthandDeath(coords,energies,alpha,numWalkers,weights,deltaTau,watersperwalker,Vref):
                #check
                averageEnergy=np.average(energies)
                # print('averageEnergy:')
                # print(averageEnergy)
                #VREF FROM PREVIOUS STEP
                #too many VREF (before or after only)
                #displace, calc Vref, not recalc after branching, want to calc once per time step
                #Vref = np.average(energies) - (alpha / numWalkers * (len(coords)/(3*watersperwalker) - numWalkers))

                # print(len(coords[:,0]))
                # print()
                birthlist=[]
                deathlist=[]
                desclist=[]
                for walker in np.arange(0,int(len(coords)/(18*watersperwalker))):
                    random=np.random.random()
                    # if energies[walker]<Vref:
                    actualwalker = walker * (18 * watersperwalker)
                    expon=np.exp(-deltaTau*(energies[walker]-Vref))
                    if np.int(expon)>0:

                        for neededwalker in np.arange(0,np.int(expon)):
                            desclist.append(weights[walker])
                            for ff in np.arange(0, (18 * watersperwalker), 1):
                                birthlist.append(coords[actualwalker + ff])

                    prob=abs(expon-int(expon))
                    if random<prob:
                        desclist.append(weights[walker])
                        for ff in np.arange(0,(18*watersperwalker),1):
                            birthlist.append(coords[actualwalker+ff])
                birthlist=np.array(birthlist)
                desclist=np.array(desclist)
                return birthlist, desclist
        angstr=0.529177
        #FIX THIS
        initialcage = [[0.80559297, 1.82637417, 0.19044583],
                       [1.64546268, 1.33062728, 0.20230004],
                       [1.03131975, 2.74531261, 0.3303837],
                       [-0.86971419, -0.05280485, 1.64663647],
                       [-0.40947453, 0.75209702, 1.37618396],
                       [-1.70683682, -0.02424652, 1.15831962],
                       [0.65167739, -1.73597316, 0.2335045],
                       [0.05821864, -1.2362209, 0.84210027],
                       [0.569203, -2.6591634, 0.4706903],
                       [-0.51396268, 0.08861126, -1.76674358],
                       [-0.09074241, 0.82334616, -1.30525568],
                       [-0.09916254, -0.6895166, -1.37517223],
                       [2.81742948, -0.01780752, 0.18363679],
                       [2.20422291, -0.77223806, 0.20893524],
                       [3.38891525, -0.17263024, -0.5686021],
                       [-2.86669414, -0.14282213, -0.31653989],
                       [-2.17356321, -0.01889467, -0.98894102],
                       [-3.61843908, 0.36974668, -0.61083718]]
        # coords = np.array(initialcage * numWalkers)/0.529177#*1.01
        coords=np.load("frozenCage/AAD/1/frozenHexAAD1_0Data.npz")['coords']
        print()
        initialcage = np.reshape(initialcage, (len(initialcage) // 18, 18, 3))/0.529177
        zeroinenergy=(hex_pot.getpot(initialcage) / 627.5094740631 / 4.5563e-6)
        print(zeroinenergy)
        weights=np.arange(0,len(coords)//18)
        count=0
        fullEnergies=[]
        fullWalkers=[]
        for i in np.arange(0,numTimeSteps):
            count+=1
            if count %10 ==0:
                print(count)
                print(Vref / (4.5563e-6) / (watersperwalker))
                print(len(coords)/18)
                biglist=[]
            if i==0:
                energies=getDemEnergies(coords,watersperwalker)
                #print(np.average(energies)/(4.5563e-6))
                Vref = getVref(energies, alpha, weights, numWalkers, coords, watersperwalker)
            coords=randommovement(coords,dimensions,deltaTau)
            energies=getDemEnergies(coords,watersperwalker)
            coords,weights=birthandDeath(coords, energies,alpha,numWalkers,weights,deltaTau,watersperwalker,Vref)
            energies = getDemEnergies(coords,watersperwalker)
            Vref = getVref(energies, alpha, weights, numWalkers, coords,watersperwalker)
            #print(Vref / (watersperwalker*4.5563e-6))
            fullEnergies.append([i,Vref/(watersperwalker*4.5563e-6)])
            fullWalkers.append([i,len(coords//18)])
        # beginning=np.array(initialcage*np.int(len(coords)/18))
        # beginning=beginning-coords
        red=np.unique(weights,return_index=True, return_counts=True)
        biglist=[]
        fullEnergies=np.array(fullEnergies)
        fullEnergies=fullEnergies-zeroinenergy
        fullWalkers=np.array(fullWalkers)
        plt.plot(fullEnergies[:,0],fullEnergies[:,1])
        # if bunchofjobs==False:
        #     plt.show()
        #     print(np.average(fullEnergies[int(len(fullEnergies)/2):-1,1]))
        #     exit()
        plt.savefig(filename)
        np.savez(resultsfilename + "Data", energies=fullEnergies, coords=coords, iwalkers=numWalkers, deltatau=deltaTau,
                 timesteps=numTimeSteps, weights=weights, watersperwalker=watersperwalker)
        np.savez(resultsfilename+"Data",energies=fullEnergies,coords=coords,iwalkers=numWalkers,deltatau=deltaTau,timesteps=numTimeSteps,weights=weights,watersperwalker=watersperwalker, walkers=fullWalkers)
        averageEnergy=np.average(fullEnergies[int(len(fullEnergies)/2):-1,1])
        stdEnergy=np.std(fullEnergies[int(len(fullEnergies)/2):-1,1])
        energieslist.append(averageEnergy)
        resultsFile = open(f"{filename}Energy.txt", 'w')
        resultsFile.write(str(averageEnergy) + '\n')
        resultsFile.write(str(stdEnergy))
        resultsFile.close()