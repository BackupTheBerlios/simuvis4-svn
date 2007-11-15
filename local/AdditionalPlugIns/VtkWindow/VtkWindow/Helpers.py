# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

# FIXME: old SimuVis code

import math

class RgbCalculator(object):
    """calculates an rgb pattern for a value"""

    def __init__(self, min, max):
        self.setMinMax(min, max)

    def RGB(self, val):
        x = (val-self.min) * (2.0*math.pi/(self.max-self.min))
        if x < 0: x = 0
        if x > 2.0*math.pi: x = 2.0*math.pi
        if x < math.pi:
            r = 0.5+0.5*math.cos(x)
            b = 0.0
        else:
            b = 0.5+0.5*math.cos(x)
            r = 0.0
        return (r, 1.0-r-b, b)

    def setMinMax(self, min, max):
        self.min = min
        self.max = max
        self.half = 0.5 * (max + min)


def isActor(a): # FIXME: HACK!
    return a and a.GetClassName() in ('vtkActor', 'vtkOpenGLActor',
                                      'vtkLODActor')


def isAssembly(a): # FIXME: HACK!
    return a and a.GetClassName() == 'vtkAssembly'


def getActorsRecursive(a):
    l = []
    parts = a.GetParts()
    numParts = parts.GetNumberOfItems()
    parts.InitTraversal()
    for i in range(0,numParts):
        p = parts.GetNextProp3D()
        if isActor(p):
            l.append(p)
        elif isAssembly(p):
            l += getActorsRecursive(p)
    return l

