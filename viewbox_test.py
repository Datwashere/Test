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

import typing

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        img = Image.open('../images/burger.jpg')
        img_arr = np.array(img)

        layout = QHBoxLayout(self)
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()

        self.plot = pg.GraphicsLayoutWidget()
        self.plot.setFixedHeight(1000)
        self.plot.ci.layout.setContentsMargins(0,0,0,0)
        self.plot.ci.layout.setSpacing(0)
        self.plot.keyPressEvent = self.scroll_area_keyPressEvent
        scroll_area = QScrollArea()
        self.plot.wheelEvent = scroll_area.wheelEvent

        self.viewboxes = []
        for i in range(5):
            vb: pg.viewBox = self.plot.addViewBox()
            vb.setMouseEnabled(x=False,y=False)
            img = pg.ImageItem(img_arr)
            vb.setDefaultPadding(0)
            vb.setBorder(pg.mkPen('g'))
            print(vb.size())
            print(vb.pos())
            vb.addItem(img)
            #vb.wheelEvent = self.viewboxWheelEvent
            #vb.wheelEvent = scroll_area.wheelEvent
            self.viewboxes.append(vb)
            self.plot.nextRow()

        scroll_area.focusNextPrevChild(True)
        #print(scroll_area.children()[2].value)
        #scroll_area.scrollContentsBy()
        print(scroll_area.size())
        print(scroll_area.pos())
        scroll_area.setWidgetResizable(True)
        scroll_area.setContentsMargins(0,0,0,0)
        scroll_area.setWidget(self.plot)
        left_layout.addWidget(scroll_area)
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        #(imageItem directly on graphicslayoutwidget test)
        plot2 = pg.plot()
        plot2.showAxes(False)
        plot2.setMouseEnabled(x=False,y=False)
        plot2.setDefaultPadding(0)
        img = pg.ImageItem(img_arr)
        img.setZValue(0)
        plot2.addItem(img)
        right_layout.addWidget(plot2)

        # (for invisibility mask)
        # a = [2, 3]
        # df.loc[a, 't'] = 16
        #
        # (for graphics layout)
        # pg.GraphicsLayoutWidget.itemIndex(item)

    def viewboxWheelEvent(self, event):
        print('hi')

    def scroll_area_keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_Up:
            print('hi')
            print(self.viewboxes[0].pos())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())