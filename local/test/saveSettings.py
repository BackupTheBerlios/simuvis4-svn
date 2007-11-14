
from PyQt4.QtGui import QFileDialog

fn = QFileDialog.getSaveFileName(mainWin, 'Select name of config file to save', '', '*.ini')
if not fn.isEmpty():
    config.write(open(unicode(fn), 'w'))





