# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import Globals, Icons, Errors, UI

import sys, os, traceback
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from UI.ExceptionDialog import Ui_ExceptionDialog
from About import AboutDlg

cfg    = Globals.config
logger = Globals.logger
    

class ExceptionDialog(QDialog, Ui_ExceptionDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        pmf = os.path.join(cfg['main:system_picture_path'], 'stop1.png')
        self.IconLabel.setPixmap(QPixmap(pmf))


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        
        self.hideExceptions = cfg.getboolean('main', 'hide_exceptions')
        if cfg.has_option('main', 'save_last_exception'):
            self.saveLastException = cfg['main:save_last_exception']
        else:
            self.saveLastException= None
        sys.excepthook = self.showException

        iconFile = os.path.join(cfg['main:system_picture_path'], cfg['main:application_icon'])
        self.setWindowIcon(QIcon(QPixmap(iconFile)))
        self.setWindowTitle(cfg['main:application_name'])

        self.workSpace = QWorkspace(self)
        self.workSpace.setScrollBarsEnabled(True)
        if cfg.has_option('main',  'background_image'):
            bgFile = os.path.join(cfg['main:system_picture_path'], cfg['main:background_image'])
            if os.path.exists(bgFile):
                self.workSpace.setBackground(QBrush(QImage(bgFile)))
        self.setCentralWidget(self.workSpace)

        self.windowMapper = QSignalMapper(self)
        self.connect(self.windowMapper, SIGNAL("mapped(QWidget *)"),
                     self.workSpace, SLOT("setActiveWindow(QWidget *)"))

        self._initActions()

        if not cfg.getboolean('main', 'disable_main_menu'):
            self._initMenus()

        self.statusBar().showMessage(QCoreApplication.translate('MainWin', 'Ready'), 5000)


    def _initActions(self):
        self.separatorAction = QAction(self)
        self.separatorAction.setSeparator(True)

        self.fileExecAction = QAction(QIcon(QPixmap(Icons.fileRun)), QCoreApplication.translate('MainWin', 'E&xecute scipt'), self)
        self.fileExecAction.setShortcut(QCoreApplication.translate('MainWin', 'Ctrl+E'))
        self.fileExecAction.setStatusTip(QCoreApplication.translate('MainWin', 'Execute python script'))
        self.connect(self.fileExecAction, SIGNAL("triggered()"), self.executeFile)

        self.filePrintAction = QAction(QIcon(QPixmap(Icons.filePrint)), QCoreApplication.translate('MainWin', '&Print'), self)
        self.filePrintAction.setShortcut(QCoreApplication.translate('MainWin', "Ctrl+P"))
        self.filePrintAction.setStatusTip(QCoreApplication.translate('MainWin', 'Print window contents'))
        self.connect(self.filePrintAction, SIGNAL("triggered()"), self.printWindow)

        self.fileRestartAction = QAction(QCoreApplication.translate('MainWin', '&Restart'), self)
        self.fileRestartAction.setShortcut(QCoreApplication.translate('MainWin', "Ctrl+R"))
        self.fileRestartAction.setStatusTip(QCoreApplication.translate('MainWin', 'Print window contents'))
        self.connect(self.fileRestartAction, SIGNAL("triggered()"), self.restartApplication)

        self.fileExitAction = QAction(QIcon(QPixmap(Icons.fileExit)), QCoreApplication.translate('MainWin', '&Quit'), self)
        self.fileExitAction.setShortcut(QCoreApplication.translate('MainWin', "Ctrl+Q"))
        self.fileExitAction.setStatusTip(QCoreApplication.translate('MainWin', 'Quit application'))
        self.connect(self.fileExitAction, SIGNAL("triggered()"), self.exitApplication)

        self.winTileAction = QAction(QCoreApplication.translate('MainWin', "&Tile"), self)
        self.winTileAction.setStatusTip(QCoreApplication.translate('MainWin', "Tile the windows"))
        self.connect(self.winTileAction, SIGNAL("triggered()"), self.workSpace.tile)

        self.winFullScreenAction = QAction(QCoreApplication.translate('MainWin', "&Fullscreen (main window)"), self)
        self.winFullScreenAction.setShortcut(QCoreApplication.translate('MainWin', "F11"))
        self.winFullScreenAction.setStatusTip(QCoreApplication.translate('MainWin', "Toggle fullscreen appearance of main window"))
        self.connect(self.winFullScreenAction, SIGNAL("triggered()"), self.toggleFullScreen)

        self.winCascadeAction = QAction(QCoreApplication.translate('MainWin', "&Cascade"), self)
        self.winCascadeAction.setStatusTip(QCoreApplication.translate('MainWin', "Cascade the windows"))
        self.connect(self.winCascadeAction, SIGNAL("triggered()"),
                     self.workSpace.cascade)

        self.winMaximizeAction = QAction(QCoreApplication.translate('MainWin', "&Maximize / Minimize"), self)
        self.winMaximizeAction.setShortcut(QCoreApplication.translate('MainWin', "Ctrl+M"))
        self.winMaximizeAction.setStatusTip(QCoreApplication.translate('MainWin', "Show current window maximized, minimized or normal"))
        self.connect(self.winMaximizeAction, SIGNAL("triggered()"),
                     self.maximizeCurrentWindow)

        self.winArrangeAction = QAction(QCoreApplication.translate('MainWin', "Arrange &icons"), self)
        self.winArrangeAction.setStatusTip(QCoreApplication.translate('MainWin', "Arrange the icons"))
        self.connect(self.winArrangeAction, SIGNAL("triggered()"),
                     self.workSpace.arrangeIcons)

        self.winNextAction = QAction(QCoreApplication.translate('MainWin', "Ne&xt"), self)
        self.winNextAction.setShortcut(QCoreApplication.translate('MainWin', "Ctrl+>"))
        self.winNextAction.setStatusTip(QCoreApplication.translate('MainWin', "Move the focus to the next window"))
        self.connect(self.winNextAction, SIGNAL("triggered()"),
                     self.workSpace.activateNextWindow)

        self.winPreviousAction = QAction(QCoreApplication.translate('MainWin', "Pre&vious"), self)
        self.winPreviousAction.setShortcut(QCoreApplication.translate('MainWin', "Ctrl+<"))
        self.winPreviousAction.setStatusTip(QCoreApplication.translate('MainWin', "Move the focus to the previous window"))
        self.connect(self.winPreviousAction, SIGNAL("triggered()"),
                     self.workSpace.activatePreviousWindow)

        self.helpAction = QAction(QIcon(), QCoreApplication.translate('MainWin', '&Help'), self)
        self.helpAction.setShortcut(QCoreApplication.translate('MainWin', "F1"))
        self.helpAction.setStatusTip(QCoreApplication.translate('MainWin', 'Help'))
        self.connect(self.helpAction, SIGNAL("triggered()"), self.help)

        self.helpAboutAction = QAction(QIcon(), QCoreApplication.translate('MainWin', '&About ...'), self)
        self.helpAboutAction.setStatusTip(QCoreApplication.translate('MainWin', 'Info about this application'))
        self.connect(self.helpAboutAction, SIGNAL("triggered()"), self.about)

        self.helpHomepageAction = QAction(QIcon(), QCoreApplication.translate('MainWin', 'Open homepage'), self)
        self.helpHomepageAction.setStatusTip(QCoreApplication.translate('MainWin', 'Open application homepage in broweser'))
        self.connect(self.helpHomepageAction, SIGNAL("triggered()"), self.showHomepage)

    def _initMenus(self):
        self.fileMenu = self.menuBar().addMenu(QCoreApplication.translate('MainWin', '&File'))
        self.fileMenu.addAction(self.fileExecAction)
        self.fileMenuSeparator = self.fileMenu.addSeparator()

        self.fileMenu.addAction(self.filePrintAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileRestartAction)
        self.fileMenu.addAction(self.fileExitAction)

        self.toolsMenu = self.menuBar().addMenu(QCoreApplication.translate('MainWin', '&Tools'))

        self.windowMenu = self.menuBar().addMenu(QCoreApplication.translate('MainWin', '&Window'))
        self.connect(self.windowMenu, SIGNAL("aboutToShow()"), self.prepareWindowMenu)

        self.plugInMenu = self.menuBar().addMenu(QCoreApplication.translate('MainWin', '&PlugIns'))

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(QCoreApplication.translate('MainWin', '&Help'))
        self.helpMenu.addAction(self.helpAction)
        self.helpMenu.addAction(self.helpHomepageAction)
        self.helpMenu.addAction(self.helpAboutAction)
        # do it one time so the actions are registered at the main window
        self.prepareWindowMenu()


    def lateInit(self, *args):
        splashScreen = Globals.mainModule.splashScreen
        def progress(msg=None):
            if splashScreen and msg:
                splashScreen.showMessage(msg)
            if Globals.application.hasPendingEvents():
                Globals.application.processEvents()

        if not cfg.getboolean('main', 'disable_log_window'):
            progress(QCoreApplication.translate('MainWin', 'Starting logging system'))
            from SimuVis4.LogWin import LogWindow
            self.logWin = LogWindow(self.workSpace)
            self.workSpace.addWindow(self.logWin)
            Globals.startLogBuffer.setTarget(self.logWin.handler)
            Globals.startLogBuffer.flush()
            Globals.logger.addHandler(self.logWin.handler)
            Globals.logger.removeHandler(Globals.startLogHandler)
            Globals.logger.removeHandler(Globals.startLogBuffer)
            self.toolsMenu.addAction(self.logWin.toggleVisibleAction)
            if not cfg.getboolean('main', 'hide_log_window'):
                self.logWin.toggleVisibleAction.setChecked(True)

        progress(QCoreApplication.translate('MainWin', 'Starting plugin manager'))
        from SimuVis4.PlugInManager import PlugInManager
        self.plugInManager =  PlugInManager()
        self.plugInManager.loadAllFromFolder(cfg['main:system_plugin_path'])
        if cfg.has_option('main', 'user_plugin_path'):
            self.plugInManager.loadAllFromFolder(cfg['main:user_plugin_path'])

        if not cfg.getboolean('main', 'disable_plugin_browser'):
            progress(QCoreApplication.translate('MainWin', 'Starting plugin browser'))
            from SimuVis4.PlugInBrowser import PlugInBrowser
            self.plugInBrowserWin = PlugInBrowser(self.workSpace)
            self.workSpace.addWindow(self.plugInBrowserWin)
            self.plugInMenu.addAction(self.plugInBrowserWin.toggleVisibleAction)
            if not cfg.getboolean('main', 'hide_plugin_browser'):
                self.plugInBrowserWin.toggleAction.setChecked(True)
            self.plugInMenu.addAction(self.separatorAction)

        progress(QCoreApplication.translate('MainWin', 'Initializing Plugins'))
        self.plugInManager.initializePlugIns(progress)

        from SimuVis4.Executor import ExecutorQt
        self.executor = ExecutorQt()
        Globals.executor = self.executor

        if not cfg.getboolean('main', 'disable_task_browser'):
            progress(QCoreApplication.translate('MainWin', 'Starting task browser'))
            from SimuVis4.TaskBrowser import TaskBrowser
            self.taskBrowserWin = TaskBrowser(self.workSpace)
            self.workSpace.addWindow(self.taskBrowserWin)
            self.toolsMenu.addAction(self.taskBrowserWin.toggleVisibleAction)
            if not cfg.getboolean('main', 'hide_task_browser'):
                self.taskBrowserWin.toggleAction.setChecked(True)

        if not cfg.getboolean('main', 'disable_help_browser'):
            progress(QCoreApplication.translate('MainWin', 'Starting help system'))
            from SimuVis4.HelpBrowser import HelpBrowser
            self.helpBrowser = HelpBrowser(self.workSpace)
            self.workSpace.addWindow(self.helpBrowser)
        else:
            self.helpBrowser = None

        logger.info(QCoreApplication.translate('MainWin', 'Main: startup succeeded'))

        if splashScreen:
            splashScreen.finish(self)

        if Globals.startScript:
            self.executeFile(Globals.startScript)
        elif cfg.has_option('main', 'system_start_script'):
            self.executeFile(cfg['main:system_start_script'])


    def executeFile(self, fn=None):
        if fn:
            self.executor.runFilename(unicode(fn))
        else:
            fn = QFileDialog.getOpenFileName(self, QCoreApplication.translate('MainWin', "Select file to execute"),
                Globals.defaultFolder)
            if not fn.isEmpty():
                fileName = unicode(fn)
                Globals.defaultFolder, tmp = os.path.split(fileName)
                self.executor.runFilename(fileName)
                self.statusBar().showMessage(unicode(QCoreApplication.translate('MainWin', 'Executing file %s')) % fileName, 5000)
            else:
                self.statusBar().showMessage(QCoreApplication.translate('MainWin', 'Loading aborted'), 5000)


    def help(self, context=None, topic=None):
        if self.helpBrowser:
            self.helpBrowser.showHelp(context, topic)


    def showException(self, t, v, tb):
        tbtmp = ''.join(traceback.format_tb(tb))
        if self.saveLastException:
            f = open(self.saveLastException, 'w')
            f.write('%s\n%s\n%s\n' % (t,v,tbtmp))
            f.close()
        logger.error(unicode(QCoreApplication.translate('MainWin', 'Main: uncatched internal exception: %s: %s:\n%s')), t, v, tbtmp)
        if not self.hideExceptions:
            if not hasattr(self, 'exceptionDlg'):
                self.exceptionDlg = ExceptionDialog(self)
                self.connect(self.exceptionDlg.ExitButton, SIGNAL("pressed()"), self.exitApplication)
                self.connect(self.exceptionDlg.KillButton, SIGNAL("pressed()"), self.killApplication)
                self.connect(self.exceptionDlg.RestartButton, SIGNAL("pressed()"), self.restartApplication)
            et = unicode(t)
            if et.find('<type ') == 0:
                et = et[7:-2]
            elif et.find('<class ') == 0:
                et = et[8:-2]
            txt = '<font color="#ff0000"><b>%s: </b><i>%s</i><br></font><i>(%s)</i>' % (et, t.__doc__, v)
            self.exceptionDlg.MainLabel.clear()
            self.exceptionDlg.MainLabel.setText(txt)
            self.exceptionDlg.TracebackView.clear()
            self.exceptionDlg.TracebackView.append(tbtmp)
            self.exceptionDlg.show()


    def about(self):
        aboutDlg = AboutDlg(self)
        aboutDlg.setWindowTitle(cfg['main:application_name'])
        aboutDlg.show()


    def showHomepage(self):
        if cfg.has_option('main', 'application_homepage'):
            url = cfg['main:application_homepage']
        else:
            url = 'http://www.simuvis.de/'
        QDesktopServices.openUrl(QUrl(url))


    def printWindow(self):
        m = self.workSpace.activeWindow()
        if (m):
          m.printWindow(None)


    def prepareWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.winFullScreenAction)
        self.windowMenu.addAction(self.winMaximizeAction)
        self.windowMenu.addAction(self.winTileAction)
        self.windowMenu.addAction(self.winCascadeAction)
        self.windowMenu.addAction(self.winArrangeAction)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.winNextAction)
        self.windowMenu.addAction(self.winPreviousAction)

        windows = self.workSpace.windowList()
        windows =  [w for w in windows if not w.isHidden()]
        if len(windows) != 0:
            self.windowMenu.addAction(self.separatorAction)
        for child in windows:
            action = self.windowMenu.addAction(child.windowTitle())
            action.setCheckable(True)
            action.setChecked(child == self.activeMdiChild())
            self.connect(action, SIGNAL("triggered()"),
                         self.windowMapper, SLOT("map()"))
            self.windowMapper.setMapping(action, child)


    def activeMdiChild(self):
        return self.workSpace.activeWindow()


    def findMdiChild(self, name):
        for window in self.workSpace.windowList():
            if window.windowTitle() == name:
                return window
        return None


    def windowsMenuActivated(self, sid):
        w = self.workSpace.windowList()[sid]
        if (w):
            w.showNormal()
            w.setFocus()


    def maximizeCurrentWindow(self):
        w = self.activeMdiChild()
        if w:
            s = w.windowState()
            if (s & Qt.WindowMinimized):
                w.showNormal()
            elif (s & Qt.WindowMaximized):
                w.showMinimized()
            else:
                w.showMaximized()


    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


    def propagateShutdown(self):
        """Ask all components if a shutdown is ok """
        # FIXME: more shutdown propagation!
        if self.plugInManager.shutdownOk():
            self.plugInManager.shutdown()
        else:
            return False
        return True


    def restartApplication(self):
        if not self.propagateShutdown():
            return
        e, a = Globals.exeFile, Globals.exeArgs
        if sys.platform.startswith('linux'):
            a[0] = e
            a.insert(0, 'python')
        elif sys.platform == 'win32':
            a[0] = '"%s"' % e
            a.insert(0, 'python')
        else:
            raise Errors.FeatureMissingError(unicode(QCoreApplication.translate('MainWin', 'restarting on platform "%s" not yet supported')) % sys.platform)
        os.execv(sys.executable, a)


    def exitApplication(self):
        if self.propagateShutdown():
            # FIXME: hide shutdown-related exception like logger-IOError on windows
            self.hideExceptions = True
            Globals.application.closeAllWindows()


    def killApplication(self):
        sys.exit(1)
