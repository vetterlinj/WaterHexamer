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
    oranges=oranges#*weights#*0.529177
    #return np.sum(oranges)
    return oranges


def bigOne(path,dataname,cageorprism):
    resultslist = []
    realweights=[]
    for wfnnumber in np.arange(1,6,1):
        path= f"IlahieStuff/Hex150K/wavefunctions{wfnnumber}/"
        for filenumber in np.arange(1,20,1):
            file = np.load(path+dataname+str(filenumber)+'.npz')
            coords=file['coords']
            weights=file['weights']
            numbers=[]
            count=0
            # coordsdict, weightsdict = concatenateseparatenpz(path)
            if cageorprism == 'prism':
                distances = [[0, 1], [1, 2], [1, 3], [2, 3], [3, 4], [4, 5], [4, 0], [5, 0], [5, 2]]
            elif cageorprism == 'cage':
                distances = [[0, 1], [0, 3], [0, 4], [1, 2], [1, 5], [2, 3], [2, 4], [3, 5]]
            elif cageorprism =='OO':
                distances = [[0, 1], [0,2], [0, 3], [0, 4], [0,5], [1, 2], [1, 3],[1, 4], [1, 5], [2, 3], [2, 4],[2, 5],[3,4], [3, 5],[4,5]]
            results = {}
            actualResults={}
            actualErrors={}


            sumweights = np.sum(weights)
            # for i in distances:
            #     if i==[0, 1]:
            #         resultslist=OODistance(coords, i[0], i[1], weights) #/ sumweights
            #         resultslist=np.array(resultslist)
            #         realweights=weights
            #     else:
            for i in distances:
                newlist=OODistance(coords, i[0], i[1], weights) #/ sumweights
                newlist=np.array(newlist)
                resultslist=np.concatenate((resultslist, newlist))
                realweights=np.concatenate((realweights,weights))

    # for number,coords in coordsdict.items():
    #     count+=1
    # #OODistance(coords,0,1,weights)
    #
    #     numbers.append(number)
    #     weights=weightsdict[f'{number}']
    #     sumweights=np.sum(weights)
    #     for i in distances:
    #         #results[f'{number} {i} distance']=OODistance(coords,i[0],i[1],weights)/sumweights
    #         np.concatenate(resultslist,OODistance(coords,i[0],i[1],weights)/sumweights)
            #resultslist.append(OODistance(coords,i[0],i[1],weights)/sumweights)
    #Take each distance, add to list, weights should be len(distances)*walkers
    # for i in distances:
    #     sum=[]
    #     for labels in numbers:
    #         sum.append(results[f'{labels} {i} distance'])
    #     actualResults[f'{i} distance'] = np.average(sum)
    #     actualErrors[f'{i} distance std']=np.std(sum)

    # resultsFile = open('Results/OODistances/' + f"{dataname}_OODistances.txt", 'w')
    # if allH == True:
    #     resultsFile.write('Results for homogeneous:' + "\n")
    # elif mostlyD == True:
    #     resultsFile.write('Hydrogen Position is: ' + str(deuterium) + "\n")
    # else:
    #     resultsFile.write('Deuterium Position is: ' + str(deuterium) + "\n")
    # for name, value in actualResults.items():
    #     changedname=name.replace('0','D')
    #     changedname=changedname.replace('1','C')
    #     changedname = changedname.replace('2', 'E')
    #     changedname = changedname.replace('3', 'B')
    #     changedname = changedname.replace('4', 'F')
    #     changedname = changedname.replace('4', 'A')
    #     resultsFile.write(changedname + "\n")
    #     resultsFile.write(str(value) + "\n")
    #     resultsFile.write(str(actualErrors[f'{name} std'])+"\n")
    # resultsFile.close()
    #Plotting:

    amp, xx = np.histogram(resultslist, bins=60, range=(2, 7), density=True, weights=realweights)
    xx = 0.5 * (xx[1:] + xx[:-1])
    plt.plot(xx, amp, label='H1')
    plt.xlabel("rOO (Å)")
    plt.ylabel("Probability Amplitude")
    plt.title(f'All Wavefunctions')
    # plt.show()
    plt.savefig(f'Results/OOTest.png')
    plt.clf()
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

# path="IlahieStuff/Hex150K/wavefunctions1/"
# bigOne(path,'wavefunction_','OO')



def checkangle(location):
    path=location+"/npzFiles/"
    npzFilePaths = glob.glob(os.path.join(path, '*.npz'))
    npzFilePaths.sort(reverse=True)
    biglist=[]
    for file in npzFilePaths:
        data=np.load(file)
        coords=data['coords']
        for molecule in np.arange(0, len(coords), 3):
            actualcoord = molecule
            actualcoord = np.int(actualcoord)
            # if coords[actualcoord][1]!=0:
            #     print('ahhh')
            actualcoord += 1
            # print((coords[(actualcoord, 1)]))
            # print((coords[(actualcoord, 1)] / np.abs(coords[(actualcoord, 0)])))
            invinput = (coords[(actualcoord, 1)] / np.abs(coords[(actualcoord, 0)]))
            degrees = np.arctan(invinput) * 360 / 2 / np.pi
            print(degrees)
            # print(invinput)
            biglist.append(180 - (np.arctan(invinput) * 360 / (2 * np.pi)))
    print(np.average(biglist))
    print(np.std(biglist))
    print(min(biglist))
    print(max(biglist))
    # print(biglist[[x>105 for x in biglist]])
    # print(biglist[[x<104 for x in biglist]])
checkangle("FixingThingsWithRyan/FixedAngle")