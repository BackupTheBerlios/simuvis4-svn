#!/usr/bin/env python
# version: $Id$
# this file is part of the SimuVis framework
# author: Joerg Raedler <jr@j-raedler.de>
# license: GPL v2

from distutils.core import setup

import os, sys
        
# there was an error in distutils when building rpms with PYTHONOPTIMIZE set:
if os.environ.has_key('PYTHONOPTIMIZE'):
    del os.environ['PYTHONOPTIMIZE']

longdesc = """SimuVis4 is intended to be a framework / working environment
for scientific programmin in Python, data analysis and
visualisation in 2D/3D. It uses Python, PyQt, PyQwt and VTK.
The program is designed to be very flexible by using a
plugin system for extensions and a lean main program.

SimuVis4 is a major rewrite of an earlier application
and is in the state of alpha software at the moment!
"""

# generate datafile list on the fly
def list_data_files():
    def add_data_path(df, dn, fi):
        if 'CVS' in fi:
            fi.remove('CVS')
        foo = [os.path.join(dn, f) for f in fi if os.path.isfile]
        bar = [os.path.normpath(f) for f in foo if os.path.isfile(f)]
        if bar:
            np = os.path.join('lib', 'SimuVis4', dn[5:])
            df.append((np, bar))
    data_files = []
    data_path = os.path.normpath(os.path.join(os.path.split(__file__)[0], 'data'))
    os.path.walk(data_path, add_data_path, data_files)
    return data_files

def generate_config_file():
    print "Configfile not copied, SimuVis may not run!"
    # FIXME: generate and fill a SimuVis4.ini file, need to know directories
    # Unix (pure)	prefix/lib/python2.0/site-packages
    # Unix (non-pure) exec-prefix/lib/python2.0/site-packages
    # Windows prefix C:\Python
    # Mac OS (pure) prefix:Lib:site-packages
    # Mac OS (non-pure) prefix:Lib:site-packages
    # 
    # --home
    # pure module distribution	home/lib/python	--install-purelib
    # non-pure module distribution	home/lib/python	--install-platlib
    # scripts	home/bin	--install-scripts
    # data	home/share	--install-data
    # 
    # --prefix (UNIX)
    # pure module distribution	prefix/lib/python2.X/site-packages	--install-purelib
    # non-pure module distribution	exec-prefix/lib/python2.X/site-packages	--install-platlib
    # scripts	prefix/bin	--install-scripts
    # data	prefix/share	--install-data
    # 
    # --prefix (Windows)
    # pure module distribution	prefix	--install-purelib
    # non-pure module distribution	prefix	--install-platlib
    # scripts	prefix\Scripts	--install-scripts
    # data	prefix\Data	--install-data
    # 
    # --prefix (Mac OS 9)
    # pure module distribution	prefix:Lib:site-packages	--install-purelib
    # non-pure module distribution	prefix:Lib:site-packages	--install-platlib
    # scripts	prefix:Scripts	--install-scripts
    # data	prefix:Data	--install-data
    pass


args = { 'name' : "SimuVis4",
         'version' : '4.0a3',
         'description' : "Scientific programming, data analysis and visualisation framework",
         'long_description' : longdesc,
         'license' : "GPL",
         'author' : "Joerg Raedler",
         'author_email' : "jr@j-raedler.de",
         'maintainer' : "dezentral gbr Berlin",
         'maintainer_email' : "software@dezentral.de",
         'url' : "http://www.dezentral.de/soft/SimuVis4",
         'download_url' : "http://download.dezentral.de/soft/",
         'classifiers' : ['Development Status :: 5 - Production/Stable',
                           'Intended Audience :: Developers',
                           'Intended Audience :: Science/Research',
                           'License :: Freely Distributable',
                           'License :: Other/Proprietary License',
                           'Programming Language :: Python',
                           'Operating System :: OS Independent',
                           'Topic :: Scientific/Engineering :: Mathematics',
                           'Topic :: Scientific/Engineering :: Visualization',
                           'Topic :: Multimedia :: Graphics'
                           ],
         'packages' : ['SimuVis4', 'SimuVis4/UI'],
         'scripts' : ['bin/SimuVis.py'],
         'data_files' : list_data_files(),
}

#setup(**args)

if 'install' in sys.argv:
    print generate_config_file()
