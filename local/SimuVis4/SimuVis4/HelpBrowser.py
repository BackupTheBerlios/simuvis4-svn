# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import Globals, sys, os, threading, mimetypes, posixpath, urllib, urlparse
from PyQt4.QtGui import QWidget, QIcon, QPixmap, QTextBrowser, QDesktopServices
from PyQt4.QtCore import QCoreApplication, QUrl
from SubWin import SubWindow
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
try:
    from docutils.core import publish_string
    from docutils.writer import html4css1
except ImportError:
    publish_string = None

## FIXME: internal browser disabled for now
##useExternalBrowser = Globals.config.getboolean('main', 'help_browser_external')
useExternalBrowser = True

helpPath   = os.path.join(Globals.config['main:system_help_path'], Globals.config['main:i18n_language'])
helpPathEn = os.path.join(Globals.config['main:system_help_path'], 'en')
helpURL = 'http://127.0.0.1:%d/simuvis/index.html' % Globals.config.getint('main', 'help_server_port')

internalBrowser = None
serverThread = None


# paths should be:
# /simuvis/path_under_doc_path
# /plugin/FooBar/path_under_module_doc
# /python/module
# /quit - quit the server thread
class HelpRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def do_GET(self):
        """Serve a GET request."""
        path = urlparse.urlparse(self.path)[2]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        unit = words[0].lower()
        c = None
        if unit == 'simuvis':
            mt, c = self.getMain(words[1:])
        elif unit == 'plugin':
            mt, c = self.getPlugIn(words[1:])
        elif unit == 'python':
            mt, c = self.getPython(words[1:])
        elif unit == 'quit':
            self.send_response(200)
            c = "Shutting down..."
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", len(c))
            self.end_headers()
            self.wfile.write(c)
            self.wfile.close()
            sys.exit(0)
        if not c:
            self.send_error(404, "File not found")
            return
        self.send_response(200)
        self.send_header("Content-type", mt)
        self.send_header("Content-Length", len(c))
        self.end_headers()
        self.wfile.write(c)


    def getMain(self, w):
        p = os.path.join(helpPath, *w)
        if not os.path.exists(p):
            p = os.path.join(helpPathEn, *w)
            if not os.path.exists(p):
                return None, None
        base, ext = os.path.splitext(p)
        mimetype = self.mimeType(ext)
        p = open(p, 'rb').read()
        # FIXME: on-the-fly processing of rest
        #if ext == '.txt' and publish_string:
        #    mimetype = 'text/html'
        #    p = publish_string(p, writer=html4css1.Writer())
        return mimetype, p


    def getPlugIn(self, w):
        return 'text/plain', 'Dummy - sorry!'


    def getPython(self, w):
        return 'text/plain', 'Dummy - sorry'


    def mimeType(self, ext):
        # FIXME: !
        return 'text/html' 

    def log_message(self, fmt, *args):
        Globals.logger.debug('Help: Server: %s', fmt % args)



def runServer(port):
    httpd = HTTPServer(('127.0.0.1', port), HelpRequestHandler)
    httpd.serve_forever()



def startServer():
    global serverThread
    serverThread = threading.Thread(target=runServer, args=(Globals.config.getint('main', 'help_server_port'),))
    serverThread.start()



def stopServer():
    global serverThread
    if serverThread:
        try:
            urllib.urlretrieve('http://127.0.0.1:%d/quit' % Globals.config.getint('main', 'help_server_port'))
        except:
            pass
    serverThread = None



def showHelp(url=helpURL):
    global internalBrowser
    if not serverThread:
        startServer()
    if useExternalBrowser:
        QDesktopServices.openUrl(QUrl(url))
    else:
        if not internalBrowser:
            internalBrowser = HelpBrowser(Globals.mainWin.workSpace)
            Globals.mainWin.workSpace.addSubWindow(internalBrowser)
        internalBrowser.browser.setSource(QUrl(url))
        internalBrowser.show()



class HelpBrowser(SubWindow):

    def __init__(self, parent):
        SubWindow.__init__(self, parent)
        icon = QIcon(QPixmap(os.path.join(Globals.config['main:system_picture_path'], 'help.xpm')))
        self.setWindowIcon(icon)
        self.setWindowTitle(QCoreApplication.translate('HelpBrowser', 'Help Browser'))
        self.browser = QTextBrowser(self)
        self.setWidget(self.browser)
        # FIXME: need to implement open external URLs
