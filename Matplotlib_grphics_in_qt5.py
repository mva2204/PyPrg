# -*- coding: utf-8 -*-
import sys
import time
#import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QFileDialog, QTableView, QWidget, QMessageBox
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont, QKeySequence


from uis.text_bot_gui_mpl import Ui_MainWindow
from my_bot import TextBot
from  MyGraphics import plot_graph_smart

from  MplForWidget import MplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from Valid_Email_Thread import function1
from datetime import datetime
from validate_email import validate_email
from threading import Thread

#df1 = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
#                   'b': [100, 200, 300],
#                   'c': ['a', 'b', 'c']})

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.df = pd.DataFrame

        self.fig = plot_graph_smart()
        self.companovka_for_mpl = QtWidgets.QVBoxLayout(self.widget)
        self.canavas = MplCanvas(self.fig)
        self.companovka_for_mpl.addWidget(self.canavas)
        self.toolbar = NavigationToolbar(self.canavas, self)
        self.companovka_for_mpl.addWidget(self.toolbar)

        # Обработка нажатий на TableView
        self.tableView.clicked.connect(self.clickedTableView)
#        self.tableView.viewportEntered.connect(self.clickedTableView)

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
        #Создаем диалог открытия файла
        self.BtnOpenFile.clicked.connect(self.open_file)
        self.pushButton.clicked.connect(self.show_answer)
        self.pushButton_update.clicked.connect(self.validate)
        self.pushButton_map.clicked.connect(self.fun_map)
        self.path = 'valid.xlsx'
        self.pushButton_save.clicked.connect(self.save_table_to_excel)

        #Ctrl+Enter  QtCore.Qt.CTRL+QtCore.Qt.Key_Return)
        shortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL+QtCore.Qt.Key_Return), self.input_text_line)
        shortcut.activated.connect(self.show_answer)

        self.horizontalSlider.valueChanged.connect(self.font_resize)

        self.horizontalSlider.valueChanged.connect(self.lcdNumber.display)

    #b Обработка закрытия окна
    def closeEvent(self, event):
        #close = QMessageBox()
        #close.setText("You sure?")
        #close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        #close = close.exec()

        #if close == QMessageBox.Yes:
        #    event.accept()
        #else:
        #    event.ignore()
        if MainWindow.th:
            self.th.join()

    def fun_map(self):
        # Using lambda function we first convert all
        # the cell to a string value and then find
        # its length using len() function
#        self.df['Validate'] = False
        self.df['Validate'] = self.df.applymap(lambda x: validate_email(x, verify=True))
        if len(self.df.index) > 1:
            for index, row in self.df.iterrows():
                print("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[index, 0],index, self.df.iat[index, 1], is_valid, len(self.df.index)-1))

    def fun_lamda(self, index):
        # Using lambda function we first convert all
        # the cell to a string value and then find
        # its length using len() function
        self.df.iat[index, 1] = validate_email(self.df.iat[index, 0], verify=True)


    #Обработка нажатий на TableView
    def clickedTableView(self):
        indexes = self.tableView.selectionModel().selectedIndexes()
        for index in sorted(indexes):
            #так только  номер выделлной строки TableView видно
            # self.label_state.setText(str(index.row()))

            #Устанавливаем текст из выделеной ячейки в значение Lable
            self.label_state.setText(self.tableView.model().index(index.row(),0).data())
            print('Row %d is selected' % index.row())

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
            self.df = pd.read_excel(xlsx)
            self.zagolovok = self.df.head()
            print('Sheet name:{0}'.format(xlsx.sheet_names))
            print('заголовок:{0}'.format(self.df.head()))
            print('Строки-Столбцы: {0}'.format(self.df.shape))
#            print('Sheet name:{0} \n'.format(df.columns[1]))
            print('две перывые строки: {0}'.format(self.df[:2]))
            print('ячейка 1, 0: {0}'.format(self.df.iloc[[3],[0]]))
#            for index, row in df.iterrows():
#                print(row['c1'], row['c2'])
            cell = self.df.iat[3,0]

            for index, row in self.df.iterrows():
                self.label_state.setText(self.df.iat[index,0])
            print('ячейка : {0}'.format(cell))

            print('DF : {0}'.format(self.df))
            self.model = PandasModel(self.df)
            print('model: {0}'.format(self.model))
            self.tableView.setModel(self.model)


    def validate(self, email):
        self.df['Validate'] = False
        df_list = list(self.df)
        print("list len: {0}".format(len(df_list)))
        for i in range(len(df_list)):
            print("list : {0}".format(df_list[i]))
        model = PandasModel(self.df)
        self.tableView.setModel(model)
        self.tableView.update()
        print("Нажата кнопка валидации")
        self.th = Thread(target=self.func)
        self.startTime = datetime.now()
        print("Начало выполнения: {0}".format(self.startTime))
        self.th.start()
#        function1.start(self.df)
#        function1.get_index_cur()



    def fun_lamda(self):
        is_valid = validate_email(self.df.iat[index, 0], verify=True)
        self.df.iat[index, 1] = is_valid
        print("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[index, 0], index, self.df.iat[index, 1],
                                                                    is_valid, len(self.df.index) - 1))
        # Количество строк DataFrame len(self.df.index)-1
        self.label_state.setText("{0} из {1}".format(index, len(self.df.index) - 1))

        #Поток валидации email
    def func(self):
        if len(self.df.index) > 1:
            for index, row in self.df.iterrows():
                is_valid = validate_email(self.df.iat[index, 0], verify=True)
                self.df.iat[index, 1] = is_valid
                print("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[index, 0],index, self.df.iat[index, 1], is_valid, len(self.df.index)-1))
    #            self.Main_text_window.setText("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[index, 0],index, self.df.iat[index, 1], is_valid, len(self.df.index)-1))
                #Количество строк DataFrame len(self.df.index)-1
                self.label_state.setText("{0} из {1}".format(index, len(self.df.index)-1))
    #            model = PandasModel(self.df)
    #            self.tableView.setModel(model)
    #            self.tableView.update()
        self.endTime = datetime.now()
        print("Конец выполнения: {0}".format(self.endTime))
        print("Время выполнения: {0}".format(self.endTime-self.startTime))
        self.save_table_to_excel()



    def save_table_to_excel(self):
        # Specify a writer
        self.model = PandasModel(self.df)
#        self.tableView.setModel(model)
#        self.tableView.update()

        writer = pd.ExcelWriter(self.path, engine='xlsxwriter')

        # Write your DataFrame to a file
        self.df.to_excel(writer, 'Валидные email')

        # Save the result
        writer.save()


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

main()


