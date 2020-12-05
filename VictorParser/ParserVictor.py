import numpy as np
import struct
wfns=[]
weights=[]

skip_ws = lambda data, b=4: data.read(b)
get_int = lambda a: struct.unpack("i", a)[0]
read_int = lambda data: get_int(data.read(4))
get_float = lambda ag: struct.unpack("d", ag)[0]
read_float = lambda datag: get_float(datag.read(8))
read_float_block = lambda data, nblocks: np.frombuffer(data.read(8*nblocks), dtype=float)

hasWeights=False
for simulation in np.arange(1, 2):
    count=0

    data = open('UpdatedPrism/Raw/h2o6_prism_coords_noimp_150k_walkers.dat', "rb")
    if hasWeights==True:
        weightfile = open('UpdatedPrism/Raw/d2o6/d2o6_prism_weight.dat', "r")
    skip_ws(data)
    numberofsets = read_int(data)
    print(numberofsets)
    for x in range(0,numberofsets):
        walkertracer = []
        # skip_ws(data, 2)
        count=count+1
        wfns=[]
        read_int(data);
        read_int(data)
        number=read_int(data)
        print(number)
        walkertracer.append(number)
        initialwalkers= read_int(data)
        time=read_float(data)
        for x in range(0, number):
            read_int(data)
            read_int(data)
            wfns.append(read_float_block(data, 54))
            #ONLY USE BELOW LINE FOR BOTTOM HOMO CAGE AND PRISM, extra zero padding
            # read_float(data)
        wfns=np.array(wfns)
        newwfns=np.reshape(wfns,(number,18,3))
        #Weights file:
        if hasWeights==True:
            weightfile.readline()
            weights=[]
            print('weightstime')

            for x in range(0, number):
                weights.append(weightfile.readline())
                weights[x] = weights[x].strip()
                weights[x] = np.double(weights[x])

        paddednumber=str(count).zfill(3)
        if hasWeights==False:
            # np.savez(f'UpdatedPrism/Parsed/150kh2o6/150kprismwfn{paddednumber}',coords=newwfns,time=time,NumWalkers=number,InitialWalkers=initialwalkers,Size=number)
            print(count)
        if hasWeights==True:
            np.savez(f'UpdatedPrism/Parsed/d2o6/d2o6{paddednumber}', coords=newwfns, weights=weights,
                     time=time, NumWalkers=number, InitialWalkers=initialwalkers, Size=number)
            print(count)
np.save(f'UpdatedPrism/Parsed/150kh2o6/initial_prism_walkers',newwfns)
print()