import time
SimTools = mainWin.plugInManager.getPlugIn('SimTools')
if not SimTools:
    from SimuVis4.Errors import PlugInMissingError
    raise PlugInMissingError("Could not find PlugIn SimTools!")

Q = SimTools.Quantities

q1 = Q.Text('text', 'default text', descr='some text', maxLen=15)
tmp = ['Entry '+str(i) for i in range(10)]
q2 = Q.Choice('choice', tmp[4], descr='you choose!', choices=tmp)
q3 = Q.Integer('int', 42, descr='integer number', min=39, max=50, step=3, unit='kWh')
q4 = Q.Float('float', 42.42, descr='float number')
q5 = Q.Bool('bool', True, descr='boolean value')
q6 = Q.MLText('mltext', 'default text\non two\nlines', descr='some multiline text')
q7 = Q.MultiChoice('mchoice', (tmp[3], tmp[7]), descr='choose one or more', choices=tmp)
q8 = Q.DateTime('datetime', int(time.time()), descr='date and time')

dlg = SimTools.Widgets.SimpleQuantitiesDialog(mainWin, windowTitle='Test')
dlg.addQuantity(q1, q2, q3, q4, q5, q6, q7, q8)
dlg.exec_()

print q1, q2, q3, q4, q5, q6, q7, q8
