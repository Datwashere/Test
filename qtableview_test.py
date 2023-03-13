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

class TableModel(QAbstractTableModel):
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

    def cellClicked(self):
        print('bb')

class QueryDataframeWindow(QWidget):
    def __init__(self, dataframe, parent=None):
        super(QueryDataframeWindow, self).__init__(parent)
        self.setWindowTitle("Query Dataframe Result")
        self.resize(400,600)
        self.df = dataframe

        layout = QVBoxLayout(self)
        save_button = QPushButton("save")
        save_button.clicked.connect(self.save_button_clicked)
        layout.addWidget(save_button)

        table = QTableView()
        model = TableModel(self.df)
        table.setModel(model)
        layout.addWidget(table)

    def changed(self):
        print('ho')

    def save_button_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "csv file (*.csv)")
        if file_path != "":
            self.df.to_csv(file_path)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.df = pd.read_csv('../data.csv',
                         # delimiter=',',
                         # skipcols=1,
                         usecols=['x', 'y', 't', 'category'],
                         nrows=50
                         )

        layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        layout.addLayout(left_layout, 3)
        layout.addLayout(right_layout, 1)

        plot = pg.plot()
        left_layout.addWidget(plot)

        self.txt = QPlainTextEdit()
        # self.txt.setReadOnly(True)
        self.txt.old_func = self.txt.keyPressEvent
        self.txt.keyPressEvent = self.new_keyPressEvent
        self.txt.setPlaceholderText(
            'Write pandas query here. \n> Press \'Enter\' key to search \n> Press \'Shift\'+\'Enter\' keys to filter')
        self.txt.setFixedSize(200, 100)
        right_layout.addWidget(self.txt)

        grid_layout = QGridLayout()
        right_layout.addLayout(grid_layout)

        query_dataframe_button = QPushButton('Dataframe')
        query_dataframe_button.clicked.connect(self.query_dataframe_button_clicked)

        grid_layout.addWidget(query_dataframe_button, 0, 3)
        right_layout.addStretch(0)

    def new_keyPressEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_Return:
            text = self.txt.toPlainText()
            try:
                result = self.df.query(text)
            except Exception as e:
                result = repr(e)
        elif event.key() == Qt.Key_Return:
            text = self.txt.toPlainText()
            try:
                result = self.df.query(text)
            except Exception as e:
                result = repr(e)
        else:
            self.txt.old_func(event)

    def query_dataframe_button_clicked(self):
        self.query_dataframe_window = QueryDataframeWindow(self.df)
        self.query_dataframe_window.show()
        # self.window = QMainWindow()
        # selectNameFilter.window.setWindowTitle("Query Dataframe Result")
        # self.window.resize(400,600)
        # self.window.show()
        #
        # widget = QWidget()
        # layout = QVBoxLayout()
        # widget.setLayout(layout)
        #
        # save_button = QPushButton("save")
        # save_button.clicked.connect(self.save_button_clicked)
        # layout.addWidget(save_button)
        #
        # table = QTableView()
        # model = TableModel(self.df)
        # table.setModel(model)
        # layout.addWidget(table)
        # self.window.setCentralWidget(widget)
        #self.window.setCentralWidget(table)


#CHECK if self.filtered_df belongs to closest points func or track func

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
