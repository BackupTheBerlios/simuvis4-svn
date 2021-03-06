# encoding: utf-8
# version:  $Id: DSBrowser.py 181 2007-12-13 16:35:24Z jraedler $
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

import SimuVis4, sys, types

from datastorage.graphics.matplot_lines_matrix import MatplotLineMatrix
from datastorage.graphics.matplot_matrix import MatplotMatrix
from datastorage.graphics.carpetplot_matrix import CarpetPlotMatrix
from datastorage.graphics.carpetplot import CarpetPlot

timeValues = [60, 3600, 86400, 604800, 2592000, 31536000]
timeNames = ['Minute', 'Hour', 'Day', 'Week', 'Month', 'Year']

RT = SimuVis4.Globals.plugInManager.getPlugIn('SimTools').RichTypes
## import RichTypes as RT



class ChartTemplate(object):
    """base class to hold information on one type of chart: name, description, etc...
       - subclasses should reimplement init(), setup() and createChart()
    """
    def __init__(self):
        self.name = ''
        self.chartName = '-unnamed-'
        self.previewImage = 'default.png'
        self.description = 'Only for subclassing - this template should never be used directly!'
        self.sensorgroup = None
        self.init()

    def defProp(self, p):
        self.properties.append(p)
        self.__propDict[p.name] = p

    def __getitem__(self, name):
        return self.__propDict[name].v

    def setSensorgroup(self, sensorgroup):
        self.sensorgroup = sensorgroup
        self.sensorNames = sensorgroup.keys()
        self.properties = []
        self.__propDict = {}
        self.setup()
        self.setupDone = True

    def makeChart(self, sensorgroup):
        if sensorgroup != self.sensorgroup:
            self.setSensorgroup(sensorgroup)
        chart = self.createChart()
        self.sensorgroup.addChart(chart)
        self.sensorgroup.flush()
        return chart

    def init(self):
        """overwrite this to set name, description, previewImage etc.
        - self.name will appear in the GUI to select this template
        - self.chartName is the suggested Name of the chart in datastorage
        - self.description should contain a (multi-line) desription
        - self.previewImage can point to an example image file
        """
        pass

    def setup(self):
        """overwrite this to set information on the chart properties, sensors etc.:
        - define properties with defProp()
        - you have self.sensorgroup and self.sensorNames available at this point
        """
        pass

    def createChart(self):
        """overwrite this to create the chart:
        - defined properties are accessible with self['property name']
        - must contain something like self.sensorgroup.addChart(chart)
        """
        pass



#####################################################################
#### Start of user defined ChartTemplates
#####################################################################

class WeatherData(ChartTemplate):

    def init(self):
        self.name = 'Weather data matrix'
        self.chartName = 'WeatherData'
        self.description = """this is a matrix chart of some weather data ..."""
        self.previewImage = 'WeatherData.png'

    def setup(self):
        self.defProp(RT.Text('Title', self.chartName, maxLen=100, descr='title of the chart'))
        sensors = ['Ta', 'Rha', 'Iglob']
        for s in sensors:
            if not s in self.sensorNames:
                sensors.remove(s)
        self.defProp(RT.MultiChoice('Sensors', sensors, choices=self.sensorNames, descr='sensors to plot'))
        self.defProp(RT.Float('Y-axis end', 0.8, min=0.0, max=1.0, descr=' ??? '))
        self.defProp(RT.Choice('Standard slice', timeNames[2], choices=timeNames, descr='standard slice in plot'))
        self.defProp(RT.Integer('Canvas width', 1000, min=200, max=5000, descr='standard width of plot'))
        self.defProp(RT.Integer('Canvas height', 800, min=200, max=5000, descr='standard height of plot'))

    def createChart(self):
        sensors = [[str(s)] for s in self['Sensors']]
        canvasSize = (self['Canvas width'], self['Canvas height'])
        chart = MatplotLineMatrix(title=self['Title'], name=self.chartName,
            yaxis_end=self['Y-axis end'], size=canvasSize)
        chart.setSensorNames([[]], sensors)
        chart.setStandardSlice(timeValues[timeNames.index(self['Standard slice'])])
        return chart



class ConsumptionCarpet(ChartTemplate):

    def init(self):
        self.name = 'Consumption carpet chart'
        self.chartName = 'ConsumptionCarpet'
        self.description = """this is a consumption carpet chart ..."""
        self.previewImage = 'ConsumptionCarpet.png'

    def setup(self):
        self.defProp(RT.Text('Title', self.chartName, maxLen=100, descr='title of the chart'))
        sensors = ['Ta', 'Waermezaehler_Uebergabestation', 'Elektrozaehler_Uebergabe_Badenova']
        for s in sensors:
            if not s in self.sensorNames:
                sensors.remove(s)
        self.defProp(RT.MultiChoice('Sensors', sensors, choices=self.sensorNames, descr='sensors to plot'))
        self.defProp(RT.Float('Y-axis end', 0.85, min=0.0, max=1.0, descr=' ??? '))
        self.defProp(RT.Float('Y-axis gap', 0.04, min=0.0, max=1.0, descr=' ??? '))
        self.defProp(RT.Choice('Standard slice', timeNames[2], choices=timeNames, descr='standard slice in plot'))
        self.defProp(RT.Integer('Canvas width', 1000, min=200, max=5000, descr='standard width of plot'))
        self.defProp(RT.Integer('Canvas height',1600, min=200, max=5000, descr='standard height of plot'))

    def createChart(self):
        sensors = list([str(s)] for s in self['Sensors'])
        canvasSize = (self['Canvas width'], self['Canvas height'])
        chart = CarpetPlotMatrix(name=self.chartName, xaxis_end=self['Y-axis end'],
            yaxis_gap=self['Y-axis gap'], title=self['Title'], size=canvasSize)
        chart.setSensorNames([[]], sensors)
        chart.setStandardSlice(timeValues[timeNames.index(self['Standard slice'])])
        return chart



class dtDistrictHeat(ChartTemplate):

    def init(self):
        self.name = 'dt District Heat'
        self.chartName = 'dt_DistrictHeat'
        self.description = """another chart ... who cares?"""
        self.previewImage = 'dtDistrictHeat.png'

    def setup(self):
        self.defProp(RT.Text('Title', self.chartName, maxLen=100, descr='title of the chart'))
        self.defProp(RT.Choice('Sensor', 'dT_fw_threshold', choices=self.sensorNames, descr='sensors to plot'))
        self.defProp(RT.Choice('Standard slice', timeNames[2], choices=timeNames, descr='standard slice in plot'))

    def createChart(self):
        from matplotlib import rc
        rc('axes', grid=True)
        rc('lines', linewidth=3)
        rc('font', family='sans-serif')
        rc('font', size=18)
        rc('axes', titlesize=18)
        rc('axes', labelsize=16)
        rc('xtick', labelsize=16)
        rc('ytick', labelsize=16)
        chart = CarpetPlot(name=self.chartName, title=self['Title'])
        chart.setSensorNames(None, [[str(self['Sensor'])]])
        chart.setStandardSlice(timeValues[timeNames.index(self['Standard slice'])])
        return chart

#####################################################################
#### End of user defined ChartTemplates
#####################################################################



# collect and instantiate all subclasses of ChartTemplates
templateList = [c() for c in sys.modules[__name__].__dict__.values() \
    if type(c) == types.TypeType and issubclass(c, ChartTemplate) and not c == ChartTemplate]
