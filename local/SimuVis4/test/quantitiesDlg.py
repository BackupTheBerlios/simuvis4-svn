SimTools = mainWin.plugInManager.getPlugIn('SimTools')
if not SimTools:
    from SimuVis4.Errors import PlugInMissingError
    raise PlugInMissingError("Could not find PlugIn SimTools!")

Q = SimTools.Quantities

q1 = Q.Text('text0', 'default text', descr='some text', maxLen=15)
tmp = ['Entry '+str(i) for i in range(10)]
q2 = Q.Choice('choice0', tmp[4], descr='you choose!', choices=tmp)
q3 = Q.Integer('int0', 42, descr='integer number', min=39, max=50, step=3, unit='kWh')
q4 = Q.Float('float0', 42.42, descr='float number')
q5 = Q.Bool('bool0', True, descr='boolean value')

dlg = SimTools.Widgets.SimpleQuantitiesDialog(mainWin, windowTitle='Test')
dlg.addQuantity(q1, q2, q3, q4, q5)
dlg.exec_()

print q1, q2, q3, q4, q5
