#!/usr/bin/env python

import string, os, sys, shutil, tempfile, select

BUFSIZE = 1024

class Process:
    WAITING = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self, cmdLine, environ=None, workDir=None):
        self.environ = os.environ.copy()
        if environ:
            self.environ.update(environ)
        self.cmdLine = cmdLine
        self.workDir = workDir or tempfile.mktemp()
        if not os.path.exists(self.workDir):
            os.mkdir(self.workDir)
        self.exitStatus = 0
        self._started = 0
        self._pty = None
        self.pid = None
        self._poll = select.poll()

    def start(self):
        self.pid, self._pty = os.forkpty()
        if self.pid == 0:
            os.chdir(self.workDir)
            try:
                os.execve(self.cmdLine[0], self.cmdLine, self.environ)
            except:
                sys.exit(99)
        self._poll.register(self._pty, select.POLLIN)
        self._started = 1

    def read(self, bufsize=BUFSIZE):
        if self._pty and (self._pty, select.POLLIN) in self._poll.poll():
            return os.read(self._pty, bufsize)

    def status(self):
        if not self._started:
            return self.WAITING
        pid, status = os.waitpid(self.pid, os.WNOHANG)
        if pid == self.pid:
            self.exitStatus = status
            return self.FINISHED
        else:
            return self.RUNNING

    def addFiles(self, *files):
        for file in files:
            shutil.copy(file, self.workDir)

    def fileName(self, name=''):
        return os.path.join(self.workDir, name)

    def kill(self, sig=15):
        if self.pid:
            os.kill(self.pid, sig)

    def __del__(self):
        if not self.pid:
            return
        try:
            if self._pty:
                os.close(self._pty)
            shutil.rmtree(self.workDir, 1)
        except:
            pass

if __name__ == '__main__':
    import time

    if '--test' in sys.argv:
        print os.environ['BLA']
        f = open('test.dat', 'w')
        for i in range(10):
            sys.stdout.write('Zahl %d\n' % i)
            sys.stdout.flush()
            f.write(str(i)+'\n')
            time.sleep(1)
        f.close()
        sys.exit()

    else:
        p = Process(['/usr/bin/python', './Process.py', '--test'], environ={'BLA': 'HELLO!'})
        p.addFiles(sys.argv[0])
        p.start()
        while p.status() == Process.RUNNING:
            x = p.read()
            while x:
                sys.stdout.write(x)
                x = p.read()
            sys.stdout.flush()
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.1)
        if p.exitStatus == 0:
            f = open(p.fileName('test.dat'), 'r')
            print '\n'+'-'*80
            print f.read()
            print '-'*80
            f.close()
        else:
            print '\nFAILED:', p.exitStatus
            print p.workDir
        del p
