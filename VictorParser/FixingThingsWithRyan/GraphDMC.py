import numpy as np
import matplotlib.pyplot as plt
from VictorParser.Constants import *
import os,glob
def plotthispls(location,label,numberofeach):
    path=location+"/npzFiles/"
    npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths.sort()
    print(npzFilePaths)

    count=0
    Xval=[]
    Yval=[]
    Ystd=[]
    for file in npzFilePaths:
        data=np.load(file)
        if count ==(numberofeach-1):
            count-=numberofeach
        if count==0:
            groupedY =[]
            Xval.append(data['deltatau'])
        count +=1
        fullEnergies=data['energies']
        # print(np.average(fullEnergies[1000:2000,1]))
        averageEnergy = np.average(fullEnergies[int(len(fullEnergies) / 2):-1, 1])
        # averageEnergy = np.average(fullEnergies[9950:-1, 1])
        groupedY.append(averageEnergy)
        if count ==4:
            Yval.append(np.average(groupedY))
            Ystd.append(np.std(groupedY))
    sort=np.argsort(Xval)
    Xval=np.array(Xval)[sort]
    Yval=np.array(Yval)[sort]
    Ystd=np.array(Ystd)[sort]
    plt.errorbar(Xval,Yval,Ystd,label=label)
    plt.plot(np.arange(11), np.repeat(4638, 11), 'k',label="Minimum of Potential Surface")
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
#plotthispls('10',"10000 Timesteps, deltaTau=5")
#plotthispls('1',"1000 Timesteps, deltaTau=1")
#plotthispls('2',"2000 Timesteps, deltaTau=1")
#plotOverTime('10',"10K walkers over time")
#plotthispls('T',"10K timesteps, 8k Walkers")
#plotthispls('0',"10K timesteps, 8k Walkers")
#plotthispls("8Kwalkers","10K timesteps, 8k Walkers")
plotthispls("8kWalkers10Sims","10K timesteps, 8k Walkers",10)

plt.ylabel("Energy (Wavenumbers)")
#plt.xlabel("Walkers")
plt.xlabel("Time step size")
plt.legend(loc='top right')
plt.show()


# for key, value in data.items():
#     print(key)