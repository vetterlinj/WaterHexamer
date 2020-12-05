import os,glob
import numpy as np

def loadnpz(path):
    npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths.sort()
    print(npzFilePaths)
    return npzFilePaths

def concatenatenpz(path, metadata):
    '''
    Takes a path to a folder of npz files and concatenates them, returning the concatenated matrix, the weights, and metadata
    :param path: (string) path to folder of npz files
    :return:
    '''
    wavefunctions=np.empty([0,18,3], float)
    weights=[]
    metadata=[]
    tracing=[]
    filepaths=loadnpz(path)
    for file in filepaths:
        data = np.load(file)
        # make a large matrix
        wavefunctions=np.concatenate((wavefunctions,data['coords']))
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
        return wavefunctions,weights

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
writeMeAnXYZFile(np.load("FixingThingsWithRyan/DeuterMillion/initial_prism_walkers.npy")[0],"prismcheck.xyz",22)