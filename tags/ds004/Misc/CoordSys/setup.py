#!/usr/bin/env python
# 	$Id: setup.py,v 1.15 2003-08-10 13:34:19 joerg Exp $	

from distutils.core import setup, Extension

# ------ no changes below! If you need to change, it's a bug! -------
version = '0.52'
mac = [('CSYSVERSION', version)]

# there is an error in distutils when building rpms with PYTHONOPTIMIZE set:
import os, sys
if os.environ.has_key('PYTHONOPTIMIZE'):
    del os.environ['PYTHONOPTIMIZE']


longdesc = """
CoordSys is for the fast transformation of points between
cartesian coordinate systems. It's usually used to transform points
from 3D to 2D and back.
"""

args = { 'name' : "CoordSys",
         'version' : version,
         'description' : "cartesian coordinate system transformation",
         'long_description' : longdesc,
         'license' : "LGPL",
         'author' : "Joerg Raedler",
         'author_email' : "jr@j-raedler.de",
         'maintainer' : "Joerg Raedler",
         'maintainer_email' : "jr@j-raedler.de",
         'url' : "http://www.j-raedler.de/pages/software/coordsys.php",
         'py_modules' : ["CoordSys"],
         'ext_modules' : [Extension('cCoordSys', ['cCoordSys.c'],
                                    include_dirs=['.'], define_macros=mac)]
         }
if sys.version_info[:3] >= (2,2,3):
    args['download_url'] = "http://www.j-raedler.de/pages/software/coordsys.php"
    args['classifiers'] = ['Development Status :: 4 - Beta',
                           'Intended Audience :: Developers',
                           'License :: Freely Distributable',
                           'Programming Language :: C',
                           'Operating System :: OS Independent',
                           'Topic :: Scientific/Engineering :: Mathematics'
                           ]
setup(**args)
