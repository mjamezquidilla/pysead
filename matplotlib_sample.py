import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
plt.style.use('fivethirtyeight')

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

x = [0, 10]
y = [2, 3]
z = [3, 5]

ax.plot(x,y,z, marker = 'o', linewidth = 1)
plt.show()





