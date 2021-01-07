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
                         num_cores=2)
# oranges=np.random.random((100,18,3))
# print(hex_pot.getpot(oranges))
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
    numWalkers = 1000
    numTimeSteps = 1000
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
            filename = f"Results/Multiple/{foldername}/" + fnameExtension  # + f"_{namedeltaTau}_{i}"
            # print(filename)
            resultsfilename = f"Results/Multiple/{foldername}/npzFiles/" + fnameExtension  # + f"_{namedeltaTau}_{i}"
            # alpha = 1 / (2 * deltaTau)
        # sigma=np.sqrt(deltaTau/m)
        # V=h2o_pot.calc_hoh_pot
        #first is array, second is length of the array
        #mass for each coord
        def randommovement(coords,dimensions,deltaTau):
            #check
            countmove = 0
            eqdegrees=104.5080029
            eqangle=eqdegrees/360*2*np.pi
            amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
            mO =1/( 15.9994 * amutoelectron)
            mH =1/( 1.00794 * amutoelectron)
            mOH=(1/mO)*(1/mH)/((1/mO)+(1/mH))
            OHsigma=np.sqrt(deltaTau/mOH)
            mnormal= 1.00794 * amutoelectron
            normalsigma=np.sqrt(deltaTau / mnormal)
            masssymm=mH+mO*(1+np.cos(eqangle))
            sigmasymm = np.sqrt(deltaTau * masssymm)
            massasymm=mH+mO*(1-np.cos(eqangle))
            sigmaasymm = np.sqrt(deltaTau * massasymm)
            for atom in np.arange(0, len(coords)):
                countmove += 1
                # if countmove % 3 == 0:
                #     # Oxygen
                #     if atomicMass==True:
                #         m = 15.9994 * amutoelectron
                #     else:
                #         m =99.76/100*29148.94642+0.048/100*30979.52128+0.20/100*32810.46286
                # else:
                #     # Hydrogen
                #     if atomicMass == True:
                #         m = 1.00794 * amutoelectron
                #     else:
                #         m=99.985/100*1836.152697+3670.483031/100*(100-99.985)
                if countmove % 3 == 0:
                    # Oxygen
                    m = 15.9994 * amutoelectron
                # elif countmove %3 == 1:
                else:
                    # Hydrogen
                    m = 1.00794 * amutoelectron
                # elif countmove %3 == 2:
                #     # Deuterium
                #     m = 2.014102 * amutoelectron
                sigma = np.sqrt(deltaTau / m)
                randomCoord = np.zeros((dimensions))
                for coordinate in np.arange(0, dimensions):
                    randomCoord[coordinate] += np.random.normal(0, sigma)
                coords[atom] += randomCoord
            return coords


        '''for molecule in np.arange(0, len(coords)/3):
            dOH=np.random.normal(0,OHsigma)
            s=np.random.normal(0, sigmasymm)
            a=np.random.normal(0, sigmaasymm)
            r1=(s+a)/np.sqrt(2)
            r2 = (s - a) / np.sqrt(2)
            randomCoord = np.zeros((dimensions))
            # randomCoord[0] += r1
            randomCoord[0] += dOH
            coords[np.int(molecule*3)]+=randomCoord'''

        '''randomCoord2 = np.zeros((dimensions))
        randomCoord2[0]-=r2*np.cos((180-eqdegrees)/360*2*np.pi)
        randomCoord2[1] += r2 * np.sin((180 - eqdegrees) / 360 * 2 * np.pi)
        coords[np.int(molecule * 3)+1] += randomCoord2'''
        if CarringtonPot==False:
            def getDemEnergies(coords,watersperwalker):
                #check
                #################
                reshapedcoords = np.reshape(coords, (len(coords) // 3, 3, 3))
                # listenergies = h2o_pot.calc_hoh_pot(reshapedcoords, len(coords) // 3)
                if TryUncorrPot==True:
                    listenergies = h2o_uncorr_pot.calc_hoh_pot(reshapedcoords, len(coords) // 3)
                else:
                    listenergies = h2o_pot.calc_hoh_pot(reshapedcoords, len(coords) // 3)
                #numwalkersx18x3
                #hex_pot.getpot(coords)
                energies = np.add.reduceat(listenergies, np.arange(0, len(listenergies), watersperwalker))
                return energies

        if CarringtonPot==True:
            def getDemEnergies(coords,watersperwalker):
                #Carrington
                #make things work
                #ajtoJtoHartree
                aJconv=(10**(-18)*(2.293712*10**(17)))
                #Angstroms/Bohr
                AinvConv=0.529177
                frr = 8.428 * aJconv * AinvConv ** 2
                frrr = -51.91 * aJconv * AinvConv ** 3
                frrrr = 248.7 * aJconv * AinvConv ** 4
                ftt = 0.6990 * aJconv
                fttt = -0.9186 * aJconv
                ftttt = -0.1 * aJconv
                frrprime =primecup* -0.101 * aJconv * AinvConv ** 2
                frrrprime =primecup* 0.645 * aJconv * AinvConv ** 3
                frt = 0.219 * aJconv * AinvConv
                frtt = -0.314 * aJconv * AinvConv
                frrt = 1.341 * aJconv * AinvConv**2
                frrprimet =primecup* 0.414 * aJconv * AinvConv**2
                frrtt = -2.0 * aJconv * AinvConv ** 2
                #radians
                #can check frequencies
                Re=0.9575/AinvConv
                Anglee=104.51
                V=[]
                for molecule in np.arange(len(coords)/3):
                    actualcoord=int(molecule*3)
                    diffs1=coords[actualcoord+1,:] - coords[actualcoord+2,:]
                    diffs2=coords[ actualcoord,:] - coords[ actualcoord+2,:]
                    #diffs3=coords[:, 0] - coords[:, 1]
                    dist1 = np.linalg.norm(diffs1, axis=0)
                    dist2 = np.linalg.norm(diffs2, axis=0)
                    #dist3=np.linalg.norm(diffs3, axis=0)

                    cosine_angle = np.dot(diffs1, diffs2) / (np.linalg.norm(diffs1) * np.linalg.norm(diffs2))
                    angle = np.degrees(np.arccos(cosine_angle))


                    theta=(angle-Anglee)/360*2*np.pi
                    r1=dist1-Re
                    r2=dist2-Re
                    V12=0.5*frr*(r1**2+r2**2)+0.5*(ftt*theta**2)+frrprime*r1*r2+frt*theta*(r1+r2)
                    V3=(1/6)*frrr*(r1**3+r2**3)+(1/6)*fttt*theta**3+0.5*frtt*(theta**2)*(r1+r2)
                    V4=0.1*frrrprime*(r1**2*r2+r1*r2**2)
                    V5=0.5*frrt*theta*(r1**2+r2**2)+frrprimet*r1*r2*theta
                    V6=(1/24)*frrrr*(r1**4+r2**4)+(1/24)*ftttt*theta**4
                    V7=(1/4)*frrtt*(r1**2+r2**2)*theta**2
                    V.append(V12+V3+V4+V5+V6+V7)
                return V
        if ContWeights==False:
            def getVref(energies,alpha,weights,numWalkers,coords,watersperwalker):
                #if debut==True:
                    #print(len(coords) / 3/watersperwalker)
                Vref = np.average(energies) - (alpha / numWalkers * (len(coords)/(3*watersperwalker) - numWalkers))
                #print(np.average(energies))
                #print(alpha / numWalkers * (len(coords)/(3*watersperwalker) - numWalkers))
                #print(alpha)
                #print(numWalkers)
                #print((len(coords)/(3*watersperwalker) - numWalkers))
                if len(coords)/(3*watersperwalker)!= len(energies):
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
                for walker in np.arange(0,int(len(coords)/(3*watersperwalker))):
                    random=np.random.random()
                    # if energies[walker]<Vref:
                    actualwalker = walker * (3 * watersperwalker)
                    expon=np.exp(-deltaTau*(energies[walker]-Vref))
                    if np.int(expon)>0:
                        for neededwalker in np.arange(0,np.int(expon)):
                            for ff in np.arange(0, (3 * watersperwalker), 1):
                                birthlist.append(coords[actualwalker + ff])

                    prob=abs(expon-int(expon))
                    if random<prob:
                        for ff in np.arange(0,(3*watersperwalker),1):
                            birthlist.append(coords[actualwalker+ff])
                        #birth more walkers eg 5 for 5.8 with then prob as if .8
                    # elif energies[walker]>Vref:
                    #     prob=1-np.exp(-deltaTau*(energies[walker]-Vref))
                    #     # print('probability')
                    #     # print(prob)
                    #     # print(np.exp(-deltaTau*(energies[walker]-Vref)))
                    #     # exit()
                    #     if random<prob:
                    #         actualwalker=walker*(3*watersperwalker)
                    #         for ff in np.arange(0, (3*watersperwalker), 1):
                    #             deathlist.append(actualwalker+ff)
                    # else:
                    #     print('I am confuse destroyer of work')
                birthlist=np.array(birthlist)
                # deathlist=np.array(deathlist)
                # if debut==True:
                #     print("Number Killed: "+str(len(deathlist)/(3*watersperwalker)))
                # # deletedcoords=np.delete(coords,deathlist,0)
                # # deletedcoords=np.array(deletedcoords)
                # # if len(birthlist)==0:
                #     #print('empty')
                #     birthedcoords=deletedcoords
                # else:
                #     if debut == True:
                #         print(len(birthlist)/(3*watersperwalker))
                #     birthedcoords=np.append(deletedcoords,birthlist,axis=0)
                return birthlist, weights
        elif ContWeights==True:
            def getVref(energies,alpha,weights,numWalkers,coords,watersperwalker):
                energies=getDemEnergies(coords,watersperwalker)
                Vref = np.average(energies, weights=weights) - (alpha * np.log(np.sum(weights) / numWalkers))
                return Vref
            def birthandDeath(coords, energies, alpha, numWalkers,weights,deltaTau,watersperwalker,Vref):
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
                walkeratbeginning = len(coords/3)
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
        #middlenumber=[-0.2399535,0.9272970,0.0000000]
        startingGeo=np.array([[0.9578400,0.0000000,0.0000000],
                             [-0.2399535,0.9272970,0.0000000],
                     [0.0000000,0.0000000,0.0000000]])/angstr*1.01
        # perfectGeo=np.array([[-np.cos(75.49/360*2*np.pi)*1.8094134854689452,np.sin(75.49/360*2*np.pi)*1.8094134854689452,0.0000000],
        #              [1.8094134854689452,0.0000000,0.0000000],
        #              [0.0000000,0.0000000,0.0000000]])
        # print(np.average(quarticEnergies(perfectGeo,1))/(4.5563e-6))
        # exit()
        ###################
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
                print(len(coords)/3)
                biglist=[]
                # for molecule in np.arange(0, len(coords), 3):
                #     actualcoord = molecule
                #     actualcoord = np.int(actualcoord)
                #     # if coords[actualcoord][1]!=0:
                #     #     print('ahhh')
                #     actualcoord += 1
                #     print((coords[(actualcoord, 1)]))
                #     print((coords[(actualcoord, 1)] / np.abs(coords[(actualcoord, 0)])))
                #     invinput = (coords[(actualcoord, 1)] / np.abs(coords[(actualcoord, 0)]))
                #     degrees = np.arctan(invinput) * 360 / 2 / np.pi
                #     print(degrees)
                #     # print(invinput)
                #     biglist.append(180 - (np.arctan(invinput) * 360 / (2 * np.pi)))
                # print(np.average(biglist))
            if i==0:
                energies=getDemEnergies(coords,watersperwalker)
                #print(np.average(energies)/(4.5563e-6))
                Vref = getVref(energies, alpha, weights, numWalkers, coords, watersperwalker)
            coords=randommovement(coords,dimensions,deltaTau)
            energies=getDemEnergies(coords,watersperwalker)
            # Vref=getVref(energies,alpha,weights,numWalkers,coords,watersperwalker)
            # print(Vref / (4.5563e-6) / 6)
            # fullEnergies.append([i,Vref/(watersperwalker*4.5563e-6)])
            coords,weights=birthandDeath(coords, energies,alpha,numWalkers,weights,deltaTau,watersperwalker,Vref)
            energies = getDemEnergies(coords,watersperwalker)
            Vref = getVref(energies, alpha, weights, numWalkers, coords,watersperwalker)
            #print(Vref / (watersperwalker*4.5563e-6))
            fullEnergies.append([i,Vref/(watersperwalker*4.5563e-6)])

            # print(len(coords))

        # coords = randommovement(coords, dimensions, deltaTau)
        biglist=[]
        # for molecule in np.arange(0, len(coords), 3):
        #     actualcoord = molecule
        #     actualcoord = np.int(actualcoord)
        #     # if coords[actualcoord][1]!=0:
        #     #     print('ahhh')
        #     actualcoord += 1
        #     # print((coords[(actualcoord, 1)]))
        #     # print((coords[(actualcoord, 1)] / np.abs(coords[(actualcoord, 0)])))
        #     invinput = (coords[(actualcoord, 1)] / np.abs(coords[(actualcoord, 0)]))
        #     degrees = np.arctan(invinput) * 360 / 2 / np.pi
        #     print(degrees)
        #     # print(invinput)
        #     biglist.append(180 - (np.arctan(invinput) * 360 / (2 * np.pi)))
        # print(np.average(biglist))
        # exit()
        # energies = getDemEnergies(coords,watersperwalker)
        # Vref=getVref(energies,alpha,weights,numWalkers,coords,watersperwalker)
        # fullEnergies.append([numTimeSteps, Vref / (watersperwalker*4.5563e-6)])
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






