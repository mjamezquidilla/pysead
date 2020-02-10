import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

x = [0, 1]
y = [2, 3]
z = [4, 5]

ax.plot(x,y,z)
plt.show()