import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *

def checkdistance(walkercoords, particleOne, particleTwo):
    return np.sqrt(np.sum(np.square(walkercoords[particleOne] - walkercoords[particleTwo]))) * 0.529177
def OODistance(coords,waterone,watertwo,weights):
    onecoords=coords[:,waterone*3,:]
    twocoords=coords[:,watertwo*3,:]
    oranges=onecoords-twocoords
    oranges=np.square(oranges)
    oranges=oranges[:,0]+oranges[:,1]+oranges[:,2]
    oranges=np.sqrt(oranges)
    oranges=oranges*weights
    #*0.529177
    return np.sum(oranges)
    #return oranges


path='d2o6_prism/PythonData/d2o6_prism.npz'
dataname='d2o6_prism'
def bigOne(path,dataname,cageorprism):
    # file = np.load(path+dataname+'.npz')
    # coords=file['coords']
    # weights=file['weights']
    numbers=[]
    count=0
    coordsdict, weightsdict = concatenateseparatenpz(path)
    if cageorprism == 'prism':
        distances = [[0, 1], [1, 2], [1, 3], [2, 3], [3, 4], [4, 5], [4, 0], [5, 0], [5, 2]]
    elif cageorprism == 'cage':
        distances = [[0, 1], [0, 3], [0, 4], [1, 2], [1, 5], [2, 3], [2, 4], [3, 5]]
    results = {}
    actualResults={}
    actualErrors={}
    for number,coords in coordsdict.items():
        count+=1
    #OODistance(coords,0,1,weights)

        numbers.append(number)
        weights=weightsdict[f'{number}']
        sumweights=np.sum(weights)
        for i in distances:
            results[f'{number} {i} distance']=OODistance(coords,i[0],i[1],weights)/sumweights

    for i in distances:
        sum=[]
        for labels in numbers:
            sum.append(results[f'{labels} {i} distance'])
        actualResults[f'{i} distance'] = np.average(sum)
        actualErrors[f'{i} distance std']=np.std(sum)

    resultsFile = open('Results/OODistances/' + f"{dataname}_OODistances.txt", 'w')
    # if allH == True:
    #     resultsFile.write('Results for homogeneous:' + "\n")
    # elif mostlyD == True:
    #     resultsFile.write('Hydrogen Position is: ' + str(deuterium) + "\n")
    # else:
    #     resultsFile.write('Deuterium Position is: ' + str(deuterium) + "\n")
    for name, value in actualResults.items():
        resultsFile.write(name + "\n")
        resultsFile.write(str(value) + "\n")
        resultsFile.write(str(actualErrors[f'{name} std'])+"\n")
    resultsFile.close()
    #Plotting:
    # amp, xx = np.histogram(OODistance(coords,0,1), bins=75, range=(2, 4), density=True, weights=weights)
    # xx = 0.5 * (xx[1:] + xx[:-1])
    # plt.plot(xx, amp, label='H1')
    # plt.title(f'Water')
    # plt.savefig(f'Results/OOTest.png')
    # plt.clf()
#10 and 17?
#stdev: block average the 5 then compute stdev of the second


# for simulation in np.arange(1, 7):
#     path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
#     # path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
#     # path = f'h2o6_prism/PythonData/'
#     dataname = f'h2o5_d2o_prism_{simulation}'
#     mostlyD = False
#     allH=False
#     bigOne(path,dataname)
# for simulation in np.arange(1, 6):
#     #path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
#     path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
#     # path = f'h2o6_prism/PythonData/'
#     dataname = f'h2o_d2o5_prism_{simulation}'
#     mostlyD = True
#     allH=False
#     bigOne(path,dataname)
#
# path = f'h2o6_prism/PythonData/'
# dataname = 'h2o6_prism'
# mostlyD = False
# allH=True
# simulation=0
# bigOne(path,dataname)
# path = f'd2o6_prism/PythonData/'
# dataname = 'd2o6_prism'
# mostlyD = False
# allH=True
# bigOne(path,dataname)

# for simulation in np.arange(2, 3):
#     path=f'h2o5_d2o_prismPythonData/Uncategorized/minimum{simulation}_wfns/PythonData/'
#     # path = f'h2o_d2o5_prism/minimum{simulation}_wfns/PythonData/'
#     # path = f'h2o6_prism/PythonData/'
#     dataname = f'h2o5_d2o_prism_{simulation}'
#     mostlyD = False
#     allH=False
#     bigOne(path,dataname)

path="MarkOutput/wavefunctions/"
bigOne(path,'MarkSimulation','cage')

