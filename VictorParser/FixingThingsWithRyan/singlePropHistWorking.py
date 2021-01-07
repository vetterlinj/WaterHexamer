import numpy as np
import argparse
import matplotlib.pyplot as plt
import sys
import os,glob
import matplotlib.pyplot as plt
import h2o_pot
from pyvibdmc import potential_manager as pm
from VictorParser.loadnpz import *
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
        for file in np.arange(0,1):
            # data=np.load(file)
            # coords=data['coords']
            coords, weights=concatenatenpz(fullpath)

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
            icoords = np.array(initialcage * (len(coords)//18)) / 0.529177
            # diffcoords=coords-icoords


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
                    if atom %10000 ==0:
                        print('10000')
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
                coords = data['coords']/0.529177
                weights=data['weights']
                initialenergies = hex_pot.getpot(coords) / 627.5094740631 / (4.5563e-6)/6
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
                finalenergies = hex_pot.getpot(reshapedcoords) / 627.5094740631 / (4.5563e-6)/6
                print(np.average(finalenergies))
                diffenergies = finalenergies - initialenergies
                print(np.average(diffenergies))
                amp, xx = np.histogram(diffenergies, range=(-5000, 5000), bins=100, density=True)
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