# -- coding: utf-8 --
import sys
import time
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QFileDialog
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont, QKeySequence


from uis.text_bot_gui_mpl import Ui_MainWindow
from my_bot import TextBot
from  MyGraphics import plot_graph_smart

from  MplForWidget import MplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        #Создаем диалог открытия файла
        self.BtnOpenFile.clicked.connect(self.open_file)


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
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", "CSV Files (*.csv)")
        if self.file_name[0] != '':
            self.label_path_openfile.setText(self.file_name[0])

def main():

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
#    plot_graph_smart()

main()


