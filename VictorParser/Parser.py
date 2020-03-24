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
#fstrings
#list of files
#files=['h2o6_book','h2o_d2o5_book','h2o_d2o5_prism','h2o_d2o5_cage','h2o5_d2o_book','h2o5_d2o_prism','h2o5_d2o_cage','d2o6_book','sample']
#Use above for above files, and below for below. Additional zero padding in below means they must be parsed differently.
#REMEMBER TO USE ADDITIONAL LINE BELOW
#files=['h2o6_prism','d2o6_prism','d2o6_cage','h2o6_cage']
#'d2o6_prism','d2o6_cage','h2o6_prism','h2o6_cage',
files=['sample']
#numberofsets=1

#numbersum=0
for file in files:
    count = 0
    # data = open(f"NickFiles/VictorData/{file}/{file}_coords.dat", "rb")
    # weightfile = open(f"NickFiles/VictorData/{file}/{file}_weight.dat", "r")
    data = open(f"{file}_coords.dat", "rb")
    weightfile = open(f"{file}_weight.dat", "r")
    skip_ws(data)
    numberofsets = read_int(data)
    print(file)
    print(numberofsets)
    for x in range(0,numberofsets):
        # skip_ws(data, 2)
        count=count+1
        wfns=[]
        read_int(data);
        read_int(data)
        number=read_int(data)
        print(number)
        initialwalkers= read_int(data)
        time=read_float(data)
        # print(read_int(data))
        # print(read_int(data))
        # print(read_float(data))
        # print(read_float(data))
        # read_int(data);
        # read_int(data)
        # print(read_float_block(data, 54))
        for x in range(0, number):
            # print(read_int(data))
            # print(read_int(data))
            # print(read_float_block(data, 54))
            read_int(data)
            read_int(data)
            wfns.append(read_float_block(data, 54))
            #ONLY USE BELOW LINE FOR BOTTOM HOMO CAGE AND PRISM, extra zero padding
            #read_float(data)
        wfns=np.array(wfns)
        newwfns=np.reshape(wfns,(number,18,3))
        # wfnsx=wfns[:,0::3]
        # wfnsy=wfns[:,1::3]
        # wfnsz=wfns[:,2::3]
        # print(newwfns)
        #filename='SampleCoords/'+str(count)+'NumWalkers'+str(number)+'InitialWalkers'+str(initialwalkers)+'Time'+str(int(time))
        # print(filename)
        #np.save(filename,newwfns)
        #Weights file:
        weightfile.readline()
        weights=[]
        print('weightstime')
        if file == 'h2o6_prism':
            print('oranges')
        for x in range(0, number):
            weights.append(weightfile.readline())
            weights[x] = weights[x].strip()
            weights[x] = np.double(weights[x])

        paddednumber=str(count).zfill(3)

#        numbersum=numbersum+number
        np.savez(f'PythonData/{file}{paddednumber}',coords=newwfns,weights=weights,time=time,NumWalkers=number,InitialWalkers=initialwalkers)
#        np.savez(f'NickFiles/VictorData/{file}/PythonData/{file}{paddednumber}',coords=newwfns,weights=weights,time=time,NumWalkers=number,InitialWalkers=initialwalkers)
        print(count)
        #weightsname='SampleCoords/'+str(count)+'NumWalkersWeights'+str(number)
        #np.save(weightsname, weights)
        #print(weights)

# oranges=weights.readline()
# print(oranges)
#
#         print(type(weights[0]))
#np.concatonate
#np.save
#np.load
# print(struct.unpack("i",weights.read(4)))
# read_int(data);read_int(data)
# print(read_int(data))
# print(read_int(data))
# print(read_float(data))
# # print(read_float(data))
# read_int(data);read_int(data)
# print(read_float_block(data, 54))
# for x in range(0,199,1):
#     print(read_int(data))
#     print(read_int(data))
#     print(read_float_block(data, 54))

#np.loadtext




