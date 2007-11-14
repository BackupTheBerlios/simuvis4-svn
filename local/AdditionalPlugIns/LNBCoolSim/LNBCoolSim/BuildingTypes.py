#!/usr/bin/env python
# encoding: latin-1
# version:  $Id: BuildingTypes.py,v 1.2 2007/04/23 07:37:22 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import BuildingData

buildingTypes = ['OneZone', 'TwoZones']

Innenputz   = BuildingData.MaterialData(id="g1070", name='Leichtputz 1000',              rho=1000.0, lam=0.38, c=1.0, rgb=(0.8,0.8,0.8))
Ziegel      = BuildingData.MaterialData(id="g1084", name='Voll-, Hochlochziegel 1200',   rho=1200.0, lam=0.50, c=0.9, rgb=(1.0,0.5,0.5))
Styropor    = BuildingData.MaterialData(id="g1318", name='Schaumgummi 60',               rho=60.0,   lam=0.04, c=1.5, rgb=(0.9,0.9,1.0))
Aussenputz  = BuildingData.MaterialData(id="g1087", name='Aussenputz',                   rho=1800.0, lam=0.87, c=1.0, rgb=(0.7,0.7,0.7))
Normalbeton = BuildingData.MaterialData(id="g1176", name='Normalbeton 2400',             rho=2400.0, lam=2.00, c=1.0, rgb=(0.6,0.6,0.6))
Hartschaum  = BuildingData.MaterialData(id="g1047", name='Phenolharz Hartschaum 30 - 2', rho=30.0,   lam=0.04, c=1.5, rgb=(0.7,1.0,0.7))
Estrich     = BuildingData.MaterialData(id="g1394", name='Estrich',                      rho=2000.0, lam=0.14, c=1.0, rgb=(0.5,0.5,0.5))
Unknown0    = BuildingData.MaterialData(id="g1339", name='Bitumen',                      rho=1050.0, lam=0.17, c=1.0, rgb=(0.5,0.8,0.8))
Unknown1    = BuildingData.MaterialData(id="g1143", name='Porenbeton Planstein 600',     rho=1000.0, lam=0.19, c=1.0, rgb=(0.5,0.8,0.8))
undefined   = BuildingData.MaterialData(id="g1000", name='Undefiniert',                  rho=1000.0, lam=0.38, c=1.0, rgb=(0.9,0.9,0.9))

def standardWindow(*arg, **kwarg):
    kwarg['framePortion'] = 0.2
    kwarg['nPanes'] = 2
    kwarg['kWindow'] = 1.837
    return apply(BuildingData.WindowData, arg, kwarg)

def standardDoor(*arg, **kwarg):
    # FIXME: Tuer komplettieren!
    return apply(BuildingData.DoorData, arg, kwarg)

def standardWall(num, *arg, **kwarg):
    """return a standard Wall with a window"""
    kwarg['name'] = 'Wand %d' % num
    w = apply(BuildingData.WallData, arg, kwarg)
#    w.layer.append(BuildingData.LayerData(thickness=0.015, material=Innenputz))
#    w.layer.append(BuildingData.LayerData(thickness=0.24,  material=Ziegel))
#    w.layer.append(BuildingData.LayerData(thickness=0.2,   material=Styropor))
#    w.layer.append(BuildingData.LayerData(thickness=0.02,  material=Aussenputz))
    w.layer.append(BuildingData.LayerData(thickness=0.1,   material=undefined))
    w.innerAlphaShortwave = 0.35
    w.outerAlphaShortwave = 0.58
    w.innerEpsilonLongwave = 0.95
    w.outerEpsilonLongwave = 0.97
    #w.window.append(standardWindow(name=('Fenster %d' % num), a=(1.0, 1.0), b=(2.0,2.0), _parent=w))
    return w

def standardInnerWall(num, *arg, **kwarg):
    # no windows, but a door
    kwarg['name'] = 'Wand %d' % num
    w = apply(BuildingData.WallData, arg, kwarg)
#    w.layer.append(BuildingData.LayerData(thickness=0.015, material=Innenputz))
#    w.layer.append(BuildingData.LayerData(thickness=0.24,  material=Ziegel))
#    w.layer.append(BuildingData.LayerData(thickness=0.015, material=Innenputz))
    w.layer.append(BuildingData.LayerData(thickness=0.1,   material=undefined))
    w.innerAlphaShortwave = 0.35
    w.outerAlphaShortwave = 0.35
    w.innerEpsilonLongwave = 0.95
    w.outerEpsilonLongwave = 0.95
    return w


def standardInsideWall(num, *arg, **kwarg):
    # no windows, but a door
    kwarg['name'] = 'Innenwand %d' % num
    w = apply(BuildingData.WallData, arg, kwarg)
#    w.layer.append(BuildingData.LayerData(thickness=0.015, material=Innenputz))
#    w.layer.append(BuildingData.LayerData(thickness=0.06,  material=Ziegel))
#    w.layer.append(BuildingData.LayerData(thickness=0.015, material=Innenputz))
    w.layer.append(BuildingData.LayerData(thickness=0.1,   material=undefined))
    w.innerAlphaShortwave = 0.35
    w.outerAlphaShortwave = 0.35
    w.innerEpsilonLongwave = 0.95
    w.outerEpsilonLongwave = 0.95
    return w


def standardRoof(*arg, **kwarg):
    r = apply(BuildingData.SlabData, arg, kwarg)
#    r.layer.append(BuildingData.LayerData(thickness=0.015, material=Innenputz))
#    r.layer.append(BuildingData.LayerData(thickness=0.16,  material=Normalbeton))
#    r.layer.append(BuildingData.LayerData(thickness=0.22,  material=Hartschaum))
#    r.layer.append(BuildingData.LayerData(thickness=0.011, material=Unknown0))
#    r.layer.append(BuildingData.LayerData(thickness=0.05,  material=Unknown1))
    r.layer.append(BuildingData.LayerData(thickness=0.10,  material=undefined))
    return r

def standardFloor(*arg, **kwarg):
    f = apply(BuildingData.SlabData, arg, kwarg)
#    f.layer.append(BuildingData.LayerData(thickness=0.04,  material=Estrich))
#    f.layer.append(BuildingData.LayerData(thickness=0.35,  material=Hartschaum))
#    f.layer.append(BuildingData.LayerData(thickness=0.16,  material=Normalbeton))
#    f.layer.append(BuildingData.LayerData(thickness=0.015, material=Innenputz))
    f.layer.append(BuildingData.LayerData(thickness=0.10,  material=undefined))
    f.boundaryCondition = BuildingData.BoundaryConditionData(temperature = 283.15)
    return f


def OneZone():
    """ gives an instance of BuildingData with one zone,
    4 walls and one window in every wall """
    bd = BuildingData.BuildingData(name='Gebäude', buildingType='OneZone', location='Berlin')
    bd.zone.append(BuildingData.ZoneData(name='Zone', _parent=bd))
    z = bd.zone[0]

    coord = ((0.0, 0.0), (5.0, 0.0), (5.0, 8.0), (0.0, 8.0))
    for i in range(len(coord)):
        x, y = coord[i]
        z.joint.append(BuildingData.JointData(x=x, y=y, _parent=z))
        z.wall.append(standardWall(i))

    for i in range(4):
        z.joint[i].wall.append(z.wall[i-1])
        z.joint[i].wall.append(z.wall[i])

    z.wall[0].window.append(standardWindow(name='Fenster 1', a=(1.0, 1.0), b=(2.0,2.0), _parent=z.wall[0]))
    z.insideWall.append(standardInsideWall(0, a=(1.0, 2.0), b=(4.0, 2.0), _parent=z))
    z.insideWall.append(standardInsideWall(1, a=(1.0, 7.0), b=(4.0, 7.0), _parent=z))
    z.roof  = standardRoof(name='Decke', _parent=z)
    z.floor = standardFloor(name='Boden', _parent=z)
    return bd


def TwoZones():
    """ gives an instance of BuildingData with two zones,
    with one common wall"""
    bd = BuildingData.BuildingData(name='Gebäude', buildingType='TwoZones', location='Berlin')
    # Zonen
    bd.zone.append(BuildingData.ZoneData(name='Zone 0', _parent=bd))
    bd.zone.append(BuildingData.ZoneData(name='Zone 1', _parent=bd))
    z = bd.zone[0]
    z.wall.append(standardWall(0, a=(0.0, 0.0), b=(3.0, 0.0), _parent=z))
    z.wall.append(standardInnerWall(1, a=(3.0, 0.0), b=(3.0, 5.0), _parent=z))
    z.wall.append(standardWall(2, a=(3.0, 5.0), b=(0.0, 5.0), _parent=z))
    z.wall.append(standardWall(3, a=(0.0, 5.0), b=(0.0, 0.0), _parent=z))
    points = [ w.a for w in z.wall ]
    z.roof  = standardRoof(name='Decke', points=points, _parent=z)
    z.floor = standardFloor(name='Boden', points=points, _parent=z)
    z = bd.zone[1]
    o = bd.zone[0].wall[1].thickness()
    z.wall.append(standardWall(0, a=(o+3.0, 0.0), b=(o+6.0, 0.0), _parent=z))
    z.wall.append(standardWall(1, a=(o+6.0, 0.0), b=(o+6.0, 5.0), _parent=z))
    z.wall.append(standardWall(2, a=(o+6.0, 5.0), b=(o+3.0, 5.0), _parent=z))
    z.wall.append(BuildingData.AdapterData(name='Wand 3 (Adapter)', object=bd.zone[0].wall[1], _parent=z))
    tmp = bd.zone[0].wall[1]
    points = [ w.a for w in z.wall[:3] ]
    points.append((tmp.b[0]+ tmp.thickness(), tmp.b[1]))
    z.roof  = standardRoof(name='Decke', points=points, _parent=z)
    z.floor = standardFloor(name='Boden', points=points, _parent=z)
    return bd
