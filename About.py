from PyQt6 import uic
from PyQt6.QtWidgets import *
import os
import sys

class About(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi()
        self.statusBar = QStatusBar()

    def setupUi(self):
        # uic.loadUi("D:\\07 Github Repo\\Engineering\\pysead\\About.ui", self)
        uic.loadUi(self.resource_path("About.ui"), self)

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
    
        return os.path.join(base_path, relative_path)