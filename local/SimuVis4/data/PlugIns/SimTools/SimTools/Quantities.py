# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from sets import Set


class Quantity:
    """abstract quantity with a name, a value and a description"""

    mimetype = "applicaton/x-sv4-quantity"

    def __init__(self):
        self.editable = True
        self._v = None

    def __repr__(self):
        return '<%s name="%s" v="%s"/>' % (self.__class__, self.name, self._v)

    def set(self, v):
        self._v = v

    def get(self):
        return self._v

    v = property(get, set)



class Text(Quantity):
    """string quantity """

    def __init__(self, name, v='', **kwarg):
        Quantity.__init__(self)
        self.name = name
        self._v = unicode(v)
        self.descr = kwarg.get('descr', '')
        self.maxLen = kwarg.get('maxLen', None)

    def set(self, v):
        if self.maxLen and len(v) > self.maxLen:
            v = v[:maxLen]
        self._v = unicode(v)

    v = property(Quantity.get, set)



class MLText(Text):
    """multiline string quantity """

    pass



class Choice(Quantity):
    """quantity which value can be one out of a list"""
    def __init__(self, name, v=None, choices=None, **kwarg):
        Quantity.__init__(self)
        self.name = name
        self._v = v
        self.descr = kwarg.get('descr', '')
        self.choices = Set(choices)

    def set(self, v):
        if v in self.choices:
            self._v = v

    v = property(Quantity.get, set)



class MultiChoice(Quantity):
    """quantity which value can be one or more out of a list"""
    def __init__(self, name, v=(), choices=None, **kwarg):
        Quantity.__init__(self)
        self.name = name
        self._v = Set(v)
        self.descr = kwarg.get('descr', '')
        self.choices = Set(choices)

    def set(self, v):
        v = Set(v)
        if v.issubset(self.choices):
            self._v = v

    v = property(Quantity.get, set)



class Bool(Quantity):
    """boolean quantity"""

    def __init__(self, name, v=True, **kwarg):
        Quantity.__init__(self)
        self.name = name
        self._v = bool(v)
        self.descr = kwarg.get('descr', '')

    def set(self, v):
        self._v = bool(v)

    v = property(Quantity.get, set)



class Integer(Quantity):
    """integer quantity"""

    def __init__(self, name, v=0, **kwarg):
        Quantity.__init__(self)
        self.name = name
        self._v = int(v)
        self.descr = kwarg.get('descr', '')
        self.min = None
        self.max = None
        self.step = None
        if 'min' in kwarg:
            self.min = int(kwarg['min'])
        if 'max' in kwarg:
            self.max = int(kwarg['max'])
        if 'step' in kwarg:
            self.step = int(kwarg['step'])
        self.unit = kwarg.get('unit', None)

    def __float__(self):
        return float(self._v)

    def __int__(self):
        return int(self._v)

    def set(self, v):
        self._v = int(v)

    def add(self, v):
        self.set(self._v + v)

    v = property(Quantity.get, set)



class Float(Quantity):
    """float quantity"""

    def __init__(self, name, v=0.0, **kwarg):
        Quantity.__init__(self)
        self.name = name
        self._v = float(v)
        self.descr = kwarg.get('descr', '')
        self.min = None
        self.max = None
        self.step = None
        if 'min' in kwarg:
            self.min = float(kwarg['min'])
        if 'max' in kwarg:
            self.max = float(kwarg['max'])
        if 'step' in kwarg:
            self.step = float(kwarg['step'])
        self.unit = kwarg.get('unit', None)

    def __float__(self):
        return float(self._v)

    def __int__(self):
        return int(self._v)

    def set(self, v):
        self._v = float(v)

    def add(self, v):
        self.set(self._v + v)

    v = property(Quantity.get, set)



class DateTime(Quantity):
    """integer quantity"""

    def __init__(self, name, v=0, **kwarg):
        Quantity.__init__(self)
        self.name = name
        self._v = int(v)
        self.descr = kwarg.get('descr', 'date and time')
        self.min = None
        self.max = None
        if 'min' in kwarg:
            self.min = int(kwarg['min'])
        if 'max' in kwarg:
            self.max = int(kwarg['max'])
        self.unit = kwarg.get('unit', 's')

    def __float__(self):
        return float(self._v)

    def __int__(self):
        return int(self._v)

    def set(self, v):
        self._v = int(v)

    def add(self, v):
        self.set(self._v + v)

    v = property(Quantity.get, set)

