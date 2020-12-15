import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
def call_a_cpot(cds):
   cdsang=cds*0.529177
   lib = ctypes.cdll.LoadLibrary("./libmbpol.so")
   example_fun = lib.calcpot_
   example_fun.restype = None
   example_fun.argtypes = [ctypes.POINTER(ctypes.c_int),
                   ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                   ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]
   nw = ctypes.c_int32(6) #some integer that needs to be passed to the potential
   v = np.zeros(1)
   vpot = np.zeros(len(cdsang))
   for num,coord in enumerate(cdsang):
       # print(v)
       v = np.zeros(1)
       # print(coord)
       example_fun(ctypes.byref(nw),v,cdsang[num])
       vpot[num] = v[0]
   return vpot
