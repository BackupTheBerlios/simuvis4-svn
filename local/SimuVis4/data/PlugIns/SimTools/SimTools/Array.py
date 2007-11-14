# encoding: latin-1
# version:  $Id: Array.py,v 1.1 2007/08/23 12:49:03 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
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
