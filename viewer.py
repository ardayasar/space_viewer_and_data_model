import json
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


data = open(os.getcwd() + '/flightdata-1686185770.660619.json', 'r', encoding='utf-8').read()
data = json.loads(data)

x = []
y = []
z = []

for sector in data:
    x.append(sector['long'])
    y.append(sector['lat'])
    z.append(sector['altitude'])
    # print(sector['headin'])

ax.scatter(x, y, z)
ax.set_xlabel('Long')
ax.set_ylabel('Lat')
ax.set_zlabel('Altitude')
ax.set_title('Flight Data')

for i in range(1, len(x)):
    point1 = (x[i-1], y[i-1], z[i-1])
    point2 = (x[i], y[i], z[i])
    ax.plot([point1[0], point2[0]], [point1[1], point2[1]], [point1[2], point2[2]], color='red')


# Show the plot
plt.show()