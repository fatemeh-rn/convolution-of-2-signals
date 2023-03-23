import math
import sys

import numpy as np
import scipy.integrate
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QWidget, QSlider, QSizePolicy,
                             QLabel)
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Window(QWidget):
        def __init__(self, parent=None):
            super(Window, self).__init__(parent)
            self.left = 10
            self.top = 350
            self.width = 640
            self.height = 400

            grid = QGridLayout()
            self.figure = Figure(figsize=(2,4))
            self.canvas = FigureCanvas(self.figure)
            self.slider = QSlider(Qt.Horizontal)

            self.button1 = QPushButton("select first")
            self.button1.setGeometry(180, 100, 100, 50)
            self.button1.setCheckable(True)
            self.button1.toggle()

            self.button1.setFixedHeight(50)
            self.button1.setFixedWidth(100)
            self.button1.move(180,100)

            self.button1.clicked.connect(self.on_click)
            grid.addWidget(self.button1)

            self.lbl2 = QLabel('function 1 : rectangular', self)
            self.lbl2.move(200, 10)
            #self.pixmap = QPixmap('12.png')
            #self.lbl2.setPixmap(pixmap)
            self.lbl4 = QLabel(self)
            self.lbl4.setPixmap(QPixmap("11.png"))
            self.lbl4.move(400,4)
            self.lbl4.setFixedSize(50,50)

            self.lbl3 = QLabel('function 2 : rectangular', self)
            self.lbl3.move(600, 10)
            self.lbl5 = QLabel(self)
            self.lbl5.setPixmap(QPixmap("11.png"))
            self.lbl5.move(750, 4)
            self.lbl5.setFixedSize(50, 50)
           # self.lbl2.move(800, 10)
            #self.lbl2.setFixedSize(50, 50)


            self.button2 =QPushButton("select second ")
            self.button2.setGeometry(300, 170, 100, 50)
            self.button2.setCheckable(True)
            self.button2.toggle()
            self.button2.setFixedHeight(40)
            self.button2.setFixedWidth(100)
            self.button2.move(300, 160)
            #self.button131.colorCount()
            self.button2.clicked.connect(self.on_click1)
            grid.addWidget(self.button2)
            self.lbl4 = QLabel('function 1 : exp', self)
            self.lbl4.move(200, 80)
            self.lbl6 = QLabel(self)
            self.lbl6.setPixmap(QPixmap("16.png"))
            self.lbl6.move(400, 60)
            self.lbl6.setFixedSize(100, 70)

            self.lbl5 = QLabel('function 2 : sin', self)
            self.lbl5.move(600, 80)
            self.lbl7 = QLabel(self)
            self.lbl7.setPixmap(QPixmap("14.png"))
            self.lbl7.move(750, 60)
            self.lbl7.setFixedSize(80, 50)

            self.button3 =QPushButton("select third")
            self.button3.setGeometry(300, 160, 100, 50)
            self.button3.setFixedHeight(50)
            self.button3.setFixedWidth(100)
            self.button3.move(300, 160)
            self.button3.setCheckable(True)
            self.button3.toggle()
            self.button3.clicked.connect(self.on_click2)
            grid.addWidget(self.button3)
            self.lbl7 = QLabel('function 1 : abs', self)
            self.lbl7.move(200, 140)
            self.lbl8 = QLabel(self)
            self.lbl8.setPixmap(QPixmap("181.png"))
            self.lbl8.move(400, 140)
            self.lbl8.setFixedSize(50, 40)

            self.lbl8 = QLabel('function 2 : exp', self)
            self.lbl8.move(600, 140)
            self.lbl9 = QLabel(self)
            self.lbl9.setPixmap(QPixmap("18.png"))
            self.lbl9.move(750, 115)
            self.lbl9.setFixedSize(110, 75)

            grid.addWidget(self.slider)
            grid.addWidget(self.canvas)
            self.setLayout(grid)
            self.slider.setMaximum(10)
            self.slider.setMinimum(-10)
            self.slider.setValue(-10)
            self.slider.tickInterval()
            self.slider.valueChanged.connect(self.value_change)

            self.setGeometry(self.left, self.top, self.width, self.height)
            self.setWindowTitle(" Slider")
            self.resize(300, 300)
            self.show()

            FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)

        def on_click(self):
                global f1
                global f2
                global t
                print("yess got it")
                f1 = lambda t: np.where(abs(t) < (math.pi / 2), 1, 0)  # lambda t: np.maximum(0, 1 - abs(t))
                f2 = lambda t: np.where(abs(t) < (3 * (math.pi / 4)), 1, 0)



        def on_click1(self):
            global f1
            global f2
            global t
            print('PyQt5 button click')
            f1 = lambda t: (t > 0) * np.exp(-2 * t)
            f2 = lambda t: np.sin(2 * np.pi * t) * (t > 0)

        def on_click2(self):
                global f1
                global f2
                global t
                print('PyQt5 button clickfd2')
                f1 = lambda t: np.maximum(0, 1 - abs(t))
                f2 = lambda t: (t > 0) * np.exp(-2 * t)
        def value_change(self):
            val = self.slider.value()

            T = 2*math.pi # the time range we are interested in
            Fs = 50  # our sampling frequency for the plotting
            global t
            t = np.arange(-T, T, 1 / Fs)  # the time samples
            global f_shift
            global prod
            global  convolution
            convolution = np.zeros(len(t))
            for n, t_ in enumerate(t):
                prod = lambda tau: f1(tau) * f2(t_ - tau)
                convolution[n] = scipy.integrate.simps(prod(t), t)

            # Create the shifted and flipped function
            global t0
            t0 = val
            f_shift = lambda t: f2(t0 - t)
            prod = lambda tau: f1(tau) * f2(t0 - tau)
            global current_value
            current_value = scipy.integrate.simps(prod(t), t)
            self.plot1()
            self.plot2(convolution)
            self.plot3()
            self.canvas.draw_idle()

        def plot1(self):
            global ax
            ax = self.figure.add_subplot(311)
            ax.clear()
            ax.plot(t, f_shift(t))

            ax.plot(t0, f_shift(t0))
            ax.plot(t, f1(t))
            ax.plot(t0, f1(t0))


        def plot2(self,convolution):
            global ax2
            ax2 = self.figure.add_subplot(313)
            ax2.clear()
            convolution1 = np.heaviside(t0<0,convolution)*convolution
            y1 = convolution*(t<t0) + 0*(t>t0)

            ax2.plot(t ,y1)
            ax2.plot(t0 ,current_value,'ro')



        def plot3(self):
            global ax3
            ax3 = self.figure.add_subplot(312)
            ax3.clear()
            #ax3 = self.figure.subplot(312)
            ax3.plot(t,prod(t),'r-')
            #ax.plot(t0, f1(t0))
            #ax.plot(t0, f_shift(t0))
            ax3.plot(t0, prod(t0),'r-')





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())