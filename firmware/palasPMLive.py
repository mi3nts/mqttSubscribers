from datetime import datetime
from os import name
import time
import random
import pyqtgraph as pg
from collections import deque
from pyqtgraph.Qt import QtGui, QtCore
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsLatest as mL

import numpy as np
from pyqtgraph import AxisItem
from datetime import datetime, timedelta
from time import mktime




class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]

class Graph:
    def __init__(self, ):
        self.initRun = True
        self.pm1_frog            = []
        self.pm2_5_frog          = []
        self.pm4_frog            = []
        self.pm10_frog           = []
        self.bins_frog           = []
        self.dateTime_frog       = []
        self.binCenters_frog     =  np.arange(94)
        self.maxLen              = 600          #max number of data points to show on graph
        self.app                 = QtGui.QApplication([])
        self.date_axis           = TimeAxisItem(orientation='bottom')
    
        self.win                 = pg.GraphicsWindow( title="MINTS Ground Vehicle")
    
         # setting pyqtgraph configuration 
 
        self.p1 = self.win.addPlot(axisItems= {'bottom': self.date_axis},title="Fidas® Frog PM Measurment")
        
        self.win.nextRow()
  
        self.curve1 = self.p1.plot()
        self.curve2 = self.p1.plot()
        self.curve3 = self.p1.plot()
        self.curve4 = self.p1.plot()
        self.p1.showGrid(x=True, y=True)
        
        # Legend 
        self.legend = pg.LegendItem(offset=(0., .5))
       
        self.legend.setParentItem(self.p1.graphicsItem())
        self.legend.addItem(self.curve1, 'PM 1')
        self.legend.addItem(self.curve2, 'PM 2.5')
        self.legend.addItem(self.curve3, 'PM 4')
        self.legend.addItem(self.curve4, 'PM 10')

        # self.p1.setLabel('left', "PM Levels", units='μg/m3')
        # self.p1.setLabel(axis='bottom','Date Time (UTC)',units='Date Time (UTC)')
        self.p1.setLabels(
            left="PM Levels (μg/m3)",
            bottom="Date Time (UTC)") 
        # self.p1.addLegend(size=(110, 0) ,offset=(10, 230))
      
        graphUpdateSpeedMs = 1000
        timer = QtCore.QTimer()#to create a thread that calls a function at intervals
        timer.timeout.connect(self.update)#the update function keeps getting called at intervals
        timer.start(graphUpdateSpeedMs)   
        QtGui.QApplication.instance().exec_()

    def pmUpdater(self):
   
        self.pm1_frog.append(self.pm1Now)
        self.pm2_5_frog.append(self.pm2_5Now) 
        self.pm4_frog.append(self.pm4Now) 
        self.pm10_frog.append(self.pm10Now) 
        self.dateTime_frog.append(self.ctNow); 
        self.curve1.setData(x=[x.timestamp() for x in self.dateTime_frog],\
                        y=self.pm1_frog,pen=pg.mkPen('w', width=1,name="PM1"))
        self.curve2.setData(x=[x.timestamp() for x in self.dateTime_frog],\
                        y=self.pm2_5_frog,pen=pg.mkPen('g', width=1,name = "PM 2.5"))
        self.curve3.setData(x=[x.timestamp() for x in self.dateTime_frog], \
                        y=self.pm4_frog,pen=pg.mkPen('b', width=1,name="PM 4"))
        self.curve4.setData(x=[x.timestamp() for x in self.dateTime_frog], \
                        y=self.pm10_frog,pen=pg.mkPen('r', width=1,name = "PM 10"))

        self.app.processEvents()  

    def update(self):

        if len(self.pm1_frog) > self.maxLen:
            self.pm1_frog.pop(0) #remove oldest
            self.pm2_5_frog.pop(0) #remove oldest
            self.pm4_frog.pop(0) #remove oldest
            self.pm10_frog.pop(0) #remove oldest
            self.dateTime_frog.pop(0) #remove oldest 

        
        
        dataIn = mL.readJSONLatestAllMQTT("0001c0231d43","FRG001")
        self.pm1Now   = float(dataIn[0]['pm1'])
        self.pm2_5Now = float(dataIn[0]['pm2_5'])
        self.pm4Now   = float(dataIn[0]['pm4'])
        self.pm10Now  = float(dataIn[0]['pm10'])
         
        self.ctNow =  datetime.strptime(dataIn[0]['dateTime'],'%Y-%m-%d %H:%M:%S')
 
        if self.initRun:
            if (self.pm1Now>0.00):
                self.initRun = False
                self.pmUpdater()
        else: 
            if (self.pm1Now>0.00 and self.ctNow>self.dateTime_frog[-1] ):
                self.pmUpdater()

if __name__ == '__main__':
    g = Graph()
   