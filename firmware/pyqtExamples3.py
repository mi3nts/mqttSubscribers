from datetime import datetime
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

class Graph:
    def __init__(self, ):
        self.pm1_frog            = deque()
        self.pm2_5_frog          = deque()
        self.pm4_frog            = deque()
        self.pm10_frog           = deque()
        self.bins_frog           = deque()
        self.dateTime_frog       = deque()
        self.binCenters_frog     =  np.arange(94)
        self.maxLen              = 50          #max number of data points to show on graph
        self.app                 = QtGui.QApplication([])
        self.win                 = pg.GraphicsWindow()
       
        self.p1 = self.win.addPlot(colspan=2)
        self.win.nextRow()
        # self.p2 = self.win.addPlot(colspan=2)
        # self.win.nextRow()
        # self.p3 = self.win.addPlot(colspan=2)
        axis = DateAxisItem(orientation='bottom')
        axis.attachToPlotItem(self.p1.getPlotItem())

    # plot some random data with timestamps in the last hour

    
        self.curve1 = self.p1.plot()
        # self.curve2 = self.p2.plot()
        # self.curve3 = self.p3.plot()
       
        graphUpdateSpeedMs = 1000
        timer = QtCore.QTimer()#to create a thread that calls a function at intervals
        timer.timeout.connect(self.update)#the update function keeps getting called at intervals
        timer.start(graphUpdateSpeedMs)   
        QtGui.QApplication.instance().exec_()
       
    def update(self):
        if len(self.pm2_5_frog) > self.maxLen:
            self.pm2_5_frog.popleft() #remove oldest
        if len(self.dateTime_frog) > self.maxLen:
            self.dateTime_frog.popleft() #remove ol

        dataIn = mL.readJSONLatestAllMQTT("0001c0231d43","FRG001")
        print(dataIn[0]['pm2_5'])
        # now = time.time()
        

        self.pm2_5_frog.append(float(dataIn[0]['pm2_5'])); 
        self.dateTime_frog.append(datetime(dataIn[0]['dateTime'])); 
        timestamps = np.linspace(self.dateTime_frog[0],self.dateTime_frog[-1], 100)

        self.curve1.setData(x=timestamps, y= self.pm2_5_frog)
        self.app.processEvents()  

# __all__ = ["DateAxisItem"]

# import numpy
# from pyqtgraph import AxisItem
# from datetime import datetime, timedelta
# from time import mktime


class DateAxisItem(AxisItem):
    """c
    A tool that provides a date-time aware axis. It is implemented as an
    AxisItem that interpretes positions as unix timestamps (i.e. seconds
    since 1970).
    The labels and the tick positions are dynamically adjusted depending
    on the range.
    It provides a  :meth:`attachToPlotItem` method to add it to a given
    PlotItem
    """
    
    # Max width in pixels reserved for each label in axis
    # _pxLabelWidth = 80

    def __init__(self, *args, **kwargs):
        AxisItem.__init__(self, *args, **kwargs)
        self._oldAxis = None

    def tickValues(self, minVal, maxVal, size):
        """
        Reimplemented from PlotItem to adjust to the range and to force
        the ticks at "round" positions in the context of time units instead of
        rounding in a decimal base
        """

        maxMajSteps = int(size/self._pxLabelWidth)

        dt1 = datetime.fromtimestamp(minVal)
        dt2 = datetime.fromtimestamp(maxVal)

        dx = maxVal - minVal
        majticks = []

        if dx > 63072001:  # 3600s*24*(365+366) = 2 years (count leap year)
            d = timedelta(days=366)
            for y in range(dt1.year + 1, dt2.year):
                dt = datetime(year=y, month=1, day=1)
                majticks.append(mktime(dt.timetuple()))

        elif dx > 5270400:  # 3600s*24*61 = 61 days
            d = timedelta(days=31)
            dt = dt1.replace(day=1, hour=0, minute=0,
                             second=0, microsecond=0) + d
            while dt < dt2:
                # make sure that we are on day 1 (even if always sum 31 days)
                dt = dt.replace(day=1)
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 172800:  # 3600s24*2 = 2 days
            d = timedelta(days=1)
            dt = dt1.replace(hour=0, minute=0, second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 7200:  # 3600s*2 = 2hours
            d = timedelta(hours=1)
            dt = dt1.replace(minute=0, second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 1200:  # 60s*20 = 20 minutes
            d = timedelta(minutes=10)
            dt = dt1.replace(minute=(dt1.minute // 10) * 10,
                             second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 120:  # 60s*2 = 2 minutes
            d = timedelta(minutes=1)
            dt = dt1.replace(second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 20:  # 20s
            d = timedelta(seconds=10)
            dt = dt1.replace(second=(dt1.second // 10) * 10, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d

        elif dx > 2:  # 2s
            d = timedelta(seconds=1)
            majticks = range(int(minVal), int(maxVal))

        else:  # <2s , use standard implementation from parent
            return AxisItem.tickValues(self, minVal, maxVal, size)

        L = len(majticks)
        if L > maxMajSteps:
            majticks = majticks[::int(numpy.ceil(float(L) / maxMajSteps))]

        return [(d.total_seconds(), majticks)]

    def tickStrings(self, values, scale, spacing):
        """Reimplemented from PlotItem to adjust to the range"""
        ret = []
        if not values:
            return []

        if spacing >= 31622400:  # 366 days
            fmt = "%Y"

        elif spacing >= 2678400:  # 31 days
            fmt = "%Y %b"

        elif spacing >= 86400:  # = 1 day
            fmt = "%b/%d"

        elif spacing >= 3600:  # 1 h
            fmt = "%b/%d-%Hh"

        elif spacing >= 60:  # 1 m
            fmt = "%H:%M"

        elif spacing >= 1:  # 1s
            fmt = "%H:%M:%S"

        else:
            # less than 2s (show microseconds)
            # fmt = '%S.%f"'
            fmt = '[+%fms]'  # explicitly relative to last second

        for x in values:
            try:
                t = datetime.fromtimestamp(x)
                ret.append(t.strftime(fmt))
            except ValueError:  # Windows can't handle dates before 1970
                ret.append('')

        return ret

    def attachToPlotItem(self, plotItem):
        """Add this axis to the given PlotItem
        :param plotItem: (PlotItem)
        """
        self.setParentItem(plotItem)
        viewBox = plotItem.getViewBox()
        self.linkToView(viewBox)
        self._oldAxis = plotItem.axes[self.orientation]['item']
        self._oldAxis.hide()
        plotItem.axes[self.orientation]['item'] = self
        pos = plotItem.axes[self.orientation]['pos']
        plotItem.layout.addItem(self, *pos)
        self.setZValue(-1000)

    def detachFromPlotItem(self):
        """Remove this axis from its attached PlotItem
        (not yet implemented)
        """
        raise NotImplementedError()  # TODO


# if __name__ == '__main__':

#     import time
#     import sys
#     import pyqtgraph as pg
#     from PyQt5 import QtGui

#     app = QtGui.QApplication([])

#     w = pg.PlotWidget()

    # # Add the Date-time axis
    # axis = DateAxisItem(orientation='bottom')
    # axis.attachToPlotItem(w.getPlotItem())

    # # plot some random data with timestamps in the last hour
    # now = time.time()
    # timestamps = numpy.linspace(now - 3600, now, 100)
    # w.plot(x=timestamps, y=numpy.random.rand(100), symbol='o')
    
    # w.show()

    # sys.exit(app.exec_())



if __name__ == '__main__':
    g = Graph()
   