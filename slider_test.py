from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import pandas as pd
import numpy as np
from PIL import Image

import sys
import os

import typing

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        max = 100000
        x = np.random.randint(10000, size=(1, max))[0]
        y = np.random.randint(10000, size=(1, max))[0]

        plot = pg.plot()
        self.scatter = pg.ScatterPlotItem(x=x,y=y)
        plot.addItem(self.scatter)


        self.mask = np.ones(max)

        self.min_slider = QSlider(Qt.Horizontal,minimum=0,maximum=max, value=0)
        self.min_slider.valueChanged.connect(self.min_changed)
        self.max_slider = QSlider(Qt.Horizontal,minimum=0,maximum=max, value=max)
        self.max_slider.valueChanged.connect(self.max_changed)
        self.label1 = QLabel()
        self.label2 = QLabel()

        slider_layout = QGridLayout()
        slider_layout.addWidget(self.label1,1,1)
        slider_layout.addWidget(self.min_slider,1,2)
        slider_layout.addWidget(self.max_slider,2,2)
        slider_layout.addWidget(self.label2,2,3)

        layout = QVBoxLayout(self)
        layout.addWidget(plot)
        layout.addLayout(slider_layout)

    def min_changed(self, val):
        if val > self.max_slider.value():
            self.max_slider.setValue(val)
        self.label1.setText(str(val))

        self.mask[:val] = 0
        self.mask[val:self.max_slider.value()] = 1
        self.scatter.setPointsVisible(self.mask)

    def max_changed(self, val):
        if val < self.min_slider.value():
            self.min_slider.setValue(val)
        self.label2.setText(str(val))
        self.mask[val:] = 0
        self.mask[self.min_slider.value():val] = 1
        self.scatter.setPointsVisible(self.mask)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()