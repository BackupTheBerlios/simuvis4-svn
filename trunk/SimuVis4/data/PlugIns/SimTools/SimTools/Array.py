# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework


class ArrayData:
    """abstract array class, may be used to transfer array data"""

    mimetype = "applicaton/x-sv4-arraydata"

    def __init__(self, data=None, name='', attr={}, axis=None):
        self.data = data
        self.name = name
        self.attr = attr
        self.axis = axis

    def __repr__(self):
        return '<ArrayData name="%s"/>' % self.name
