import numpy as np
import matplotlib.pyplot as plt
from VictorParser.Constants import *
import os,glob
from matplotlib.pyplot import figure
from matplotlib.ticker import MaxNLocator
def plotthispls(location,label,numberofeach,xaxis):
    path=location+"/npzFiles/"
    # npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths.sort()
    print(npzFilePaths)
    if xaxis=='million':
        npyFilePaths = glob.glob(os.path.join(path, '*.npy'))
        npyFilePaths.sort()
        print(npyFilePaths)
        for file in npyFilePaths:
            data = np.load(file)
            data = np.array(data)
            averager = []
            # for a in np.arange(len(data)/6,len(data)):
            #     averager.append(data[(a)])
            millionnumber=np.average(data[1000:len(data)]) / 6 / 4.5563e-6
            print(np.average(data[2000:len(data)]) / 6 / 4.5563e-6)
            print(np.std(data[2000:len(data)]) / 6 / 4.5563e-6)
            print(np.average(data[2000:len(data)]) / 4.5563e-6)
            print(np.std(data[2000:len(data)]) / 4.5563e-6)
            plt.plot(np.arange(11), np.repeat(millionnumber, 11), 'k', label="Dtau=10 Million Number after 6000 time steps",color='purple')
            return
    secondcount=0
    count=0
    Xval=[]
    Yval=[]
    Ystd=[]
    Yref=0
    refcount=0
    for file in npzFilePaths:
        data=np.load(file)
        if count ==(numberofeach-1):
            count-=numberofeach
        if count==0:
            if xaxis=='deltaTau' or xaxis=='deltaTauRel' or xaxis=='deltaTauH' or xaxis=="deltaTauD" or xaxis=="deltaTauE":
                groupedY =[]
                Xval.append(data['deltatau'])
            elif xaxis=='walkers':
                groupedY=[]
                Xval.append(data['iwalkers'])
            elif xaxis=='size':
                groupedY=[]
                if secondcount ==0:
                    multiplier=0.5
                elif secondcount ==1:
                    multiplier=1
                elif secondcount ==2:
                    multiplier=2
                Xval.append(multiplier)
                secondcount+=1
        count +=1
        fullEnergies=data['energies']
        # print(np.average(fullEnergies[1000:2000,1]))
        averageEnergy = np.average(fullEnergies[int(len(fullEnergies) / 2):-1, 1])
        # averageEnergy = np.average(fullEnergies[9950:-1, 1])
        groupedY.append(averageEnergy)
        if count ==(numberofeach-1):
            if refcount==0 and xaxis=='deltaTauRel':
                refcount+=1
                Yref=np.average(groupedY)
            moleculesperwalker=1
            if xaxis=='deltaTauH':
                moleculesperwalker=6
            if xaxis=='deltaTauE':
                moleculesperwalker=18
            if xaxis=='deltaTauD':
                moleculesperwalker=2
            print((np.average(groupedY)-Yref)/moleculesperwalker)
            Yval.append((np.average(groupedY)-Yref)/moleculesperwalker)
            Ystd.append(np.std(groupedY)/moleculesperwalker)
    sort=np.argsort(Xval)
    Xval=np.array(Xval)[sort]
    Yval=np.array(Yval)[sort]
    Ystd=np.array(Ystd)[sort]
    plt.errorbar(Xval,Yval,Ystd,label=label)
    plt.title(f"{numberofeach} Replicates")


def plotOverTime(location,label):
    path=f"10kSmall/"
    npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths.sort()
    print(npzFilePaths)

    count=0
    Xval=[]
    Yval=[]
    for file in npzFilePaths:
        data=np.load(file)
        if count==0:
            fullEnergies=data['energies']
            # print(np.average(fullEnergies[1000:2000,1]))
            for number in np.arange(8000,10001,1):
                print(fullEnergies[number,1])
                Xval.append(fullEnergies[number,0])
                Yval.append(fullEnergies[number, 1])
        #     if count ==4:
        #         Yval.append(np.average(groupedY))
        #         Ystd.append(np.std(groupedY))
        # sort=np.argsort(Xval)
        count += 1
    print(len(Xval))
    print(len(Yval))

    plt.plot(Xval, Yval, label=label)
    plt.ylim(4000,5000)
def monomerOHstretch():
    path='50kauContW/1and10/'
    npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths.sort()
    for file in npzFilePaths:
        data =np.load(file)
        for key, value in data.items():
            print(key, value)
        exit()
        coords = data['coords']
        weights = data['weights']
        oxygen=[]
        h1=[]
        h2=[]
        for walker in np.arange(0,len(coords)/3):
            actualcoord=walker*3
            oxygen = [coords[:, 0, :], coords[:, 3, :], coords[:, 6, :], coords[:, 9, :], coords[:, 12, :], coords[:, 15, :]]
            # Oxygen is (6,walkers,3)
            h1 = [coords[:, 1, :], coords[:, 4, :], coords[:, 7, :], coords[:, 10, :], coords[:, 13, :], coords[:, 16, :]]
            h2 = [coords[:, 2, :], coords[:, 5, :], coords[:, 8, :], coords[:, 11, :], coords[:, 14, :], coords[:, 17, :]]
            h1 = np.array(h1)
            h2 = np.array(h2)
            oxygen = np.array(oxygen)
            roh1 = np.square(oxygen - h1)
            roh1 = np.sqrt(np.sum(roh1, 2))
            # roh is (6,walkers)
            roh2 = np.square(oxygen - h2)
            roh2 = np.sqrt(np.sum(roh2, 2))
    for a in np.arange(0, 6):
        amp, xx = np.histogram(roh1[a, :], bins=58, range=(1, 3), density=True, weights=weights.T)
        xx = 0.5 * (xx[1:] + xx[:-1])
        amp2, xx2 = np.histogram(roh2[a, :], bins=58, range=(1, 3), density=True, weights=weights.T)
        xx2 = 0.5 * (xx2[1:] + xx2[:-1])

        # checkfile = np.loadtxt("NickFiles/VictorData/h2o6_book/book_roh_check.dat")
        # checkfile = np.array(checkfile)
        # checkamp=checkfile[:,1]
        # checkxx=checkfile[:,0]

        plt.plot(xx, amp, label='H1')
        plt.plot(xx2, amp2, label='H2')
        # plt.plot(checkxx,checkamp,label='Victor')
        plt.title(f'Water{a}')
        plt.legend()
        b = a + 1
        plt.show()
        plt.clf()
        exit()
#plotthispls('10',"10000 Timesteps, deltaTau=5")
#plotthispls('1',"1000 Timesteps, deltaTau=1")
#plotthispls('2',"2000 Timesteps, deltaTau=1")
#plotOverTime('10',"10K walkers over time")
#plotthispls('T',"10K timesteps, 8k Walkers")
#plotthispls('0',"10K timesteps, 8k Walkers")
#plotthispls("8Kwalkers","10K timesteps, 8k Walkers", 5,)
#Original Time Step Study
# plotthispls("8kWalkers10Sims","10K timesteps, 8k Walkers",10,'deltaTau')
# plotthispls("50kau","50k AU total time, 8k Walkers",5,'deltaTau')
# plotthispls("50kauContW","50k AU total time, 8k Walkers, cont. weighting",5,'deltaTau')
# xrange=11
# plt.xlabel("Time step size")
# plotthispls('EnsembleSize3au',"3 AU time step, 50k AU total time",5,"walkers")
# plotthispls('EnsembleSize5p5au',"5.5 AU time step, 50k AU total time",5,"walkers")
# plotthispls('EnsembleSize10au',"10 AU time step, 100k AU total time",5,"walkers")
# xrange=28001
# plt.xlabel("Walkers")
# plotthispls('HSize1',"Hydrogen, 8k Walkers, 1 AU 50k total time",5,"deltaTau")
# plotthispls('HSize2',"Deuterium, 8k Walkers, 1 AU 50k total time",5,"deltaTau")
# plotthispls('HSizeHalf',"Halfdrogen, 8k Walkers, 1 AU 50k total time",5,"deltaTau")
# plt.xlabel("DeltaTau")

# plotthispls("ReWalk", "Monomer 8k Walkers",5,"deltaTau")
# plotthispls('Di1k',"Dimer 1k Walkers",5,"deltaTauD")
# plotthispls('Hex1k',"Hexamer 1k Walkers",5,"deltaTauH")
# plotthispls('SmallerCutoff',"Hexamer 0.001 cutoff 1k Walkers",5,"deltaTauH")
# plotthispls('DiscreteHex',"Hexamer Discrete weighting with 1k Walkers",5,"deltaTauH")
# # plotthispls('Hex8k',"8k Walkers",5,"deltaTauH")
# plt.xlabel("DeltaTau")
# xrange=11

# plotthispls("HarmD", "Discrete 1k Walkers",5,"deltaTau")
# plotthispls("HarmC", "Continuous 1k Walkers",5,"deltaTau")
# plotthispls("HarmCHex", "Hexamer Continuous 1k Walkers",5,"deltaTauH")
# plotthispls("HarmDHex", "Hexamer Discrete 1k Walkers",5,"deltaTauH")
# plotthispls("HarmD18", "18-mer Discrete 1k Walkers",5,"deltaTauE")
# plt.xlabel("DeltaTau")
# xrange=11

# plotthispls('DiscreteHex',"Hexamer Discrete weighting with 1k Walkers",5,"deltaTauH")

# plotthispls('NewHexDisc',"Discrete weighting Hexamer with 1k Walkers",5,"deltaTauH")
# plotthispls('NewHexCont',"Continuous weighting Hexamer with 1k Walkers",5,"deltaTauH")
# plotthispls('ContHex3K',"Continuous weighting Hexamer with 3k Walkers",5,"deltaTau")
# plotthispls('ContHex5K',"Continuous weighting Hexamer with 5k Walkers",5,"deltaTau")
# plotthispls('ContHex10K',"Continuous weighting Hexamer with 10k Walkers",5,"deltaTau")
# plotthispls("ReWalk", "Monomer 8k Walkers",5,"deltaTau")
# plt.xlabel("DeltaTau")
# xrange=11

# plotthispls('MillionTau1',"Million Walker Hexamer",5,"million")
# exit()

# annesx=[1,2,4,6,8,10]
# annesy=[4638.013643,4636.841567,4640.912251,4634.310842,4630.756066,4625.998072]
# annesstv=[0.857867151,1.731900076,0.8240529069,2.987696314,1.41147454,2.237955771]
# plt.errorbar(annesx,annesy,annesstv,label="Anne's Calcs, 20K walkers")
#
# plotthispls('NewCont20',"C weighting Hexamer 20k Walkers",5,"deltaTau")
# plotthispls('NewCont10',"Continuous weighting Hexamer with 10k Walkers",5,"deltaTau")
# plotthispls('NewCont5',"Continuous weighting Hexamer with 5k Walkers",5,"deltaTau")
# plotthispls('NewCont3',"Continuous weighting Hexamer with 3k Walkers",5,"deltaTau")
# plotthispls('NewCont2',"Continuous weighting Hexamer with 2k Walkers",5,"deltaTau")

# plotthispls('NewDesc20',"D weighting Hexamer 20k Walkers",5,"deltaTau")
#plotthispls('NewDesc2',"Discrete weighting Hexamer with 2k Walkers",5,"deltaTau")


# plotthispls('C24K',"C weighting Monomer with 24k Walkers",4,"deltaTau")
# plotthispls('D24K',"D weighting Monomer with 24k Walkers",4,"walkers")
# plotthispls('NewDisc/Mon28K',"NewDesc",5,'deltaTau')
# plotthispls("NewDisc/Hex8k","Disc Hexamer 8k walkers",5,'deltaTau')
# plotthispls('NewDisc/Mon8Total',"Monomer8k",5,'deltaTau')

#EnsembleSizeWeird
# plotthispls('NewDisc/Mon28K',"28kNew",5,'deltaTau')
# plotthispls('EnsembleSize/4k',"4k",5,'deltaTau')
# plotthispls('EnsembleSize/8k',"8k",5,'deltaTau')
# plotthispls('EnsembleSize/12k',"12k",5,'deltaTau')
# plotthispls('EnsembleSize/16k',"16k",5,'deltaTau')
# plotthispls('EnsembleSize/20k',"20k",5,'deltaTau')
# plotthispls('EnsembleSize/24k',"24k",5,'deltaTau')
# plotthispls('EnsembleSize/28k',"28k",5,'deltaTau')
plt.xlabel("DeltaTau")
xrange=11
plt.plot(np.arange(xrange), np.repeat(4638, xrange), 'k',label="Minimum")

#plotthispls('Newer/MonD8k',"8k monomer",5,'deltaTau')
# plotthispls('Newer/NucMonD24k',"24k nuclear mass",5,'deltaTau')
# plotthispls('Newer/MonD28k',"24k atomic mass",5,'deltaTau')
# plotthispls('EnsembleSize/24k',"24k atomic mass",5,'deltaTau')


# plotthispls('Newer/MonWalkTau1',"Monomers deltaTau=1",5,'walkers')

# plotthispls('Newer/HexD30k',"30k hex",5,'deltaTau')
# plotthispls('Newer/HexD20k',"20k hex",5,'deltaTau')
#plotthispls('Newer/Million1tau',"Million Walker Hexamer",5,"million")
#plotthispls('Newer/Million2tau',"Million Walker Hexamer",5,"million")

# plotthispls('Newer/Alpha10_10k',"alpha=10, 10k walkers",5,'deltaTau')
plotthispls('Newer/Alpha10_20k',"alpha=10, 20k walkers",5,'deltaTau')
plotthispls('Newer/Alpha1_20k',"alpha=1, 20k walkers",5,'deltaTau')
# plotthispls('Newer/Alpha1_10k',"alpha=1, 10k walkers",5,'deltaTau')
plotthispls('EnsembleSize/20k',"20k alpha varies",5,'deltaTau')


#Hexamer
# plotthispls("NewDisc/Hex8k","Disc Hexamer 8k walkers",5,'deltaTau')
# annesx=[1,6,8,10]
# annesy=[4631.6704,4634.310842,4630.756066,4625.998072]
# annesstv=[3.829429433,2.987696314,1.41147454,2.237955771]
# plt.errorbar(annesx,annesy,annesstv,label="Anne's Calcs, 20K walkers")
# plotthispls('NewCont20',"C weighting Hexamer 20k Walkers",5,"deltaTau")

# plt.xlabel("DeltaTau")
# xrange=11

#plotthispls('HSize',"8k walkers, 50k AU total time",5,'size')
#xrange=3




plt.ylabel("Energy per Molecule (Wavenumbers)")
# plt.xlabel("Walkers")
#plt.xlabel("Time step size")
plt.ylim(4625, 4645)
plt.yticks(np.arange(4626, 4644, 2))
# millionref=4631.355306
# plt.plot(np.arange(xrange), np.repeat(millionref, xrange), 'k',label="Million Hexamer dt=10",color="purple")
# milliontau1ref=4637.152974
# plt.plot(np.arange(xrange), np.repeat(milliontau1ref, xrange), 'k',label="Million Hexamer dt=1",color="blue")
plt.legend(loc='top right')

plt.show()
# monomerOHstretch()

# for key, value in data.items():
#     print(key)