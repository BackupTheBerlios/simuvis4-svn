# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from PyQt4.QtGui import QDialog, QPixmap
from PyQt4.QtCore import QCoreApplication, PYQT_VERSION, PYQT_VERSION_STR, qVersion
from UI.AboutDialog import Ui_AboutDialog
import Globals, Misc, os, sys


txtAbout = QCoreApplication.translate('SimuVis',
"""
<h1>SimuVis4</h1>
<p>SimuVis is designed as a common platform for applications<br>
with a focus on scientific programming and visualisation.</p>
<p>SimuVis can be used as a working environment for python programmers.<br>
The functionality can be extended by plugins.</p>
<p>SimuVis is based on python, Qt, PyQt and other toolkits<br>
like Qwt and Vtk.</p>
""")


txtAuthors = QCoreApplication.translate('SimuVis',
"""
<p>SimuVis4 and its ancestors are written by <b>Joerg Raedler</b> <i>(jr@j-raedler.de)</i>.<br></p>
<p>You can find more information at http://www.simuvis.de/.</p>

<p>Please keep in mind that SimuVis needs other software to work.<br>
I'd like to thank the authors of python, Qt and innumerable <br>
other contributors to free software projects.<p>
""")


licenseFile = os.path.join(Globals.config['main:system_data_path'], 'GPLv2.txt')
txtLicense = open(licenseFile, 'r').read()


def getLinuxDistro():
    """try to guess the name and version of the distribution
    more info at: http://linuxmafia.com/faq/Admin/release-files.html"""
    relFiles = {
        'Arch Linux': 		('/etc/arch-release',),
        'Arklinux': 		('/etc/arklinux-release',),
        'Fedora Core': 		('/etc/fedora-release',),
        'Gentoo Linux': 	('/etc/gentoo-release'),
        'Mandriva/Mandrake Linux': ('/etc/mandriva-release', '/etc/mandrake-release', '/etc/mandakelinux-release'),
        'Red Hat Linux':	('/etc/redhat-release', '/etc/redhat_version'),
        'Debian Linux':		('/etc/debian_version', '/etc/debian_release'),
        'Slackware Linux':	('/etc/slackware-version', '/etc/slackware-release'),
        'SUSE Linux':		('/etc/SuSE-release', '/etc/novell-release'),
        'Ubuntu Linux':		('/etc/lsb-release')
    }
    for n, ff in relFiles.items():
        for f in ff:
            if os.path.isfile(f):
                return '%s [%s]' % (n, open(f).readline())
    return 'Linux [unknown]'


def getWindowsVersion():
    """try to guess the name and version of windows"""
    ma, mi, bu, pl, tx = sys.getwindowsversion()
    # FIXME: check codes, what about Vista?
    versions = {
        (1, 4, 0): "95",
        (1, 4, 10): "98",
        (1, 4, 90): "ME",
        (2, 4, 0):  "NT",
        (2, 5, 0):  "2000",
        (2, 5, 1):  "XP"}
    platforms = ('win32s', '9x/ME', 'NT/2000/XP')
    version = versions.get((pl, ma, mi),
        'Windows %s %d.%d' %(platforms[pl], ma, mi))
    version_string = 'Windows %s (build %s, %s)' % (version, bu, tx)
    return version, version_string


class AboutDlg(QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        pmf = os.path.join(Globals.config['main:system_picture_path'], 'Icon128.png')
        self.AboutPicture.setPixmap(QPixmap(pmf))
        self.AboutText.setText(txtAbout)
        self.AuthorsView.setText(txtAuthors)
        self.LicenseView.setPlainText(txtLicense)

        self.collectVersions()

    def collectVersions(self):
        csw = Misc.Switcher(0, "#ffffff", "#eeeeee")
        buf = ['<table><tr bgcolor="#dddddd"><th>Component/Library</th><th>Version</th></tr>']
        buf.append('<tr bgcolor="%s"><td>SimuVis4</td><td>%s</td></tr>' % (csw(), Globals.version_string))
        buf.append('<tr bgcolor="%s"><td>Python</td><td>%s | %s</td></tr>' % \
            (csw(), '.'.join([str(i) for i in sys.version_info]), sys.version))
        buf.append('<tr bgcolor="%s"><td>PyQt</td><td>%s | %s</td></tr>' % (csw(), PYQT_VERSION_STR, PYQT_VERSION))
        buf.append('<tr bgcolor="%s"><td>Qt</td><td>%s</td></tr>' % (csw(), qVersion()))

        if sys.modules.has_key('vtk'):
            v = sys.modules['vtk'].vtkVersion.GetVTKVersion()
            vl = sys.modules['vtk'].vtkVersion.GetVTKSourceVersion()
            buf.append('<tr bgcolor="%s"><td>Vtk</td><td>%s | %s</td></tr>' % (csw(), v, vl))

        if sys.modules.has_key('OpenGL'):
            v = sys.modules['OpenGL'].__version__
            buf.append('<tr bgcolor="%s"><td>PyOpenGL</td><td>%s</td></tr>' % (csw(), v))

        for p in Globals.mainWin.plugInManager.plugIns.values():
            buf.append('<tr bgcolor="%s"><td>PlugIn: %s</td><td>%s</td></tr>' % (csw(), p.name, p.version))

        if sys.platform == 'linux2':
            n = QCoreApplication.translate('AboutDlg', 'Operating System')
            d = getLinuxDistro()
            k = os.popen('uname -o -s -r', 'r').readlines()[0]
            buf.append('<tr bgcolor="%s"><td>%s</td><td>%s (%s)</td></tr>' % (csw(), n, d, k))

        if sys.platform == 'win32':
            n = QCoreApplication.translate('AboutDlg', 'Operating System')
            v, vs = getWindowsVersion()
            buf.append('<tr bgcolor="%s"><td>%s</td><td>%s</td></tr>' % (csw(), n, vs))

        buf.append('</table>')
        self.VersionView.setHtml('\n'.join(buf))

