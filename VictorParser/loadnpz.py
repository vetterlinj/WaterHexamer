import os,glob
import numpy as np
import matplotlib.pyplot as plt
def loadnpz(path):
    npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths.sort()
    print(npzFilePaths)
    return npzFilePaths

def concatenatenpz(path, metadata=False):
    '''
    Takes a path to a folder of npz files and concatenates them, returning the concatenated matrix, the weights, and metadata
    :param path: (string) path to folder of npz files
    :return:
    '''

    weights=[]
    metadata=[]
    tracing=[]
    filepaths=loadnpz(path)
    dimdata = np.load(filepaths[0])
    initializer=0
    for file in filepaths:
        data = np.load(file)
        # make a large matrix
        if initializer!=0:
            wavefunctions=np.concatenate((wavefunctions,data['coords']))
        else:
            wavefunctions=data['coords']
            initializer+=1
        #make a weights matrix

        reshape=data['weights']
        reshape=reshape.T
        weights=np.concatenate((weights,reshape))
        # print(len(reshape))
        #print(reshape)
        if metadata==True:
        #keep track of metadata matrix?
            filemetadata=[data['NumWalkers'],data['InitialWalkers'],data['time']]
            metadata.append(filemetadata)
            tracing.append(data['Size'])
    weights = np.array(weights)
    if metadata==True:
        metadata=np.array(metadata)
        tracing=np.array(tracing)
        return wavefunctions, weights, metadata, tracing
    else:
        return wavefunctions, weights

def concatenateseparatesimulationnpz(path):
    '''
    Takes a path to a folder of npz files and concatenates them, returning the concatenated matrix, the weights, and metadata
    :param path: (string) path to folder of npz files
    :return:
    '''

    filepaths=loadnpz(path)
    count=0
    coordsdict={}
    weightsdict={}
    numberoffiles=len(filepaths)
    print(len(filepaths))

    #for file in filepaths:
    if path =='UpdatedPrism/Parsed/h2o5_d2o/D2/':
        wavefunctions = np.empty([0, 18, 3], float)
        metadata = []
        tracing = []
        count += 1
        weights = []
        for a in np.arange(0, 10):
            data = np.load(filepaths[int(a)])
            # make a large matrix
            wavefunctions = np.concatenate((wavefunctions, data['coords']))
            # make a weights matrix

            reshape = data['weights']
            reshape = reshape.T
            weights = np.concatenate((weights, reshape))
        weights = np.array(weights)
        coordsdict[f'1'] = wavefunctions
        weightsdict[f'1'] = weights
        # print(len(reshape))
        # print(reshape)
        for orange in np.arange(0, ((numberoffiles-10) / 17)):
            wavefunctions = np.empty([0, 18, 3], float)
            print(((numberoffiles-10) / 17)+2)
            weights = []
            metadata = []
            tracing = []
            count += 1
            for a in np.arange(0, 17):
                data = np.load(filepaths[int(a+10 + orange * 17)])
                # make a large matrix
                wavefunctions = np.concatenate((wavefunctions, data['coords']))
                # make a weights matrix

                reshape = data['weights']
                reshape = reshape.T
                weights = np.concatenate((weights, reshape))
            # print(len(reshape))
            # print(reshape)

            weights = np.array(weights)
            coordsdict[f'{count}'] = wavefunctions
            weightsdict[f'{count}'] = weights
    else:
        for orange in np.arange(0,numberoffiles/17):
            wavefunctions = np.empty([0, 18, 3], float)
            metadata = []
            tracing = []
            weights = []
            count+=1
            for a in np.arange(0,17):
                data = np.load(filepaths[int(a+orange*17)])
            # make a large matrix
                wavefunctions=np.concatenate((wavefunctions,data['coords']))
            #make a weights matrix

                reshape=data['weights']
                reshape=reshape.T
                weights=np.concatenate((weights,reshape))
            # print(len(reshape))
            #print(reshape)

            weights = np.array(weights)
            coordsdict[f'{count}']=wavefunctions
            weightsdict[f'{count}']=weights
            print(count*17)
    return coordsdict,weightsdict
def concatenateseparatenpz(path):
    '''
    Takes a path to a folder of npz files and concatenates them, returning the concatenated matrix, the weights, and metadata
    :param path: (string) path to folder of npz files
    :return:
    '''

    filepaths=loadnpz(path)
    count=0
    coordsdict={}
    weightsdict={}
    numberoffiles=len(filepaths)
    print(len(filepaths))
    for file in filepaths:
        wavefunctions = np.empty([0, 18, 3], float)
        weights = []
        metadata = []
        tracing = []
        count+=1
        data = np.load(file)
        # make a large matrix
        wavefunctions=np.concatenate((wavefunctions,data['coords']))
        #make a weights matrix

        reshape=data['weights']
        reshape=reshape.T
        weights=np.concatenate((weights,reshape))
        # print(len(reshape))
        #print(reshape)

        weights = np.array(weights)
        coordsdict[f'{count}']=wavefunctions
        weightsdict[f'{count}']=weights
    return coordsdict,weightsdict

def writeMeAnXYZFile(walkercoords, filename, deuteriumPosition):
    coordsfile=open(filename,"w")
    coordsfile.write("18\nRandom Prism Structure\n")
    walkercoords=walkercoords*0.529177
    for oranges in np.arange(0,6):
        oranges=oranges*3
        if oranges==deuteriumPosition:
            coordsfile.write(str("O     "+str(walkercoords[oranges,0])+"     "+str(walkercoords[oranges,1])+"     "+str(walkercoords[oranges,2])+"\n"))
            coordsfile.write(str(
                "D     " + str(walkercoords[oranges+1, 0]) + "     " + str(walkercoords[oranges+1, 1]) + "     " + str(
                    walkercoords[oranges+1, 2]) + "\n"))
            coordsfile.write(str(
                "D     " + str(walkercoords[oranges+2, 0]) + "     " + str(walkercoords[oranges+2, 1]) + "     " + str(
                    walkercoords[oranges+2, 2]) + "\n"))
        else:
            coordsfile.write(str("O     "+str(walkercoords[oranges,0])+"     "+str(walkercoords[oranges,1])+"     "+str(walkercoords[oranges,2])+"\n"))
            coordsfile.write(str(
                "H     " + str(walkercoords[oranges+1, 0]) + "     " + str(walkercoords[oranges+1, 1]) + "     " + str(
                    walkercoords[oranges+1, 2]) + "\n"))
            coordsfile.write(str(
                "H     " + str(walkercoords[oranges+2, 0]) + "     " + str(walkercoords[oranges+2, 1]) + "     " + str(
                    walkercoords[oranges+2, 2]) + "\n"))
    coordsfile.close()
# writeMeAnXYZFile(np.load("FixingThingsWithRyan/DeuterMillion/initial_prism_walkers.npy")[0],"prismcheck.xyz",22)
# writeMeAnXYZFile(np.load("FixingThingsWithRyan/frozenCage/AAD/npzFiles/frozenHexAAD1_0Data.npz")['coords'][36:54,:],"strangeCage.xyz",22)
# writeMeAnXYZFile(np.load("FixingThingsWithRyan/frozenCage/ADD/npzFiles/frozenHexADD1_0Data.npz")['coords'][0:18,:]/0.529177,"strangeCage.xyz",22)
# writeMeAnXYZFile(np.load("FixingThingsWithRyan/frozenCage/AD/npzFiles/frozenHexAD1_0Data.npz")['coords'][18:36,:]/0.529177,"strangeCage.xyz",22)
for key in np.load("test/walkers_1000.npz").keys():
    print(key)
argonism = np.argmax(np.load("test/walkers_1000.npz")['weights'])
writeMeAnXYZFile(np.load("test/walkers_1000.npz")['coords'][argonism]/0.529177,"strangerCage.xyz",22)
# fullEnergies=np.load("test/energies.npy")
# plt.plot(np.arange(0,len(fullEnergies)),fullEnergies/4.5563e-6)
# plt.xlabel("time step")
# plt.ylabel("ZPE (cm-1)")
# plt.show()
# exit()
# #627.5094740631
# fullEnergies=np.load("FixingThingsWithRyan/frozenCage/AAD/npzFiles/frozenHexAAD1_0Data.npz")['walkers']
# plt.plot(fullEnergies[:,0],fullEnergies[:,1]/18, label="Dtau=1")
# fullEnergies=np.load("FixingThingsWithRyan/frozenCage/AAD/npzFiles/frozenHexAAD10_0Data.npz")['walkers']
# plt.plot(fullEnergies[:,0],fullEnergies[:,1]/18, label="Dtau=10")
# plt.legend()
# plt.show()
        #     print(np.average(fullEnergies[int(len(fullEnergies)/2):-1,1]))
        #     exit()