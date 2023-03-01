from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QGridLayout, QFormLayout, QLineEdit, QMessageBox, QLabel
import os
from shared import constants, helpers
from utils import get_project_root
import services.docx_templating.docx_templating as docx_templating_service
import services.generator.generator_service as pdf_reporting_service
import services.excel_reporting.excel_reporting as excel_reporting_service
import services.tps_report.tps_report as fill_and_sign_report
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFileDialog
import pandas as pd
import shutil

class QDataViewer(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Layout Init.
        self.setGeometry(650, 300, 600, 600)
        self.setWindowTitle('Data Viewer')
        self.quitButton = QPushButton('QUIT', self)
        self.uploadButton = QPushButton('UPLOAD', self)
        self.uploadButton.clicked.connect(self.open)
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(self.quitButton)
        hBoxLayout.addWidget(self.uploadButton)
        self.setLayout(hBoxLayout)

    def open (self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')
        print(f'Path file : {filename}')

class FillPDFWindow(QDialog):
    filename = ""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(constants.SERVICE_FILL_SIGN)

        self.filename_line = QLineEdit()
        # Create the button
        button = QPushButton(constants.SERVICE_RUN, self)
        button.setStyleSheet("QPushButton{background-color: #2196f3}")
        button.clicked.connect(self.open_fill_pdf_window)

        # Create a layout
        layout = QFormLayout()
        layout.addRow(constants.FILENAME_LABEL, self.filename_line)
        layout.addWidget(button)

        self.setLayout(layout)

    def open_fill_pdf_window(self):
        self.filename = self.filename_line.text()
        fill_and_sign_report.run_service(self.filename)


class TemplatingWindow(QDialog):
    filename = ""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(constants.SERVICE_TEMPLATING)
        self.x_axis = None
        self.y_axis = None
        self.extension = None
        self.table_data = None

        self.filename_line = QFileDialog.getOpenFileName(self, 'Select Template', '.')[0]

        uploadButton = QPushButton('Upload Graph Data', self)
        uploadButton.setStyleSheet("QPushButton{background-color: #aa9800}")
        uploadButton.clicked.connect(self.open_add_file_window)

        # Create the button
        button = QPushButton(constants.SERVICE_RUN, self)
        button.setStyleSheet("QPushButton{background-color: #ff9800}")
        button.clicked.connect(self.open_templating_window)

        # Create a layout
        self.layout = QFormLayout()
        self.layout.addWidget(uploadButton)
        self.layout.addWidget(button)

        self.setLayout(self.layout)

    def open_templating_window(self):

        shutil.copyfile(self.filename_line, constants.DOCX_TEMPLATING_PATH + os.path.split(self.filename_line)[1])

        if self.extension == constants.CSV_EXTENSION:
            self.table_data = pd.read_csv(self.excel_filename, delimiter=self.delimiter)

        if self.extension == constants.EXCEL_EXTENSION:
            self.table_data = pd.read_excel(self.excel_filename)
        if self.x_axis and self.y_axis:
            helpers.plot(self.table_data, self.x_axis.text(), self.y_axis.text())

        docx_templating_service.run_service(self.filename_line)

    def open_add_file_window (self):
        self.excel_filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]

        if self.excel_filename:
            self.extension = os.path.splitext(self.excel_filename)[1]
            self.layout.addRow('File name:', QLabel(os.path.split(self.excel_filename)[1]))
            
            if self.extension == constants.CSV_EXTENSION:
                self.delimiter = QLineEdit()
                self.layout.addRow(constants.DELIMITER, self.delimiter) 

            if(not self.x_axis):
                self.x_axis = QLineEdit()
                self.y_axis = QLineEdit()
                 
                self.layout.addRow(constants.X_AXIS, self.x_axis) 
                self.layout.addRow(constants.Y_AXIS, self.y_axis)        
                self.setLayout(self.layout)
        
        print(f'Path file : {self.excel_filename}')

class ExcelReportWindow(QDialog):
    filename = ""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(constants.SERVICE_REPORTING)

        self.filename_line = QLineEdit()
        # Create the button
        button = QPushButton(constants.SERVICE_RUN, self)
        button.setStyleSheet("QPushButton{background-color: #f44336}")
        button.clicked.connect(self.open_excel_reporting_window)

        # Create a layout
        layout = QFormLayout()
        layout.addRow(constants.INPUT_FILENAME_LABEL, self.filename_line)
        layout.addWidget(button)

        self.setLayout(layout)

    def open_excel_reporting_window(self):
        self.filename = self.filename_line.text()
        try:
            excel_reporting_service.run_service(self.filename)
        except Exception:
            QMessageBox.information(self, constants.ACTION_FINISHED, constants.GENERATE_UNSUCCESSFUL)
        else:
            QMessageBox.information(self, constants.ACTION_FINISHED, constants.GENERATE_SUCCESSFUL)


class GenerateReportWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate PDF Reports")

        # Create the button
        button1 = QPushButton("Yearly financial report", self)
        button1.setStyleSheet("QPushButton{background-color: #4caf50}")
        button1.clicked.connect(self.open_yearly_report_window)

        # Create a layout
        layout = QFormLayout()
        layout.addWidget(button1)

        self.setLayout(layout)

    def open_yearly_report_window(self):
        pdf_reporting_service.run_service()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize all windows to None
        self.fill_pdf_window = None
        self.generate_reports_window = None
        self.templating_window = None

        self.setWindowTitle(constants.WINDOW_MAIN)
        # Create the button
        # Create the buttons
        button1 = QPushButton("Fill and Sign PDF", self)
        button2 = QPushButton("Generate Excel Report", self)
        button3 = QPushButton("Generate PDF Report", self)
        button4 = QPushButton("Templating", self)

        button1.clicked.connect(self.open_fill_pdf_window)
        button2.clicked.connect(self.open_excel_report_window)
        button3.clicked.connect(self.open_generate_reports_window)
        button4.clicked.connect(self.open_templating_window)

        # Create a grid layout
        grid = QGridLayout()

        # Add the buttons to the layout
        grid.addWidget(button1, 0, 0)
        grid.addWidget(button2, 0, 1)
        grid.addWidget(button3, 1, 0)
        grid.addWidget(button4, 1, 1)

        # Create a widget
        widget = QWidget()

        # set the layout to the widget
        widget.setLayout(grid)

        # Set the widget to the main main_window
        self.setCentralWidget(widget)

        # Set stylesheet
        button1.setStyleSheet("QPushButton{background-color: #2196f3}")
        button2.setStyleSheet("QPushButton{background-color: #f44336}")
        button3.setStyleSheet("QPushButton{background-color: #4caf50}")
        button4.setStyleSheet("QPushButton{background-color: #ff9800}")

    def open_fill_pdf_window(self):
        self.fill_pdf_window = FillPDFWindow()
        self.fill_pdf_window.show()

    def open_excel_report_window(self):
        self.plots_window = ExcelReportWindow()
        self.plots_window.show()

    def open_generate_reports_window(self):
        self.generate_reports_window = GenerateReportWindow()
        self.generate_reports_window.show()

    def open_templating_window(self):
        self.templating_window = TemplatingWindow()
        self.templating_window.show()


with open(get_project_root() + "\\styles.qss", "r") as f:
    stylesheet = f.read()

app = QApplication([])
main_window = MainWindow()
app.setStyleSheet(stylesheet)
main_window.show()
app.exec_()
