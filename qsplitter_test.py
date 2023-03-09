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

        self.df = pd.DataFrame()
        self.df['x'] = [1, 2, 3, 4, 3, 5]
        self.df['y'] = [9, 8, 7, 6, 5, 4]

        plot = pg.plot()
        scatter = pg.ScatterPlotItem(x=self.df.x, y=self.df.y)
        plot.addItem(scatter)

        hbox = QHBoxLayout(self)

        topleft = QWidget()
        vb = QVBoxLayout()
        vb.addWidget(plot)
        topleft.setLayout(vb)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.setSizes([100, 100])
        #splitter1.setCollapsible(1000, True)
        #splitter1.setChildrenCollapsible(False)
        splitter1.addWidget(topleft)

        textedit = QTextEdit()
        splitter1.addWidget(textedit)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()