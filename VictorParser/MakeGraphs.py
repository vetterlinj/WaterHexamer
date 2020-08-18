import numpy as np
import matplotlib.pyplot as plt

# x = np.linspace(0, 2, 100)
# y = np.exp(x)
#
# plt.figure()
# plt.plot(x, np.exp(-0*x),label="n=E_0-E_0")
# plt.plot(x, np.exp(-1*x),label="n=E_1-E_0")
# plt.plot(x, np.exp(-2*x),label="n=E_2-E_0")
# plt.legend(loc='top right')
# plt.xlabel('τ')
# plt.ylabel('exp(-n*τ)')
# plt.show()



x = [0]
y1 = [87]
y2=[-9]
y3 = [100]

plt.scatter(x,y1, label="Electronic Energy")
plt.scatter(x,y2)
plt.scatter(x,y3)
plt.legend(loc='top right')
plt.xlim(-20,100)
# plt.xlabel('τ')
plt.ylabel('exp(-n*τ)')
plt.show()