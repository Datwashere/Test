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
import logging

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        layout = QHBoxLayout(self)
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()

        self.df = pd.DataFrame()
        self.df['x'] = [1,2,3,4,3,5]
        self.df['y'] = [9,8,7,6,5,4]


        self.txt = QPlainTextEdit()
        #self.txt.setReadOnly(True)

        self.txt.old_func = self.txt.keyPressEvent
        self.txt.keyPressEvent = self.new_keyPressEvent
        self.txt.setPlaceholderText('Write pandas query here \n(Press \'Enter\' key to submit)')
        self.txt.resize(400, 200)

        left_layout.addWidget(self.txt)
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.output = QPlainTextEdit()
        right_layout.addWidget(self.output)

    def new_keyPressEvent(self,event):
        if event.key() == Qt.Key_Return:
            text = self.txt.toPlainText()
            try:
                result = self.df.query(text)
            except Exception as e:
                result = repr(e)
            self.output.setPlainText(str(result))
        else:
            self.txt.old_func(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())