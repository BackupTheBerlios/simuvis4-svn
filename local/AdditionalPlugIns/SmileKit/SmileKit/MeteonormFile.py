#!/usr/bin/env python
# encoding: latin-1
# version:  $Id$
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

try:
    import Numeric
except:
    import numpy as Numeric

import Scientific
from Scientific.IO.NetCDF import NetCDFFile

version = 3
file_format  = 3


# { name : (shortname, typestring, conversion func.), ...}
variables = {'time'             : ('hy',     'i', lambda v: (v-0.5)*3600.0),
            'air_pressure'      : ('p',      's', lambda v: v),
            'air_temperature'   : ('Ta',     'f', lambda v: v),
            'relative_humidity' : ('RH',     'f', lambda v: 0.01*v),
            'beam_radiation'    : ('<G_Bh>', 'f', lambda v: v),
            'diffuse_radiation' : ('<G_Dh>', 'f', lambda v: v),
            'cloud_cover'       : ('N',      's', lambda v: v),
            'wind_speed'        : ('FF',     'f', lambda v: v),
            'wind_direction'    : ('DD',     's', lambda v: v)}


mnHelpText = """Schritte in METEONORM 5:
1. "Standort" wählen oder eingeben
2. Menüpunkt "Format" / "Ausgabeformate"
3. "User defined" auswählen / "Ok"
4. "Kopfzeilen" aktivieren, Trennzeichen auf "Tab" stellen
5. Folgende Variablen in beliebiger Reihenfolge auswählen:
   Stunde im Jahr
   Luftdruck
   Lufttemperatur
   relative Luftfeuchtigkeit
   Direktstrahlung, horizontal
   Diffusstrahlung, horizontal
   Bewölkungsgrad
   Windgeschwindigkeit
   Windrichtung
6. "Ok"
7. "Stundenwerte" generieren
8. "Speichern"
"""


def progressDummy(p):
    pass


def readMnFile(fn, progress=progressDummy):
    r = {'source_file': fn}
    progress(0)
    tmp = open(fn, 'r')
    ### read header lines
    r['name'] = tmp.readline().replace('"', '').strip()
    v = tmp.readline().strip().split(',')
    r['latitude']  = float(v[0])
    r['longitude'] = -float(v[1]) # obviously changed by f***ing Meteonorm authors!
    r['height']    = int(v[2])
    r['timezone']  = int(v[3])
    tmp.readline()
    head = tmp.readline()
    head = head.replace('H_Dh', '<G_Dh>')
    head = head.replace('H_Bh', '<G_Bh>')
    head = head.split()
    # test for all needed variables
    for v in variables.values():
        if not v[0] in head:
            raise Exception("Could not find variable %s in file!" % v[0])
    ### read data matrix
    data = []
    lines = tmp.readlines()
    tmp.close()
    progress(10)
    nlines = len(lines)
    oldprg = 0 
    for i in range(nlines):
        l = lines[i].strip()
        if len(l) > 0 and not l[0] == '#':
            l = l.replace(',', '.')
            data.append([float(v) for v in l.split()])
        prg = int(10 + 40 * float(i)/nlines)
        if prg != oldprg:
            progress(prg)
            oldprg = prg
    a = Numeric.array(data)
    progress(70)
    ### data conversion
    a = Numeric.resize(a, (a.shape[0]+1, a.shape[1]))
    nvars = len(variables)
    i = 1
    for n in variables.keys():
        shortname, tc, cvt = variables[n]
        col = head.index(shortname)
        d =  cvt(a[:,col])
        ## periodic end
        if n == 'time':
            d[-1] = d[-2] + (d[1]-d[0])
        else:
            d[-1] = d[0]
        prg = int(70 + 30 * float(i)/nvars)
        progress(prg)
        r[n] = d
        i += 1
    return r


def writeNcFile(data, fileName=None, oldStyle=1):
    if not fileName:
        fileName = data['name']+'_weather.nc'
    f = NetCDFFile(fileName, 'w')
    f.createDimension('time', data['time'].shape[0])
    f.file_format = file_format
    if oldStyle:
        f.createDimension('scalar', 1)
    if data.has_key('comment'):
        f.comment = data['comment']
    else:
        f.comment = 'created by MeteonormFile.py (v%d)' % version
    if data.has_key('source_file'):
        f.source_file = str(data['source_file'])
    for vn in ('latitude', 'longitude', 'height'):
        setattr(f, vn, data[vn])
        if oldStyle:
            v = f.createVariable(vn, 'd', ('scalar', ))
            v[:] = [data[vn]]
    setattr(f, 'longitude_0', 15.0*data['timezone'])
    if oldStyle:
        v = f.createVariable('longitude_0', 'd', ('scalar', ))
        v[:] = [15.0 * data['timezone']]
    for vn in variables.keys():
        t = variables[vn][1]
        v = f.createVariable(vn, t, ('time',))
        v[:] = data[vn].astype(t)

    f.sync()
    f.close()


def makeStatistics(data):
    if not data['time'].shape[0] == 8761:
        return 'Statistics only available for whole year datasets!'
    t = []
    # check for common problems
    if len(set(data['wind_direction'])) < 15:
        t.append('\n*** WARNING: wind direction varies to little, old Meteonorm file?\n')
    if data['longitude'] * data['timezone'] < 0.0:
        t.append('\n*** WARNING: longitude and timezone have different signs, old Meteonorm file?\n')
    else:
        if abs(data['longitude'] - 15.0*data['timezone']) > 10.0:
            t.append('\n*** WARNING: significant difference between longitude and timezone!\n')
    b = data['beam_radiation']
    d = data['diffuse_radiation']
    t.append('Beam radiation (daily):      %.1f Wh/m²d' % (sum(b)/365.0))
    t.append('Diffuse radiation (daily):   %.1f Wh/m²d' % (sum(d)/365.0))
    t.append('Total radiation (year):      %.1f kWh/m²a' % ((sum(b)+ sum(d))/1000.0))
    t.append('Sun hours (beam >120 W/m²):  %d h/a' % len([x for x in b if x>120.0]))
    a = data['air_temperature']
    t.append('Air temperature (min):       %.1f °C' % min(a))
    t.append('Air temperature (max):       %.1f °C' % max(a))
    t.append('Air temperature (average):   %.1f °C' % (sum(a)/8761.0))
    t.append('Relative humidity (average): %.1f %%' % (sum(data['relative_humidity'])/87.61))
    t.append('Wind speed (average):        %.1f m/s' % (sum(data['wind_speed'])/8761.0))
    t.append('Wind direction (average):    %.1f °' % (sum(data['wind_direction'])/8761.0))
    return '\n'.join(t)


if __name__ == '__main__':
    import sys
    try:
        import ProgressBar
        pb = ProgressBar.TxtScale(40, minVal=0.0, maxVal=100.0,
            leftSign='#', arrow='#', rightSign=' ', template= '>>> |%s%c%s| % 3d%% | %s')
        def progFun(v):
            pb.set(v, (v < 100) and 'Reading' or 'Done   \n')
    except:
        progFun = progressDummy
        print '>>> Reading ...',
        sys.stdout.flush()
    if len(sys.argv) < 2:
        print "\nUsage: %s meteonormfile [netcdffile]\n" % sys.argv[0]
        print mnHelpText
        sys.exit(1)
    data = readMnFile(sys.argv[1], progress=progFun)
    if progFun == progressDummy:
        print 'done!'
    print '>>> Weather statistics:'
    print makeStatistics(data)
    if len(sys.argv) > 2:
        fileName = sys.argv[2]
    else:
        fileName = data['name']+'_weather.nc'
    print '>>> Writing "%s"...' % fileName,
    sys.stdout.flush()
    writeNcFile(data, fileName)
    print 'done!'