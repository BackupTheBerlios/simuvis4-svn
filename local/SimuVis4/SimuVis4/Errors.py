# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from exceptions import *

class SimuVisError(Exception):
    """Unspecified SimuVis error"""
    pass

class FeatureMissingError(SimuVisError):
    """Feature not yet implemented"""
    pass

class ConfigError(SimuVisError):
    """Configuration error"""
    pass

class PlugInError(SimuVisError):
    """PlugIn error"""
    pass

class IOError(SimuVisError):
    """Input/output error"""
    pass

class PlugInMissingError(SimuVisError):
    """PlugIn missing error"""
    pass
