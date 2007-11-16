#!/usr/bin/python
import os

files = ('bin/SimuVis.pyw', )
rev = int(os.popen('svnversion -n .', 'r').read().split(':')[-1])
print 'update revision number %d in files: ' % rev,
for f in files:
    print f,
    lines = open(f, 'r').readlines()
    ll = [i for i in range(len(lines)) if lines[i].startswith('svn_revision = ')]
    for l in ll:
        print '(%d)' % l,
        lines[l] = 'svn_revision = %d # this line is changed automagically by mark_svn_rev.py\n' % rev
    os.rename(f, f+'~')
    open(f, 'w').write(''.join(lines))
