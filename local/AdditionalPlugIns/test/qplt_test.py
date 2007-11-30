# a short test of PyQwt5.qplt functions inside SimuVis4

from math import sin
from PyQt4.Qwt5.qplt import *

xx = [0.1*a for a in range(50)]
yy = [sin(a) for a in xx]
Plot(Curve(xx, yy))
