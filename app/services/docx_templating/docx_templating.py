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

GENERATE_BUTTON = "generate_button"


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

    def __init__(self, data: dict):
        super().__init__()
        self.data = data
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        pythoncom.CoInitialize()
        try:
            outfile_word = "../../products/invitation.docx"
            outfile_pdf = "../../products/invitation.pdf"

            doc = DocxTemplate('../../assets/docx_templating/inviteTmpl.docx')
            context = {}
            array_keys = []
            for key, val in self.data.items():
                print(key, val)
                # Key is an image in plots
                if os.path.exists('../../assets/plots/' + key):
                    print("Plot type")
                    context[key] = InlineImage(doc, '../../assets/plots/' + key)
                # Key is an image in images
                if os.path.exists('../../assets/images/' + key):
                    print("ulazim")
                    print("Image type")
                    print("Klj", key)
                    print("Vr", val)
                    context[key.replace(".", "_")] = InlineImage(doc, '../../assets/images/' + key)
                # Key is regular string or array of strings
                else:
                    print("ulazim u else")
                    try:
                        array_value = literal_eval(val)
                    except Exception:
                        print("Failed to eval literal, checking if str type")
                        if type(val == str):
                            print("Str type val")
                            context[key] = val
                    else:
                        print("Stringed array")
                        context[key] = array_value
                        array_keys.append(key)

            if len(array_keys) == 0:
                doc.render(context)
                doc.save('../../products/invitation.docx')
                convert('../../products/invitation.docx', '../../products/invitation.pdf')

        except Exception as e:
            print("Printing exception..")
            self.signals.error.emit(str(e))
            return

        self.signals.file_saved_as.emit(outfile_pdf)


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Thread for templating
        self.threadpool = QThreadPool()

        # Get all strings to be replaced (included header, footer..)
        # Ask user for input values in UI that replace those placeholders
        doc = DocxTemplate('../../assets/docx_templating/inviteTmpl.docx')
        placeholders_set = doc.undeclared_template_variables
        placeholders_list = list(placeholders_set)
        self.map_placeholders_ui = {}

        for value in placeholders_list:
            if check_if_image_placeholder(value):
                value = value.replace("_", ".")
                self.map_placeholders_ui[value] = QLabel(value)
            # TODO ADD SUPPORT FOR GENERATING PLOTS
            # TODO Captions
            else:
                self.map_placeholders_ui[value] = QLineEdit()

        # self.map_placeholders_ui[GENERATE_BUTTON] = QPushButton("Generate")
        # self.map_placeholders_ui[GENERATE_BUTTON].pressed.connect(self.generate)

        self.generate_btn = QPushButton("Generate PDF")
        self.generate_btn.pressed.connect(self.generate)

        # UI Final
        layout = QFormLayout()
        for key, val in self.map_placeholders_ui.items():
            if type(val) == QPushButton:
                layout.addRow(val)
                continue
            if type(val) == QLabel:
                if os.path.exists('../../assets/images/' + key):
                    val.setPixmap(QPixmap('../../assets/images/{0}'.format(key)).scaled(300, 300, Qt.KeepAspectRatio))
                if os.path.exists('../../assets/plots/' + key):
                    val.setPixmap(QPixmap('../../assets/plots/{0}'.format(key)).scaled(300, 300, Qt.KeepAspectRatio))
                layout.addRow(val)
            if type(val) == QLineEdit:
                layout.addRow(key, val)

        layout.addRow(self.generate_btn)
        self.setLayout(layout)
        self.setWindowTitle("Templating")

    def generate(self):
        # self.map_placeholders_ui[GENERATE_BUTTON].setDisabled(True)
        self.generate_btn.setDisabled(True)
        data = {}
        for key, val in self.map_placeholders_ui.items():
            if type(val) == QPushButton:
                continue
            if type(val) == QLabel:
                data[key] = val.text()
                continue
            if type(val) == QLineEdit:
                data[key] = val.text()

        g = Generator(data)
        g.signals.file_saved_as.connect(self.generated)
        g.signals.error.connect(print)  # Print errors to console.
        self.threadpool.start(g)

    def generated(self, outfile_pdf):
        self.generate_btn.setDisabled(False)
        try:
            print(os.path)
            print("Opening pdf...", get_project_root() + '\\products\\invitation.pdf')
            os.startfile(get_project_root() + '\\products\\invitation.pdf')
        except Exception:
            # If startfile not available, show dialog.
            print("except")
            QMessageBox.information(self, "Finished", "PDF has been generated")


def check_if_image_placeholder(placeholder: str):
    if re.search('_jpg|_png|_jpeg|_bmp|_gif|_raw|_tiff', placeholder.lower()):
        return True
    return False


app = QApplication([])
w = Window()
w.show()
app.exec_()
