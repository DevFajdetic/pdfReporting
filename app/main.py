from fileinput import filename
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog
from ui.ui import Ui_MainWindow
import os
import shutil

from services.generator.generator_service import Generator

class App(Ui_MainWindow, QDialog):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.generateButton.clicked.connect(self.on_generate_pdf)
        self.browserButton.clicked.connect(self.browser_files)

    def on_generate_pdf(fileName = 'test'):
        generator = Generator()
        generator.generate_pdf(fileName)    
    
    def browser_files(self):
        file_filter = 'Data File (*.xlsx *.csv *.xls)'
        fname = QFileDialog.getSaveFileName(parent=self, directory=os.getcwd(), filter=file_filter, initialFilter=file_filter, caption='Select Excel or csv file')
        self.filename.setText(fname[0])
        shutil.copy(fname[0], "./assets/files")
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = App()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
