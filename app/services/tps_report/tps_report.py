from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QMessageBox, QSpinBox
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

from reportlab.pdfgen.canvas import Canvas

import os

import textwrap
from datetime import datetime

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from shared import constants
from utils import get_project_root

app = QApplication([])
w = QWidget()


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    error = pyqtSignal(str)
    file_saved_as = pyqtSignal(str)


class Generator(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    def __init__(self, data, filename):
        super().__init__()
        self.data = data
        self.filename = filename
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            outfile = get_project_root() + '\\products\\' + self.filename

            template = PdfReader(get_project_root() + '\\assets\\fill_sign_report\\' + self.filename, decompress=False).pages[0]
            template_obj = pagexobj(template)

            canvas = Canvas(outfile)

            xobj_name = makerl(canvas, template_obj)
            canvas.doForm(xobj_name)

            ystart = 443

            # Prepared by
            canvas.drawString(170, ystart, self.data['name'])

            # Date Today date
            today = datetime.today()
            canvas.drawString(500, ystart, today.strftime('%F'))

            # Device/Program Type
            canvas.drawString(230, ystart-28, self.data['program_type'])

            # Product code
            canvas.drawString(175, ystart-(2*28), self.data['product_code'])

            # Customer
            canvas.drawString(315, ystart-(2*28), self.data['customer'])

            # Vendor
            canvas.drawString(145, ystart-(3*28), self.data['vendor'])

            ystart = 250

            # Program Language
            canvas.drawString(210, ystart, "Python")

            canvas.drawString(430, ystart, self.data['n_errors'])

            comments = self.data['comments'].replace('\n', ' ')
            if comments:
                lines = textwrap.wrap(comments, width=65)  # 45
                first_line = lines[0]
                remainder = ' '.join(lines[1:])

                lines = textwrap.wrap(remainder, 75)  # 55
                lines = lines[:4]  # max lines, not including the first.

                canvas.drawString(155, 223, first_line)
                for n, l in enumerate(lines, 1):
                    canvas.drawString(80, 223 - (n*28), l)

            canvas.save()

        except Exception as e:
            self.signals.error.emit(str(e))
            return

        self.signals.file_saved_as.emit(outfile)


class Window(QWidget):

    def __init__(self, filename):
        super().__init__()

        self.filename = filename
        self.threadpool = QThreadPool()

        self.name = QLineEdit()
        self.program_type = QLineEdit()
        self.product_code = QLineEdit()
        self.customer = QLineEdit()
        self.vendor = QLineEdit()
        self.n_errors = QSpinBox()
        self.n_errors.setRange(0, 1000)
        self.comments = QTextEdit()

        self.generate_btn = QPushButton("Generate PDF")
        self.generate_btn.setStyleSheet("QPushButton{background-color: #2196f3}")
        self.generate_btn.pressed.connect(self.generate)

        layout = QFormLayout()
        layout.addRow("Name", self.name)
        layout.addRow("Program Type", self.program_type)
        layout.addRow("Product Code", self.product_code)
        layout.addRow("Customer", self.customer)
        layout.addRow("Vendor", self.vendor)
        layout.addRow("No. of Errors", self.n_errors)

        layout.addRow("Comments", self.comments)
        layout.addRow(self.generate_btn)

        self.setLayout(layout)

    def generate(self):
        self.generate_btn.setDisabled(True)
        data = {
            'name': self.name.text(),
            'program_type': self.program_type.text(),
            'product_code': self.product_code.text(),
            'customer': self.customer.text(),
            'vendor': self.vendor.text(),
            'n_errors': str(self.n_errors.value()),
            'comments': self.comments.toPlainText()
        }
        g = Generator(data, self.filename)
        g.signals.file_saved_as.connect(self.generated)
        g.signals.error.connect(print)  # Print errors to console.
        self.threadpool.start(g)

    def generated(self, outfile):
        self.generate_btn.setDisabled(False)
        try:
            print(outfile)
            os.startfile(outfile)
        except Exception:
            # If startfile not available, show dialog.
            QMessageBox.information(self, "Finished", "PDF has been generated")


def run_service(filename):
    global app, w
    try:
        w = Window(filename)
    except Exception:
        QMessageBox.information(w, constants.ACTION_FINISHED, constants.FILE_FAILED_TO_OPEN + filename)
        return
    w.show()
    app.exec_()
