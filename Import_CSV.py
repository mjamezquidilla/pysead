from PyQt6 import uic
from PyQt6.QtWidgets import *
import os
import sys

class Import_CSV(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi()
        self.statusBar = QStatusBar()

    def setupUi(self):
        # uic.loadUi("D:\\07 Github Repo\\Engineering\\pysead\\Import_CSV.ui", self)
        uic.loadUi(self.resource_path("Import_CSV.ui"), self)

        # Line Edits
        self.Nodes_LEdit = self.findChild(QLineEdit, "Nodes_LEdit")
        self.Bars_LEdit = self.findChild(QLineEdit, "Bars_LEdit")
        self.Materials_LEdit = self.findChild(QLineEdit, "Materials_LEdit")
        self.Forces_LEdit = self.findChild(QLineEdit, "Forces_LEdit")
        self.Supports_LEdit = self.findChild(QLineEdit, "Supports_LEdit")

        # Buttons
        self.Nodes_Button = self.findChild(QPushButton, "Nodes_Button")
        self.Bars_Button = self.findChild(QPushButton, "Bars_Button")
        self.Materials_Button = self.findChild(QPushButton, "Materials_Button")
        self.Forces_Button = self.findChild(QPushButton, "Forces_Button")
        self.Supports_Button = self.findChild(QPushButton, "Supports_Button")

        # Button Commands
        self.Nodes_Button.clicked.connect(self.Nodes_Open_Func)
        self.Bars_Button.clicked.connect(self.Bars_Open_Func)
        self.Materials_Button.clicked.connect(self.Materials_Open_Func)
        self.Forces_Button.clicked.connect(self.Forces_Open_Func)
        self.Supports_Button.clicked.connect(self.Supports_Open_Func)

        self.show()

    def Nodes_Open_Func(self):
        try: 
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "CSV File (*.csv);; All Files (*)")
            self.Nodes_LEdit.setText(file_name[0])
        except:
            self.statusBar.showMessage("Canceled Dialog")

    def Bars_Open_Func(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "CSV File (*.csv);; All Files (*)")
            self.Bars_LEdit.setText(file_name[0])
        except:            
            self.statusBar.showMessage("Canceled Dialog")

    def Materials_Open_Func(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "CSV File (*.csv);; All Files (*)")
            self.Materials_LEdit.setText(file_name[0])
        except:
            self.statusBar.showMessage("Canceled Dialog")

    def Forces_Open_Func(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "CSV File (*.csv);; All Files (*)")
            self.Forces_LEdit.setText(file_name[0])
        except:
            self.statusBar.showMessage("Canceled Dialog")

    def Supports_Open_Func(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "CSV File (*.csv);; All Files (*)")
            self.Supports_LEdit.setText(file_name[0])
        except:
            self.statusBar.showMessage("Canceled Dialog")

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
    
        return os.path.join(base_path, relative_path)