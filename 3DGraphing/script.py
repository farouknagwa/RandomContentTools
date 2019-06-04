import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

G = 6.67 * 10 ** -11 # Universal Gravitational Constant
rho = 5510 # Density of Earth



def sigmoid(x, a, b):
        """ Defines a sigmoid function. Returns the value of the sigmoid function at position x.
        """
        try:
                return 1 / (1 + math.exp(a * (x - b)))
        except:
                if a > 0:
                        if x > b:
                                return 0
                        else:
                                return 1
                else:
                        if x > b:
                                return 1
                        else:
                                return 0



def accelerationDueToGravityOfAPlanet(x, y, cx, cy, radius, density):
    r = math.sqrt((x - cx) ** 2 + (y - cy) ** 2) # Radial distance from the centre of the planet

    c = 2
    n = sigmoid(r, c, radius)
    m = sigmoid(r, -c, radius)

    k = (4/3) * G * math.pi * density

    if x == cx and y == cy:
            return 0 # Because 1 / x² is asymptotic at x = 0, return 0 here for when the radial position is 0 to avoid infinities

    if r < radius / 20:
            return k * r * n
    else:
            return k * (r * n + m * radius ** 3 / r ** 2)



figure = plot.figure()
axes = figure.add_subplot(111, projection = "3d")

density = rho * 10 ** 6
radius = 6.37

p = 20

x1 = np.arange(0, 2 * p, p/400)
y1 = np.arange(0, 2 * p, p/400)

x2, y2 = np.meshgrid(x1, y1)

z1 = np.array([accelerationDueToGravityOfAPlanet(x, y, 20, 20, radius  , density)  for x, y in zip(np.ravel(x2), np.ravel(y2))])
z2 = z1.reshape(x2.shape)

axes.set_zlim3d(20, -20 )
axes.set_xlim3d( 40, 0 )
axes.set_ylim3d(0, 40 )
axes.set_xlabel("Distance (10³ km)", labelpad = 20)
axes.set_ylabel("Distance (10³ km)", labelpad = 20)
axes.set_zlabel("Acceleration due to Gravity (m/s²)", labelpad = 20)

axes.plot_surface(x2, y2, z2)

plot.show()