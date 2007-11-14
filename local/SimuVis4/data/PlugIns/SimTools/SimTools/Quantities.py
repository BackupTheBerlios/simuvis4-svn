# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from sets import Set


class Quantity:
    """abstract quantity with a name, a value and a description"""

    mimetype = "applicaton/x-sv4-quantity"

    def __repr__(self):
        return '<%s name="%s" v="%s"/>' % (self.__class__, self.name, self.v)


class Text(Quantity):
    """string quantity """

    def __init__(self, name, v=None, **kwarg):
        self.name = name
        self.v = unicode(v)
        self.descr = kwarg.get('descr', '')
        self.maxLen = kwarg.get('maxLen', None)

    def set(self, v):
        if self.maxLen and len(v) > self.maxLen:
            v = v[:maxLen]
        self.v = unicode(v)


class Choice(Quantity):
    """quantity which value can be one out of a list"""
    def __init__(self, name, v=None, choices=None, **kwarg):
        self.name = name
        self.v = v
        self.descr = kwarg.get('descr', '')
        self.choices = Set(choices)

    def set(self, v):
        if v in self.choices:
            self.v = v


class Bool(Quantity):
    """boolean quantity"""

    def __init__(self, name, v=None, **kwarg):
        self.name = name
        self.v = bool(v)
        self.descr = kwarg.get('descr', '')

    def set(self, v):
        self.v = bool(v)


class ScalarNumberQuantity(Quantity):
    """quantity with a numeric value, unit and others"""

    def __init__(self, name, v=None, **kwarg):
        self.name = name
        self.v = v
        self.descr = kwarg.get('descr', '')
        self.min = kwarg.get('min', -1e+6)
        self.max = kwarg.get('max', 1e+6)
        self.step = kwarg.get('step', 1e-2)
        self.unit = kwarg.get('unit', None)

    def __float__(self):
        return float(self.v)

    def __int__(self):
        return int(self.v)

    def set(self, v):
        self.v = v

    def add(self, v):
        self.set(self.v + v)


class Integer(ScalarNumberQuantity):
    """integer quantity"""

    def set(self, v):
        self.v = int(v)


class Float(ScalarNumberQuantity):
    """float quantity"""

    def set(self, v):
        self.v = float(v)

