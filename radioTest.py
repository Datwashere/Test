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

df =pd.read_csv('..\data.csv',
                 #delimiter=',',
                 #skipcols=1,
                 usecols=['x','y','t','category'],
                 nrows=40
                 )

prevClickedLabelId = None
class customizedLabel(QLabel):
    def __init__(self, id=None, parent=None):
        super(customizedLabel, self).__init__(parent)
        self.setParent(parent)
        self.clicked = 0
        self.id = id

    def enterEvent(self, event):
        self.setStyleSheet("border: 2px solid blue; background-color: lightgreen;")

    def leaveEvent(self, event):
        if self.clicked != 1:
            self.setStyleSheet("");

    def mouseReleaseEvent(self, event):
        #print(event.type())
        self.clicked = 1
        self.setStyleSheet("border: 2px solid blue")

        #(need to use global variables?)
        global prevClickedLabelId
        prevClickedLabelId = self.id

    def turnBorderOff(self):
        self.setStyleSheet("")

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.plot = pg.plot()
        pg.setConfigOptions(antialias=True)
        #pg.setAspectLocked(True)

        #scatter = pg.ScatterPlotItem(x=df.x, y=df.y, hoverable=True)
        self.scatter = pg.ScatterPlotItem(size=7, hoverable=True)
        # mask = np.ones(len(df))
        # legend = pg.LegendItem(pen=QColor(255,255,255), frame=True, labelTextSize='9pt', verSpacing=0)
        for k in list(symbols.keys()):
            temp_df = df.loc[df.category == k]
            self.scatter.addPoints(x=temp_df.x, y=temp_df.y, symbol=symbols[k], pen={'color': colors[k]}, brush=pg.mkBrush(255, 255, 255, 120), hoverable=True, hoverSize=10, hoverSymbol=None)
            self.scatter.sigClicked.connect(self.scatter_clicked)
            self.scatter.sigHovered.connect(self.scatter_hovered)
        self.plot.addItem(self.scatter)

        layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.setLayout(layout)
        layout.addLayout(left_layout,3)
        layout.addLayout(right_layout,1)

        left_layout.addWidget(self.plot)

        radio_layout = QVBoxLayout()
        scroll_layout = QVBoxLayout()
        right_layout.addLayout(radio_layout,1)
        right_layout.addLayout(scroll_layout,3)

        #(test)
        img = Image.open('../images/map.jpg')
        img_arr = np.array(img)
        img_item = pg.ImageItem(img_arr)
        #img_item.setZValue(-100)
        #self.plot.addItem(img_item)

        # (option 1)
        #data = Image.fromarray(img_arr, 'RGB')

        # (option 2)
        height, width, channels = img_arr.shape
        bytesPerLine = channels * width
        qImg = QImage(img_arr.data, width, height, bytesPerLine, QImage.Format_RGB888)

        # img_label = QLabel()
        # img_label.setPixmap(QPixmap(qImg))
        # radio_layout.addWidget(img_label)

        radioButton = QRadioButton("A")
        #radioButton.setPix
        radioButton.setChecked(True)
        radioButton.val = "A"
        radioButton.toggled.connect(self.radioButtonState)
        radio_layout.addWidget(radioButton)
        radioButton.setStyleSheet("QRadioButton"
                                   "{"
                                   "background-image : url(../images/homer.png);"
                                   "}")

        radioButton = QRadioButton("B")
        radioButton.val = "B"
        radioButton.toggled.connect(self.radioButtonState)
        radio_layout.addWidget(radioButton)

        radioButton = QRadioButton("C")
        radioButton.val = "C"
        radioButton.toggled.connect(self.radioButtonState)
        radio_layout.addWidget(radioButton)

        #(test)
        self.info = QVBoxLayout()
        #self.info.setContentsMargins()
        self.info.setSpacing(0)
        self.info.setContentsMargins(0,0,0,0)

        box = QGroupBox()
        box.setLayout(self.info)

        self.scroll_area = QScrollArea()
        # self.scrol_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(box)
        #self.scroll_area.setFixedHeight(200)
        scroll_layout.addWidget(self.scroll_area)
        #right_layout.setCentralWidget(self.scroll_area)



        self.prev_hovered_pt = None
        self.current_pt = None
    def imgLabelMousePressEvent(self, event):
        global prevClickedLabelId
        #print(prevClickedLabelId)
        # print(self.img_labels[0].id + 1)
        #if len(prevClickedLabelId) > 1:
        if type(prevClickedLabelId) == int:
            self.img_labels[prevClickedLabelId].clicked = 0
            self.img_labels[prevClickedLabelId].turnBorderOff()
            # print(self.img_labels[0].val)

    def scatter_clicked(self, obj, points):
        #print(points[0].pos())
        idx = points[0].index()
        row = df.loc[idx]
        self.current_pt = points[0].pos()

        if hasattr(self, 'img_labels'):
            for i in self.img_labels:
                self.info.removeWidget(i)

        self.img_labels = []
        for i in range(0, len(self.cat)):
            img_label = customizedLabel(id=i)
            img_label.setPixmap(QPixmap('../images/burger.jpg'))
            img_label.mousePressEvent = self.imgLabelMousePressEvent
            self.info.addWidget(img_label)
            self.img_labels.append(img_label)

    # box.mousePressEvent = self.boxMousePressEvent

    def scatter_hovered(self, obj, points):
        if len(points) > 0 and points[0].pos() != self.prev_hovered_pt:
            self.prev_hovered_pt = points[0].pos()
            idx = points[0].index()
            # points[0].setSize(15)
            # points[0].setBrush(pg.mkBrush(100, 255, 255, 120))
            #print(points[0])
            print(points[0].pos())
            row = df.loc[idx]
            #print("color: ", points[0].brush())

            self.cat = df[df.category == row.category]
            #print(temp.index)

            #self.scatter.setData()
            #self.scatter.setPoints(x=temp.x,y=temp.y, size=20)
            if hasattr(self, 'scatter2'):
                self.plot.removeItem(self.scatter2)
            self.scatter2 = pg.ScatterPlotItem(x=self.cat.x,y=self.cat.y, size=15, symbol = 'o')
            self.scatter2.setZValue(-100)
            self.plot.addItem(self.scatter2)

            #self.scatter.points()[temp.index].setSize(20)
            #self.scatter.setPoints()
            # data_list = self.scatter.data.tolist()
            # data = self.scatter.getData()
            # print(data_list)
            # print(data)
    def radioButtonState(self):
        radioButton = self.sender()

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()