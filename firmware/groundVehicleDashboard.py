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
from dateutil import tz
import numpy as np
from pyqtgraph import AxisItem
from datetime import datetime, timedelta
from time import mktime

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]

class Graph:
    def __init__(self, ):
    
        self.win                 = pg.GraphicsWindow( title="MINTS Ground Vehicle")
        self.app                 = QtGui.QApplication([])
        self.lookBack            = timedelta(minutes=5) 
        graphUpdateSpeedMs = 100
         
        ###Frog Graphs
        
        ## Init Frog
        self.initRun_frog = True

        ## Frog Data 
        self.pm1_frog            = []
        self.pm2_5_frog          = []
        self.pm4_frog            = []
        self.pm10_frog           = []
        self.bins_frog           = []
        self.dateTime_frog       = []
        self.binCenters_frog     =  np.arange(93)

        ## Frog PM Plot 
        self.p1_frog = self.win.addPlot(axisItems= {'bottom': TimeAxisItem(orientation='bottom')},title="Fidas® Frog PM Measurment")
        self.curvePm1_frog   = self.p1_frog.plot()
        self.curvePm2_5_frog = self.p1_frog.plot()
        self.curvePm4_frog   = self.p1_frog.plot()
        self.curvePm10_frog = self.p1_frog.plot()

        self.p1_frog.showGrid(x=True, y=True)
        self.p1_frog.setLabels(
            left="PM Levels (μg/m3)",
            bottom="Date Time (Local Time)") 

        # Legend 
        self.legend_frog = pg.LegendItem(offset=(0., .5))
        self.legend_frog.setParentItem(self.p1_frog.graphicsItem())
        self.legend_frog.addItem(self.curvePm1_frog, 'PM 1')
        self.legend_frog.addItem(self.curvePm2_5_frog, 'PM 2.5')
        self.legend_frog.addItem(self.curvePm4_frog, 'PM 4')
        self.legend_frog.addItem(self.curvePm10_frog, 'PM 10')

        ## Frog Histogram Plot 
        self.p2_frog = self.win.addPlot(title="Fidas® Frog Particle Counts")
        self.curveHistogram_frog = self.p2_frog.plot()
        self.p2_frog.setLabels(
            left="Bin Counts",
            bottom="Bin #") 

        # Legend           
        self.legendHist_frog = pg.LegendItem(offset=(0., .5))
        self.legendHist_frog.setParentItem(self.p2_frog.graphicsItem())
        self.legendHist_frog.addItem(self.curveHistogram_frog, 'Histogram Bins')
        self.win.nextRow()

        ### 2BNO- Graphs
        
        ## Init 2bNOx
        self.initRun_2bno = True

        ## 2bno Data 
        self.no_2bno             = []
        self.no2_2bno            = []
        self.nox_2bno            = []
        self.dateTime_2bno       = []

        ## 2bno Plot 
        self.p1_2bno         = self.win.addPlot(axisItems= {'bottom': TimeAxisItem(orientation='bottom')},title="2B NO/NO2/NOx Measurment")
        self.curveNO_2bno    = self.p1_2bno.plot()
        self.curveNO2_2bno   = self.p1_2bno.plot()
        self.curveNOx_2bno   = self.p1_2bno.plot()
        
        self.p1_2bno.showGrid(x=True, y=True)
        self.p1_2bno.setLabels(
            left="NO/NO2/NOx Levels (ppb)",
            bottom="Date Time (Local Time)") 

        # Legend 
        self.legend_2bno = pg.LegendItem(offset=(0., .5))
        self.legend_2bno.setParentItem(self.p1_2bno.graphicsItem())
        self.legend_2bno.addItem(self.curveNO_2bno,  'NO')
        self.legend_2bno.addItem(self.curveNO2_2bno, 'NO2')
        self.legend_2bno.addItem(self.curveNOx_2bno, 'NOx')


        ###2B BC Graphs

        ## Init 2BBC
        self.initRun_2bbc = True

        ## 2BBC Data 
        self.bc_2bbc            = []
        self.dateTime_2bbc      = []
        
        ## 2BBC Plot 
        self.p1_2bbc       = self.win.addPlot(axisItems= {'bottom': TimeAxisItem(orientation='bottom')},title="2B BC Measurment")
        self.curveBC_2bbc  = self.p1_2bbc.plot()
        
        self.p1_2bbc.showGrid(x=True, y=True)
        self.p1_2bbc.setLabels(
            left="BC (μg/m3)",
            bottom="Date Time (Local Time)") 

        # Legend 
        self.legendBC_2bbc = pg.LegendItem(offset=(0., .5))
        self.legendBC_2bbc.setParentItem(self.p1_2bbc.graphicsItem())
        self.legendBC_2bbc.addItem(self.curveBC_2bbc, 'BC')


        ###2B O3 Graphs

        ## Init 2BO3
        self.initRun_2bo3 = True

        ## 2bo3 Data 
        self.o3_2bo3            = []
        self.dateTime_2bo3      = []
        
        ## 2bo3 Plot 
        self.p1_2bo3       = self.win.addPlot(axisItems= {'bottom': TimeAxisItem(orientation='bottom')},title="2B Ozone Measurment")
        self.curveO3_2bo3  = self.p1_2bo3.plot()
        
        self.p1_2bo3.showGrid(x=True, y=True)
        self.p1_2bo3.setLabels(
            left="O3 (ppbv)",
            bottom="Date Time (Local Time)") 

        # Legend 
        self.legendO3_2bo3 = pg.LegendItem(offset=(0., .5))
        self.legendO3_2bo3.setParentItem(self.p1_2bo3.graphicsItem())
        self.legendO3_2bo3.addItem(self.curveO3_2bo3, 'Ozone')
       


        self.win.nextRow()
        ###Licor Graphs

        ## Init Licor
        self.initRun_licor = True

        ## Licor Data 
        self.co2_licor           = []
        self.h2o_licor           = []
        self.dateTime_licor      = []
        
        ## LICOR CO2 Plot 
        self.p1_licor = self.win.addPlot(axisItems= {'bottom': TimeAxisItem(orientation='bottom')},title="Licor CO2 Measurment")
        self.curveCO2_licor =  self.p1_licor.plot()
        
        self.p1_licor.showGrid(x=True, y=True)
        self.p1_licor.setLabels(
            left="CO2 (ppm)",
            bottom="Date Time (Local Time)") 

        # Legend 
        self.legendCO2_licor = pg.LegendItem(offset=(0., .5))
        self.legendCO2_licor.setParentItem(self.p1_licor.graphicsItem())
        self.legendCO2_licor.addItem(self.curveCO2_licor, 'CO2')

        ## LICOR CO2 Plot 
        self.p2_licor        = self.win.addPlot(axisItems= {'bottom': TimeAxisItem(orientation='bottom')},title="Licor H20 Measurment")
        self.curveH2O_licor  = self.p2_licor.plot()
        
        self.p2_licor.showGrid(x=True, y=True)
        self.p2_licor.setLabels(
            left="H20 (mmol/mol)",
            bottom="Date Time (Local Time)") 

        # Legend 
        self.legendH20_licor = pg.LegendItem(offset=(0., .5))
        self.legendH20_licor.setParentItem(self.p2_licor.graphicsItem())
        self.legendH20_licor.addItem(self.curveH2O_licor, 'H20')

        
        ###Partector Graphs

        ## Init Np2
        self.initRun_np2 = True

        ## Np2 Data 
        self.np_np2            = []
        self.dateTime_np2      = []
        
        ## Np2 Plot 
        self.p1_np2       = self.win.addPlot(axisItems= {'bottom': TimeAxisItem(orientation='bottom')},title="Naneos Partector Measurment")
        self.curveNP_np2  = self.p1_np2.plot()
        
        self.p1_np2.showGrid(x=True, y=True)
        self.p1_np2.setLabels(
            left="Nano Particles (HV)",
            bottom="Date Time (Local Time)") 

        # Legend 
        self.legendNP_np2 = pg.LegendItem(offset=(0., .5))
        self.legendNP_np2.setParentItem(self.p1_np2.graphicsItem())
        self.legendNP_np2.addItem(self.curveNP_np2, 'Nanoes Partector HV')

        ### Final Rights 
        timer = QtCore.QTimer()#to create a thread that calls a function at intervals
        timer.timeout.connect(self.update)#the update function keeps getting called at intervals
        timer.start(graphUpdateSpeedMs)   
        QtGui.QApplication.instance().exec_()

    def recursivePoper_frog(self):

        if self.dateTime_frog[0] < self.currentTime - self.lookBack  :
            self.pm1_frog.pop(0) #remove oldest
            self.pm2_5_frog.pop(0) #remove oldest
            self.pm4_frog.pop(0) #remove oldest
            self.pm10_frog.pop(0) #remove oldest
            self.dateTime_frog.pop(0) #remove oldest 
            if len(self.dateTime_frog) == 0:
                self.initRun_frog = True
            else:
                self.recursivePoper_frog()
        else:
            return 
        

    def frogUpdater(self):
        self.pm1_frog.append(self.pm1Now_frog)
        self.pm2_5_frog.append(self.pm2_5Now_frog) 
        self.pm4_frog.append(self.pm4Now_frog) 
        self.pm10_frog.append(self.pm10Now_frog) 
        self.dateTime_frog.append(self.ctNow_frog); 
        
        # For Histogram 
        self.curvePm1_frog.setData(x=[x.timestamp() for x in self.dateTime_frog],\
                        y=self.pm1_frog,pen=pg.mkPen('w', width=1,name="PM1"))
        self.curvePm2_5_frog.setData(x=[x.timestamp() for x in self.dateTime_frog],\
                        y=self.pm2_5_frog,pen=pg.mkPen('g', width=1,name = "PM 2.5"))
        self.curvePm4_frog.setData(x=[x.timestamp() for x in self.dateTime_frog], \
                        y=self.pm4_frog,pen=pg.mkPen('b', width=1,name="PM 4"))
        self.curvePm10_frog.setData(x=[x.timestamp() for x in self.dateTime_frog], \
                        y=self.pm10_frog,pen=pg.mkPen('r', width=1,name = "PM 10"))
        self.curveHistogram_frog.setData(y=self.binsNow_frog, fillLevel=0,\
                             fillOutline=True, brush=(0,0,255,150),stepMode="left")

 
    def frogDataReader(self):

        dataIn = mL.readJSONLatestAllMQTT("0001c0231d43","FRG001")[0]
 
        self.pm1Now_frog   = float(dataIn['pm1'])
        self.pm2_5Now_frog = float(dataIn['pm2_5'])
        self.pm4Now_frog   = float(dataIn['pm4'])
        self.pm10Now_frog  = float(dataIn['pm10'])
        self.binsNow_frog  = [float(dataIn['binCount0']),float(dataIn['binCount1']) ,float(dataIn['binCount2']),float(dataIn['binCount3']),float(dataIn['binCount4']),\
                        float(dataIn['binCount5']),float(dataIn['binCount6']) ,float(dataIn['binCount7']),float(dataIn['binCount8']),float(dataIn['binCount9']),\
                        float(dataIn['binCount10']),float(dataIn['binCount11']) ,float(dataIn['binCount12']),float(dataIn['binCount13']),float(dataIn['binCount14']),\
                        float(dataIn['binCount15']),float(dataIn['binCount16']) ,float(dataIn['binCount17']),float(dataIn['binCount18']),float(dataIn['binCount19']),\
                        float(dataIn['binCount20']),float(dataIn['binCount21']) ,float(dataIn['binCount22']),float(dataIn['binCount23']),float(dataIn['binCount24']),\
                        float(dataIn['binCount25']),float(dataIn['binCount26']) ,float(dataIn['binCount27']),float(dataIn['binCount28']),float(dataIn['binCount29']),\
                        float(dataIn['binCount30']),float(dataIn['binCount31']) ,float(dataIn['binCount32']),float(dataIn['binCount33']),float(dataIn['binCount34']),\
                        float(dataIn['binCount35']),float(dataIn['binCount36']) ,float(dataIn['binCount37']),float(dataIn['binCount38']),float(dataIn['binCount39']),
                        float(dataIn['binCount40']),float(dataIn['binCount41']) ,float(dataIn['binCount42']),float(dataIn['binCount43']),float(dataIn['binCount44']),\
                        float(dataIn['binCount45']),float(dataIn['binCount46']) ,float(dataIn['binCount47']),float(dataIn['binCount48']),float(dataIn['binCount49']),\
                        float(dataIn['binCount50']),float(dataIn['binCount51']) ,float(dataIn['binCount52']),float(dataIn['binCount53']),float(dataIn['binCount54']),\
                        float(dataIn['binCount55']),float(dataIn['binCount56']) ,float(dataIn['binCount57']),float(dataIn['binCount58']),float(dataIn['binCount59']),\
                        float(dataIn['binCount60']),float(dataIn['binCount61']) ,float(dataIn['binCount62']),float(dataIn['binCount63']),float(dataIn['binCount64']),\
                        float(dataIn['binCount65']),float(dataIn['binCount66']) ,float(dataIn['binCount67']),float(dataIn['binCount68']),float(dataIn['binCount69']),\
                        float(dataIn['binCount70']),float(dataIn['binCount71']) ,float(dataIn['binCount72']),float(dataIn['binCount73']),float(dataIn['binCount74']),\
                        float(dataIn['binCount75']),float(dataIn['binCount76']) ,float(dataIn['binCount77']),float(dataIn['binCount78']),float(dataIn['binCount79']),\
                        float(dataIn['binCount80']),float(dataIn['binCount81']) ,float(dataIn['binCount82']),float(dataIn['binCount83']),float(dataIn['binCount84']),\
                        float(dataIn['binCount85']),float(dataIn['binCount86']) ,float(dataIn['binCount87']),float(dataIn['binCount88']),float(dataIn['binCount89']),\
                        float(dataIn['binCount90']),float(dataIn['binCount91']) ,float(dataIn['binCount92']),float(dataIn['binCount93'])]
        self.binsNow_frog  = [(i > 0) * i for i in self.binsNow_frog]

        self.ctNow_frog =  datetime.strptime(dataIn['dateTime'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.tzutc()).astimezone(tz.gettz())

        if self.initRun_frog:
            if (self.pm1Now_frog>0.00):
                    self.initRun_frog = False
                    self.frogUpdater()
        else: 
            if (self.pm1Now_frog>0.00 and self.ctNow_frog>=self.dateTime_frog[-1] ):
                    
                    self.recursivePoper_frog()
                    self.frogUpdater()

# FOR Licor 

    def recursivePoper_licor(self):

        if self.dateTime_licor[0] < self.currentTime - self.lookBack  :
            self.co2_licor.pop(0) #remove oldest
            self.h2o_licor.pop(0) #remove oldest
            self.dateTime_licor.pop(0) #remove oldest 
            if len(self.dateTime_licor) == 0:
                self.initRun_licor = True
            else:
                self.recursivePoper_licor()

        else:
            return 

    def licorUpdater(self):

        self.co2_licor.append(self.co2Now_licor)
        self.h2o_licor.append(self.h2oNow_licor) 
        self.dateTime_licor.append(self.ctNow_licor); 
        
        # For Histogram 
        self.curveCO2_licor.setData(x=[x.timestamp() for x in self.dateTime_licor],\
                        y=self.co2_licor,pen=pg.mkPen('w', width=1,name="CO2"))
        self.curveH2O_licor.setData(x=[x.timestamp() for x in self.dateTime_licor],\
                        y=self.h2o_licor,pen=pg.mkPen('b', width=1,name = "H20"))


    def licorDataReader(self):

        dataIn = mL.readJSONLatestAllMQTT("001e0610c2e7","LICOR")[0]
        self.co2Now_licor   = float(dataIn['CO2'])
        self.h2oNow_licor   = float(dataIn['H2O'])
        self.ctNow_licor    =  datetime.strptime(dataIn['dateTime'],'%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.gettz())

        if self.initRun_licor:
            if (self.co2Now_licor>0.00):
                    self.initRun_licor = False
                    self.licorUpdater()
        else: 
            if (self.co2Now_licor>0.00 and self.ctNow_licor>=self.dateTime_licor[-1] ):
                    self.recursivePoper_licor()
                    self.licorUpdater()

# FOR 2BBC 

    def recursivePoper_2bbc(self):

        if self.dateTime_2bbc[0] < self.currentTime - self.lookBack  :
            self.bc_2bbc.pop(0) #remove oldest
            self.dateTime_2bbc.pop(0) #remove oldest 
            if len(self.dateTime_2bbc) == 0:
                self.initRun_2bnc = True
            else:
                self.recursivePoper_2bbc()

        else:
            return 

    def t2bbcUpdater(self):

        self.bc_2bbc.append(self.bcNow_2bbc)
        self.dateTime_2bbc.append(self.ctNow_2bbc)
        self.curveBC_2bbc.setData(x=[x.timestamp() for x in self.dateTime_2bbc],\
                        y=self.bc_2bbc,pen=pg.mkPen((150,150,150), width=1,name = "BC"))


    def t2bbcDataReader(self):

        dataIn = mL.readJSONLatestAllMQTT("001e0610c2e7","2B-BC")[0]
        self.bcNow_2bbc  = float(dataIn['BC'])
        self.ctNow_2bbc  =  datetime.strptime(dataIn['dateTime'],'%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.gettz())

        if self.initRun_2bbc:
            if (self.bcNow_2bbc>-100.00):
                    self.initRun_2bbc = False
                    self.t2bbcUpdater()
        else: 
            if (self.bcNow_2bbc>-100.00 and self.ctNow_2bbc>=self.dateTime_2bbc[-1] ):
                    self.recursivePoper_2bbc()
                    self.t2bbcUpdater()

    # FOR 2BNO
    def recursivePoper_2bno(self):

        if self.dateTime_2bno[0] < self.currentTime - self.lookBack  :
            self.no_2bno.pop(0) #remove oldest
            self.no2_2bno.pop(0) #remove oldest
            self.nox_2bno.pop(0) #remove oldest
            self.dateTime_2bno.pop(0) #remove oldest 
            if len(self.dateTime_2bno) == 0:
                self.initRun_2bno = True
            else:
                self.recursivePoper_2bno()
        else:
            return 
        

    def t2bnoUpdater(self):
        self.no_2bno.append(self.noNow_2bno)
        self.no2_2bno.append(self.no2Now_2bno) 
        self.nox_2bno.append(self.noxNow_2bno) 
        self.dateTime_2bno.append(self.ctNow_2bno); 
        
        # For Histogram 
        self.curveNO_2bno.setData(x=[x.timestamp() for x in self.dateTime_2bno],\
                        y=self.no_2bno,pen=pg.mkPen('b', width=1,name="NO"))
        self.curveNO2_2bno.setData(x=[x.timestamp() for x in self.dateTime_2bno],\
                        y=self.no2_2bno,pen=pg.mkPen('g', width=1,name = "NO2"))
        self.curveNOx_2bno.setData(x=[x.timestamp() for x in self.dateTime_2bno], \
                        y=self.nox_2bno,pen=pg.mkPen('r', width=1,name="NOx"))
 
    def t2bnoDataReader(self):

        dataIn = mL.readJSONLatestAllMQTT("001e0610c2e7","2B-NOX")[0]
     
        self.noNow_2bno   = float(dataIn['NO'])
        self.no2Now_2bno  = float(dataIn['NO2'])
        self.noxNow_2bno  = float(dataIn['NOX'])
        self.ctNow_2bno   =  datetime.strptime(dataIn['dateTime'],'%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.gettz())

        if self.initRun_2bno:
            if (self.noNow_2bno>-100.00):
                    self.initRun_2bno = False
                    self.t2bnoUpdater()
        else: 
            if (self.noNow_2bno>-100.00 and self.ctNow_2bno>=self.dateTime_2bno[-1] ):
                    self.recursivePoper_2bno()
                    self.t2bnoUpdater()

    # For 2BO3
    def recursivePoper_2bo3(self):
        if self.dateTime_2bo3[0] < self.currentTime - self.lookBack  :
            self.o3_2bo3.pop(0) #remove oldest
            self.dateTime_2bo3.pop(0) #remove oldest 
            if len(self.dateTime_2bo3) == 0:
                self.initRun_2bo3 = True
            else:
                self.recursivePoper_2bo3()
        else:
            return 

    def t2bo3Updater(self):
        self.o3_2bo3.append(self.o3Now_2bo3)
        self.dateTime_2bo3.append(self.ctNow_2bo3)
        self.curveO3_2bo3.setData(x=[x.timestamp() for x in self.dateTime_2bo3],\
                        y=self.o3_2bo3,pen=pg.mkPen('b', width=1,name = "Ozone"))


    def t2bo3DataReader(self):
        dataIn = mL.readJSONLatestAllMQTT("001e0610c2e7","2B-O3")[0]
        self.o3Now_2bo3  = float(dataIn['ozone'])
        self.ctNow_2bo3  =  datetime.strptime(dataIn['dateTime'],'%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.gettz())

        if self.initRun_2bo3:
            if (self.o3Now_2bo3>-100.00):
                    self.initRun_2bo3 = False
                    self.t2bo3Updater()
        else: 
            if (self.o3Now_2bo3>-100.00 and self.ctNow_2bo3>=self.dateTime_2bo3[-1] ):
                    self.recursivePoper_2bo3()
                    self.t2bo3Updater()

    # For Naneos Partector
    def recursivePoper_np2(self):
        
        if self.dateTime_np2[0] < self.currentTime - self.lookBack  :
            self.np_np2.pop(0) #remove oldest
            self.dateTime_np2.pop(0) #remove oldest 
            if len(self.dateTime_np2) == 0:
                self.initRun_np2 = True
            else:
                self.recursivePoper_np2()
        else:
            return 

    def np2Updater(self):
        self.np_np2.append(self.npNow_np2)
        self.dateTime_np2.append(self.ctNow_np2)
        self.curveNP_np2.setData(x=[x.timestamp() for x in self.dateTime_np2],\
                        y=self.np_np2,pen=pg.mkPen('y', width=1,name ="Nano Particles"))


    def np2DataReader(self):
        dataIn = mL.readJSONLatestAllMQTT("001e0610c2e7","NP2")[0]
        self.npNow_np2  = float(dataIn['p3'])
        self.ctNow_np2  =  datetime.strptime(dataIn['dateTime'],'%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.gettz())

        if self.initRun_np2:
            if (self.npNow_np2>-100.00):
                    self.initRun_np2 = False
                    self.np2Updater()
        else: 
            if (self.npNow_np2>-100.00 and self.ctNow_np2>=self.dateTime_np2[-1] ):
                    self.recursivePoper_np2()
                    self.np2Updater()
                    
    def update(self):
        self.currentTime=  datetime.now().astimezone(tz.gettz())
        self.frogDataReader()
        self.licorDataReader()
        self.t2bbcDataReader()
        self.t2bnoDataReader()
        self.t2bo3DataReader()
        self.np2DataReader()
        self.app.processEvents() 

if __name__ == '__main__':
    g = Graph()
 