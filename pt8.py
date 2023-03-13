# import pyqtgraph.examples
# pyqtgraph.examples.run()

import pyqtgraph as pg
import pandas as pd
import numpy as np
from PIL import Image

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd

df = pd.read_csv('..\data.csv',
                 #delimiter=',',
                 #skipcols=1,
                 usecols=['x','y','t','category'],
                 nrows=50
                 )

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame([
          [1, 9, 2],
          [1, 0, -1],
          [3, 5, 2],
          [3, 3, 2],
          [5, 8, 9],
        ], columns = ['A', 'B', 'C'], index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])

        self.model = TableModel(df)
        self.table.setModel(self.model)
        self.selectionModel = self.table.selectionModel()
        self.table.selectRow(3)
        self.selectionModel.selectionChanged.connect(self.changed)
        self.setCentralWidget(self.table)

    def changed(self, selected,deselected):


        b =self.table.selectedIndexes()
        for index in b:
            row = index.row()
            print(row)

        print(selected.indexes()[0].row())
        print('sdadas')
"""
try:
lockAspect=True
setBorder(0)
"""
app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()