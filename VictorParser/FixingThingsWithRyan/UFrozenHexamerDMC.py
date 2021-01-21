import numpy as np
import argparse
import matplotlib.pyplot as plt
import sys
#import h2o_pot
import pyvibdmc
from pyvibdmc.pyvibdmc import potential_manager as pm
TryUncorrPot=False
if TryUncorrPot==True:
    import h2o_uncorr_pot
import os
#DMC using Ryan's potential manager from pyvibdmc and Victor's optimized cage and keeps all but one (the first) water frozen in place while propagating the unfrozen water.
pot_dir = 'legacy_mbpol/'  # this directory is part of the one you copied that is outside of pyvibdmc.
py_file = 'callmbpol.py'
pot_func = 'call_a_cpot'  # def water_pot(cds) in h2o_potential.py
# The Potential object assumes you have already made a .so file and can successfully call it from Python
hex_pot = pm.Potential(potential_function=pot_func,
                         python_file=py_file,
                         potential_directory=pot_dir,
                         num_cores=28)

initialcage=[[ 0.80559297,  1.82637417,  0.19044583],
 [ 1.64546268,  1.33062728,  0.20230004],
 [ 1.03131975,  2.74531261,  0.3303837 ],
 [-0.86971419, -0.05280485,  1.64663647],
 [-0.40947453,  0.75209702,  1.37618396],
 [-1.70683682, -0.02424652,  1.15831962],
 [ 0.65167739, -1.73597316,  0.2335045 ],
 [ 0.05821864, -1.2362209 ,  0.84210027],
 [ 0.569203  , -2.6591634 ,  0.4706903 ],
 [-0.51396268,  0.08861126, -1.76674358],
 [-0.09074241,  0.82334616, -1.30525568],
 [-0.09916254, -0.6895166 , -1.37517223],
 [ 2.81742948, -0.01780752,  0.18363679],
 [ 2.20422291, -0.77223806,  0.20893524],
 [ 3.38891525, -0.17263024, -0.5686021 ],
 [-2.86669414, -0.14282213, -0.31653989],
 [-2.17356321, -0.01889467, -0.98894102],
 [-3.61843908,  0.36974668, -0.61083718]]
# initialcage=np.array([[0.9578400,0.0000000,0.0000000],
                             # [-0.2399535,0.9272970,0.0000000],
                     # [0.0000000,0.0000000,0.0000000]])*0.529177
initialcage=np.array(initialcage*2)/0.529177
initialcage=np.reshape(initialcage, (len(initialcage) // 18, 18, 3))
# initialcage=np.load("initial_prism_walkersgeo.npy")
# initialcage=initialcage*0.529177
# np.save('initial_prism_walkersgeo.npy', initialcage)
print(hex_pot.getpot(initialcage)/627.5094740631/4.5563e-6)
# exit()
# from VictorParser.Constants import *
# import sys
# sys.path.insert(0, 'FixingThingsWithRyan')
for weirdsimthingy in np.arange(0,1):
    amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
    # massH = 1.008 * amutoelectron
    # massO = 16 * amutoelectron
    # m = (massH * massO) / (massH + massO)
    # omega=1
    # omega = 3000 * (4.5563e-6)
    # k = m * (omega ** 2)
    dimensions = 3
    watersperwalker=1
    numWalkers = 200
    numTimeSteps = 200
    deltaTau = 10
    # sigma = np.sqrt(deltaTau / m)
    alpha = 1 / (2 * deltaTau)
    bunchofjobs=False
    ContWeights=False
    debut=False
    atomicMass=True
    CarringtonPot=False
    primecup=0
    print('running')
    filename='DMCResult'
    energieslist=[]
    if bunchofjobs == True:
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--string', help='<Required> File Name', required=True)
        parser.add_argument('-l', '--list', nargs='+', help='<Required> Set flag', required=True)
        args = parser.parse_args()
        fnameExtension=args.string

        numWalkers=int(args.list[0])
        deltaTau=int(args.list[2])
        #alphaTau=int(args.list[3])
        numTimeSteps = int(args.list[1])/deltaTau
        namedeltaTau = str(deltaTau).replace(".", "point")
        # sigma = np.sqrt(deltaTau / m)
        alpha = 1 / (2 * deltaTau)
    for i in np.arange(0,1):
        if bunchofjobs == True:
            if ContWeights==True:
                foldername="ContHex"
            elif ContWeights==False:
                foldername="DiscHex"

            # fnameExtension=sys.argv[1]
            # arg2=sys.argv[2]
            # numWalkers=int(arg2)
            # arg3 = sys.argv[3]
            # totalTime=int(arg3)
            # arg4= sys.argv[4]
            # deltaTau=float(arg4)-weirdsimthingy/2
            # numTimeSteps=int(totalTime/deltaTau)
            # print(numTimeSteps)
            # namedeltaTau=str(deltaTau).replace(".","point")
            filename = f"Results/Multiple/{foldername}/" + fnameExtension #+ f"_{namedeltaTau}_{i}"
            # print(filename)
            resultsfilename = f"Results/Multiple/{foldername}/npzFiles/" + fnameExtension #+ f"_{namedeltaTau}_{i}"
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
                for walker in np.arange(0,int(len(coords)/(18*watersperwalker))):
                    random=np.random.random()
                    # if energies[walker]<Vref:
                    actualwalker = walker * (18 * watersperwalker)
                    expon=np.exp(-deltaTau*(energies[walker]-Vref))
                    if np.int(expon)>0:
                        for neededwalker in np.arange(0,np.int(expon)):
                            for ff in np.arange(0, (18 * watersperwalker), 1):
                                birthlist.append(coords[actualwalker + ff])

                    prob=abs(expon-int(expon))
                    if random<prob:
                        for ff in np.arange(0,(18*watersperwalker),1):
                            birthlist.append(coords[actualwalker+ff])
                birthlist=np.array(birthlist)
                return birthlist, weights
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
        coords = np.array(initialcage * numWalkers)/0.529177#*1.01
        initialcage = np.reshape(initialcage, (len(initialcage) // 18, 18, 3))/0.529177
        zeroinenergy=(hex_pot.getpot(initialcage) / 627.5094740631 / 4.5563e-6)
        print(zeroinenergy)
        weights=np.ones(numWalkers)
        count=0
        fullEnergies=[]
        fullWalkers=[]
        for i in np.arange(0,numTimeSteps):
            count+=1
            if count %100 ==0:
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
        biglist=[]
        fullEnergies=np.array(fullEnergies)
        fullEnergies=fullEnergies-zeroinenergy
        fullWalkers=np.array(fullWalkers)
        plt.plot(fullEnergies[:,0],fullEnergies[:,1])
        if bunchofjobs==False:
            plt.show()
            print(np.average(fullEnergies[int(len(fullEnergies)/2):-1,1]))
            exit()
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




#OO bend wfns
#Zero in E?
#energy ranges
#atom atom distances

