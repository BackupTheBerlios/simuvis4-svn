
vtkpi = mainWin.plugInManager.getPlugIn("VtkWindow")

if not vtkpi:
    from SimuVis4.Errors import PlugInMissingError
    raise PlugInMissingError("PlugIn VtkWindow not found!")

vtk     = vtkpi.vtk
Helpers = vtkpi.Helpers
Objects = vtkpi.Objects

def makeTextDemo():
    window = vtkpi.manager.newWindow("Test of SimuVis' VTK-PlugIn")
    ren = vtk.vtkRenderer()
    window.vtkWidget.GetRenderWindow().AddRenderer(ren)
    txt = 'SimuVis4'
    cbar = Objects.ColorBar(max=len(txt)-1, title="character position")
    cbar.addToRenderer(ren)
    spacing = (0.0, 0.1, 0.14, 0.27, 0.35, 0.45, 0.5, 0.58)
    text = []
    rgbCalc = Helpers.RgbCalculator(0.0, float(len(txt)-1))
    text3D = Objects.GroupBase()
    for i in range(len(txt)):
        text.append(Objects.Text3D())
        text[i].setText(txt[i])
        text[i]._actor.SetScale(0.1, 0.1, 0.1)
        text[i]._actor.SetPosition(-0.3 + spacing[i], 0, 0)
        text3D.addPart(text[i])
        rgb = cbar.RGB(float(i))
        text[i]._actor.GetProperty().SetColor(rgb[0], rgb[1], rgb[2])
    text[-1]._actor.SetScale(0.12, 0.12, 0.12)
    text3D.addToRenderer(ren)

    axes = Objects.Axes()
    axes.addToRenderer(ren)
    axes._actor.SetScale(0.15, 0.15, 0.15)
    axes._actor.SetPosition(-0.3, -0.03, -0.01)

    window.show()
    window.vtkWidget.Initialize()
    window.vtkWidget.Start()
    return window


def makeEarthDemo():
    window = vtkpi.manager.newWindow("Test of SimuVis' VTK-PlugIn")
    ren = vtk.vtkRenderer()
    window.vtkWidget.GetRenderWindow().AddRenderer(ren)

    earth = Objects.Earth()
    earth.showGrid()
    earth.showTexture()
    earth.addToRenderer(ren)

    ren.AddActor(earth.showPosition(52.2526, 13.1524, "Berlin"))
    ren.AddActor(earth.showPosition(59.5742, 24.0726, "Helsinki"))
    ren.AddActor(earth.showPosition(53.3324,  9.4206, "Hamburg"))

    #axes = vtk.vtkAxesActor()
    #ren.AddActor(axes)

    window.show()
    window.vtkWidget.Initialize()
    window.vtkWidget.Start()
    #window.makeToolBar()
    return window

makeTextDemo()
makeEarthDemo()
