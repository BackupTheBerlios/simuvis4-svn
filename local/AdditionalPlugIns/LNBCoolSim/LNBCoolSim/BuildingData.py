#!/usr/bin/env python
# encoding: latin-1
# version:  $Id: BuildingData.py,v 1.2 2007/04/23 07:37:22 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import operator, sys, pickle


class Data:
    def __init__(self, **kwarg):
        self.name    = 'unknown'
        self.id      = idGen()
        self._parent = kwarg.get('_parent', None)
        if kwarg.has_key('_parent'):
            del kwarg['_parent']
        if kwarg.has_key('id'):
            del kwarg['id']
        self.setup()
        for (k,v) in kwarg.items():
            setattr(self, k, v)
    def dump(self):
        return pickle.dumps(self)
    def setup(self):
        pass


class TimeRowData(Data):
    def setup(self):
        self.value = []
        self.time  = []


class BoundaryConditionData(Data):
    def setup(self):
        self.temperature = 293.15 # 0.0 for adiabatic
        self.radiationShortWave = 0.0
        self.radiationLongWave  = 0.0


class WindowData(Data):
    def setup(self):
        self.a = ()
        self.b = ()
        self.framePortion = 0.2
        self.nPanes = 2.0
        self.kWindow = 1.837
        self.boundaryCondition = None
	self.shadingFc = 1.0


class MaterialData(Data):
    def setup(self):
        self.rgb = [0.5, 0.5, 0.5]
        self.rho = 1400.0
        self.lam = 0.58
        self.c   = 1.0
        self.id  = '-1'


class LayerData(Data):
    def setup(self):
        self.thickness = 0.24
        self.material = None


class LayeredObjectData(Data):
    def setup(self):
        self.layer = []
        self.boundaryCondition = None
        self.innerAlphaShortwave = 0.35
        self.outerAlphaShortwave = 0.58
        self.innerEpsilonLongwave = 0.95
        self.outerEpsilonLongwave = 0.97
    def thickness(self):
        return reduce(operator.add, (map(lambda l: l.thickness, self.layer)))


class WallData(LayeredObjectData):
    def setup(self):
        self.a = ()
        self.b = ()
        self.window = []
        self.door   = []
        LayeredObjectData.setup(self)


class DoorData(LayeredObjectData):
    def setup(self):
        self.a = ()
        self.b = ()
        LayeredObjectData.setup(self)


class SlabData(LayeredObjectData):
    def setup(self):
        self.points = ()
        self.offset = 0.0
        LayeredObjectData.setup(self)


class AdapterData(Data):
    __virtual__ = 1
    def setup(self):
        self._adapter = 1
        self.object = None


class UserProfileData(Data):
    def setup(self):
        self.TsetHeat = 294.15
        self.TsetCool = 299.15
        self.deltaTNight = 5.0
        self.heatingPeriod = (258, 120)
        self.innerHeatWeekDay=[0.0]*24
        self.innerHeatWeekEnd=[0.0]*24
        self.radiationPortionWeekDay = 0.5
        self.radiationPortionWeekEnd = 0.5
        self.innerHumidityWeekDay=[0.0]*24
        self.innerHumidityWeekEnd=[0.0]*24
        self.outerAirchangeWeekDay=[0.0]*24
        self.outerAirchangeWeekEnd=[0.0]*24


class JointData(Data):
    def setup(self):
        self.wall = []
        self.x = 0.0
        self.y = 0.0


class ZoneData(Data):
    def setup(self):
        self.baseHeight = 0.0
        self.height = 3.0
        self.roof = None
        self.floor = None
        self.joint = []
        self.wall = []
        self.insideWall = []
        self.userProfile = UserProfileData(_parent=self)


class BuildingData(Data):
    def setup(self):
        self.zone = []
        self.location = "Default"
        self.northAngle = 42.0
        self.buildingType = 'UNKNOWN'
        self.simInfo = SimulationData(_parent=self)


class SimulationData(Data):
    def setup(self):
        self.username = ''
        self.password = ''
        self.server   = ''
        self.taskId   = ''
        self.results  = None
        self.queued   = 0
        self.done     = 0
        self.timeRange = (0.0, 0.0)


class IdGenerator:
    def __init__(self, init=0, inc=1):
        self.v = init
        self.inc = inc
    def __call__(self, prefix=''):
        id= '%s%d' % (prefix, self.v)
        self.v += self.inc
        return id


idGen = IdGenerator()
load = pickle.loads
