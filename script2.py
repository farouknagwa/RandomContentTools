import math
import random

def randrange(start, stop, step):
    d = stop - start
    d2 = d * random.random()
    d2 = d2 / step
    d2 = round(d2)
    d2 = d2 * step
    return d2

c = 3.0e8
e = 1.6e-19

def gamma(u):
    return 1 / math.sqrt(1 - u**2 / c**2)

def distanceTravelledAtU(t, u):
    t2 = gamma(u) * t
    return u * t

q = 1 * e
m = 1869.61

B = randrange(0.01, 0.4, 0.01)
f = randrange(0.001, 0.02, 0.001)

u = f * c
mkgs = m * 1.0e6 * 1.783e-36
r = mkgs * u / (q * B)
qm = q / mkgs

print "B = {0} T".format(B)
print "m = {0} kg".format(mkgs)
print "q/m = {0} C/kg".format(qm)
print "r = {0} m".format(r)
print "v = {0} m/s".format(u)

m2 = B * r * q / (u *  1.0e6 * 1.783e-36)

print m2
