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
    # amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
    # massH = 1.008 * amutoelectron
    # massO = 16 * amutoelectron
    # m = (massH * massO) / (massH + massO)
    # omega=1
    # omega = 3000 * (4.5563e-6)
    # k = m * (omega ** 2)
    dimensions = 3
    watersperwalker=6
    numWalkers = 2000
    numTimeSteps = 1000
    deltaTau = 1
    # sigma = np.sqrt(deltaTau / m)
    alpha = 1 / (2 * deltaTau)
    bunchofjobs=True
    ContWeights=True
    debut=False
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
        # sigma = np.sqrt(deltaTau / m)
        alpha = 1 / (2 * deltaTau)
    for i in np.arange(0,5):
        if bunchofjobs == True:
            if ContWeights==True:
                foldername="ContHex"
            elif ContWeights==False:
                foldername="DiscHex"
            filename = f"Results/Multiple/{foldername}/" + fnameExtension + f"_{namedeltaTau}_{i}"
            print(filename)
            resultsfilename = f"Results/Multiple/{foldername}/npzFiles/" + fnameExtension + f"_{namedeltaTau}_{i}"
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
        def randommovement(coords,dimensions,deltaTau):
            #check
            countmove = 0
            amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
            for atom in np.arange(0, len(coords)):
                countmove += 1
                if countmove % 3 == 0:
                    # Oxygen
                    m = 15.9994 * amutoelectron
                else:
                    # Hydrogen
                    m = 1.00794 * amutoelectron
                sigma = np.sqrt(deltaTau / m)
                randomCoord = np.zeros((dimensions))
                for coordinate in np.arange(0, dimensions):
                    randomCoord[coordinate] += np.random.normal(0, sigma)
                coords[atom] += randomCoord
            return coords

        def getDemEnergies(coords,watersperwalker):
            #check
            reshapedcoords = np.reshape(coords, (len(coords) // 3, 3, 3))
            listenergies = h2o_pot.calc_hoh_pot(reshapedcoords, len(coords) // 3)
            energies = np.add.reduceat(listenergies, np.arange(0, len(listenergies), watersperwalker))
            return energies
        if ContWeights==False:
            def getVref(energies,alpha,weights,numWalkers,coords,watersperwalker):
                if debut==True:
                    print(len(coords) / 3/watersperwalker)
                Vref = np.average(energies) - (alpha / numWalkers * (len(coords)/(3*watersperwalker) - numWalkers))
                return Vref
            def birthandDeath(coords,energies,alpha,numWalkers,weights,deltaTau,watersperwalker):
                #check
                averageEnergy=np.average(energies)
                # print('averageEnergy:')
                # print(averageEnergy)
                Vref = np.average(energies) - (alpha / numWalkers * (len(coords)/(3*watersperwalker) - numWalkers))

                # print(len(coords[:,0]))
                # print()
                birthlist=[]
                deathlist=[]
                for walker in np.arange(0,int(len(coords)/(3*watersperwalker))):
                    random=np.random.random()
                    if energies[walker]<Vref:
                        prob=np.exp(-deltaTau*(energies[walker]-Vref))-1
                        if random<prob:
                            actualwalker=walker*(3*watersperwalker)
                            for ff in np.arange(0,(3*watersperwalker),1):
                                birthlist.append(coords[actualwalker+ff])
                    elif energies[walker]>Vref:
                        prob=1-np.exp(-deltaTau*(energies[walker]-Vref))
                        # print('probability')
                        # print(prob)
                        # print(np.exp(-deltaTau*(energies[walker]-Vref)))
                        # exit()
                        if random<prob:
                            actualwalker=walker*(3*watersperwalker)
                            for ff in np.arange(0, (3*watersperwalker), 1):
                                deathlist.append(actualwalker+ff)
                    else:
                        print('I am confuse destroyer of work')
                birthlist=np.array(birthlist)
                deathlist=np.array(deathlist)
                if debut==True:
                    print("Number Killed: "+str(len(deathlist)/(3*watersperwalker)))
                deletedcoords=np.delete(coords,deathlist,0)
                deletedcoords=np.array(deletedcoords)
                if len(birthlist)==0:
                    #print('empty')
                    birthedcoords=deletedcoords
                else:
                    if debut == True:
                        print(len(birthlist)/(3*watersperwalker))
                    birthedcoords=np.append(deletedcoords,birthlist,axis=0)
                return birthedcoords, weights
        elif ContWeights==True:
            def getVref(energies,alpha,weights,numWalkers,coords,watersperwalker):
                energies=getDemEnergies(coords,watersperwalker)
                Vref = np.average(energies, weights=weights) - (alpha * np.log(np.sum(weights) / numWalkers))
                return Vref
            def birthandDeath(coords, energies, alpha, numWalkers,weights,deltaTau,watersperwalker):
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
                for walker in np.arange(0, int(len(coords)/(3*watersperwalker))):
                    expon=np.exp(-deltaTau * (energies[walker] - Vref))
                    weights[walker]*=expon
                    if weights[walker]<(0.001):
                        actualwalker = walker * (3*watersperwalker)
                        for ff in np.arange(0, (3*watersperwalker), 1):
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
                        actualwalker = walker * (3*watersperwalker)
                        for gg in np.arange(0, (3*watersperwalker), 1):
                            birthlist.append(deletedcoords[actualwalker+gg])
                        deletedweights[walker]/=2
                        # deletedweights.append(deletedweights[walker])
                        appendlist.append(deletedweights[walker])
                deletedweights=np.array(deletedweights)
                birthlist = np.array(birthlist)
                appendlist=np.array(appendlist)
                if debut == True:
                    print("Number Killed: " + str(len(deathlist) / (3*watersperwalker)))
                if len(birthlist) == 0:
                    print('empty')
                    birthedcoords = deletedcoords
                    birthedweights=deletedweights
                else:
                    if debut == True:
                        print(len(birthlist) / (3*watersperwalker))
                    birthedcoords = np.append(deletedcoords, birthlist, axis=0)
                    birthedweights=np.append(deletedweights,appendlist)
                return birthedcoords,birthedweights
        angstr=0.529177
        startingGeo=np.array([[0.9578400,0.0000000,0.0000000],
                             [-0.2399535,0.9272970,0.0000000],
                     [0.0000000,0.0000000,0.0000000]])/angstr * 1.01
        coords=np.zeros((numWalkers*(3*watersperwalker),dimensions))
        weights=np.ones(numWalkers)
        for i in np.arange(0,numWalkers*watersperwalker):
            coords[i*3]+= startingGeo[0]
            coords[i*3+1]+= startingGeo[1]
            coords[i*3+2]+=startingGeo[2]
        count=0
        fullEnergies=[]
        for i in np.arange(0,numTimeSteps):
            count+=1
            if count %100 ==0:
                print(count)
                print(Vref / (4.5563e-6) / (watersperwalker))
            coords=randommovement(coords,dimensions,deltaTau)
            energies=getDemEnergies(coords,watersperwalker)
            Vref=getVref(energies,alpha,weights,numWalkers,coords,watersperwalker)
            # print(Vref / (4.5563e-6) / 6)
            fullEnergies.append([i,Vref/(watersperwalker*4.5563e-6)])
            coords,weights=birthandDeath(coords, energies,alpha,numWalkers,weights,deltaTau,watersperwalker)
            # energies = getDemEnergies(coords,watersperwalker)
            # Vref = getVref(energies, alpha, weights, numWalkers, coords,watersperwalker)
            # fullEnergies.append([i, Vref / (4.5563e-6)])

            # print(len(coords))
        coords = randommovement(coords, dimensions, deltaTau)
        energies = getDemEnergies(coords,watersperwalker)
        Vref=getVref(energies,alpha,weights,numWalkers,coords,watersperwalker)
        fullEnergies.append([numTimeSteps, Vref / (watersperwalker*4.5563e-6)])
        fullEnergies=np.array(fullEnergies)
        # plt.errorbar(fullEnergies[:,0],fullEnergies[:,1],yerr=fullEnergies[:,2])
        plt.plot(fullEnergies[:,0],fullEnergies[:,1])
        if bunchofjobs==False:
            plt.show()
            print(np.average(fullEnergies[int(len(fullEnergies)/2):-1,1]))
            exit()
        plt.savefig(filename)
        np.savez(resultsfilename+"Data",energies=fullEnergies,coords=coords,iwalkers=numWalkers,deltatau=deltaTau,timesteps=numTimeSteps,weights=weights,watersperwalker=watersperwalker)
        averageEnergy=np.average(fullEnergies[int(len(fullEnergies)/2):-1,1])
        stdEnergy=np.std(fullEnergies[int(len(fullEnergies)/2):-1,1])
        energieslist.append(averageEnergy)
        resultsFile = open(f"{filename}Energy.txt", 'w')
        resultsFile.write(str(averageEnergy) + '\n')
        resultsFile.write(str(stdEnergy))
        resultsFile.close()






