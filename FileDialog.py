import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

def open_file(self):
    self.file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", "CSV Files (*.csv)")
    if self.file_name[0] != '':
        self.lineEdit.setText(self.file_name[0])

