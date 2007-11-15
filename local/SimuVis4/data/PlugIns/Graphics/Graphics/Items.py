# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import QGraphicsItem, QGraphicsItemGroup, QGraphicsLineItem,\
    QGraphicsEllipseItem, QGraphicsTextItem, QPen, QColor
from PyQt4.QtCore import QLineF


class ItemGroupBase(QGraphicsItemGroup):
    """abstract item group"""
    def __init__(self, **kwarg):
        QGraphicsItemGroup.__init__(self)
        if kwarg.has_key('movable'):
            self.setFlag(QGraphicsItem.ItemIsMovable, kwarg['movable'])
            del kwarg['movable']
        if kwarg.has_key('toolTip'):
            self.setToolTip(kwarg['toolTip'])
            del kwarg['toolTip']
        self._setup(**kwarg)
    def _setup():
        raise Exception('ItemGroupBase needs to be subclassed for usage!')


class Cross(ItemGroupBase):
    """a cross (+) made of two lines"""
    def _setup(self, x=0, y=0, size=10, pen=QPen(QColor(0,0, 255))):
        a = 0.5*size
        self.p1 = QGraphicsLineItem(QLineF(x-a, y, x+a, y))
        self.p2 = QGraphicsLineItem(QLineF(x, y-a, x, y+a))
        self.p1.setPen(pen)
        self.p2.setPen(pen)
        self.addToGroup(self.p1)
        self.addToGroup(self.p2)


class CrossX(ItemGroupBase):
    """a cross (x) made of two lines"""
    def _setup(self, x=0, y=0, size=10, pen=QPen(QColor(0,0, 255))):
        a = 0.5*size
        self.p1 = QGraphicsLineItem(QLineF(x-a, y-a, x+a, y+a))
        self.p2 = QGraphicsLineItem(QLineF(x-a, y+a, x+a, y-a))
        self.p1.setPen(pen)
        self.p2.setPen(pen)
        self.addToGroup(self.p1)
        self.addToGroup(self.p2)


class Axes(ItemGroupBase):
    """two rectangular lines as axes"""
    def _setup(self, x=[0, -100, 100], y=[0, -100, 100], pen=QPen(QColor(255,0,0))):
        if x:
            self.xAxis = QGraphicsLineItem(QLineF(x[1], x[0], x[2], x[0]))
            self.xAxis.setPen(pen)
            self.addToGroup(self.xAxis)
        if y:
            self.yAxis = QGraphicsLineItem(QLineF(y[0], y[1], y[0], y[2]))
            self.yAxis.setPen(pen)
            self.addToGroup(self.yAxis)


class Grid(ItemGroupBase):
    """a x,y-grid"""
    def _setup(self, size=(-100, -100, 100, 100), xstep=10, ystep=10, pen=None, z=-10.0):
        self.lines = []
        if not pen:
            pen = QPen(QColor(200,200,200))
            pen.setWidth(0.0)
        for x in range(size[0], size[2]+xstep, xstep):
            self.lines.append(QGraphicsLineItem(QLineF(x, size[1], x , size[3])))
        for y in range(size[1], size[3]+ystep, ystep):
            self.lines.append(QGraphicsLineItem(QLineF(size[0], y, size[2] , y)))
        for l in self.lines:
            l.setPen(pen)
            self.addToGroup(l)
        self.setZValue(z)


class NodeMixIn:
    """to be used with some other QGraphicsItem,
    attached edges must be QGraphicsLineItem or similar,
    endpoint of edge will be moved with the node"""

    def __init__(self, *arg, **kwarg):
        pass

    def addEdge(self, edge, point):
        if not hasattr(self, '_edges'):
            self._edges = []
        self._edges.append((edge, point))

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            if hasattr(self, '_edges'):
                newp = value.toPointF()
                for e, p in self._edges:
                    if p == 1:   e.setLine(QLineF(newp, e.line().p2()))
                    elif p == 2: e.setLine(QLineF(e.line().p1(), newp))
        return QGraphicsItem.itemChange(self, change, value)


class NodeCross(Cross, NodeMixIn):
    """a cross (+) with node behaviour"""
    pass


class NodeCrossX(CrossX, NodeMixIn):
    """a cross (x) with node behaviour"""
    pass


class NodeEllipse(QGraphicsEllipseItem, NodeMixIn):
    """an QGraphicsEllipseItem with node behaviour"""
    pass


class NodeText(QGraphicsTextItem, NodeMixIn):
    """a QGraphicsTextItem with node behaviour"""
    pass
