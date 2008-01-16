import time
SimTools = plugInManager.getPlugIn('SimTools')
if not SimTools:
    from SimuVis4.Errors import PlugInMissingError
    raise PlugInMissingError("Could not find PlugIn SimTools!")

Q = SimTools.Quantities
W = SimTools.Widgets

tmp = ['Entry '+str(i) for i in range(10)]

quant = []
quant.append(Q.Text('text', 'default text', descr='some text', maxLen=15))
quant.append(Q.Choice('choice', tmp[4], descr='you choose!', choices=tmp))
quant.append(Q.Integer('int', 42, descr='integer number', min=39, max=50, step=3, unit='kWh'))
quant.append(Q.Float('float', 42.42, descr='float number'))
quant.append(Q.Bool('bool', True, descr='boolean value'))
quant.append(Q.MLText('mltext', 'default text\non two\nlines', descr='some multiline text'))
quant.append(Q.MultiChoice('mchoice', (tmp[3], tmp[7]), descr='choose one or more', choices=tmp))
quant.append(Q.DateTime('datetime', int(time.time()), descr='date and time'))

txt = "Test of Quantities from SimTools"
dlg = W.ComplexQuantitiesDialog(mainWin, windowTitle='Complex Test', text=txt, scrolling=True)
dlg.addQuantities(quant)
if dlg.exec_():
    quant = dlg.result

dlg = W.SimpleQuantitiesDialog(mainWin, windowTitle='Complex Test', text=txt, scrolling=True)
dlg.addQuantities(quant)
if dlg.exec_():
    quant = dlg.result
