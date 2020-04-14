import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *
#coords, weights, metadata=concatenatenpz('NickFiles/VictorData/h2o6_book/PythonData/')
coords, weights, metadata=concatenatenpz('h2o6_prismPythonData/')

def freeHydrogenCandidates(coords):
    #find  OH distances, determine which are shortest
    oxygen = [coords[0, :], coords[3, :], coords[6, :], coords[9, :], coords[12, :], coords[15, :]]
    # Oxygen is (6,walkers,3)
    h1 = [coords[1, :], coords[4, :], coords[7, :], coords[10, :], coords[13, :], coords[16, :]]
    h2 = [coords[2, :], coords[5, :], coords[8, :], coords[11, :], coords[14, :], coords[17, :]]
    h1 = np.array(h1)
    h2 = np.array(h2)
    oxygen = np.array(oxygen)
    distances=[]
    for hydrogenatom in np.arange(0,6):
        listh1=[]
        listh2=[]
        for oxygenatom in np.arange(0,6):
            listh1.append(np.sqrt(np.sum(np.square(h1[hydrogenatom]-oxygen[oxygenatom]))))
            listh2.append(np.sqrt(np.sum(np.square(h2[hydrogenatom]-oxygen[oxygenatom]))))
        distances.append(listh1)
        distances.append(listh2)
    distances=np.array(distances)
    sorted=np.sort(distances)
    argsorted=np.argsort(sorted[:,1])
    candidates=argsorted[9],argsorted[10],argsorted[11]
    actualcandidates = []
    water = np.arange(0, 6) * 3
    h1 = water + 1
    h2 = h1 + 1
    for i in candidates:
        if i % 2 == 0:
            a = np.int(i / 2)
            actualcandidates.append(h1[a])
        elif i % 2 == 1:
            a = np.int((i - 1) / 2)
            actualcandidates.append(h2[a])
    return actualcandidates
    # bondeddistances=[]
    # for i in np.arange(0,6):
    #     list=[]
    #     list.append(sorted[i*2,1])
    #     list.append(sorted[i*2+1,1])
    #     bondeddistances.append(list)
    # bondeddistances=np.array(bondeddistances)
    # sortedbondeddistances=np.sort(bondeddistances)
def whichisfurthest(coords,candidates):
    hydrogendistances=[]
    for i in candidates:
        temp=[]
        for j in candidates:
            temp.append(np.sqrt(np.sum(np.square(coords[i] - coords[j]))))
        hydrogendistances.append(np.sort(temp))
    hydrogendistances=np.array(hydrogendistances)
    oranges=np.argsort(hydrogendistances[:,1])
    return candidates[oranges[-1]]
def whichisnextwater(walkercoords,currentwater):
    water = np.arange(0, 6) * 3
    list=[]
    for i in water:
        list.append(np.sqrt(np.sum(np.square(walkercoords[currentwater+1]-walkercoords[i]))))
    sort=np.argsort(list)[1]
    nextwater=sort*3
    tradewater=currentwater+3
    # coords[a][[nextwater, tradewater]] = coords[a][[tradewater, nextwater]]
    # coords[a][[nextwater+1, tradewater+1]] = coords[a][[tradewater+1, nextwater+1]]
    # coords[a][[nextwater + 2, tradewater + 2]] = coords[a][[tradewater + 2, nextwater + 2]]
    # checkingtool[np.int(tradewater/3)]=np.int(nextwater/3)
    # checkingtool[np.int(nextwater/3)]=np.int(tradewater/3)
    # print(checkingtool)
    return tradewater
def doublewatertime(walkercoords, currentwater):
    water = np.arange(0, 6) * 3
    listh1=[]
    listh2=[]
    for i in water:
        listh1.append(np.sqrt(np.sum(np.square(walkercoords[currentwater+1]-walkercoords[i]))))
        listh2.append(np.sqrt(np.sum(np.square(walkercoords[currentwater + 2] - walkercoords[i]))))
    sorth1=np.argsort(listh1)[1]
    sorth2=np.argsort(listh2)[1]
    return sorth1*3,sorth2*3
def whichpointsattheother(walkercoords, waterone, watertwo):
    water = np.arange(0, 6) * 3
    listh1=[]
    listh2=[]
    listh3=[]
    listh4=[]
    for i in water:
        listh1.append(np.sqrt(np.sum(np.square(walkercoords[waterone+1]-walkercoords[i]))))
        listh2.append(np.sqrt(np.sum(np.square(walkercoords[waterone + 2] - walkercoords[i]))))
        listh3.append(np.sqrt(np.sum(np.square(walkercoords[watertwo+1]-walkercoords[i]))))
        listh4.append(np.sqrt(np.sum(np.square(walkercoords[watertwo + 2] - walkercoords[i]))))
    sorth1=np.argsort(listh1)[1]
    sorth2=np.argsort(listh2)[1]
    if listh1[sorth1] < listh2[sorth2]:
        pointerfirst=sorth1
        firsthydrogenpointing=1
    if listh2[sorth2]<listh1[sorth1]:
        pointerfirst=sorth2
        firsthydrogenpointing=2
    sorth3=np.argsort(listh3)[1]
    sorth4 = np.argsort(listh4)[1]
    if listh3[sorth3] < listh4[sorth4]:
        pointersecond=sorth3
        secondhydrogenpointing=1
    if listh4[sorth4]<listh3[sorth3]:
        pointersecond=sorth4
        secondhydrogenpointing=2
    if pointerfirst*3==watertwo:
        return waterone, watertwo, firsthydrogenpointing,secondhydrogenpointing
    elif pointersecond*3==waterone:
        return watertwo,waterone, secondhydrogenpointing,firsthydrogenpointing
    else:
        print('oh no sad')
        exit()
def watertrader(walkercoords, currentwater, watertotrade, hydrogenpointer):
    walkercoords[[currentwater, watertotrade]] = walkercoords[[watertotrade, currentwater]]
    walkercoords[[currentwater+1, watertotrade+hydrogenpointer]] = walkercoords[[watertotrade+hydrogenpointer, currentwater+1]]
    if hydrogenpointer ==1:
        walkercoords[[currentwater+2, watertotrade+2]] = walkercoords[[watertotrade+2, currentwater+2]]
    elif hydrogenpointer ==2:
        walkercoords[[currentwater+2, watertotrade+1]] = walkercoords[[watertotrade+1, currentwater+2]]
    return walkercoords

for a in np.arange(0,1):
    candidates=freeHydrogenCandidates(coords[a])
    hydrogenZero=whichisfurthest(coords[a],candidates)
    checker=[]
    for candidate in candidates:
        if np.int(hydrogenZero)==candidate:
            zzzcandidate=candidate
        else:
            # checker.append(coords[a][candidate])
            checker.append(candidate)
    checkeyecker=[]
    for i in checker:
        if i %3==1:
            checkeyecker.append(i-1)
        elif i%3==2:
            checkeyecker.append(i-2)
        else:
            print('this should be a 1 or 2, not a whater?')
    firstcheck=np.copy(coords[a][checkeyecker[0]])
    secondcheck=np.copy(coords[a][checkeyecker[1]])
    #Check hydrogen zero is in the second slot:
    if (hydrogenZero-1)%3==0:
        coords[a][[hydrogenZero, hydrogenZero + 1]] = coords[a][[hydrogenZero + 1, hydrogenZero]]
        hydrogenZero = hydrogenZero + 1
    if hydrogenZero-2 !=0:
        coords[a][[0, hydrogenZero -2]] = coords[a][[hydrogenZero -2, 0]]
        coords[a][[1, hydrogenZero - 1]] = coords[a][[hydrogenZero - 1, 1]]
        coords[a][[2, hydrogenZero]] = coords[a][[hydrogenZero, 2]]
        # checkingtool[0]=np.int((hydrogenZero-2)/3)
        # checkingtool[np.int((hydrogenZero-2)/3)]=0
        # print(checkingtool)
    nextwater=whichisnextwater(coords[a], 0)
    if nextwater != 3:
        hydrogenpointer=1
        #THISMUSTBEFIXED
        coords[a]=watertrader(coords[a],3,nextwater,hydrogenpointer)
        nextwater=3
    nearh1,nearh2 = doublewatertime(coords[a], nextwater)
    if coords[a][np.int(nearh1)].all()!=firstcheck.all() and coords[a][np.int(nearh1)].all!=secondcheck.all():
        print('problem in waters')
        print(a)
        exit()
    if coords[a][np.int(nearh2)].all() != firstcheck.all() and coords[a][np.int(nearh2)].all != secondcheck.all():
        print('problem in waters')
        print(a)
        print('a')
        exit()
    firstwater,secondwater, firstpointer, secondpointer = whichpointsattheother(coords[a],nearh1,nearh2)
    #keeptrackusingnearh1
    nextwater=nextwater+3
    coords[a]=watertrader(coords[a],nextwater,firstwater,firstpointer)
    nextwater=nextwater+3
    coords[a]=watertrader(coords[a],nextwater,secondwater,secondpointer)
    nextwater=nextwater+3
    firstwater=whichisnextwater(coords[a],9)
    coords[a]=watertrader(coords[a],nextwater,firstwater,1)
    nearh1,nearh2 = doublewatertime(coords[a], nextwater)
    if coords[a][np.int(nearh1)].all()!=coords[a][0].all() and coords[a][np.int(nearh1)].all!=coords[a][15].all():
        print('problem in waters')
        print(a)
        exit()
    if coords[a][np.int(nearh2)].all() != coords[a][0].all() and coords[a][np.int(nearh2)].all != coords[a][15].all():
        print('problem in waters')
        print(a)
        print('a')
        exit()
    print('layercompletefornow')

