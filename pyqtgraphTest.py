import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
import numpy as np
from PIL import Image

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.im = QPixmap("./images/map.jpg")
        #self.im.setZValue(-100)
        self.label = QLabel()
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label,1,1)


        self.setGeometry(50,50,320,200)
        self.setWindowTitle("PyQT show image")

        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        self.plot = pg.plot(x, y, pen=None, symbol='o')

        image = Image.open('images/map.jpg')
        self.plot.setBackground(None)
        #self.im2 = pg.ImageItem(np.random.normal(size=(100, 100)))

        image = Image.open('images/map.jpg')
        arr = np.array(image)
        self.im2 = pg.ImageItem(arr)

        self.im2.setZValue(-100)
        self.grid.addWidget(self.plot,1,1)
        self.plot.addItem(self.im2)
        self.setLayout(self.grid)
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())