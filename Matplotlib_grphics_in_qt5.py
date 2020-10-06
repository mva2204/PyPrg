# -- coding: utf-8 --
import sys
import time
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QFileDialog, QTableView, QWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont, QKeySequence


from uis.text_bot_gui_mpl import Ui_MainWindow
from my_bot import TextBot
from  MyGraphics import plot_graph_smart

from  MplForWidget import MplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import pandas as pd

df1 = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        #Создаем диалог открытия файла
        self.BtnOpenFile.clicked.connect(self.open_file)

        self.df1Model = PandasModel(df1)
        self.tableView.setModel(self.df1Model)

        self.fig = plot_graph_smart()
        self.companovka_for_mpl = QtWidgets.QVBoxLayout(self.widget)
        self.canavas = MplCanvas(self.fig)
        self.companovka_for_mpl.addWidget(self.canavas)
        self.toolbar = NavigationToolbar(self.canavas, self)
        self.companovka_for_mpl.addWidget(self.toolbar)


        self.jake = TextBot('...')
        self.jake.answer_the_question()
        self.Main_text_window.setText(str(self.jake.bot_dialog_memory))

        self.font = QFont()
        self.input_text_line.setFocus()
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setMaximum(30)
        self.label.setGeometry(QtCore.QRect(150,70,70,50))
        self.label.setText('Bot:'+self.jake.bot_name)

#        self.isSignalConnected(self.pushButton, PYQT_SIGNAL('clicked()'), self.show_answer())
        self.pushButton.clicked.connect(self.show_answer)
        #Ctrl+Enter  QtCore.Qt.CTRL+QtCore.Qt.Key_Return)
        shortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL+QtCore.Qt.Key_Return), self.input_text_line)
        shortcut.activated.connect(self.show_answer)

        self.horizontalSlider.valueChanged.connect(self.font_resize)

        self.horizontalSlider.valueChanged.connect(self.lcdNumber.display)


    def font_resize(self, value):
        self.font.setPointSize(value)
        self.label.setFont(self.font)
        self.label.adjustSize()
        self.Main_text_window.setFont(self.font)
        self.input_text_line.setFont(self.font)
        self.input_text_line.setFont(self.font)

    def show_answer(self):
        self.jake.input = self.input_text_line.toPlainText()
        self.input_text_line.clear()
        time.sleep(0.5)
        self.jake.answer_the_question()
        self.Main_text_window.setText(str(self.jake.bot_dialog_memory))

    def open_file(self):
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", "XLSX Files (*.xlsx);;CSV Files (*.csv);;All Files (*)")
        if self.file_name[0] != '':
            print(self.file_name[0])
            self.label_path_openfile.setText(self.file_name[0])
#            xl = pd.read_excel(self.file_name[0])
            xlsx = pd.ExcelFile(self.file_name[0])
            df = pd.read_excel(xlsx)

            print('Sheet name:{0}'.format(xlsx.sheet_names))
            print('заголовок:{0}'.format(df.head()))
            print('Строки-Столбцы: {0}'.format(df.shape))
            print('Sheet name:{0} \n'.format(df.columns[1]))
            print('две перывые строки: {0}'.format(df[:2]))
            print('ячейка 1, 0: {0}'.format(df.iloc[[1],[0]]))
            model = PandasModel(df)
            print('model: {0}'.format(model))
            self.tableView.setModel(model)


class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

def main():

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
#    plot_graph_smart()

main()


