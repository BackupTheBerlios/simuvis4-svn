#!/usr/bin/env python
# version: $Id$
# this file is part of the SimuVis framework
# author: Joerg Raedler <jr@j-raedler.de>
# license: GPL v2

from distutils.core import setup

import os, sys, string

svn_revision = 357 # this line is changed automagically by mark_svn_rev.py
version_info = (4, 0, svn_revision)
version_string = '4.0.%03d' % svn_revision

# there was an error in distutils when building rpms with PYTHONOPTIMIZE set:
if os.environ.has_key('PYTHONOPTIMIZE'):
    del os.environ['PYTHONOPTIMIZE']

longdesc = """
SimuVis4 is intended to be a framework / working environment
for scientific programmin in Python, data analysis and
visualisation in 2D/3D. It uses Python, PyQt, PyQwt and VTK.
The program is designed to be very flexible by using a
plugin system for extensions and a lean main program.

SimuVis4 is a major rewrite of an earlier application
and is in the state of beta software at the moment!
"""

# generate datafile list on the fly
def list_data_files():
    def add_data_path(df, dn, fi):
        if '.svn' in fi:
            fi.remove('.svn')
        foo = [os.path.join(dn, f) for f in fi if os.path.isfile]
        bar = [os.path.normpath(f) for f in foo if os.path.isfile(f)]
        if bar:
            np = os.path.join('lib', 'SimuVis4', dn[5:])
            df.append((np, bar))
    data_files = []
    data_path = os.path.normpath(os.path.join(os.path.split(__file__)[0], 'data'))
    os.path.walk(data_path, add_data_path, data_files)
    return data_files


cfgTemplate = string.Template("""
[main]
# global configuration file of SimuVis4
system_data_path     = ${system_data_path}
""")


def generate_config_file():
    """generate a configfile"""
    name = 'SimuVis4.ini'
    if sys.platform == 'linux2':
        cfg_path = '/etc'
        system_data_path = '/usr/share/SimuVis4'
    elif sys.platform == 'win32':
        cfg_path = ''
        system_data_path = ''
    elif sys.platform == 'macos_x':
        cfg_path = ''
        system_data_path = ''
    else:
        raise 'platform not supported'
    cfg = cfgTemplate.substitute(system_data_path=system_data_path, sep=os.path.sep)
    f = open(name, 'w')
    f.write(cfg)
    f.close()
    return cfg_path, [name]
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


args = { 'name' : "SimuVis4",
         'version' : version_string,
         'description' : "Scientific programming, data analysis and visualisation framework",
         'long_description' : longdesc,
         'license' : "GPL",
         'author' : "Joerg Raedler",
         'author_email' : "jr@j-raedler.de",
         'maintainer' : "Joerg Raedler",
         'maintainer_email' : "jr@j-raedler.de",
         'url' : "http://www.simuvis.de",
         'download_url' : "http://www.simuvis.de/pages/download.php",
         'classifiers' : ['Development Status :: 4 - Beta',
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
         'scripts' : ['bin/SimuVis.pyw', 'bin/SV4ClientRC.pyw'],
         'data_files' : list_data_files(),
}

setup(**args)
