#!/usr/bin/env python
# 	$Id: CoordSys.py,v 1.7 2003-05-08 13:26:33 joerg Exp $	

from cCoordSys import *


def planeCheck(points, tol):
    """ check if 3D-points ae on a 2D-plane by transformation
    to a local 2D-system, tol is the max. distance of a
    point from the plane"""
    cs = CoordSys()
    cs.setTol2D(tol)
    cs.find2D(points)
    #print cs
    plane = 1
    try:
        cs.toLocal2D(points)
    except Error:
        #print map(lambda x: x[2], cs.toLocal(points)), tol
        plane = 0
    return plane


## support for pickling and unpickling

def __createCoordSys(o, u, v, w, tol2D):
    c = CoordSys(o, u, v, w)
    c.setTol2D(tol2D)
    return c


def __reduceCoordSys(c):
    return (__createCoordSys, (c.o(), c.u(), c.v(), c.w(), c.getTol2D()))


import copy_reg
copy_reg.constructor(__createCoordSys)
copy_reg.pickle(CoordSysType, __reduceCoordSys)
del copy_reg


if __name__ == '__main__':
    import math, random, time

    def randomTest():
        def r():
            return math.sin(random.random()*2.0*math.pi)* random.random() * 1000.0
        def tdiff(x, y):
            for i in range(len(x)):
                for j in range(3):
                    if math.fabs(x[i][j] - y[i][j]) > 1.0e-10:
                        return 1
            return 0
        print "RandomTest:"
        x = CoordSys((3,2,1), (0,1,2), (0,2,1), (1,0,3))
        for i in range(1000):
            g = ((r(), r(), r()), (r(), r(), r()),(r(), r(), r()),(r(), r(), r())) 
            l = x.toLocal(g)
            ng = x.toGlobal(l)
            if tdiff(ng, g):
                print "  ERROR"
                print "    ", g
                print "    ", ng
                print "    ", l
                break
        print "  ok!" 


    def speedTest():
        print "SpeedTest:"
        x = CoordSys((3,2,1), (0,1,2), (0,2,1), (1,0,3))
        pl = tuple([(42.0, 43.0, 44.0)] * 100)
        t = time.time()
        for i in range(10000):
            l = x.toLocal(pl)
        print "  1e+6 points converted to local in %f s" % (time.time()-t,)
        t = time.time()
        for i in range(10000):
            g = x.toGlobal(l)
        print "  1e+6 points converted to global in %f s" % (time.time()-t,)


    def two2Test():
        import math
        print "2D-Test:"
        vDiff =  lambda a,b: (a[0]-b[0], a[1]-b[1], a[2]-b[2])
        vLen  =  lambda a: math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])
        p = ((0.0, 0.0, 0.0), (5.0, 0.0, 0.0),(10.0, 42.0, 0.0))
        c = CoordSys()
        c.find2D(p)
        print c
        if vLen(vDiff(c.o(), (0,0,0))) or vLen(vDiff(c.u(), (1,0,0))) or \
           vLen(vDiff(c.v(), (0,1,0))) or vLen(vDiff(c.w(), (0,0,1))):
            print '  failed!'
        else:
            print '  ok!'


    def planeTest():
        print 'PlaneTest:'
        # plane z = x - y
        p0 = ((3.0, 2.0, 1.0), (7.0, 10.0, -3.0), (2.5, 0.9, 1.6), (100.0, 100.0, 0.0))
        if planeCheck(p0, 0.0001):
            print '  ok!'
        else:
            print '  failed!'
        # change a value a little
        p1 = ((3.0, 2.0, 1.0), (7.0, 10.0, -3.0), (2.5, 0.9, 1.6), (100.0, 100.0, 0.01))
        if planeCheck(p1, 0.001):
            print '  failed!'
        else:
            print '  ok!'
        # again, but with increased tolerance
        if planeCheck(p1, 0.01):
            print '  ok!'
        else:
            print '  failed!'


    def pickleTest():
        import pickle, cPickle
        x = CoordSys((3,2,1), (0,1,2), (0,2,1), (1,0,3))
        x.setTol2D(42.0)
        s = pickle.dumps(x)
        y = cPickle.loads(s)
        for a in ('o', 'u', 'v', 'w'):
            i = getattr(x, a)()
            j = getattr(y, a)()
            if not i == j:
                print "Pickle error:", a, i, j
        if not x.getTol2D() == y.getTol2D():
                print "Pickle error:", 'Tol2D'

    print "Testing CoordSys, version", version
    randomTest()
    two2Test()
    planeTest()
    speedTest()
    pickleTest()
