# encoding: utf-8
# version:  $Id: Quantities.py 276 2008-01-14 17:28:08Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2

"""
RichTypes are classes to hold values of specified types with
some extra information like unit, min/max etc.

"""

import RTypes
try:
    import Qt4Widgets
except ImportError:
    Qt4Widgets = None
