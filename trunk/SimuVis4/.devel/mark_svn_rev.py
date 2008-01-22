#!/usr/bin/python
import os, stat

files = ('bin/SimuVis.pyw', 'SimuVis4/__init__.py', 'setup.py')
tmp = os.popen('svnversion -n .', 'r').read().split(':')[-1]
while not tmp[-1].isdigit():
    tmp = tmp[:-1]
rev = int(tmp)

print 'update revision number %d in files: ' % rev,
for f in files:
    print f,
    st = os.stat(f)
    lines = open(f, 'r').readlines()
    ll = [i for i in range(len(lines)) if lines[i].startswith('svn_revision = ')]
    for l in ll:
        print '(%d)' % l,
        lines[l] = 'svn_revision = %d # this line is changed automagically by mark_svn_rev.py\n' % rev
    os.rename(f, f+'~')
    open(f, 'w').write(''.join(lines))
    os.chmod(f, stat.S_IMODE(st[stat.ST_MODE]))
