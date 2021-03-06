# -*- coding: utf-8 -*-
import sys
import time
import os
#import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QFileDialog, QTableView, QWidget, QMessageBox, QLabel
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont, QKeySequence
from pandas import DataFrame

from uis.text_bot_gui_mpl import Ui_MainWindow
from my_bot import TextBot
from  MyGraphics import plot_graph_smart

from  MplForWidget import MplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
# from Valid_Email_Thread import function1
from datetime import datetime
from validate_email import validate_email
from threading import Thread
import re

#df1 = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
#                   'b': [100, 200, 300],
#                   'c': ['a', 'b', 'c']})

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.check_mx = True #Провекра домменого имени 1=отмечена
        self.check_verify = True#Проверка почтового адреса 1=отмечена
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
        self.label.setGeometry(QtCore.QRect(70,70,70,50))
        self.label.setText('Bot:'+self.jake.bot_name)

#        self.isSignalConnected(self.pushButton, PYQT_SIGNAL('clicked()'), self.show_answer())
        #Создаем диалог открытия файла
        self.BtnOpenFile.clicked.connect(self.open_file)
        self.pushButton.clicked.connect(self.show_answer)
# Это рабочая функция без QThread       self.pushButton_update.clicked.connect(self.validate)
        self.pushButton_update.clicked.connect(self.launch_valid_email)
        self.pushButton_map.clicked.connect(self.fun_map)
        self.path = 'valid.xlsx'
        self.pushButton_save.clicked.connect(self.save_table_to_excel)

        #Ctrl+Enter  QtCore.Qt.CTRL+QtCore.Qt.Key_Return)
        shortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL+QtCore.Qt.Key_Return), self.input_text_line)
        shortcut.activated.connect(self.show_answer)

        self.horizontalSlider.valueChanged.connect(self.font_resize)

        self.horizontalSlider.valueChanged.connect(self.lcdNumber.display)

        self.checkBox_check_mx.stateChanged.connect(lambda : self.selectBooks(self.check_mx, self.checkBox_check_mx))
        self.checkBox_verify.stateChanged.connect(lambda : self.selectBooks(self.check_verify, self.checkBox_verify))
        # self.checkBox_verify.stateChanged.connect(
        #     lambda state=self.checkBox_verify.isChecked(), no=2: self.selectBooks(state, no, self.checkBox_verify))

    def launch_valid_email(self):
        self.index = 0
        self.text_log = ''
        # check_mx Checking domain has SMTP Server
        # check_verify Check if the host has SMTP Server and the email really exists:
        self.ProgressValidEmail = ValidEmailThread(self.df, self.index, self.check_mx, self.check_verify)
        print('{}-{}'.format(self.check_mx,self.check_verify))
        self.ProgressValidEmail.update_valid_email.connect(self.update_valid_email)
        self.ProgressValidEmail.finish_valid_email.connect(self.finish_valid_email)
        self.ProgressValidEmail.start()
#        self.pushbutton.setEnabled(False)

    def update_valid_email(self, df, index):
        self.label_state.setText("{0} из {1}".format(index, len(df.index) - 1))
        # Запись перевода на новую строку и ответа в log память бота
        self.text_log = "Проверка email: {0} - {1} - {2} из {3}".format(df.iat[index, 0], df.iat[index, 1], index, len(df.index)-1) + '\n' + self.text_log
        self.Main_text_window.setText(self.text_log)
        self.Main_text_window.ensureCursorVisible()
        model = PandasModel(df)
        self.tableView.setModel(model)
        self.tableView.update()


    def finish_valid_email(self):
        self.save_table_to_excel()

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
 #       if MainWindow.th:
 #           self.th.join()
        pass

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
            self.pathopenfile = 'valid_' + self.file_name[0]
            self.label_path_openfile.setText(self.file_name[0])
#            xl = pd.read_excel(self.file_name[0])
            xlsx = pd.ExcelFile(self.file_name[0])
            self.df = pd.read_excel(xlsx)

            # Добавляем вначало заголовок
            self.df['Validate'] = False
            self.df.shift(1)
            self.df.iat[0, 0] = list(self.df)[0]
            self.df.columns = ['Adress', 'Validate']

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
            #Формируем наименование файла для сохранения валидации
            #Выделить из пути имя файла без расширения os.path.splitext(os.path.basename(self.file_name[0]))[0]
            self.path = 'Valid_'+os.path.splitext(os.path.basename(self.file_name[0]))[0]+'.xlsx'
            print(self.path)



    def validate(self, email):
        self.df['Validate'] = "False"
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

        #Поток валидации email
    def func(self):
        if len(self.df.index) > 1:
            for index, row in self.df.iterrows():
                is_valid = validate_email(self.df.iat[index, 0], verify=True)
                print("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[index, 0],index, self.df.iat[index, 1], is_valid, len(self.df.index)-1))
                 #Количество строк DataFrame len(self.df.index)-1
                self.label_state.setText("{0} из {1}".format(index, len(self.df.index)-1))
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

#Пока не работает
    def fun_lamda(self):
        is_valid = validate_email(self.df.iat[self.index, 0], verify=True)
        self.df.iat[self.index, 1] = is_valid
        print("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[self.index, 0], self.index, self.df.iat[self.index, 1],
                                                                    is_valid, len(self.df.index) - 1))
        # Количество строк DataFrame len(self.df.index)-1
        self.label_state.setText("{0} из {1}".format(self.index, len(self.df.index) - 1))

    #Обработка CheckBox
    def selectBooks(self, check, checkBox):
        toggle = checkBox.isChecked()
        if toggle:# == QtCore.Qt.Checked:
            print('toggle=`{}`, checked'.format(toggle))
            # if no == 1:
            check = True
            print('checked_{} -> галочка поставлена выполнилось действие'.format(check))
        else:
            check = False
            print('toggle=`{}`, unchecked_{}'.format(toggle, check))

        s1 = checkBox.text()
        s = re.sub(r'_True|_False', '', s1)
        checkBox.setText("{0}_{1}".format(s, check))
        # checkBox_check_mx.setText("check_mx_{0}".format(self.check_mx))
        # if no == 2:
        #     self.checkBox_verify.setText("checkBox_verify__{0}".format(self.check_verify))



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


#Класс поток обработки valid_email
class ValidEmailThread(QThread):

    update_valid_email = pyqtSignal(DataFrame, int)
    finish_valid_email = pyqtSignal()

    #check_mx Checking domain has SMTP Server
    #check_verify Check if the host has SMTP Server and the email really exists:
    def __init__(self, df, index, chex_mx, check_verify, paren = None):
        super().__init__()
        self.df = df
        self.index = index
        self.check_mx = chex_mx
        self.check_verify = check_verify
        print('check verify {}'.format(self.check_verify))
        print('check mx {}'.format(self.check_mx))

    def run(self):
        # #Добавляем вначало заголовок
        # self.df.shift(1)
        # self.df.iat[0,0] = list(self.df)[0]
        # self.df.columns = ['Adress','Validate']
        # self.df.iat[0,1] = 'Valid'
        # #добавляем второй столбец значения валидации
        # self.df['Validate'] = False
        #Запоминаем налало проверки
        self.startTime = datetime.now()
        if len(self.df.index) > 1:
            for k, row in self.df.iterrows():
                self.is_valid = validate_email(self.df.iat[k, 0], verify=self.check_verify, smtp_timeout=5, check_mx=True)
#                print("valid = {0}-{1}".format(self.is_valid, type(self.is_valid)))
                self.df.iat[k, 1] = self.is_valid
                self.index = k
                self.update_valid_email.emit(self.df, self.index)
                print("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[k, 0], k,
                                                                            self.df.iat[k, 1], self.is_valid,
                                                                            len(self.df.index) - 1))


#        for self.index, row in self.df.iterrows():
#            self.is_valid = validate_email(self.df.iat[self.index, 0], verify=True, smtp_timeout=3, check_mx=True)
#            self.df.iat[self.index, 1] = self.is_valid
#            self.update_valid_email.emit(self.df, self.index, self.is_valid)
#            print("Проверка email: {0} - {1} - {2} - {3} из {4}".format(self.df.iat[self.index, 0], self.index,
#                                                                        self.df.iat[self.index, 1], self.is_valid,
#                                                                        len(self.df.index) - 1))
        self.endTime = datetime.now()
        print("Конец выполнения: {0}".format(self.endTime))
        print("Время выполнения: {0}".format(self.endTime - self.startTime))
        self.finish_valid_email.emit()



def main():

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

main()


