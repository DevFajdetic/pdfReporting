# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templating.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.generateButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateButton.setGeometry(QtCore.QRect(30, 190, 75, 23))
        self.generateButton.setObjectName("generateButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 140, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 60, 331, 51))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.keyLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.keyLabel.setObjectName("keyLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.keyLabel)
        self.keyLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.keyLineEdit.setObjectName("keyLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.keyLineEdit)
        self.valueLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.valueLabel.setObjectName("valueLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.valueLabel)
        self.valueLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.valueLineEdit.setObjectName("valueLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.valueLineEdit)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 131, 31))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.generateButton.setText(_translate("MainWindow", "Generate"))
        self.keyLabel.setText(_translate("MainWindow", "Key"))
        self.valueLabel.setText(_translate("MainWindow", "Value"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; color:blue;\">Templating</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())