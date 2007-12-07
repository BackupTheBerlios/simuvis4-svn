###
### this Example seems to fail with mazplotlib 0.91.1
###

from vtk import *

import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pylab as p

# The vtkImageImporter will treat a python string as a void pointer
importer = vtkImageImport()
importer.SetDataScalarTypeToUnsignedChar()
importer.SetNumberOfScalarComponents(4)

# It's upside-down when loaded, so add a filp filter
imflip = vtkImageFlip()
imflip.SetInput(importer.GetOutput())
imflip.SetFilteredAxis(1)

# Map the plot as a texture on a cube
cube = vtkCubeSource()

cubeMapper = vtkPolyDataMapper()
cubeMapper.SetInput(cube.GetOutput())

cubeActor = vtkActor()
cubeActor.SetMapper(cubeMapper)

# Create a texure based off of the image
cubeTexture = vtkTexture()
cubeTexture.InterpolateOn()
cubeTexture.SetInput(imflip.GetOutput())
cubeActor.SetTexture(cubeTexture)

ren = vtkRenderer()
ren.AddActor(cubeActor)

win = plugInManager['VtkWindow'].winManager.newWindow()
win.vtkWidget.GetRenderWindow().AddRenderer(ren)

# Now create our plot
fig = Figure()
canvas = FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_xlabel('Hello from VTK!', size=16)
ax.bar(xrange(10), p.rand(10))

# Powers of 2 image to be clean
w,h = 1024, 1024
dpi = canvas.figure.get_dpi()
fig.set_figsize_inches(w / dpi, h / dpi)
canvas.draw() # force a draw

# This is where we tell the image importer about the mpl image
extent = (0, w - 1, 0, h - 1, 0, 0)
importer.SetWholeExtent(extent)
importer.SetDataExtent(extent)
importer.SetImportVoidPointer(canvas.buffer_rgba(0,0), 1)
importer.Update()
