import numpy as np

import argparse
import matplotlib.pyplot as plt
import sys
import h2o_pot
import os
# from VictorParser.Constants import *
# import sys
# sys.path.insert(0, 'FixingThingsWithRyan')
for weirdsimthingy in np.arange(0,1):
    amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
    massH = 1.008 * amutoelectron
    massO = 16 * amutoelectron
    m = (massH * massO) / (massH + massO)
    # omega=1
    omega = 3000 * (4.5563e-6)
    k = m * (omega ** 2)
    dimensions = 1
    numWalkers = 1000
    numTimeSteps = 1000
    deltaTau = 10
    sigma = np.sqrt(deltaTau / m)
    alpha = 1 / (2 * deltaTau)
    numberperwalker=18
    bunchofjobs=False
    ContWeights=True
    debug=False
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
        numTimeSteps = int(args.list[1])/deltaTau
        namedeltaTau = str(deltaTau).replace(".", "point")
        sigma = np.sqrt(deltaTau / m)
        alpha = 1 / (2 * deltaTau)
    for i in np.arange(0,5):
        if bunchofjobs == True:
            filename = "Results/Multiple/Harmonic/" + fnameExtension + f"_{namedeltaTau}_{i}"
            print(filename)
            resultsfilename = "Results/Multiple/Harmonic/npzFiles/" + fnameExtension + f"_{namedeltaTau}_{i}"
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
            # filename="Results/Multiple/Harmonic/"+fnameExtension+f"_{namedeltaTau}_{i}"
            # print(filename)
            # resultsfilename="Results/Multiple/Harmonic/npzFiles/"+fnameExtension+f"_{namedeltaTau}_{i}"
        # sigma=np.sqrt(deltaTau/m)
        # V=h2o_pot.calc_hoh_pot
        #first is array, second is length of the array
        #mass for each coord
        def randommovement(coords,dimensions,sigma):
            for walker in np.arange(0,len(coords)):
                coords[walker]+=np.random.normal(0,sigma)
            return coords

        def getDemEnergies(coords):
            listenergies=0.5*k*(np.square(coords))
            energies = np.add.reduceat(listenergies, np.arange(0, len(listenergies), numberperwalker))
            return energies
        if ContWeights==False:
            def getVref(energies,alpha,weights,numWalkers,coords):
                energies=getDemEnergies(coords)
                Vref = np.average(energies) - (alpha / numWalkers * (len(coords)/numberperwalker - numWalkers))
                return Vref
            def birthandDeath(coords,energies,alpha,numWalkers,weights,deltaTau):
                averageEnergy=np.average(energies)
                # print('averageEnergy:')
                # print(averageEnergy)
                Vref = np.average(energies) - (alpha / numWalkers * (len(coords)/numberperwalker - numWalkers))

                # print(len(coords[:,0]))
                # print()
                birthlist=[]
                deathlist=[]
                for walker in np.arange(0,int(len(coords)/numberperwalker)):
                    random=np.random.random()
                    if energies[walker]<Vref:
                        prob=np.exp(-deltaTau*(energies[walker]-Vref))-1
                        if random<prob:
                            actualwalker=walker*numberperwalker
                            for ff in np.arange(0,numberperwalker,1):
                                birthlist.append(coords[actualwalker+ff])
                    elif energies[walker]>Vref:
                        prob=1-np.exp(-deltaTau*(energies[walker]-Vref))
                        # print('probability')
                        # print(prob)
                        # print(np.exp(-deltaTau*(energies[walker]-Vref)))
                        # exit()
                        if random<prob:
                            actualwalker=walker*numberperwalker
                            for ff in np.arange(0, numberperwalker, 1):
                                deathlist.append(actualwalker+ff)
                    else:
                        print('I am confuse destroyer of work')
                birthlist=np.array(birthlist)
                deathlist=np.array(deathlist)
                deletedcoords=np.delete(coords,deathlist,0)
                deletedcoords=np.array(deletedcoords)
                if debug==True:
                    print("Number Killed: " + str(len(deathlist) / numberperwalker))
                if len(birthlist)==0:
                    print('empty')
                    birthedcoords=deletedcoords
                else:
                    if debug == True:
                        print(len(birthlist) / numberperwalker)
                    birthedcoords=np.append(deletedcoords,birthlist,axis=0)
                return birthedcoords, weights
        elif ContWeights==True:
            def getVref(energies,alpha,weights,numWalkers,coords):
                energies=getDemEnergies(coords)
                Vref = np.average(energies, weights=weights, axis=0) - (alpha * np.log(np.sum(weights) / numWalkers))
                return Vref
            def birthandDeath(coords, energies, alpha, numWalkers,weights,deltaTau):
                averageEnergy = np.average(energies, weights=weights)
                # print('averageEnergy:')
                # print(averageEnergy)
                # Vref = averageEnergy - (alpha / numWalkers * (len(coords) - numWalkers))
                Vref = averageEnergy - (alpha * np.log(np.sum(weights) / numWalkers))
                # print(len(coords[:,0]))
                # print()
                birthlist = []
                deathlist = []
                deathweights=[]
                deathcount=0
                for walker in np.arange(0, int(len(coords)/numberperwalker)):
                    expon=np.exp(-deltaTau * (energies[walker] - Vref))
                    weights[walker]*=expon
                    if weights[walker]<(0.01):

                        actualwalker = walker * numberperwalker
                        for ff in np.arange(0, numberperwalker, 1):
                            deathlist.append(actualwalker+ff)
                        deathweights.append(walker)
                        deathcount+=1
                deathlist = np.array(deathlist)
                deathweights=np.array(deathweights)
                deletedcoords = np.delete(coords, deathlist, 0)
                deletedcoords = np.array(deletedcoords)
                deletedweights = np.delete(weights,deathweights,0)
                if len(weights)-len(deathweights)!=len(deletedweights):
                    print('issue')
                appendlist = []
                if deathcount>0:
                    for neededwalker in np.arange(0,deathcount):
                        walker=np.argmax(deletedweights)
                        actualwalker = walker * numberperwalker
                        for ff in np.arange(0, numberperwalker, 1):
                            birthlist.append(deletedcoords[actualwalker+ff])
                        deletedweights[walker]/=2
                        # deletedweights.append(deletedweights[walker])
                        appendlist.append(deletedweights[walker])
                deletedweights=np.array(deletedweights)
                birthlist = np.array(birthlist)
                appendlist=np.array(appendlist)
                if debug == True:
                    print("Number Killed: " + str(len(deathlist) / numberperwalker))
                if len(birthlist) == 0:
                    print('empty')
                    birthedcoords = deletedcoords
                    birthedweights=deletedweights
                else:
                    if debug == True:
                        print(len(birthlist) / numberperwalker)
                    birthedcoords = np.append(deletedcoords, birthlist, axis=0)
                    birthedweights=np.append(deletedweights,appendlist)
                return birthedcoords,birthedweights
        angstr=0.529177
        # startingGeo=np.array([[0.9578400,0.0000000,0.0000000],
        #                      [-0.2399535,0.9272970,0.0000000],
        #              [0.0000000,0.0000000,0.0000000]])/angstr * 1.01
        coords=np.zeros(numWalkers*numberperwalker)
        weights=np.ones(numWalkers)
        # print(len(coords[:,0]))
        count=0
        fullEnergies=[]
        for i in np.arange(0,numTimeSteps):
            count+=1
            if count %100 ==0:
                print(count)
            coords=randommovement(coords,dimensions,sigma)
            energies=getDemEnergies(coords)
            Vref = getVref(energies, alpha, weights, numWalkers, coords)
            fullEnergies.append([i,Vref/(numberperwalker*4.5563e-6)])
            coords,weights=birthandDeath(coords, energies,alpha,numWalkers,weights,deltaTau)
            # Vref = getVref(energies, alpha, weights, numWalkers, coords)
            # fullEnergies.append([i, Vref / (4.5563e-6)])

            # print(count)
            # print(len(coords))
        # coords = randommovement(coords, dimensions, sigma)
        # energies = getDemEnergies(coords)
        # Vref=getVref(energies,alpha,weights,numWalkers,coords)
        # fullEnergies.append([numTimeSteps, Vref / (4.5563e-6)])
        fullEnergies=np.array(fullEnergies)
        # plt.errorbar(fullEnergies[:,0],fullEnergies[:,1],yerr=fullEnergies[:,2])
        plt.plot(fullEnergies[:,0],fullEnergies[:,1])
        if bunchofjobs==False:
            plt.show()
            print(np.average(fullEnergies[int(len(fullEnergies)/2):-1,1]))
            exit()
        plt.savefig(filename)
        np.savez(resultsfilename+"Data",energies=fullEnergies,coords=coords,iwalkers=numWalkers,deltatau=deltaTau,timesteps=numTimeSteps,weights=weights)
        averageEnergy=np.average(fullEnergies[int(len(fullEnergies)/2):-1,1])
        stdEnergy=np.std(fullEnergies[int(len(fullEnergies)/2):-1,1])
        energieslist.append(averageEnergy)
        resultsFile = open(f"{filename}Energy.txt", 'w')
        resultsFile.write(str(averageEnergy) + '\n')
        resultsFile.write(str(stdEnergy))
        resultsFile.close()






