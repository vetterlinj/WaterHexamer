import numpy as np
import matplotlib.pyplot as plt
from VictorParser.loadnpz import *
def markthing():
  with open('test_mbpol_KNL.sh') as temp_f:
    template = temp_f.read()
  write_dir = ...

  out_file_template = 'KNL_test_{nodes}_{NMPI}_round2.sh'
  # for n in range(2,10,2):
  #   total_cores = n * 64
  #   for i in range(1,total_cores):
  #     if total_cores % i ==0:
  #       # template_to_write = template.format(NMPI=i, nodes=n, NOMP=total_cores)
  #       template_to_write = template.format(NMPI=i, nodes=n, NOMP=int(total_cores/i))
  #       template_out_file = out_file_template.format(nodes=n, NMPI=i)
  #       with open(template_out_file, 'w+') as bleh:
  #         bleh.write(template_to_write)
  for n in range(8,18,2):
    total_cores = n * 64

        # template_to_write = template.format(NMPI=i, nodes=n, NOMP=total_cores)
    template_to_write = template.format(NMPI=n, nodes=n, NOMP=64)
    template_out_file = out_file_template.format(nodes=n, NMPI=n)
    with open(template_out_file, 'w+') as bleh:
      bleh.write(template_to_write)

def getEnergies():
  name='BigRestartEnergies5000'
  data=np.load(f'/Users/nicholasvetterli/PycharmProjects/WaterHexamer/VictorParser/IlahieStuff/{name}.npy')
  resultsFile = open(f"/Users/nicholasvetterli/PycharmProjects/WaterHexamer/VictorParser/IlahieStuff/{name}.txt", 'w')
  for item in data:
    resultsFile.write(str(item)+'\n')
  resultsFile.close()

def makeinitialwalkers():
  data=np.load('/Users/nicholasvetterli/PycharmProjects/WaterHexamer/VictorParser/IlahieStuff/walkers_12000.npz')
  coords=data['coords']
  np.save('/Users/nicholasvetterli/PycharmProjects/WaterHexamer/VictorParser/IlahieStuff/initial_mark_walkers',coords)

def test():
  data=np.load('/Users/nicholasvetterli/PycharmProjects/WaterHexamer/VictorParser/IlahieStuff/initial_walkers.npy')
  print()
getEnergies()


