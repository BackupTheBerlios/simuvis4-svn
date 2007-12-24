# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import Globals, sys, os, threading, mimetypes, posixpath, urllib, urlparse
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtCore import QCoreApplication, QUrl, QString, QRegExp, QDateTime, SIGNAL
from PyQt4.QtNetwork import QTcpServer, QTcpSocket, QHostAddress

helpPath   = os.path.join(Globals.config['main:system_help_path'], Globals.config['main:i18n_language'])
helpPathEn = os.path.join(Globals.config['main:system_help_path'], 'en')
helpURL = 'http://127.0.0.1:%d/simuvis/index.html' % Globals.config.getint('main', 'help_server_port')

helpServer = None



class HelpServer(QTcpServer):

    def __init__(self, port=Globals.config.getint('main', 'help_server_port')):
        QTcpServer.__init__(self)
        self.disabled = False
        self.listen(QHostAddress(QHostAddress.LocalHost), port)


    def incomingConnection(self, socket):
        if self.disabled:
            return
        s = QTcpSocket(self)
        self.connect(s, SIGNAL('readyRead()'), self.readClient)
        self.connect(s, SIGNAL('disconnected()'), self.discardClient)
        s.setSocketDescriptor(socket)


    def pause(self):
        self.disabled = True


    def resume(self):
        self.disabled = False


    def readClient(self):
        if self.disabled:
            return
        s = self.sender()
        if s.canReadLine():
            tokens = QString(s.readLine()).split(QRegExp("[ \r\n][ \r\n]*"))
            if tokens[0] == "GET":
                path = str(tokens[1])
                Globals.logger.debug("HelpServer: request to %s", path)
                self.doGET(path)
                s.close()
                if s.state() == QTcpSocket.UnconnectedState:
                    del s


    def discardClient(self):
        socket = self.sender()
        socket.deleteLater()


    def doGET(self, path):
        s = self.sender()
        words = path.split('/')
        words = filter(None, words)
        if len(words) == 0:
            # show index page
            mt, c = self.getIndex()
        else:
            unit = words[0].lower()
            c = None
            if unit == 'simuvis':
                # show simuvis main documentation
                mt, c = self.getSimuVis(words[1:])
            elif unit == 'plugin':
                # show plugin documentation
                mt, c = self.getPlugIn(words[1:])
            elif unit == 'python':
                # show python documentation
                mt, c = self.getPython(words[1:])
        if not c:
            s.writeData("HTTP/1.0 404 File Not Found\r\n")
            return
        s.writeData("HTTP/1.0 200 Ok\r\n")
        s.writeData("Content-type: %s;\r\n" % mt)
        s.writeData("Content-Length: %s;\r\n" % len(c))
        s.writeData("\r\n")
        s.writeData(c)


    def getIndex(self):
        return 'text/plain', 'Dummy - sorry'


    def getSimuVis(self, w):
        p = os.path.join(helpPath, *w)
        if not os.path.exists(p):
            p = os.path.join(helpPathEn, *w)
            if not os.path.exists(p):
                return None, None
        base, ext = os.path.splitext(p)
        mimetype = self.mimeType(ext)
        p = open(p, 'rb').read()
        return mimetype, p


    def getPlugIn(self, w):
        return 'text/plain', 'Dummy - sorry!'


    def getPython(self, w):
        return 'text/plain', 'Dummy - sorry'


    def mimeType(self, ext):
        # FIXME: !
        return 'text/html'


# paths should be:
# / for main index page
# /simuvis/path_under_doc_path
# /plugin/FooBar/path_under_module_doc
# /python/module
# /quit - quit the server thread
#class HelpRequestHandler(BaseHTTPRequestHandler):
    #protocol_version = "HTTP/1.0"

    #def do_GET(self):
        #"""Serve a GET request."""
        #path = urlparse.urlparse(self.path)[2]
        #path = posixpath.normpath(urllib.unquote(path))
        #words = path.split('/')
        #words = filter(None, words)
        #if len(words) == 0:
            ## show index page
            #mt, c = self.getIndex()
        #else:
            #unit = words[0].lower()
            #c = None
            #if unit == 'simuvis':
                ## show simuvis main documentation
                #mt, c = self.getSimuVis(words[1:])
            #elif unit == 'plugin':
                ## show plugin documentation
                #mt, c = self.getPlugIn(words[1:])
            #elif unit == 'python':
                ## show python documentation
                #mt, c = self.getPython(words[1:])
            #elif unit == 'quit':
                ## make some kind of shutdown ...
                #self.send_response(200)
                #c = "Shutting down..."
                #self.send_header("Content-type", "text/plain")
                #self.send_header("Content-Length", len(c))
                #self.end_headers()
                #self.wfile.write(c)
                #self.wfile.close()
                #sys.exit(0)
        #if not c:
            #self.send_error(404, "File not found")
            #return
        #self.send_response(200)
        #self.send_header("Content-type", mt)
        #self.send_header("Content-Length", len(c))
        #self.end_headers()
        #self.wfile.write(c)


    #def getIndex(self):
        #return 'text/plain', 'Dummy - sorry'


    #def getSimuVis(self, w):
        #p = os.path.join(helpPath, *w)
        #if not os.path.exists(p):
            #p = os.path.join(helpPathEn, *w)
            #if not os.path.exists(p):
                #return None, None
        #base, ext = os.path.splitext(p)
        #mimetype = self.mimeType(ext)
        #p = open(p, 'rb').read()
        #return mimetype, p


    #def getPlugIn(self, w):
        #return 'text/plain', 'Dummy - sorry!'


    #def getPython(self, w):
        #return 'text/plain', 'Dummy - sorry'


    #def mimeType(self, ext):
        ## FIXME: !
        #return 'text/html' 

    #def log_message(self, fmt, *args):
        #Globals.logger.debug('Help: Server: %s', fmt % args)


def startServer():
    global helpServer
    helpServer = HelpServer()


def stopServer():
    global helpServer
    helpServer.pause()
    del helpServer
    helpServer = None



def showHelp(url=helpURL):
    if not helpServer:
        startServer()
    QDesktopServices.openUrl(QUrl(url))
