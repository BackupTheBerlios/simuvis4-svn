# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from ConfigParser import SafeConfigParser

class Config(SafeConfigParser):
    """ConfigParser with a flag to show if the configuration was changed
(need to be saved). String option can be evaluated by item
access with a keycfg['section:option']."""

    def __init__(self, defaults=None):
        SafeConfigParser.__init__(self, defaults or {})
        self.changed = False

    def set(self, section, option, value):
        SafeConfigParser.set(self, section, option, value)
        self.changed = True

    def add_section(self, section):
        SafeConfigParser.add_section(self, section)
        self.changed = True

    def remove_option(self, section, option):
        SafeConfigParser.remove_option(self, section, option)
        self.changed = True
        
    def remove_section(self, section):
        SafeConfigParser.remove_section(self, section)
        self.changed = True
        
    def set_def(self, section, option, value):
        if not self.has_option(section, option):
            self.set(section, option, value)

    def __getitem__(self, n):
        section, option = n.split(':')
        return self.get(section, option)
