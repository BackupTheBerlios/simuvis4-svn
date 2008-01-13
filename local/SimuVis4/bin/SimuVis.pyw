#!/usr/bin/env python
# encoding: utf-8
# version:  $Id: SimuVis.pyw 43 2007-11-14 20:29:17Z jraedler $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import sys, os

usage = """
Usage: %s [options]
    options include:
        -h
        --help
            print this help and exit
        -f
        --fullscreen
            start in fullscreen mode
        -m
        --maximized
            start with maximized window
        -e script
        --execute=script
            run the python script
        -c inifile
        --config=inifile
            load inifile instead of system and user configfiles
        -l lang
        --language=lang
            use language lang if available
""" % sys.argv[0]

svn_revision = 261 # this line is changed automagically by mark_svn_rev.py
version_info = (4, 0, svn_revision)
version_string = '4.0.%03d' % svn_revision

print "This is SimuVis4 (%s) by Joerg Raedler, starting ..." % version_string

def errorExit(h, *msg):
    try:
        # try to show a tkinter dialog box
        import tkMessageBox
        tkMessageBox.showerror('SimuVis4 error: %s' % h, '\n'.join(msg))
    except:
        # give a text message instead
        print "\n>> SimuVis4 - Error: %s <<" % h
        for m in msg:
            print m
        print
    sys.exit(1)

### check for needed modules and versions
if sys.version_info < (2, 3, 0):
    errorExit("wrong version", "please use python 2.3 or better!")
try:
    import PyQt4
    import PyQt4.QtGui as qtgui
    import PyQt4.QtCore as qtcore
except:
    errorExit("module missing", "PyQt4 not found, please install PyQt4")

p = sys.argv[0]
if not os.path.isabs(p):
    p = os.path.normpath(os.path.join(os.getcwd(), p))
exeFile = os.path.realpath(p)
exeArgs = sys.argv[:]
binDir = os.path.split(exeFile)[0]
baseDir = os.path.split(binDir)[0]

### Options
startScript = None
forceConfig = None
language = None

import getopt
if os.environ.has_key('SIMUVIS4_OPTIONS'):
    tmp = os.environ['SIMUVIS4_OPTIONS'].split()
    tmp.reverse()
    for o in tmp:
        sys.argv.insert(1, o)
sopt = 'hfme:c:l:'
lopt  = ['help', 'fullscreen', 'maximized', 'execute=', 'config=', 'language=']
# first let qt delete qt-specific options...
application = qtgui.QApplication(sys.argv)
try:
    opts, args = getopt.getopt(sys.argv[1:], sopt, lopt)
except getopt.GetoptError:
    errorExit("wrong options", usage)

fullScreen = False
maxiScreen = False

for o, a in opts:
    if o in ('-h', '--help'):
        print usage
        sys.exit(0)
    if o in ('-e', '--execute'):
        startScript = a
    if o in ('-c', '--config'):
        forceConfig = a
    if o in ('-l', '--language'):
        language = a
    if o in ('-f', '--fullscreen'):
        fullScreen = True
    if o in ('-m', '--maximized'):
        maxiScreen = True

### Globals and some startup things
if os.path.exists(os.path.join(baseDir, 'setup.py')):
    print "local installation: temporary adding folder '%s' to the module search path." % baseDir
    sys.path.insert(0, baseDir)
try:
    import SimuVis4
except ImportError:
    errorExit("Module not found", "Could not import the main SimuVis4 module package!",
            "Make sure SimuVis is installed correctly.",
            "Let your $PYTHONPATH include the SimuVis4 module package folder!")

glb = SimuVis4.Globals
glb.startScript = startScript
glb.exeFile = exeFile
glb.exeArgs = exeArgs


# i18n - install translators
if language or glb.config.has_option('main', 'i18n_language'):
    if not language:
        language = glb.config.get('main', 'i18n_language')
    if not language == 'en':
        translatorQt = qtcore.QTranslator()
        if translatorQt.load('qt_%s' % language, qtcore.QLibraryInfo.location(qtcore.QLibraryInfo.TranslationsPath)):
            application.installTranslator(translatorQt)
        else:
            glb.logger.warning('Main: Qt4\'s translation for "%s" not found, some dialogs will be untranslated', language)
        translator = qtcore.QTranslator()
        if translator.load(language, glb.config.get('main', 'system_language_path')):
            application.installTranslator(translator)
        else:
            glb.logger.error('Main: translation "%s" not found, falling back to default language', language)
    glb.language = language
else:
    glb.language = None

# splash
if glb.config.has_option('main', 'disable_splash') and not glb.config.getboolean('main', 'disable_splash'):
    splash = os.path.join(glb.config.get('main', 'system_picture_path'), glb.config.get('main', 'splash_image'))
    if os.path.isfile(splash):
        splashScreen = qtgui.QSplashScreen(qtgui.QPixmap(splash), qtcore.Qt.WindowStaysOnTopHint)
        splashScreen.show()
        splashScreen.showMessage(qtcore.QCoreApplication.translate('SimuVis', 'Starting SimuVis'))
    else:
        glb.logger.error(unicode(qtcore.QCoreApplication.translate('SimuVis', 'Main: splash screen image not found: "%s"')), splash)
        splashScreen = None
else:
    splashScreen = None


### MainWindow
from SimuVis4.MainWin import MainWindow

mainWin = MainWindow()
pyver = '.'.join([str(i) for i in sys.version_info[:3]])
mainWin.setWindowTitle("%s | %s | %s@%s | Python %s" % (glb.appName, version_string, glb.userName, glb.hostName, pyver))

if fullScreen:
    mainWin.showFullScreen()
elif maxiScreen:
    mainWin.showMaximized()
else:
    mainWin.show()

application.connect(application, qtcore.SIGNAL('lastWindowClosed()'), application, qtcore.SLOT('quit()'))
qtcore.QTimer().singleShot(0, mainWin.lateInit)

# store main parts
glb.mainWin = mainWin
glb.application = application

# let's rock!
sys.exit(application.exec_())
