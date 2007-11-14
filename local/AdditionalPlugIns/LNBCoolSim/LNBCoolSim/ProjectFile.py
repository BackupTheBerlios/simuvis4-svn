# encoding: latin-1
# version:  $Id: ProjectFile.py,v 1.2 2007/04/23 07:37:22 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED, ZIP_STORED
import types, time

import BuildingData

class ProjectFile(ZipFile):

    def putData(self, data):
        zi = ZipInfo(filename='building.dat')
        zi.date_time=time.localtime()[:6]
        zi.compress_type=ZIP_DEFLATED
        self.writestr(zi, data.dump())

    def getData(self):
        if not 'building.dat' in self.namelist():
            return None
        else:
            return BuildingData.load(self.read('building.dat'))

    def listResults(self):
        return [f.split('/')[1] for f in self.namelist() \
                if f.startswith('results')]

    def getResult(self, name):
        return self.read('results/'+name)

    def putResult(self, name, data):
        print name
        zi = ZipInfo(filename='results/'+name)
        zi.date_time=time.localtime()[:6]
        zi.compress_type=ZIP_DEFLATED
        self.writestr(zi, data)

    def putComment(self, data):
        zi = ZipInfo(filename='comment.txt')
        zi.date_time=time.localtime()[:6]
        zi.compress_type=ZIP_STORED
        self.writestr(zi, data)

    def getComment(self):
        if not 'comment.txt' in self.namelist():
            return None
        else:
            return self.read('comment.txt')

if __name__ == '__main__':
    import BuildingTypes
    import sys
    if len(sys.argv) < 3 or sys.argv[1] not in BuildingTypes.buildingTypes:
        print '\nUsage: %s type filename' % sys.argv[0]
        print 'Defined types:'
        print '  ' + '\n  '.join(BuildingTypes.buildingTypes) + '\n'
        sys.exit(3)
    prf = ProjectFile(sys.argv[2], 'w')
    bdata = eval('BuildingTypes.%s()' % sys.argv[1])
    prf.putData(bdata)
    #z.putResult('foo.obs', 'dummy data foo')
    #z.putResult('bar.obs', 'dummy data bar')
    prf.close()

    prf = ProjectFile(sys.argv[2], 'r')
    print prf.getData().id
    print prf.listResults()
    print [prf.getResult(r) for r in prf.listResults()]

