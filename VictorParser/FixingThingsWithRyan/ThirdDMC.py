import numpy as np
import argparse
import matplotlib.pyplot as plt
import h2o_pot
class DMC:
    def __init__(self,
                 fileName="unnamedFile",
                 weighting='disc',
                 numWalkers=10000,
                 numTimeSteps=6000,
                 numPerWalker=1,
                 deltaTau=1,
                 dimensions=3,
                 numReplicates=5
                 ):
        self.filename=fileName
        self.weighting=weighting
        self.dimensions = dimensions
        self.watersperwalker=numPerWalker
        self.numWalkers = numWalkers
        self.numTimeSteps = numTimeSteps
        self.deltaTau = deltaTau
        self.numReplicates=numReplicates

    def run(self):
        self.alpha = 1 / (2 * self.deltaTau)
        bunchofjobs = False
        ContWeights = False
        debut = False
        self.atomicMass = False
        print('running')
        filename = 'DMCResult'
        energieslist = []
        if bunchofjobs == True:
            parser = argparse.ArgumentParser()
            parser.add_argument('-s', '--string', help='<Required> File Name', required=True)
            parser.add_argument('-l', '--list', nargs='+', help='<Required> Set flag', required=True)
            args = parser.parse_args()
            fnameExtension = args.string

            self.numWalkers = int(args.list[0])
            self.deltaTau = int(args.list[2])
            self.alphaTau = int(args.list[3])
            self.numTimeSteps = int(args.list[1]) / self.deltaTau
            self.namedeltaTau = str(self.deltaTau).replace(".", "point")
            # sigma = np.sqrt(deltaTau / m)
            self.alpha = 1 / (2 * self.alphaTau)

        for i in np.arange(0, self.numReplicates):
            if bunchofjobs == True:
                if ContWeights == True:
                    foldername = "ContHex"
                elif ContWeights == False:
                    foldername = "DiscHex"
                filename = f"Results/Multiple/{foldername}/" + fnameExtension + f"_{self.namedeltaTau}_{i}"
                print(filename)
                resultsfilename = f"Results/Multiple/{foldername}/npzFiles/" + fnameExtension + f"_{self.namedeltaTau}_{i}"

            angstr = 0.529177
            startingGeo = np.array([[0.9578400, 0.0000000, 0.0000000],
                                    [-0.2399535, 0.9272970, 0.0000000],
                                    [0.0000000, 0.0000000, 0.0000000]]) / angstr * 1.01
            self.coords = np.zeros((self.numWalkers * (3 * self.watersperwalker), self.dimensions))
            self.weights = np.ones(self.numWalkers)
            for i in np.arange(0, self.numWalkers * self.watersperwalker):
                self.coords[i * 3] += startingGeo[0]
                self.coords[i * 3 + 1] += startingGeo[1]
                self.coords[i * 3 + 2] += startingGeo[2]
                ###Fix using Jacob's method
            count = 0
            fullEnergies = []
            for i in np.arange(0, self.numTimeSteps):
                count += 1
                if count % 100 == 0:
                    print(count)
                    print(self.Vref / (4.5563e-6) / (self.watersperwalker))
                if i == 0:
                    self.getDemEnergies()
                    self.getVref()
                self.randommovement()
                self.getDemEnergies()
                self.birthandDeath()
                self.getDemEnergies()###
                self.getVref()
                fullEnergies.append([i, self.Vref / (self.watersperwalker * 4.5563e-6)])
            fullEnergies = np.array(fullEnergies)
            plt.plot(fullEnergies[:, 0], fullEnergies[:, 1])
            if bunchofjobs == False:
                plt.show()
                print(np.average(fullEnergies[int(len(fullEnergies) / 2):-1, 1]))
                exit()
            plt.savefig(filename)
            np.savez(resultsfilename + "Data", energies=fullEnergies, coords=self.coords, iwalkers=self.numWalkers,
                     deltatau=self.deltaTau, timesteps=self.numTimeSteps, weights=self.weights, watersperwalker=self.watersperwalker)
            averageEnergy = np.average(fullEnergies[int(len(fullEnergies) / 2):-1, 1])
            stdEnergy = np.std(fullEnergies[int(len(fullEnergies) / 2):-1, 1])
            energieslist.append(averageEnergy)
            resultsFile = open(f"{filename}Energy.txt", 'w')
            resultsFile.write(str(averageEnergy) + '\n')
            resultsFile.write(str(stdEnergy))
            resultsFile.close()

    def randommovement(self):
        countmove = 0
        amutoelectron = 1.000000000000000000 / 6.02213670000e23 / 9.10938970000e-28
        for atom in np.arange(0, len(self.coords)):
        #Ryan loops
            countmove += 1
            if countmove % 3 == 0:
                # Oxygen
                if self.atomicMass == True:
                    m = 15.9994 * amutoelectron
                else:
                    m = 99.76 / 100 * 29148.94642 + 0.048 / 100 * 30979.52128 + 0.20 / 100 * 32810.46286
            else:
                # Hydrogen
                if self.atomicMass == True:
                    m = 1.00794 * amutoelectron
                else:
                    m = 99.985 / 100 * 1836.152697 + 3670.483031 / 100 * (100 - 99.985)
            sigma = np.sqrt(self.deltaTau / m)
            randomCoord = np.zeros((self.dimensions))
            for coordinate in np.arange(0, self.dimensions):
                randomCoord[coordinate] += np.random.normal(0, sigma)
            self.coords[atom] += randomCoord

    def getDemEnergies(self):
        reshapedcoords = np.reshape(self.coords, (len(self.coords) // 3, 3, 3))
        listenergies = h2o_pot.calc_hoh_pot(reshapedcoords, len(self.coords) // 3)
        self.energies = np.add.reduceat(listenergies, np.arange(0, len(listenergies), self.watersperwalker))

    def getVref(self):
        if self.weighting=='disc':
            self.Vref = np.average(self.energies) - (self.alpha / self.numWalkers * (len(self.coords) / (3 * self.watersperwalker) - self.numWalkers))
        elif self.weighting=='cont':
            self.energies = self.getDemEnergies()
            self.Vref = np.average(self.energies, weights=self.weights) - (self.alpha * np.log(np.sum(self.weights) / self.numWalkers))

    def birthandDeath(self):
        if self.weighting=='disc':
            self.averageEnergy = np.average(self.energies)
            birthlist = []
            deathlist = []
            for walker in np.arange(0, int(len(self.coords) / (3 * self.watersperwalker))):
            #Ryan loops (also cont. but they work similarly)
                random = np.random.random()
                # if energies[walker]<Vref:
                actualwalker = walker * (3 * self.watersperwalker)
                expon = np.exp(-self.deltaTau * (self.energies[walker] - self.Vref))
                if np.int(expon) > 0:
                    for neededwalker in np.arange(0, np.int(expon)):
                        for ff in np.arange(0, (3 * self.watersperwalker), 1):
                            birthlist.append(self.coords[actualwalker + ff])
                prob = abs(expon - int(expon))
                if random < prob:
                    for ff in np.arange(0, (3 * self.watersperwalker), 1):
                        birthlist.append(self.coords[actualwalker + ff])
            self.coords = np.array(birthlist)
        elif self.weighting=='cont':
            averageEnergy = np.average(self.energies, weights=self.weights)
            # print('averageEnergy:')
            # print(averageEnergy)
            # Vref = averageEnergy - (alpha / numWalkers * (len(coords) - numWalkers))
            Vref = averageEnergy - (self.alpha * np.log(np.sum(self.weights) / self.numWalkers))
            # print(len(coords[:,0]))
            # print()
            birthlist = []
            deathlist = []
            deathweights = []
            deathcount = 0
            for walker in np.arange(0, int(len(self.coords) / (3 * self.watersperwalker))):
                expon = np.exp(-self.deltaTau * (self.energies[walker] - Vref))
                self.weights[walker] *= expon
                if self.weights[walker] < (0.001):
                    actualwalker = walker * (3 * self.watersperwalker)
                    for ff in np.arange(0, (3 * self.watersperwalker), 1):
                        deathlist.append(actualwalker + ff)
                    deathweights.append(walker)
                    deathcount += 1
            deathlist = np.array(deathlist)
            deathweights = np.array(deathweights)
            deletedcoords = np.delete(self.coords, deathlist, 0)
            deletedcoords = np.array(deletedcoords)
            deletedweights = np.delete(self.weights, deathweights, 0)
            if len(self.weights) - len(deathweights) != len(deletedweights):
                print('issue')
            appendlist = []
            if deathcount > 0:
                for neededwalker in np.arange(0, deathcount):
                    walker = np.argmax(deletedweights)
                    actualwalker = walker * (3 * self.watersperwalker)
                    for gg in np.arange(0, (3 * self.watersperwalker), 1):
                        birthlist.append(deletedcoords[actualwalker + gg])
                    deletedweights[walker] /= 2
                    # deletedweights.append(deletedweights[walker])
                    appendlist.append(deletedweights[walker])
            deletedweights = np.array(deletedweights)
            birthlist = np.array(birthlist)
            appendlist = np.array(appendlist)
            if len(birthlist) == 0:
                print('empty')
                self.coords = deletedcoords
                self.weights = deletedweights
            else:
                if debut == True:
                    print(len(birthlist) / (3 * self.watersperwalker))
                self.coords = np.append(deletedcoords, birthlist, axis=0)
                self.weights = np.append(deletedweights, appendlist)

if __name__ == "__main__":
    dmcThing=DMC()
    dmcThing.run()







