import os
import re
from ast import literal_eval

import pythoncom
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QMessageBox, QLabel
from docx2pdf import convert
from docxtpl import DocxTemplate, InlineImage

from app.utils import get_project_root
import app.shared.constants as constants

# Templating window will get deleted immediately if local variables (called from main.py)
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

    :param data: The data to add to replace placeholders
    """

    def __init__(self, data: dict, filename: str):
        super().__init__()
        self.data = data
        self.filename_docx = filename
        self.filename_pdf = str.replace(filename, ".docx", ".pdf")
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        pythoncom.CoInitialize()  # For some reason required in pycharm :')
        try:
            outfile_word = "./products/{}".format(self.filename_docx)
            outfile_pdf = "./products/{}".format(self.filename_pdf)

            doc = DocxTemplate('./assets/docx_templating/{}'.format(self.filename_docx))
            context = {}
            array_keys = []
            for key, val in self.data.items():
                # Key is an image in plots
                if os.path.exists('./assets/plots/' + key):
                    context[key.replace(".", "_")] = InlineImage(doc, './assets/plots/' + key)
                # Key is an image in images
                if os.path.exists('./assets/images/' + key):
                    context[key.replace(".", "_")] = InlineImage(doc, './assets/images/' + key)
                # Key is regular string or array of strings
                else:
                    try:
                        array_value = literal_eval(val)
                    except Exception:
                        print("Failed to eval literal, checking if str type")
                        if type(val == str):
                            context[key] = val
                    else:
                        context[key] = array_value
                        array_keys.append(key)

            if len(array_keys) == 0:
                doc.render(context)
                doc.save('./products/{}'.format(self.filename_docx))
                convert('./products/'.format(self.filename_docx), './products/'.format(self.filename_pdf))

        except Exception as e:
            self.signals.error.emit(str(e))
            return

        self.signals.file_saved_as.emit(outfile_pdf)


class Window(QWidget):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        # Thread for templating
        self.threadpool = QThreadPool()
        # Get all strings to be replaced (included header, footer..)
        # Ask user for input values in UI that replace those placeholders
        doc = DocxTemplate('./assets/docx_templating/{}'.format(self.filename))
        placeholders_list = list(doc.undeclared_template_variables)
        print(placeholders_list)
        self.map_placeholders_ui = {}

        for value in placeholders_list:
            if check_if_image_placeholder(value):
                # example.jpg -> example_jpg so templating and search don't break
                value = value.replace("_", ".")
                # map unique placeholders for UI
                self.map_placeholders_ui[value] = QLabel(value)
                self.map_placeholders_ui[value + "_caption"] = QLineEdit(value)
            else:
                self.map_placeholders_ui[value] = QLineEdit()
            # TODO ADD SUPPORT FOR GENERATING PLOTS WITH COMMAND PLACEHOLDER ex. {{generate_monthly_report}}

        self.generate_btn = QPushButton(constants.GENERATE_BUTTON)
        self.generate_btn.pressed.connect(self.generate)
        # UI Layout Setup
        layout = QFormLayout()
        for key, val in self.map_placeholders_ui.items():
            if type(val) == QPushButton:
                layout.addRow(val)
                continue
            if type(val) == QLabel:
                # Show placeholders for images as pixel map of found image or plot
                if os.path.exists('./assets/images/' + key):
                    val.setPixmap(QPixmap('./assets/images/{0}'.format(key)).scaled(300, 300, Qt.KeepAspectRatio))
                if os.path.exists('./assets/plots/' + key):
                    val.setPixmap(QPixmap('./assets/plots/{0}'.format(key)).scaled(300, 300, Qt.KeepAspectRatio))
                layout.addRow(val)
            if type(val) == QLineEdit:
                layout.addRow(key, val)

        layout.addRow(self.generate_btn)
        self.setLayout(layout)
        self.setWindowTitle(constants.SERVICE_TEMPLATING)

    def generate(self):
        self.generate_btn.setDisabled(True)
        data = {}  # Take inputted values
        for key, val in self.map_placeholders_ui.items():
            if type(val) == QPushButton:
                continue
            if type(val) == QLabel:
                data[key] = val.text()
                continue
            if type(val) == QLineEdit:
                data[key] = val.text()

        g = Generator(data, self.filename)
        g.signals.file_saved_as.connect(self.generated)
        g.signals.error.connect(print)  # Print errors to console.
        self.threadpool.start(g)

    def generated(self):
        self.generate_btn.setDisabled(False)
        try:
            os.startfile(get_project_root() + '\\products\\{}'.format(str.replace(self.filename, 'docx', 'pdf')))
        except Exception:
            # If startfile not available, show dialog.
            QMessageBox.information(self, constants.ACTION_FINISHED, constants.GENERATE_SUCCESSFUL)


def check_if_image_placeholder(placeholder: str):
    if re.search('_jpg|_png|_jpeg|_bmp|_gif|_raw|_tiff', placeholder.lower()):
        return True
    return False


def run_service(filename):
    global app, w
    try:
        w = Window(filename)
    except Exception:
        QMessageBox.information(w, constants.ACTION_FINISHED, constants.FILE_FAILED_TO_OPEN + filename)
        return
    w.show()
    app.exec_()
