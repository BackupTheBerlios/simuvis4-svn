# encoding: latin-1
# version:  $Id: Objects.py,v 1.10 2007/08/14 12:10:10 joerg Exp $
# author:   Joerg Raedler <joerg@dezentral.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

# FIXME: old SimuVis code

import vtk, Helpers, os, math


class ObjectBase:

    def __init__(self, src=None, mapperType=vtk.vtkPolyDataMapper,
                 actorType=vtk.vtkActor):
        self._source = None
        self._mapper = mapperType()
        self._actor  = actorType()
        self._actor.SetMapper(self._mapper)
        if src:
            self.setSource(src)
        else:
            self.setup()
            
    def setup(self):
        self.setSource(vtk.vtkConeSource())
        
    def setSource(self, src):
        self._source = src
        self._mapper.SetInput(src.GetOutput())
        
    def addToRenderer(self, ren):
        ren.AddActor(self._actor)


class GroupBase:
    
    def __init__(self):
        self._parts  = []
        self._actor  = vtk.vtkAssembly()
        self.setup()
        
    def setup(self):
        pass
    
    def addPart(self, part):
        self._parts.append(part)
        if hasattr(part, "_actor"):
            self._actor.AddPart(part._actor)
        else:
            self._actor.AddPart(part)
        return part
        
    def delPart(self, part):
        try:
            self._parts.remove(part)
            if hasattr(part, "_actor"):
                self._actor.RemovePart(part._actor)
            else:
                self._actor.RemovePart(part)
        except:
            pass
            
    def addToRenderer(self, ren):
        ren.AddActor(self._actor)


class Text3D(ObjectBase):
    
    def setup(self):
        #self.textSrc = vtk.vtkTextSource()
        self.textSrc = vtk.vtkVectorText()
        self.textSrc.SetText('SMILE')
        #self.textSrc.BackingOff()
        self.extruder = vtk.vtkLinearExtrusionFilter()
        self.extruder.SetInput(self.textSrc.GetOutput())
        self.extruder.SetVector(0,0,0.4)
        self.normals = vtk.vtkPolyDataNormals()
        self.normals.SplittingOff()
        self.normals.SetInput(self.extruder.GetOutput())
        self.setSource(self.normals)
        self._actor.GetProperty().SetAmbient(0.8)
        
    def setText(self, txt):
        self.textSrc.SetText(txt)


class SimpleArrow(GroupBase):
    
    def setup(self):
        self.head = ObjectBase(vtk.vtkConeSource())
        self.head._source.SetRadius(0.2)
        self.head._source.SetHeight(0.25)
        self.head._source.SetResolution(18)
        self.head._actor.SetPosition(0.625, 0.0, 0.0)
        self.head._actor.GetProperty().SetAmbient(0.4)
        self.addPart(self.head)
        self.body = ObjectBase(vtk.vtkCylinderSource())
        self.body._source.SetHeight(1.0)
        self.body._source.SetRadius(0.1)
        self.body._source.SetResolution(18)
        self.body._actor.RotateZ(90)
        self.body._actor.GetProperty().SetAmbient(0.4)
        self.addPart(self.body)
        self.rgbCalc = Helpers.RgbCalculator(-1.0, 1.0)
        
    def setSize(self, s):
        if s > 1.0:
            s = 1.0
        if s < 0.0:
            s = 0.0
        self.head._source.SetRadius(0.2*s)
        self.body._source.SetRadius(0.09*s+0.01)

class DoubleArrow(GroupBase):
    
    def setup(self):
        self.head1 = ObjectBase(vtk.vtkConeSource())
        self.head1._source.SetRadius(0.2)
        self.head1._source.SetHeight(0.25)
        self.head1._source.SetResolution(18)
        self.head1._actor.SetPosition(0.625, 0.0, 0.0)
        self.head1._actor.GetProperty().SetAmbient(0.4)
        self.addPart(self.head1)
        self.head2 = ObjectBase(vtk.vtkConeSource())
        self.head2._source.SetRadius(0.2)
        self.head2._source.SetHeight(0.25)
        self.head2._source.SetResolution(18)
        self.head2._actor.RotateZ(180)
        self.head2._actor.SetPosition(-0.625, 0.0, 0.0)
        self.head2._actor.GetProperty().SetAmbient(0.4)
        self.addPart(self.head2)
        self.body = ObjectBase(vtk.vtkCylinderSource())
        self.body._source.SetHeight(1.0)
        self.body._source.SetRadius(0.1)
        self.body._source.SetResolution(18)
        self.body._actor.RotateZ(90)
        self.body._actor.GetProperty().SetAmbient(0.4)
        self.addPart(self.body)
        self.rgbCalc = Helpers.RgbCalculator(-1.0, 1.0)
        
    def setSize(self, s):
        if s > 0.0:
            if s > 1.0:
                s = 1.0
            self.head1._source.SetRadius(0.2*s)
            self.head2._source.SetRadius(0.0)
            self.body._source.SetRadius(0.09*s+0.01)
        else:
            if s < -1.0:
                s = -1.0
            self.head1._source.SetRadius(0.0)
            self.head2._source.SetRadius(-0.2*s)
            self.body._source.SetRadius(-0.09*s+0.01)
        r, g, b = self.rgbCalc.RGB(s)
        self.head1._actor.GetProperty().SetColor(r, g, b)
        self.head2._actor.GetProperty().SetColor(r, g, b)
        self.body._actor.GetProperty().SetColor(r, g, b)


class ColorBar:
    
    def __init__(self, min=0, max=1, nColors=80, title='Scale', reverse=False):
        self.cTable = vtk.vtkLookupTable()
        self.cTable.SetNumberOfColors(nColors)
        self.cTable.SetRange((min, max))
        self.cTable.Build()
        if reverse:
            c = map(self.cTable.GetTableValue, range(nColors))
            c.reverse()
            map(self.cTable.SetTableValue, range(nColors), c)
        self._actor = vtk.vtkScalarBarActor()
        self._actor.SetLookupTable(self.cTable)
        self._actor.SetTitle(title)
        #self._actor.ShadowOn()
        self._actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        self._actor.GetPositionCoordinate().SetValue(0.1,0.1)
        self._actor.SetOrientationToHorizontal()
        self._actor.SetWidth(0.8)
        self._actor.SetHeight(0.17)

    def RGB(self, v):
        l = [0, 0, 0]
        self.cTable.GetColor(v, l)
        return l

    def addToRenderer(self, ren):
        ren.AddActor(self._actor)


class Axes(GroupBase):
    
    def setup(self):
        self.axes = self.addPart(ObjectBase(vtk.vtkAxes()))
        self.xcone = self.addPart(ObjectBase(vtk.vtkConeSource()))
        self.xcone._actor.SetScale(0.1,0.05,0.05)
        self.xcone._actor.AddPosition(1.0,0.0,0.0)
        self.xcone._actor.GetProperty().SetColor(1.0,0.3,0.3)
        self.ycone = self.addPart(ObjectBase(vtk.vtkConeSource()))
        self.ycone._actor.SetScale(0.1,0.05,0.05)
        self.ycone._actor.RotateZ(90.0)
        self.ycone._actor.AddPosition(0.0,1.0,0.0)
        self.ycone._actor.GetProperty().SetColor(1.0,1.0,0.0)
        self.zcone = self.addPart(ObjectBase(vtk.vtkConeSource()))
        self.zcone._actor.SetScale(0.1,0.05,0.05)
        self.zcone._actor.RotateY(-90.0)
        self.zcone._actor.AddPosition(0.0,0.0,1.0)
        self.zcone._actor.GetProperty().SetColor(0.3,1.0,0.3)
        self.balls = self.addPart(ObjectBase(vtk.vtkSphereSource()))
        self.balls._actor.SetScale(0.05,0.05,0.05)
        self.balls._actor.GetProperty().SetColor(0.3,0.3,1.0)
        self.xtxt = ObjectBase(vtk.vtkVectorText(),
                                            actorType=vtk.vtkFollower)
        self.xtxt._source.SetText('X')
        self.xtxt._actor.SetScale(0.1,0.1,0.1)
        self.xtxt._actor.AddPosition(1.0,0.0,0.0)
        self.xtxt._actor.GetProperty().SetColor(1.0,0.3,0.3)
        self.addPart(self.xtxt)
        self.ytxt = ObjectBase(vtk.vtkVectorText(),
                                            actorType=vtk.vtkFollower)
        self.ytxt._source.SetText('Y')
        self.ytxt._actor.SetScale(0.1,0.1,0.1)
        self.ytxt._actor.AddPosition(0.0,1.0,0.0)
        self.ytxt._actor.GetProperty().SetColor(1.0,1.0,0.0)
        self.addPart(self.ytxt)
        self.ztxt = ObjectBase(vtk.vtkVectorText(),
                                            actorType=vtk.vtkFollower)
        self.ztxt._source.SetText('Z')
        self.ztxt._actor.SetScale(0.1,0.1,0.1)
        self.ztxt._actor.AddPosition(0.0,0.0,1.0)
        self.ztxt._actor.GetProperty().SetColor(0.3,1.0,0.3)
        self.addPart(self.ztxt)
        self.ntxt = ObjectBase(vtk.vtkVectorText(),
                                            actorType=vtk.vtkFollower)
        self.ntxt._source.SetText('0')
        self.ntxt._actor.SetScale(0.1,0.1,0.1)
        self.ntxt._actor.GetProperty().SetColor(0.3,0.3,1.0)
        self.addPart(self.ntxt)
        
    def setCamera(self, cam):
        self.xtxt._actor.SetCamera(cam)
        self.ytxt._actor.SetCamera(cam)
        self.ztxt._actor.SetCamera(cam)
        self.ntxt._actor.SetCamera(cam)


class Earth(GroupBase):
    
    def setup(self):
        self.res = 32
        self.height = 0.0005
        self.sphere = self.addPart(ObjectBase(vtk.vtkTexturedSphereSource()))
        self.sphere._source.SetThetaResolution(self.res)
        self.sphere._source.SetPhiResolution(self.res)
        self.sphere._actor.GetProperty().SetColor(0.0, 0.0, 0.4)
        self.earth = self.addPart(ObjectBase(vtk.vtkEarthSource()))
        self.earth._source.SetRadius(0.5 + self.height)
        self.earth._source.SetOnRatio(0)

    def showTexture(self):
        self.reader  = vtk.vtkJPEGReader()
        self.reader.SetFileName(os.path.join(os.path.split(__file__)[0], 'earth.jpg'))
        self.texture = vtk.vtkTexture()
        self.texture.SetInput(self.reader.GetOutput())
        self.sphere._actor.GetProperty().SetColor(1.0, 1.0, 1.0)
        self.sphere._actor.SetTexture(self.texture)

    def showGrid(self):
        self.grid = []
        # latitude
        tmp = self.addPart(ObjectBase(vtk.vtkRegularPolygonSource()))
        tmp._source.SetGeneratePolyline(True)
        tmp._source.SetGeneratePolygon(False)
        tmp._source.SetNumberOfSides(self.res)
        tmp._source.SetRadius(0.5 + self.height)
        tmp._actor.GetProperty().SetColor(0.3, 0.3, 0.3)
        self.grid.append(tmp)
        for i in range(10, 90, 10):
            u = i * math.pi / 180.0
            h = (0.5 + self.height) * math.cos(u)
            r = (0.5 + self.height) * math.cos(0.5*math.pi-u)
            a = self.addPart(ObjectBase(vtk.vtkRegularPolygonSource()))
            a._source.SetGeneratePolyline(True)
            a._source.SetGeneratePolygon(False)
            a._source.SetNumberOfSides(self.res)
            a._source.SetRadius(r)
            a._source.SetCenter(0.0, 0.0, h)
            a._actor.GetProperty().SetColor(0.3, 0.3, 0.3)
            self.grid.append(a)
            b = self.addPart(ObjectBase(vtk.vtkRegularPolygonSource()))
            b._source.SetGeneratePolyline(True)
            b._source.SetGeneratePolygon(False)
            b._source.SetNumberOfSides(self.res)
            b._source.SetRadius(r)
            b._source.SetCenter(0.0, 0.0, -h)
            b._actor.GetProperty().SetColor(0.3, 0.3, 0.3)
            self.grid.append(b)
        # longitude
        for i in range(0, 180, 10):
            u = i * math.pi / 180.0
            a = self.addPart(ObjectBase(vtk.vtkRegularPolygonSource()))
            a._source.SetGeneratePolyline(True)
            a._source.SetGeneratePolygon(False)
            a._source.SetNumberOfSides(2*self.res)
            a._source.SetNormal(math.sin(u), math.cos(u), 0.0)
            a._source.SetRadius(0.5 + self.height)
            a._actor.GetProperty().SetColor(0.3, 0.3, 0.3)
            self.grid.append(a)

    def showPosition(self, lat, lon, txt='Position'):
        s = self.addPart(ObjectBase(vtk.vtkSphereSource()))
        s._source.SetRadius(0.005)
        s._source.SetCenter(0.5, 0, 0)
        s._actor.GetProperty().SetColor(1.0, 0, 0)
        s._actor.RotateWXYZ(-lat, 0, 1, 0)
        s._actor.RotateWXYZ(lon, 0, 0, 1)
        c = vtk.vtkCaptionActor2D()
        c.SetCaption(txt)
        c.SetWidth(0.1)
        c.SetHeight(0.04)
        c.SetAttachmentPoint(s._actor.GetCenter())
        return c
