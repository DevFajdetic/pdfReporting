from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QGridLayout, QFormLayout, \
    QLineEdit, QMessageBox

from app.shared import constants
from app.utils import get_project_root
import app.services.docx_templating.docx_templating as docx_templating_service
import app.services.generator.generator_service as pdf_reporting_service
import app.services.excel_reporting.excel_reporting as excel_reporting_service
import app.services.tps_report.tps_report as fill_and_sign_report
from PyQt5.QtWidgets import QApplication, QMainWindow


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

        self.filename_line = QLineEdit()
        # Create the button
        button = QPushButton(constants.SERVICE_RUN, self)
        button.setStyleSheet("QPushButton{background-color: #ff9800}")
        button.clicked.connect(self.open_templating_window)

        # Create a layout
        layout = QFormLayout()
        layout.addRow(constants.FILENAME_LABEL, self.filename_line)
        layout.addWidget(button)

        self.setLayout(layout)

    def open_templating_window(self):
        self.filename = self.filename_line.text()
        docx_templating_service.run_service(self.filename)


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
