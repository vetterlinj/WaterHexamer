import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *
coords, weights, metadata=concatenatenpz('PythonData/')
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
amp,xx=np.histogram(roh1[0,:],bins=50,range=(1.25,2.5),density=True, weights=weights.T)
xx = 0.5*(xx[1:] + xx[:-1])
plt.plot(xx,amp)
plt.show()


#amp, xx = np.histogram(...)
#bin centers: xx = 0.5*(xx[1:] + xx[:-1])
#numpy.linalg.norm(vector,axis=1)
#set area under curve to 1, set density=True






"""
#filenumbers=np.arange(1,18)
#a set of the filenumbers so I can loop through the files
filenumbers=[1]
#a set of waters so I can loop through each water in each Walker
waters=np.arange(0,6)
print(waters)
print(filenumbers)
#glob module to get filenames
#os.listdir can list all the files in a directory, then pull .npz
#function in pulldataset.py,
#np.concatenate
#numpy transpose :,0-:,1
for filenumber in filenumbers:
    #takes each file and loads it
    data = np.load(f'PythonData/sample{filenumber}.npz')
    print(data['time'])
    #Takes the coordinate matrix from the dataset
    coords=data['coords']
    #Takes the number of Walkers from the dataset
    number=data['NumWalkers']
    #Takes the weights matrix (each entry corresponds to a Walker)
    weights=data['weights']
    walkers=np.arange(0,number)
    print(walkers)
    #Loops over the Walkers in this file
    for walker in walkers:
        weightofwalker=weights[walker]
        #Loops over each of the 6 waters in each Hexamer Walker
        for water in waters:
            water=water*3
            layer=coords[walker,:,:]
            watercoords=layer[water]
            h1coords=layer[water+1]
            h2coords=layer[water+2]
            h1sub=(watercoords-h1coords)**2
            roh1=np.sqrt(np.sum(h1sub))
            h2sub = (watercoords - h2coords) ** 2
            roh2 = np.sqrt(np.sum(h2sub))
        #do xy things
    # roh2=np.sqrt()
    # roh3=np.sqrt()
#for i in range
"""
