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
        self.resize(700,700)

        img = Image.open('../images/burger.jpg')
        self.img_arr = np.array(img)

        self.scroll_bar = QScrollBar(Qt.Vertical)
        self.scroll_bar.setMaximum(100)
        self.scroll_bar.valueChanged.connect(self.scroll_value_changed)

        layout = QHBoxLayout(self)
        right_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()

        layout.addLayout(self.left_layout,6)
        layout.addLayout(right_layout,1)
        self.graphics_layout, self.viewboxes, self.images = self.create_page(5,5)
        self.graphics_layout.setFixedWidth(1000)
        #self.left_layout.addWidget(self.graphics_layout)

        right_layout.addWidget(self.scroll_bar)



        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0,0,0,0)
        self.scroll_area.setWidget(self.graphics_layout)
        self.left_layout.addWidget(self.scroll_area)
        self.pages = {}
        self.prev_val = -1

    def scroll_value_changed(self,val):
        self.images[self.prev_val].setImage(np.zeros((1,1)))
        self.images[val].setImage(self.img_arr*val)
        print('current: '+str(val)+' prev: '+str(self.prev_val))
        self.prev_val = val

        # if self.prev_val in self.pages:
        #     print(self.pages[self.prev_val])
        #     self.left_layout.removeWidget(self.pages[self.prev_val])
        #
        # if val > self.prev_val:
        #     for i in range(self.prev_val, val+1):
        #         if i not in self.pages:
        #             graphics_layout, viewboxes = self.create_page(i, 5)
        #             self.pages[i] = graphics_layout
        #
        # self.left_layout.addWidget(self.pages[val])
        # self.prev_val = val

    def create_page(self, row, col):
        plot = pg.GraphicsLayoutWidget()
        viewboxes = []
        images = []
        for i in range(row):
            for j in range(col):
                vb = plot.addViewBox(i,j)
                vb.setGeometry(0,0,400,200)
                vb.setMouseEnabled(x=False,y=False)

                vb.setContentsMargins(0,0,0,0)
                vb.setBorder(pg.mkColor('w'))
                img = pg.ImageItem(np.zeros((128,25)))
                vb.setAspectLocked(True)
                aspect_ratio = img.width() / img.height()
                vb.setAspectLocked(lock=True, ratio=aspect_ratio)
                vb.addItem(img)
                images.append(img)
                viewboxes.append(vb)
        return plot, viewboxes, images

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

