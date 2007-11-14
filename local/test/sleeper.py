# this test demonstrates the progress of a slow script

from PyQt4.QtGui import QMessageBox
import time

for i in range(33):
    executor.progress(i*3)
    if executor.cancelFlag:
        QMessageBox.information(mainWin, 'Script execution cancelled!',
            "The execution of this script was cancelled by the user!")
        break
    time.sleep(0.3)
