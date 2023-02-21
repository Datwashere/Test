from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import distance

import sys
import os

colors = {
    1: 'red',
    2: 'green',
    3: 'blue',
    4: 'yellow',
    5: 'purple',
    6: 'pink',
    7: 'black',
    8: 'pink',
    9: 'orange'
}

symbols = {
    1: 'o',
    2: 't',
    3: 't1',
    4: 'p',
    5: 'h',
    6: 'star',
    7: '+',
    8: 'x',
    9: 'd'
}

df = pd.read_csv('..\data.csv',
                 #delimiter=',',
                 #skipcols=1,
                 usecols=['x','y','t','category'],
                 nrows=1000
                 )
#print(df)

path = 'C:\\Users\\datph\\Downloads\\countries.geojson'
#path = 'geoData.geojson'
mapData = gpd.read_file(path, driver='GeoJSON',
                        rows=10
                        )
x,y = mapData.geometry[0].exterior.coords.xy

# plot = pg.plot()
# poly = pg.arrayToQPath(np.array(x),np.array(y))
# item = QGraphicsPathItem(poly)
# #item.setBrush()
# item.setPen(QColor(168, 34, 3))
#
# plot.addItem(item)
# plot.show()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        layout = QVBoxLayout()
        sliderLayout = QGridLayout()
        rightLayout = QHBoxLayout()

        self.plot = pg.plot()
        scatter = pg.ScatterPlotItem(size=7, hoverable=True)
        #mask = np.ones(len(df))
        #legend = pg.LegendItem(pen=QColor(255,255,255), frame=True, labelTextSize='9pt', verSpacing=0)
        for k in list(symbols.keys()):
            temp_df = df.loc[df.category == k]
            scatter.addPoints(x=temp_df.x, y=temp_df.y, symbol=symbols[k], pen={'color':colors[k]})
            #legend.addItem(scatter, 'scatter')
        #scatter.setPointsVisible(visible=True, update=True, mask=mask)
        scatter.sigClicked.connect(self.clicked)
        self.plot.addItem(scatter)
        #(limit plot range here)
        #self.plot.setLimits(xMin=0, xMax=15, yMin=0, yMax=15)
        layout.addWidget(self.plot)

        #legend.setParentItem(self.plot)
        plot2 = pg.plot()
        #plot2.setGeometry(10,20,5,5)
        plot2.setLimits(xMin=0, xMax=10, yMin=0, yMax=10)
        legend = pg.ScatterPlotItem()
        for i in range(len(symbols)):
            legend.addPoints(x=[1],y=[i+1], symbol=symbols[i+1],pen={'color':colors[i+1]})
            text = pg.TextItem(symbols[i+1])
            text.setPos(2,i+1)
            plot2.addItem(text)
        plot2.addItem(legend)
        rightLayout.addWidget(plot2)

        min = df.t.min()
        max = df.t.max()
        self.min_slider = QSlider(Qt.Horizontal, minimum=min, maximum=max, value=min)
                              #tickInterval=60*60,
                              #tickPosition=QSlider.TicksBelow)
        self.min_slider.valueChanged.connect(self.update_plot)

        self.max_slider = QSlider(Qt.Horizontal, minimum=min, maximum=max, value=max)
        self.max_slider.valueChanged.connect(self.update_plot)

        self.time = QLabel("time: ",self)
        self.minLabel = QLabel("min: "+str(min), self)
        self.maxLabel = QLabel("max: "+str(max), self)

        # sliderLayout.addWidget(self.time,1,1)
        sliderLayout.addWidget(self.minLabel, 1, 1)
        sliderLayout.addWidget(self.min_slider, 1, 2)
        sliderLayout.addWidget(self.maxLabel, 1, 4)
        sliderLayout.addWidget(self.max_slider, 1, 3)

        self.setLayout(layout)
        layout.addLayout(sliderLayout)
        layout.addLayout(rightLayout)
        #(mask)
        self.mask = np.zeros(max)

    def update_plot(self):
        self.max_slider.setMinimum(self.min_slider.value())
        self.min_slider.setMaximum(self.max_slider.value())

        self.mask[self.min_slider.value():self.max_slider.value()] = 1
        self.mask[:self.min_slider.value()] = 0
        self.mask[self.max_slider.value():] = 0
        #print(self.mask)

        self.minLabel.setText("min: " + str(self.min_slider.value()))
        self.maxLabel.setText("max: " + str(self.max_slider.value()))

    def clicked(self, points):

        #print(points.pos.x())
        #y = ev.pos().y()
        x = points.data[0][0]
        y = points.data[0][1]

        #(test)
        # temp = df.query('x-5 <= x <= x+5 and y-5 < x < y+5')
        # arr = df.sort_values(by=['x', 'y'])
        # pt_idx = 20
        # temp = df.loc[pt_idx-5:pt_idx+5]

        pt = (x,y)
        print(pt)
        n = 6
        arr = np.stack((df.x, df.y), axis=1)
        closest_idx = distance.cdist([pt], arr).argsort()
        closest_pts = arr[closest_idx[0][:n]]
        print(closest_pts[0][0])
        connected_nodes = [[0,i] for i in range(n)]

        timeDelta = pg.GraphItem()
        # Update the graph
        timeDelta.setData(pos=closest_pts, adj=np.array(connected_nodes), pxMode=False , size=5)
        self.plot.addItem(timeDelta)
        texts = ["Point %d" % i for i in range(6)]

        for i in range(1,len(closest_pts)):
            text = pg.TextItem('hi')
            text.setPos(closest_pts[i][0],closest_pts[i][1])
            self.plot.addItem(text)

    # def mouseClickEvent(self, ev):
    #     if ev.button() == Qt.MouseButton.RightButton:
    #         self.autoRange()
def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()