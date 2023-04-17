from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import pandas as pd
import geopandas as gpd
import numpy as np

import sys
import os


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(400, 200)
        layout = QVBoxLayout(self)

        text_box = QLineEdit()

        self.combo_box = QComboBox()
        self.combo_box.setEditable(True)
        self.combo_box.setInsertPolicy(QComboBox.InsertAtTop)
        self.combo_box.setLineEdit(text_box)
        self.combo_box.addItems(self.get_history())

        layout.addWidget(self.combo_box)

    def get_history(self):
        with open("history.txt", "r+") as file:
            history = file.read().split('\n')
        return list(filter(None, history))

    def leaveEvent(self, QEvent):
        with open("history.txt", "w") as file:
            [file.write(self.combo_box.itemText(i)+'\n') for i in range(min(5,self.combo_box.count()))]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
