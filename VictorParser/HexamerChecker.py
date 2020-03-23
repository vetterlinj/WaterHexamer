import numpy as np
#filenumbers=np.arange(1,18)
#a set of the filenumbers so I can loop through the files
filenumbers=[1]
#a set of waters so I can loop through each water in each Walker
waters=np.arange(0,6)
print(waters)
print(filenumbers)

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