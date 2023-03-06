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
                 # delimiter=',',
                 # skipcols=1,
                 usecols=['x', 'y', 't', 'category'],
                 nrows=100
                 )
# print(df)

path = 'C:\\Users\\datph\\Downloads\\countries.geojson'
# path = 'geoData.geojson'
mapData = gpd.read_file(path, driver='GeoJSON',
                        #rows=100
                        )
#x, y = mapData.geometry[0].exterior.coords.xy

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        layout = QHBoxLayout(self)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.plot = pg.plot()
        #(plot map test)
        arr = self.shapes()
        # painter = QPainter()
        # painter.setPen(pg.mkPen('w'))
        # painter.setBrush(pg.mkBrush('g') )
        # painter.drawPolygon(self.polygon)
        for i in range(len(arr)):
            poly = pg.arrayToQPath(np.array(arr[0][i]), np.array(arr[1][i]), connect='all')
            item = QGraphicsPathItem(poly)
            item.setPen(pg.mkPen('b'))
            item.setBrush(QColor(200, 0, 0))
            self.plot.addItem(item)
        left_layout.addWidget(self.plot)

        layout.addLayout(left_layout, 3)
        layout.addLayout(right_layout, 1)

        self._options_dict()

        self.tabs = QTabWidget()
        right_layout.addWidget(self.tabs)
        self.tab1()
        self.tab2()


    def shapes(self):
        arr = [[] for i in range(2)]
        for i in range(len(mapData)):
            #print(mapData.geometry[i].geom_type)
            if mapData.geometry[i].geom_type == 'MultiPolygon':
                count = 0
                for poly in list(mapData.geometry[i].geoms):
                    xx, yy = poly.exterior.coords.xy
                    arr[0].append(xx.tolist())
                    arr[1].append(yy.tolist())
                    if count > 6:
                        break
                    count+=1
            else:
                xx, yy = mapData.geometry[i].exterior.coords.xy
                arr[0].append(xx.tolist())
                arr[1].append(yy.tolist())
        #print(arr)
        # print('sdasd:', arr)
        # print(len(arr[0][0]), len(arr[1][0]))
        return arr

    def _options_dict(self):
        # self.options = {
        #     'scatter': [True, self.plot_scatter()],
        #     'line1': [True, self.plot_line()],
        #     'line2': [True, self.plot_line2()]
        # }
        self.options = {
            'scatter': self.plot_scatter,
            'line1': self.plot_line,
            'line2': self.plot_line2
        }

    def tab1(self):
        tab1 = QWidget()
        self.tabs.addTab(tab1, "tab1")

        layout = QVBoxLayout()
        tab1.setLayout(layout)

    def tab2(self):
        tab2 = QWidget()
        self.tabs.addTab(tab2, "tab2")

        layout = QVBoxLayout()
        tab2.setLayout(layout)


        self.checkboxes = []
        self.checked_options = list(self.options.keys())
        #self.draw_items()
        for val in self.options.keys():
            cb = QCheckBox(val)
            cb.setChecked(True)
            cb.stateChanged.connect(self.option_toggled)
            layout.addWidget(cb)
            self.checkboxes.append(cb)
        layout.addStretch(0)


    def option_toggled(self):
        button = self.sender()
        # print('hi', button.text())
        # print(button.isChecked())
        # self.options[button.text()][0] = button.isChecked()

        if button.isChecked():
            self.checked_options.append(button.text())
        else:
            self.checked_options.remove(button.text())
        print(self.checked_options)
        self.draw_items()

    def draw_items(self):
        self.clear_drawings()
        for val in self.checked_options:
            self.options[val]()

    def clear_drawings(self):
        if hasattr(self, 'scatter'):
            self.plot.removeItem(self.scatter)
        if hasattr(self, 'line'):
            self.plot.removeItem(self.line)
        if hasattr(self, 'line2'):
            self.plot.removeItem(self.line2)

    def plot_scatter(self):
        arr = [[1, 2, 3, 4, 5], [2, 3, 5, 3, 6]]
        self.scatter = pg.ScatterPlotItem(x=arr[0], y=arr[1])
        self.plot.addItem(self.scatter)

    def plot_line(self):
        arr = [[1,4],[4,3]]
        self.line = pg.PlotDataItem(x=arr[0], y=arr[1])
        self.plot.addItem(self.line)

    def plot_line2(self):
        arr = [[2, 2], [2, 5]]
        self.line2 = pg.PlotDataItem(x=arr[0], y=arr[1])
        self.plot.addItem(self.line2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
