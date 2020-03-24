import os,glob
import numpy as np

def loadnpz(path):
    npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths.sort()
    print(npzFilePaths)
    return npzFilePaths

def concatenatenpz(path):
    '''
    Takes a path to a folder of npz files and concatenates them, returning the concatenated matrix, the weights, and metadata
    :param path: (string) path to folder of npz files
    :return:
    '''
    wavefunctions=np.empty([0,18,3], float)
    weights=[]
    metadata=[]
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

        #keep track of metadata matrix?
        filemetadata=[data['NumWalkers'],data['InitialWalkers'],data['time']]
        metadata.append(filemetadata)
    weights = np.array(weights)
    metadata=np.array(metadata)
    return wavefunctions, weights, metadata