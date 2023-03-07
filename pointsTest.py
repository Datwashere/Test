from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import distance
from PIL import Image

import sys
import os

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        xy = [[1,2,3,4,5,6],[2,5,1,5,6,8]]
        self.plot = pg.plot()
        scatter = pg.ScatterPlotItem(x=xy[0],y=xy[1],symbol='o', symbolSize=10, data=np.flip(xy[0]),
                                  #symbolPen=pg.mkPen(qRgba(199,23,53,0), width=10),
                                  symbolPen=pg.mkPen(qRgba(0,255,0,10), width=10),
                                  symbolBrush=pg.mkBrush(qRgba(0,255,0,10), width=10),
                                  #fillOutline = True
                                  #pen=pg.mkPen(qRgba(10,23,53,0), width=10),
                                  #pen=pg.mkPen('black', width=20),
                                  # pen=pg.mkPen(pg.getConfigOption('foreground')),
                                  #   brush=pg.mkBrush(100, 100, 150),
                                  #brush=pg.mkBrush(qRgba(255, 255, 255, 120)),
                                  #shadowPen=pg.mkPen(qRgb(155,2,5), width=40),
                                  #shadowPen=pg.mkPen('w', width=25),

                                  )
        mask = np.zeros(len(xy[0]))
        scatter.setPointsVisible(mask)
        scatter.setZValue(-100)

        #(test)
        print(scatter.points()[0].isVisible())
        print(scatter.data['visible'])
        print(scatter.points()[0].data())

        self.plot.addItem(scatter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.plot)

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()