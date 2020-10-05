# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MplCanvas(FigureCanvas):
    def __init__(self, fig, parent = None):
        #Получаем виджет на котором будем отображать график
        self.fig = fig
        FigureCanvas.__init__(self, self.fig)
        #Уставнавливаем размер на весь виджет
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        #Обновление размеров
        FigureCanvas.updateGeometry(self)
