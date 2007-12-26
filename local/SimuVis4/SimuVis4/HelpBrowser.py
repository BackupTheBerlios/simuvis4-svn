# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import Globals, sys, os, mimetypes, string
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtCore import QCoreApplication, QUrl, QString, QRegExp, QDateTime, SIGNAL
from PyQt4.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
from cgi import escape

lang = Globals.config['main:i18n_language']
helpPath   = os.path.join(Globals.config['main:system_help_path'], lang)
helpPathEn = os.path.join(Globals.config['main:system_help_path'], 'en')
helpURL = 'http://127.0.0.1:%d/' % Globals.config.getint('main', 'help_server_port')

helpServer = None

# some templates
piDocStart = """
<p><table border="1">
"""

piDocLine = string.Template(unicode("""
<tr><td><a href="/plugin/$name/index.html">$name</a></td><td>$descr</td></tr>
"""))

piDocEnd = """
</table></p>
"""


class HelpServer(QTcpServer):

    def __init__(self, port=Globals.config.getint('main', 'help_server_port')):
        QTcpServer.__init__(self)
        self.enabled = True
        self.listen(QHostAddress(QHostAddress.LocalHost), port)


    def incomingConnection(self, socket):
        if not self.enabled:
            return
        s = QTcpSocket(self)
        self.connect(s, SIGNAL('readyRead()'), self.readClient)
        self.connect(s, SIGNAL('disconnected()'), self.discardClient)
        s.setSocketDescriptor(socket)


    def setEnabled(self, e):
        self.enabled = e


    def readClient(self):
        if not self.enabled:
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
            mt = 'text/html'
            p = os.path.join(helpPath, 'errorTemplate.html')
            if not os.path.exists(p):
                p = os.path.join(helpPathEn, 'errorTemplate.html')
            if not os.path.exists(p):
                c = '<head></head><body>404 - File not found!</body>'
            else:
                c = open(p, 'rb').read()
                c = c.replace('FAILED_ADDRESS', path)
        else:
            s.writeData("HTTP/1.0 200 Ok\r\n")
        s.writeData("Content-type: %s;\r\n" % mt)
        s.writeData("Content-Length: %s;\r\n" % len(c))
        s.writeData("\r\n")
        s.writeData(c)


    def getIndex(self):
        p = os.path.join(helpPath, 'mainIndexTemplate.html')
        if not os.path.exists(p):
            p = os.path.join(helpPathEn, 'mainIndexTemplate.html')
            if not os.path.exists(p):
                return None, None
        c = open(p, 'rb').read()
        piLines = [piDocLine.substitute(name=escape(n), descr=escape(pi.description)) \
            for n,pi in Globals.plugInManager.plugIns.items()]
        piLines.insert(0, piDocStart)
        piLines.append(piDocEnd)
        c = c.replace('PLUGIN_DOC_PLACEHOLDER', '\n'.join(piLines))
        return 'text/html', c.encode('utf8')


    def getSimuVis(self, w):
        p = os.path.join(helpPath, *w)
        if not os.path.exists(p):
            p = os.path.join(helpPathEn, *w)
            if not os.path.exists(p):
                return None, None
        base, ext = os.path.splitext(p)
        mimetype = mimetypes.types_map.get(ext, 'application/octet-stream')
        c = open(p, 'rb').read()
        return mimetype, c


    def getPlugIn(self, w):
        pi = Globals.plugInManager.plugIns[w[0]]
        base, ext = os.path.splitext(w[-1])
        mimetype = mimetypes.types_map.get(ext, 'application/octet-stream')
        c = None
        try:
            c = pi.openFile(os.path.join('Doc', lang, *w[1:])).read()
        except:
            try:
                c = pi.openFile(os.path.join('Doc', 'en', *w[1:])).read()
            except:
                pass
        return mimetype, c


    def getPython(self, w):
        return 'text/plain', 'Dummy - sorry'



def startServer():
    global helpServer
    helpServer = HelpServer()



def stopServer():
    global helpServer
    #helpServer.setEnabled(False)
    del helpServer
    helpServer = None



def showHelp(url=helpURL):
    if not helpServer:
        startServer()
    QDesktopServices.openUrl(QUrl(url))
