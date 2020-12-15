import numpy as np
import argparse
import matplotlib.pyplot as plt
import sys
import os,glob
import matplotlib.pyplot as plt
import h2o_pot
from pyvibdmc import potential_manager as pm
pot_dir = 'legacy_mbpol/'  # this directory is part of the one you copied that is outside of pyvibdmc.
py_file = 'callmbpol.py'
pot_func = 'call_a_cpot'  # def water_pot(cds) in h2o_potential.py
# The Potential object assumes you have already made a .so file and can successfully call it from Python
hex_pot = pm.Potential(potential_function=pot_func,
                         python_file=py_file,
                         potential_directory=pot_dir,
                         num_cores=6)
amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
def doPropMakeHist(path,mer,identity):
    timesteps=[1,10]
    for i in timesteps:
        fullpath=path+f"/{i}/"
        npzFilePaths = glob.glob(os.path.join(fullpath, '*.npz'))
        for file in npzFilePaths:
            data=np.load(file)
            coords=data['coords']
            reshapedcoords = np.reshape(coords, (len(coords) // (mer*3), (mer*3), 3))
            if mer==6:
                initialenergies = hex_pot.getpot(reshapedcoords) / 627.5094740631 /(4.5563e-6)
            elif mer ==1:
                initialenergies=h2o_pot.calc_hoh_pot(reshapedcoords, len(coords) // 3)/ (4.5563e-6)
            # energies = np.add.reduceat(listenergies, np.arange(0, len(listenergies), 1))
            # print(listenergies)
            if mer==6:
                for atom in np.arange(0, len(coords)/18):
                    actualcoord=atom*18
                    countmove = 0
                    for actualatom in np.arange(0,3):

                        if countmove == 0:
                            # Oxygen
                            m = 15.9994 * amutoelectron
                        # elif countmove %3 == 1:
                        else:
                            # Hydrogen
                            m = 1.00794 * amutoelectron

                        # elif countmove %3 == 2:
                        #     # Deuterium
                        #     m = 2.014102 * amutoelectron
                        sigma = np.sqrt(i / m)
                        randomCoord = np.zeros((3))
                        for coordinate in np.arange(0, 3):
                            randomCoord[coordinate] += np.random.normal(0, sigma)
                        coords[int(actualcoord+actualatom)] += randomCoord
                        countmove += 1
            if mer ==1:
                countmove = 0
                for atom in np.arange(0, len(coords)):
                    countmove += 1
                    if countmove%3 == 0:
                            # Oxygen
                        m = 15.9994 * amutoelectron
                        # elif countmove %3 == 1:
                    else:
                            # Hydrogen
                        m = 1.00794 * amutoelectron

                        # elif countmove %3 == 2:
                        #     # Deuterium
                        #     m = 2.014102 * amutoelectron
                    sigma = np.sqrt(i / m)
                    randomCoord = np.zeros((3))
                    for coordinate in np.arange(0, 3):
                        randomCoord[coordinate] += np.random.normal(0, sigma)
                    coords[atom] += randomCoord
            reshapedcoords = np.reshape(coords, (len(coords) // (mer * 3), (mer * 3), 3))
            if mer ==6:
                finalenergies = hex_pot.getpot(reshapedcoords) / 627.5094740631 / (4.5563e-6)
            elif mer==1:
                finalenergies=h2o_pot.calc_hoh_pot(reshapedcoords, len(coords) // 3)/ (4.5563e-6)
            diffenergies=finalenergies-initialenergies
            print(np.average(diffenergies))

            amp, xx = np.histogram(diffenergies,range=(-5000, 5000), bins=100, density=True)
            #
            xx = 0.5 * (xx[1:] + xx[:-1])
            if mer==6:
                plt.plot(xx, amp, label=f'{identity} Frozen Hex with dtau={i}')
            elif mer==1:
                plt.plot(xx, amp, label=f'H2O with dtau={i}')
            plt.xlabel("Efinal-Einitial(cm-1)")
            plt.ylabel("Count")
            plt.title(f'All Wavefunctions')
            # plt.show()

            plt.legend()

            if mer==6:
                plt.savefig(f'Results/{identity}{i}.png')
            elif mer==1:
                plt.savefig(f'Results/H2O{i}.png')
            # plt.clf()
            if mer==1 and i==10:
                print('hi')
                mer=6
                data = np.load('PotExpl/HOH/cage/walkers_20000.npz')
                coords = data['coords']
                weights=data['weights']
                initialenergies = hex_pot.getpot(coords) / 627.5094740631 / (4.5563e-6)
                print(np.average(initialenergies, weights=weights))
                # exit()
                print(data)
                coords=np.reshape(coords,(len(coords)*18,3))
                countmove = 0
                for atom in np.arange(0, len(coords)):
                    if countmove%3 == 0:
                                # Oxygen
                            m = 15.9994 * amutoelectron
                            # elif countmove %3 == 1:
                    else:
                                # Hydrogen
                            m = 1.00794 * amutoelectron
                            # elif countmove %3 == 2:
                            #     # Deuterium
                            #     m = 2.014102 * amutoelectron
                    sigma = np.sqrt(i / m)
                    randomCoord = np.zeros((3))
                    for coordinate in np.arange(0, 3):
                        randomCoord[coordinate] += np.random.normal(0, sigma)
                    coords[atom] += randomCoord
                    countmove += 1
                reshapedcoords = np.reshape(coords, (len(coords) // (6 * 3), (6 * 3), 3))
                finalenergies = hex_pot.getpot(reshapedcoords) / 627.5094740631 / (4.5563e-6)
                print(np.average(finalenergies, weights=weights))
                diffenergies = finalenergies - initialenergies
                print(np.average(diffenergies))
                amp, xx = np.histogram(diffenergies, range=(-40000, 40000), bins=100, density=True,weights=weights)
                #
                xx = 0.5 * (xx[1:] + xx[:-1])
                plt.plot(xx, amp, label=f'Hex with dtau=10')
                plt.xlabel("Efinal-Einitial(cm-1)")
                plt.ylabel("Count")
                plt.title(f'All Wavefunctions')
                # plt.show()
                plt.legend()
                plt.savefig(f'Results/Hex.png')
            # plt.clf()
        # print(npzFilePaths)
doPropMakeHist('frozenCage/AAD',6,"AAD")
# doPropMakeHist('frozenCage/ADD',6,"ADD2")
doPropMakeHist('PotExpl/HOH',1,"H2O")