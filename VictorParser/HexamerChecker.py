import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *
#data=np.load('NickFiles/VictorData/h2o6_book/SortedWithoutProblems.npz')
# data=np.load('FixingThingsWithRyan/EnsembleSize/16k/npzFiles/16k_3point0_0Data.npz')
data=np.load("FixingThingsWithRyan/frozenCage/ADD/npzFiles/frozenHexADD1_0Data.npz")
print(data['iwalkers'])
#1k_10_0Data.npz
coords=data['coords']
weights=data['weights']
coords=np.reshape(coords,(len(coords)//18,18,3))/0.529177
# exit()
# problems=data['problems']
# print(problems)
oxygen=[coords[:,0,:],coords[:,3,:],coords[:,6,:],coords[:,9,:],coords[:,12,:],coords[:,15,:]]
#Oxygen is (6,walkers,3)
h1=[coords[:,1,:],coords[:,4,:],coords[:,7,:],coords[:,10,:],coords[:,13,:],coords[:,16,:]]
h2=[coords[:,2,:],coords[:,5,:],coords[:,8,:],coords[:,11,:],coords[:,14,:],coords[:,17,:]]
h1=np.array(h1)
h2=np.array(h2)
oxygen=np.array(oxygen)
roh1=np.square(oxygen-h1)
roh1=np.sqrt(np.sum(roh1,2))
#roh is (6,walkers)
roh2=np.square(oxygen-h2)
roh2=np.sqrt(np.sum(roh2,2))
# for a in np.arange(0,6):
for a in np.arange(1,2):

    amp,xx=np.histogram(roh1[a,:],bins=58,range=(1,3),density=True)
    #, weights=weights.T
    xx = 0.5*(xx[1:] + xx[:-1])
    amp2,xx2=np.histogram(roh2[a,:],bins=58,range=(1,3),density=True)
    xx2 = 0.5*(xx2[1:] + xx2[:-1])

    # checkfile = np.loadtxt("NickFiles/VictorData/h2o6_book/book_roh_check.dat")
    # checkfile = np.array(checkfile)
    # checkamp=checkfile[:,1]
    # checkxx=checkfile[:,0]

    plt.plot(xx,amp,label='H1')
    plt.plot(xx2,amp2, label='H2')
    # plt.plot(checkxx,checkamp,label='Victor')
    plt.title(f'Water{a}')
    plt.legend()
    b=a+1
    plt.show()
    # plt.savefig(f'NickFiles/VictorData/h2o6_book/SortedOxygen{b}.png')
    print()
#amp, xx = np.histogram(...)
#bin centers: xx = 0.5*(xx[1:] + xx[:-1])
#numpy.linalg.norm(vector,axis=1)
#set area under curve to 1, set density=True





