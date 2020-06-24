import numpy as np
name = 'energies'
data = np.load(f'{name}.npy')
resultsFile = open(f"{name}.txt", 'w')
for item in data:
    resultsFile.write(str(item) + '\n')
resultsFile.close()