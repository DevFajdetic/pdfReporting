from fileinput import filename
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.ui import Ui_MainWindow

from services.generator.generator_service import Generator

class App(Ui_MainWindow):
    def setupUi(self, MainWindow):
        print(self)
        super().setupUi(MainWindow)
        self.generateButton.clicked.connect(self.on_generate_pdf)

    def on_generate_pdf(fileName = 'test'):
        print('weee')
        generator = Generator()
        generator.generate_pdf(fileName)

    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = App()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
