import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

G = 6.67 * 10 ** -11  # Universal Gravitational Constant
rho = 5510  # Density of Earth
image = 4


def sigmoid(x, a, b):
    """ Defines a sigmoid function. Returns the value of the sigmoid function at position x.
    """
    try:
        return 1 / (1 + math.exp(a * (x - b)))
    except:
        return 0 if (a > 0 and x > b) or (a <= 0 and x <= b) else 1


def accelerationDueToGravityOfAPlanet(x, y, cx, cy, radius, density):
    """ Gets the acceleration due to the gravity of a planet that is at position cx, cy, with the given radius and density, at a position x, y.
    """
    r = math.sqrt((x - cx) ** 2 + (y - cy) **
                  2)  # Radial distance from the centre of the planet

    c = 2  # Smoothing factor between functions
    n = sigmoid(r, c, radius)
    m = sigmoid(r, -c, radius)

    k = (4/3) * G * math.pi * density

    if x == cx and y == cy:
        return 0  # Because 1 / x^{2} is asymptotic at x = 0, return 0 here for when the radial position is 0 to avoid infinities

    return k * (r * n + m * radius ** 3 / r ** 2)




figure = plot.figure()
axes = figure.add_subplot(111, projection="3d")

density = rho * 10 ** 6
radius = 6.37

p = 40

x1 = np.arange(0,  p, p/200)
y1 = np.arange(0,  p, p/200)

x2, y2 = np.meshgrid(x1, y1)

if image == 1:
        z1 = np.array([accelerationDueToGravityOfAPlanet(x, y, 20, 20, radius, density) for x, y in zip(np.ravel(x2), np.ravel(y2))])
if image == 2:
        z1 = np.array([accelerationDueToGravityOfAPlanet(x, y, 10, 30, radius / 2, density) + accelerationDueToGravityOfAPlanet(x, y, 25, 15, radius, density) for x, y in zip(np.ravel(x2), np.ravel(y2))])
if image == 3:
        z1 = np.array([accelerationDueToGravityOfAPlanet(x, y, 10, 30, radius / 1.5 , density / 2) + accelerationDueToGravityOfAPlanet(x, y, 30, 10, radius / 1.5, density) for x, y in zip(np.ravel(x2), np.ravel(y2))])
if image == 4:
        z1 = np.array([accelerationDueToGravityOfAPlanet(x, y, 10, 30, radius  , density ) + accelerationDueToGravityOfAPlanet(x, y, 30, 10, radius , density * 3) for x, y in zip(np.ravel(x2), np.ravel(y2))])

z2 = z1.reshape(x2.shape)

axes.set_zlim3d(20, -20)
axes.set_xlim3d(40, 0)
axes.set_ylim3d(0, 40)
axes.set_xlabel("Distance (10³ km)", labelpad=20)
axes.set_ylabel("Distance (10³ km)", labelpad=20)
axes.set_zlabel("Acceleration due to Gravity (m/s²)", labelpad=20)

axes.plot_surface(x2, y2, z2)

plot.show()
