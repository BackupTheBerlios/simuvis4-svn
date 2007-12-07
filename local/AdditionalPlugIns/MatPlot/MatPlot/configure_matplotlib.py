#!/usr/bin/env python
# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import sys, os

doit = '--doit' in sys.argv

if not doit:
    print """
*************************************************************
*    DEMO MODE                                              *
* This script does not change any existing files unless you *
* start it with the option "--doit".                        *
* Use the script at your own risk!                          *
* Changed files will be stored as <filename>.new to let you *
* view the changes without overwritng the original files.   *
*************************************************************
"""
else:
    print """
*************************************************************
*    CHANGE MODE                                            *
* This script will make permanent changes to files.         *
* Old versions are stored as <filename>.old to be recoved   *
* in case of errors.                                        *
*************************************************************
"""

import matplotlib, matplotlib.backends
modules = [matplotlib, matplotlib.backends]
try:
    import matplotlib.rcsetup
    modules.append(matplotlib.rcsetup)
except ImportError:
    pass

for m in modules:
    ff = m.__file__
    if ff.endswith('.pyo') or ff.endswith('.pyc'):
        ff = ff[:-1]
    if not os.path.exists(ff):
        raise Exception("Error: File %s not found!" % (ff,))
    ffnew = ff+'.new'
    ffold = ff+'.old'
    c = open(ff, 'r').read()
    if 'SV4Agg' in c:
        print "Looks like %s is already modified, skipping!" % (ff,)
    else:
        print "Modifying %s:" % (ff,)
        print "Generating", ffnew
        open(ff+'.new', 'w').write(c.replace("'Qt4Agg'", "'Qt4Agg', 'SV4Agg'"))
        if doit:
            print "Moving %s\n  to %s" % (ff, ffold)
            os.rename(ff, ffold)
            print "Moving %s\n  to %s" % (ffnew, ff)
            os.rename(ffnew, ff)
    print

be = 'backend_sv4agg.py'
src = os.path.join(os.path.split(__file__)[0], be)
if not os.path.isabs(src):
    src = os.path.join(os.getcwd(), src)
dst = os.path.join(os.path.split(matplotlib.backends.__file__)[0], be)
try:
    if doit:
        if os.path.exists(dst):
            os.remove(dst)
        os.symlink(src, dst)
    print "Making link: %s\n  pointing to %s" % (dst, src)
except:
    print "Copying %s\n  to %s" % (src, dst)
    if doit:
        open(dst, 'w').write(open(src, 'r').read())

