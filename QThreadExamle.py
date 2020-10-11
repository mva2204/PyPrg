import sys, time
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QTextEdit, QProgressBar, QVBoxLayout
from PyQt5.Qt import Qt, QThread, pyqtSignal


class ProgressBarThread(QThread):

    update_progressbar = pyqtSignal(int)
    finish_progressbar = pyqtSignal()

    def __init__(self, value, paren = None):
        super().__init__()
        self.value = value

    def run(self):
        while self.value < 100:
            self.value += 1
            self.update_progressbar.emit(self.value)
            QThread.msleep(200) #time.sleep(0.2)
        self.finish_progressbar.emit()

class MyProgressbarwindow(QDialog):
    def __init__(self, parent = None):
        super().__init__()
        self.value = 0
        self.progressbar = QProgressBar()
        self.progressbar.setAlignment(Qt.AlignCenter)
        self.pushbutton = QPushButton('Старт прогресс')
        self.textedit = QTextEdit('...')
        self.setGeometry(300,400, 300, 150)

        vbox = QVBoxLayout()
        vbox.addWidget(self.textedit)
        vbox.addWidget(self.progressbar)
        vbox.addWidget(self.pushbutton)
        self.setLayout(vbox)

        self.pushbutton.clicked.connect(self.launch_progress_bar_fililing)

#        self.ProgressBarThread_instance = ProgressBarThread(mainwindow=self)

    def launch_progress_bar_fililing(self):
        self.ProgressBarThreadInstance = ProgressBarThread(self.value)
        self.ProgressBarThreadInstance.update_progressbar.connect(self.updateProgressbar)
        self.ProgressBarThreadInstance.finish_progressbar.connect(self.finishProgressbar)
        self.ProgressBarThreadInstance.start()
        self.pushbutton.setEnabled(False)

    def updateProgressbar(self, value):
        self.progressbar.setValue(value)

    def finishProgressbar(self):
        self.pushbutton.setEnabled(True)
        self.value = 0

app = QApplication(sys.argv)
main = MyProgressbarwindow()
if __name__ == '__main__':
    main.show()
    sys.exit(app.exec_())