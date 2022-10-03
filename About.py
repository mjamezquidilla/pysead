from PyQt5 import uic
from PyQt5.QtWidgets import *

class About(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi()
        self.statusBar = QStatusBar()

    def setupUi(self):
        # uic.loadUi("D:\\07 Github Repo\\Engineering\\pysead\\About.ui", self)
        uic.loadUi("About.ui", self)

        self.show()
