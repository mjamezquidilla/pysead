# from PyQt5 import QtWidgets
import os
import sys
import gc

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import qdarkstyle

# Using PyQt6
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# Using PySide6
# from PySide6.QtUiTools import QUiLoader
# from PySide6.QtWidgets import *
# from PySide6.QtCore import *
# from PySide6.QtGui import *
# os.environ["PYSIDE_DESIGNER_PLUGINS"]="."

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

# PySEAD Modules
from pysead import Truss_2D
from Import_CSV import Import_CSV
from About import About

# Material Theme
from qt_material import apply_stylesheet
extra = {
    # Density Scale
    'density_scale': '-2',
    'PyQt6': True,
    'windows': True
}

# PyInstaller Splash Screen
if getattr(sys, 'frozen', False):
    import pyi_splash


plt.style.use('dark_background_pysead_materialdark')

os.environ['QT_API'] = 'PyQt6'


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setFocus()
        
        #Global Variables
        self.nodes = {}
        self.elements = {}
        self.supports = {}
        self.forces = {}
        self.forces_LC1 = {}
        self.forces_LC2 = {}
        self.forces_LC3 = {}
        self.forces_LC4 = {}
        self.forces_LC5 = {}
        self.forces_LC6 = {}
        self.forces_LC7 = {}
        self.forces_LC8 = {}
        self.forces_LC9 = {}
        self.forces_LC10 = {}
        self.elasticity = {}
        self.areas = {}
        self.load_case_index = 0
        
        # Load the UI file
        # PyQt5
        uic.loadUi(self.resource_path("Truss2D_GUI.ui"), self)
        
        self.setWindowIcon(QIcon(self.resource_path("icon.ico")))
        
        # PySide6
        # ui_file = QFile(self.resource_path("Truss2D_GUI.ui"))
        # # if not ui_en(QFile.read)
        # loader = QUiLoader()
        # uic = loader.load(ui_file, self)
        # ui_file.close()
        # if not uic:
        #     print(loader.errorString())
        #     sys.exit(-1)
        # uic.show()

        # Define our widgets
        # Button Widget
        self.Add_Node_Button = self.findChild(QPushButton, "Add_Node_Button")
        self.Renumber_Nodes_Button = self.findChild(QPushButton, "Renumber_Nodes_Button")
        self.Remove_Node_Button = self.findChild(QPushButton, "Remove_Node_Button")
        self.Update_Truss_Nodes_Button = self.findChild(QPushButton, "Update_Truss_Nodes_Button")
        
        self.Add_Bar_Button = self.findChild(QPushButton, "Add_Bar_Button")
        self.Renumber_Bar_Button = self.findChild(QPushButton, "Renumber_Bar_Button")
        self.Remove_Bar_Button = self.findChild(QPushButton, "Remove_Bar_Button")
        self.Update_Truss_Bars_Button = self.findChild(QPushButton, "Update_Truss_Elements_Button")
        
        self.Update_Material_Button = self.findChild(QPushButton, "Update_Material_Button")
        
        # self.Add_Load_Case_Button = self.findChild(QPushButton, "Add_Load_Case_Button")
        # self.Remove_Load_Case_Button = self.findChild(QPushButton, "Remove_Load_Case_Button")
        self.Add_Load_Combo_Button = self.findChild(QPushButton, "Add_Load_Combo_Button")
        self.Remove_Load_Combo_Button = self.findChild(QPushButton, "Remove_Load_Combo_Button")
        
        self.Self_Weight_Button = self.findChild(QPushButton, "Self_Weight_Button")
        
        self.Add_Force_Button = self.findChild(QPushButton, "Add_Force_Button")
        self.Remove_Force_Button = self.findChild(QPushButton, "Remove_Force_Button")
        self.Update_Truss_Forces_Button = self.findChild(QPushButton, "Update_Truss_Forces_Button")
        
        self.Add_Support_Button = self.findChild(QPushButton, "Add_Support_Button")
        self.Remove_Support_Button = self.findChild(QPushButton, "Remove_Support_Button")
        self.Update_Truss_Supports_Button = self.findChild(QPushButton, "Update_Truss_Supports_Button")
        
        self.Show_Load_Case_Table_Button = self.findChild(QPushButton, "Show_Load_Case_Table_Button")
        self.Solve_Truss_Button = self.findChild(QPushButton, "Solve_Truss_Button")
        self.Setup_Button = self.findChild(QPushButton, "Setup_Button")
        self.Reactions_Button = self.findChild(QPushButton, "Reactions_Button")
        self.Axial_Force_Button = self.findChild(QPushButton, "Axial_Force_Button")
        self.Displacement_Button = self.findChild(QPushButton, "Displacement_Button")

        self.Save_Figure_Button = self.findChild(QPushButton, "Save_Figure_Button")

        # Line Edit Widget
        self.Node_Number_From_LEdit = self.findChild(QLineEdit, "Node_Number_From_LEdit")
        self.X1_Coord_LEdit = self.findChild(QLineEdit, "X1_Coord_LEdit")
        self.Y1_Coord_LEdit = self.findChild(QLineEdit, "Y1_Coord_LEdit")
        self.Node_Number_Current_LEdit = self.findChild(QLineEdit, "Node_Number_Current_LEdit")
        self.X2_Coord_LEdit = self.findChild(QLineEdit, "X2_Coord_LEdit")
        self.Y2_Coord_LEdit = self.findChild(QLineEdit, "Y2_Coord_LEdit")
        self.Node_Step_LEdit = self.findChild(QLineEdit, "Node_Step_LEdit")
        

        self.Bar_Number_From_LEdit = self.findChild(QLineEdit, "Bar_Number_From_LEdit")
        self.Bar_Number_Current_LEdit = self.findChild(QLineEdit, "Bar_Number_Current_LEdit")
        self.Node_1_From_LEdit = self.findChild(QLineEdit, "Node_1_From_LEdit")
        self.Node_2_From_LEdit = self.findChild(QLineEdit, "Node_2_From_LEdit")
        
        self.Self_Weight_LEdit = self.findChild(QLineEdit, "Self_Weight_LEdit")
        self.Force_Node_Number_LEdit = self.findChild(QLineEdit, "Force_Node_Number_LEdit")
        self.Force_Node_To_LEdit = self.findChild(QLineEdit, "Force_Node_To_LEdit")
        self.Force_Step_LEdit = self.findChild(QLineEdit, "Force_Step_LEdit")
        
        self.Displacement_Factor_LEdit = self.findChild(QLineEdit, "Displacement_Factor_LEdit")
        self.Line_Width_LEdit = self.findChild(QLineEdit, "Line_Width_LEdit")
        self.Label_Offset_LEdit = self.findChild(QLineEdit, "Label_Offset_LEdit")
        self.Arrow_Length_LEdit = self.findChild(QLineEdit, "Arrow_Length_LEdit")
        self.Arrow_Head_Size_LEdit = self.findChild(QLineEdit, "Arrow_Head_Size_LEdit")
        self.Arrow_Line_Width_LEdit = self.findChild(QLineEdit, "Arrow_Line_Width_LEdit")
        self.DPI_LEdit = self.findChild(QLineEdit, "DPI_LEdit")
        self.Font_Size_LEdit = self.findChild(QLineEdit, "Font_Size_LEdit")

        # Combo Box
        self.X_Coord_ComboBox = self.findChild(QComboBox, "X_Coord_ComboBox")
        self.Y_Coord_ComboBox = self.findChild(QComboBox, "Y_Coord_ComboBox")
        self.Load_Case_ComboBox = self.findChild(QComboBox, "LoadCaseComboBox_Widget")
        self.Load_Combination_Combo_Box = self.findChild(QComboBox, "Load_Combination_Combo_Box")
       
        # Table Widget
        self.Nodes_Table_Widget = self.findChild(QTableWidget, "Nodes_Table_Widget")
        self.Element_Table_Widget = self.findChild(QTableWidget, "Element_Table_Widget")
        self.Material_Table_Widget = self.findChild(QTableWidget, "Material_Table_Widget")
        
        self.Load_Case_Table_Widget = self.findChild(QTableWidget, "LoadCase_Table_Widget")
        self.Load_Combination_Table_Widget = self.findChild(QTableWidget, "LoadCombination_Table_Widget")
        
        self.Force_Table_Widget = self.findChild(QTableWidget, "Force_Table_Widget")
        self.Support_Table_Widget = self.findChild(QTableWidget, "Support_Table_Widget")
        
        self.Post_Processing_Table = self.findChild(QTableWidget, "Post_Processing_Table")

        # Frame Widget
        self.Matplotlib_Frame = self.findChild(QFrame,"Matplotlib_Frame")

        # Put Matplotlib inside Matplotlib Frame
        self.verticalLayout_Matplotlib = QVBoxLayout(self.Matplotlib_Frame)
        self.verticalLayout_Matplotlib.setObjectName("Matplotlib_layout")
        self.figure = plt.figure(dpi=75)
        # self.figure.tight_layout()
        plt.rcParams.update({'font.size': float(self.Font_Size_LEdit.text()), 'figure.autolayout': True})
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.verticalLayout_Matplotlib.addWidget(self.canvas)
        self.verticalLayout_Matplotlib.addWidget(NavigationToolbar(self.canvas, self))
        self.ax = plt.gca()

        # Graphics View # TODO Graphics View
        # self.GraphicsView_Frame = self.findChild(QFrame,"GraphicsView_Frame")
        # self.GraphicsView_Layout = QHBoxLayout(self.GraphicsView_Frame)
        # self.GraphicsView_Layout.setObjectName("Graphics_layout")

        # Menu Items
        self.New_Menu = self.findChild(QAction, "actionNew")
        self.Open_Menu = self.findChild(QAction, "actionOpen")
        self.Save_As_Menu = self.findChild(QAction, "actionSave_As")
        self.Quit_Menu = self.findChild(QAction, "actionQuit")
        self.Import_CSV = self.findChild(QAction, "actionImport_CSV")
        self.About = self.findChild(QAction, "actionPySEAD_Truss")
        self.Export_HTML = self.findChild(QAction, "actionHTML")

        self.DarkMode_Menu = self.findChild(QAction, "actionDarkMode")
        # self.LightMode_Menu = self.findChild(QAction, "actionLightMode")
        self.MaterialDark_Menu = self.findChild(QAction, "actionMaterial_Dark")
        self.MaterialLight_Menu = self.findChild(QAction, "actionMaterial_Light")

        self.PySEAD_Truss_Menu = self.findChild(QAction, "actionPySEAD_Truss")

        # Keyboard Shortcuts
        self.New_Menu.setShortcut("Ctrl+N")
        self.Save_As_Menu.setShortcut("Ctrl+S")
        self.Open_Menu.setShortcut("Ctrl+O")
        self.Quit_Menu.setShortcut("Ctrl+Q")
        self.Setup_Button.setShortcut("F4")
        self.Solve_Truss_Button.setShortcut("F5")
        self.Reactions_Button.setShortcut("F6")
        self.Displacement_Button.setShortcut("F7")
        self.Axial_Force_Button.setShortcut("F8")

        # Run Commands

        # Button Commands
        # Nodes
        self.Add_Node_Button.clicked.connect(self.Add_Node_Button_Func)
        self.Remove_Node_Button.clicked.connect(self.Remove_Node_Button_Func)
        self.Renumber_Nodes_Button.clicked.connect(self.Renumber_Nodes_Func)
        self.Update_Truss_Nodes_Button.clicked.connect(self.Draw_Setup_Load_Case)

        # Elements
        self.Add_Bar_Button.clicked.connect(self.Add_Bar_Button_Func)
        self.Remove_Bar_Button.clicked.connect(self.Remove_Bar_Button_Func)
        self.Renumber_Bar_Button.clicked.connect(self.Renumber_Bars_Func)
        self.Update_Truss_Bars_Button.clicked.connect(self.Draw_Setup_Load_Case)
        
        # Materials
        self.Update_Material_Button.clicked.connect(self.Update_Material_Button_Func)
        
        # Load Case and Load Combinations
        # self.Add_Load_Case_Button.clicked.connect(self.Add_Load_Case_Button_Func)
        # self.Remove_Load_Case_Button.clicked.connect(self.Remove_Load_Case_Button_Func)
        # self.Show_Load_Case_Table_Button.clicked.connect(self.Show_Load_Case_Table_Button_Func)

        # Forces
        self.Self_Weight_Button.clicked.connect(self.Self_Weight_Func)
        
        self.Add_Force_Button.clicked.connect(self.Add_Force_Button_Func)
        self.Remove_Force_Button.clicked.connect(self.Remove_Force_Button_Func)
        self.Update_Truss_Forces_Button.clicked.connect(self.Draw_Setup_Load_Case)

        # Supports
        self.Add_Support_Button.clicked.connect(self.Add_Support_Button_Func)
        self.Remove_Support_Button.clicked.connect(self.Remove_Support_Button_Func)
        self.Update_Truss_Supports_Button.clicked.connect(self.Draw_Setup_Load_Case)

        # Solve
        self.Solve_Truss_Button.clicked.connect(self.Solve_Truss_Func)
        self.Setup_Button.clicked.connect(self.Draw_Setup_Load_Combo)
        self.Reactions_Button.clicked.connect(self.Draw_Truss_Reactions)
        self.Axial_Force_Button.clicked.connect(self.Draw_Truss_Axial_Force_Map)
        self.Displacement_Button.clicked.connect(self.Draw_Truss_Displacement)
        
        self.Save_Figure_Button.clicked.connect(self.Save_Figure_Func)

        # Menu Commands
        self.New_Menu.triggered.connect(self.New_File_Func)
        self.Open_Menu.triggered.connect(self.Open_File_Func)
        self.Save_As_Menu.triggered.connect(self.Save_As_Func)
        self.Quit_Menu.triggered.connect(self.Quit_Func)
        self.Import_CSV.triggered.connect(self.Import_CSV_Func)
        self.Export_HTML.triggered.connect(self.Export_Nodes_HTML_Func)
        
        self.DarkMode_Menu.triggered.connect(self.DarkMode_Menu_Func)
        # self.LightMode_Menu.triggered.connect(self.LightMode_Menu_Func)
        self.MaterialDark_Menu.triggered.connect(self.MaterialDark_Menu_Func)
        self.MaterialLight_Menu.triggered.connect(self.MaterialLight_Menu_Func)
        
        self.About.triggered.connect(self.About_Func)
        
        self.Node_row_Position = self.Nodes_Table_Widget.rowCount()
        self.Bar_row_Position = self.Element_Table_Widget.rowCount()
        

        # status bar
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Ready")

        # Automate Combo Box when it changes values
        try:
            self.Load_Case_ComboBox.activated.connect(self.Show_Load_Case_Table_Button_Func)
            self.Load_Combination_Combo_Box.activated.connect(self.Draw_Setup_Load_Combo)
        except:
            pass

        # Show the App
        # self.show()
    
    def clicked(self):
        type(file_name[0])


    ###### Nodes Function ######
    def Add_Node_Button_Func(self):
        # Check if all textbox is not empty
        if self.Node_Number_From_LEdit.text() == "" or self.X1_Coord_LEdit.text() == "" or self.Y1_Coord_LEdit.text() == "":
            print("Do not leave nodes textboxes empty")
        else:
            # Grabe Item from LEdit Box
            node1 = int(self.Node_Number_From_LEdit.text())
            x1_coord = float(self.X1_Coord_LEdit.text())
            y1_coord = float(self.Y1_Coord_LEdit.text())
            
            node2 = int(self.Node_Number_Current_LEdit.text())
            x2_coord = float(self.X2_Coord_LEdit.text())
            y2_coord = float(self.Y2_Coord_LEdit.text())
            
            step = int(self.Node_Step_LEdit.text())
            
            # self.node_number = int(node) + 1

            # # Add Items to Table Widget
            # self.Node_row_Position = self.Nodes_Table_Widget.rowCount()
            
            # # Clear the Textboxes
            self.Node_Number_Current_LEdit.setText("")
            self.X2_Coord_LEdit.setText("")
            self.Y2_Coord_LEdit.setText("")

            # Update the nodes and auto sort
            # self.nodes.update({node: [x_coord, y_coord]})
            
            no_of_nodes = int((node2 - node1)/step + 1)

            x_array = np.linspace(x1_coord, x2_coord, num=no_of_nodes, endpoint=True)
            y_array = np.linspace(y1_coord, y2_coord, num=no_of_nodes, endpoint=True)

            for i in range(int(no_of_nodes)):
                self.nodes.update({node1 + i: [round(x_array[i],3), round(y_array[i],3)]})
            
            self.nodes = {k: v for k, v in sorted(self.nodes.items(), key=lambda item: item[0])}

            # Remove duplicated nodes
   
            # Remove the table items
            self.Nodes_Table_Widget.setRowCount(0)

            # Loop all the nodes dictionary and replace/update the table widget
            for key, item in self.nodes.items():
                node = str(key)
                x_coord = str(item[0])
                y_coord = str(item[1])

                # Add Items to Table Widget
                rowPosition = self.Nodes_Table_Widget.rowCount()

                # print(rowPosition)
                self.Nodes_Table_Widget.insertRow(rowPosition)
                self.Nodes_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
                self.Nodes_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(x_coord))
                self.Nodes_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(y_coord))

            self.Renumber_Nodes_Func()

            # Change LineEdit to maximum number of rows
            self.Node_Number_From_LEdit.setText(str(int(self.Nodes_Table_Widget.rowCount())))
            self.X1_Coord_LEdit.setText(str(int(x2_coord)))
            self.Y1_Coord_LEdit.setText(str(int(y2_coord)))
            
            self.Node_Number_From_LEdit.setFocus()

            # Draw Truss
            self.Draw_Setup_Load_Case()
            print(self.nodes)

        
    def Remove_Node_Button_Func(self):
        try:
            # Grab Item from Highlighted Row
            clicked = self.Nodes_Table_Widget.currentRow()

            # Delete Highlighted Row
            self.Nodes_Table_Widget.removeRow(clicked)
            self.Renumber_Nodes_Func()
            
            if int(self.Node_Number_From_LEdit.text()) == 2:
                self.Node_Number_From_LEdit.setText(str(int(self.Node_Number_From_LEdit.text()) - 1))

            # Reinitialize nodes dictionary and copy all data from table into dictionary        
            self.nodes = {}
            for index in range(self.Nodes_Table_Widget.rowCount()):
                node = int(self.Nodes_Table_Widget.item(index,0).text())
                x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
                y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
                self.nodes.update({index+1:[int(node), float(x_coord), float(y_coord)]})

            # Change LineEdit to maximum number of rows
            self.Node_Number_From_LEdit.setText(str(int(self.Nodes_Table_Widget.rowCount()+1)))
            
            # Draw Truss
            self.Draw_Setup_Load_Case()
        except:
            self.statusBar.showMessage("Error Deleting node. Double check Bar Elements nodes")

    def Renumber_Nodes_Func(self):
        for index in range(self.Nodes_Table_Widget.rowCount()):
            # node = int(self.Nodes_Table_Widget.item(index,0).text())
            x_coord = self.Nodes_Table_Widget.item(index,1).text()
            y_coord = self.Nodes_Table_Widget.item(index,2).text()

            if x_coord == "":
                x_coord = '0'

            if y_coord == "":
                y_coord = '0'
            
            # print(type(str(index)), type(x_coord), type(y_coord))
            self.Nodes_Table_Widget.setItem(index, 0, QTableWidgetItem(str(index+1)))
            self.Nodes_Table_Widget.setItem(index, 1, QTableWidgetItem(x_coord))
            self.Nodes_Table_Widget.setItem(index, 2, QTableWidgetItem(y_coord))
            
            # Reinitialize nodes dictionary and copy all data from table into dictionary        
            self.nodes = {}
            for index in range(self.Nodes_Table_Widget.rowCount()):
                node = int(self.Nodes_Table_Widget.item(index,0).text())
                x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
                y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
                self.nodes.update({index+1:[int(node), float(x_coord), float(y_coord)]})
            
    ###### Elements Function ######
    def Add_Bar_Button_Func(self):
        if self.Bar_Number_From_LEdit.text() == "" or self.Node_1_From_LEdit.text() == "" or self.Node_2_From_LEdit.text() == "":
            print("Do not leave Bar/Elements textboxes empty")
        else:
            # Grabe Item from LEdit Box
            bar1 = int(self.Bar_Number_From_LEdit.text())
            bar2 = int(self.Bar_Number_Current_LEdit.text())
            node_1 = int(self.Node_1_From_LEdit.text())
            node_2 = int(self.Node_2_From_LEdit.text())            
            
            area = float(self.Area_LEdit.text())
            elasticity = float(self.Elasticity_LEdit.text())

            new_bar_number = bar1 + 1

            # Update the elements, areas, and elasticity 
            # self.elements.update({bar1: [node_1, node_2]})
            no_of_bars = int((bar2+1) - bar1)
            node1_array = np.arange(node_1, node_1 + (no_of_bars), 1)
            node2_array = np.arange(node_2, node_2 + (no_of_bars), 1)
            
            if node2_array[-1] in self.nodes:
                
                for i in range(int(no_of_bars)):
                    self.elements.update({bar1 + i: [int(node1_array[i]), int(node2_array[i])]})
                
                # self.areas.update({bar1: area})
                for i in range(int(no_of_bars)):
                    self.areas.update({bar1 + i: area})
                
                # self.elasticity.update({bar1: elasticity})
                for i in range(int(no_of_bars)):
                    self.elasticity.update({bar1 + i: elasticity})
                
                # auto sort the elements, areas, and elasticity 
                self.elements = {k: v for k, v in sorted(self.elements.items(), key=lambda item: item[0])}
                self.areas = {k: v for k, v in sorted(self.areas.items(), key=lambda item: item[0])}
                self.elasticity = {k: v for k, v in sorted(self.elasticity.items(), key=lambda item: item[0])}


                # Remove the table items
                self.Element_Table_Widget.setRowCount(0)
                self.Material_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.elements.items():
                    bar1 = str(key)
                    node_1 = str(item[0])
                    node_2 = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Element_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Element_Table_Widget.insertRow(rowPosition)
                    self.Element_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(bar1))
                    self.Element_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(node_1))
                    self.Element_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(node_2))

                for (key, area), (_, elasticity) in zip(self.areas.items(), self.elasticity.items()):
                    bar1 = str(key)
                    areas = str(area)
                    elasticity = str(elasticity)

                    rowPosition = self.Material_Table_Widget.rowCount()
                    self.Material_Table_Widget.insertRow(rowPosition)
                    self.Material_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(bar1))
                    self.Material_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(areas))
                    self.Material_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(elasticity))

                # Clear the Textboxes
                self.Bar_Number_From_LEdit.setText(str(new_bar_number))
                self.Node_1_From_LEdit.setText("")
                self.Node_2_From_LEdit.setText("")

                self.Renumber_Bars_Func()

                # Change LineEdit to maximum number of rows
                self.Bar_Number_From_LEdit.setText(str(int(self.Element_Table_Widget.rowCount()+1)))
                self.Bar_Number_Current_LEdit.setText(str(int(self.Element_Table_Widget.rowCount()+2)))

                # Draw Truss
                self.Draw_Setup_Load_Case()
                self.statusBar.showMessage("")
            
            else:
                self.statusBar.showMessage("Error in maximum number of bars")


    def Renumber_Bars_Func(self):
        for index in range(self.Element_Table_Widget.rowCount()):
            node_1 = self.Element_Table_Widget.item(index,1).text()
            node_2 = self.Element_Table_Widget.item(index,2).text()
            area = self.Material_Table_Widget.item(index,1).text()
            elasticity = self.Material_Table_Widget.item(index,2).text()

            if node_1 == "":
                node_1 = '0'

            if node_2 == "":
                node_2 = '0'

            if area == "":
                area = '0'

            if elasticity == "":
                elasticity = '0'
            
            self.Element_Table_Widget.setItem(index, 0, QTableWidgetItem(str(index+1)))
            self.Element_Table_Widget.setItem(index, 1, QTableWidgetItem(node_1))
            self.Element_Table_Widget.setItem(index, 2, QTableWidgetItem(node_2))
            self.Material_Table_Widget.setItem(index, 0, QTableWidgetItem(str(index+1)))
            self.Material_Table_Widget.setItem(index, 1, QTableWidgetItem(area))
            self.Material_Table_Widget.setItem(index, 2, QTableWidgetItem(elasticity))

    def Remove_Bar_Button_Func(self):
        # Grab Item from Highlighted Row
        clicked = self.Element_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Element_Table_Widget.removeRow(clicked)
        self.Material_Table_Widget.removeRow(clicked)

        if int(self.Bar_Number_From_LEdit.text()) == 2:
            self.Bar_Number_From_LEdit.setText(str(int(self.Bar_Number_From_LEdit.text())-1))
        
        self.Renumber_Bars_Func()

        self.elements = {}
        self.areas = {}
        self.elasticity = {}

        # Elements
        for index in range(self.Element_Table_Widget.rowCount()):
            bar = int(self.Element_Table_Widget.item(index,0).text())
            node_1 = int(self.Element_Table_Widget.item(index,1).text())
            node_2 = int(self.Element_Table_Widget.item(index,2).text())
            self.elements.update({bar:[node_1, node_2]})

        # Materials
        for index in range(self.Material_Table_Widget.rowCount()):
            bar = int(self.Material_Table_Widget.item(index,0).text())
            area = float(self.Material_Table_Widget.item(index,1).text())
            elasticity = float(self.Material_Table_Widget.item(index,2).text())
            self.areas.update({int(bar): float(area)})
            self.elasticity.update({int(bar): float(elasticity)})
                        
        # Change LineEdit to maximum number of rows
        self.Bar_Number_From_LEdit.setText(str(int(self.Element_Table_Widget.rowCount()+1)))
        
        # Draw Truss
        self.Draw_Setup_Load_Case()
        print(self.elements)
        print(self.areas)
        print(self.elasticity)
        
    ###### Materials Function ######
    def Update_Material_Button_Func(self):
        try:
            # Grab Item from Highlighted Row
            # clicked_row = self.Material_Table_Widget.currentRow()
            clicked_row = self.Material_Table_Widget.selectionModel().selectedRows()
            
            # Get all row index
            indexes = []
            for row in clicked_row:
                indexes.append(row.row())
            
            # Delete Highlighted Row
            # self.Material_Table_Widget.removeRow(clicked_row)

            # Grab Items from Columns of the Selected Row
            # bar = self.Element_Table_Widget.item(clicked_row,0).text()
            area = self.Area_LEdit.text()
            elasticity = self.Elasticity_LEdit.text()

            # Add Items to Table Widget

            # self.Material_Table_Widget.insertRow(clicked_row)
            # self.Material_Table_Widget.setItem(clicked_row, 0, QTableWidgetItem(bar))
            # self.Material_Table_Widget.setItem(clicked_row, 1, QTableWidgetItem(area))
            # self.Material_Table_Widget.setItem(clicked_row, 2, QTableWidgetItem(elasticity))
    
            for rowidx in indexes:
                self.Material_Table_Widget.setItem(rowidx, 1, QTableWidgetItem(area))
                self.Material_Table_Widget.setItem(rowidx, 2, QTableWidgetItem(elasticity))

        # def Remove_Material_Button_Func(self):
        #     # Grab Item from Highlighted Row
        #     clicked = self.Material_Table_Widget.currentRow()

        #     # Delete Highlighted Row
        #     self.Material_Table_Widget.removeRow(clicked)
        #     self.Element_Table_Widget.removeRow(clicked)
        except:
            pass

    ###### Load Cases and Load Combinations Function ######
    # def Add_Load_Case_Button_Func(self):
    #     self.Load_Case_Table_Widget.insertRow(self.Load_Case_Table_Widget.rowCount())
        
    # def Remove_Load_Case_Button_Func(self):
    #     print("Remove Load Case")
        
    def Show_Load_Case_Table_Button_Func(self):
        # load_case_index = self.Load_Case_ComboBox.currentIndex()
        # print(load_case_index)
        if self.Load_Case_ComboBox.currentIndex() == 0:
            self.forces = self.forces_LC1
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC1)
            self.Load_Combination_Combo_Box.setCurrentIndex(0)
        elif self.Load_Case_ComboBox.currentIndex() == 1:
            self.forces = self.forces_LC2
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC2)
            self.Load_Combination_Combo_Box.setCurrentIndex(1)
        elif self.Load_Case_ComboBox.currentIndex() == 2:
            self.forces = self.forces_LC3
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC3)
            self.Load_Combination_Combo_Box.setCurrentIndex(2)
        elif self.Load_Case_ComboBox.currentIndex() == 3:
            self.forces = self.forces_LC4
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC4)
            self.Load_Combination_Combo_Box.setCurrentIndex(3)
        elif self.Load_Case_ComboBox.currentIndex() == 4:
            self.forces = self.forces_LC5
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC5)
            self.Load_Combination_Combo_Box.setCurrentIndex(4)
        elif self.Load_Case_ComboBox.currentIndex() == 5:
            self.forces = self.forces_LC6
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC6)
            self.Load_Combination_Combo_Box.setCurrentIndex(5)
        elif self.Load_Case_ComboBox.currentIndex() == 6:
            self.forces = self.forces_LC7
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC7)
            self.Load_Combination_Combo_Box.setCurrentIndex(6)
        elif self.Load_Case_ComboBox.currentIndex() == 7:
            self.forces = self.forces_LC8
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC8)
            self.Load_Combination_Combo_Box.setCurrentIndex(7)
        elif self.Load_Case_ComboBox.currentIndex() == 8:
            self.forces = self.forces_LC9
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC9)
            self.Load_Combination_Combo_Box.setCurrentIndex(8)
        elif self.Load_Case_ComboBox.currentIndex() == 9:
            self.forces = self.forces_LC10
            # self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC10)
            self.Load_Combination_Combo_Box.setCurrentIndex(9)

        self.Force_Table_Widget.setRowCount(0)
                    
        # Loop all the force dictionary and replace/update the table widget
        for key, item in self.forces.items():
            node = str(key)
            f_x = str(item[0])
            f_y = str(item[1])

            # Add Items to Table Widget
            rowPosition = self.Force_Table_Widget.rowCount()

            # print(rowPosition)
            self.Force_Table_Widget.insertRow(rowPosition)
            self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
            self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
            self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
        
        # Draw Truss
        self.Draw_Setup_Load_Case()


    ###### Forces Function ######
    def Add_Force_Button_Func(self): #TODO ADD FORCES
        if self.Force_Node_Number_LEdit.text() == "" or self.Force_X_LEdit.text() == "" or self.Force_Y_LEdit.text() == "":
            print("Do not leave Force textboxes empty")
        else:
            # Grabe Item from LEdit Box
            node1 = int(self.Force_Node_Number_LEdit.text())
            node2 = int(self.Force_Node_To_LEdit.text())
            f_x = float(self.Force_X_LEdit.text())
            f_y = float(self.Force_Y_LEdit.text())
            step = int(self.Force_Step_LEdit.text())
            
            node_array = np.arange(node1, node2+step, step)

            if self.Load_Case_ComboBox.currentIndex() == 0:
                
                # self.forces_LC1.update({node1:[f_x,f_y]})
                
                for i in node_array:
                    self.forces_LC1.update({i: [f_x, f_y]})                    
                    
                self.forces_LC1 = {k: v for k, v in sorted(self.forces_LC1.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC1.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
                    
            elif self.Load_Case_ComboBox.currentIndex() == 1:
                # self.forces_LC2.update({node1:[f_x,f_y]})
                
                for i in node_array:
                    self.forces_LC2.update({i: [f_x, f_y]})
                    
                self.forces_LC2 = {k: v for k, v in sorted(self.forces_LC2.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC2.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))

                    
            elif self.Load_Case_ComboBox.currentIndex() == 2:
                # self.forces_LC3.update({node1:[f_x,f_y]})
                                
                for i in node_array:
                    self.forces_LC3.update({i: [f_x, f_y]})
                    
                self.forces_LC3 = {k: v for k, v in sorted(self.forces_LC3.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC3.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
                    
            elif self.Load_Case_ComboBox.currentIndex() == 3:
                # self.forces_LC4.update({node1:[f_x,f_y]})
                                                
                for i in node_array:
                    self.forces_LC4.update({i: [f_x, f_y]})
                
                self.forces_LC4 = {k: v for k, v in sorted(self.forces_LC4.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC4.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))

            elif self.Load_Case_ComboBox.currentIndex() == 4:
                # self.forces_LC5.update({node1:[f_x,f_y]})
                                                                
                for i in node_array:
                    self.forces_LC5.update({i: [f_x, f_y]})                
                
                self.forces_LC5 = {k: v for k, v in sorted(self.forces_LC5.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC5.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
                    
            elif self.Load_Case_ComboBox.currentIndex() == 5:
                # self.forces_LC6.update({node1:[f_x,f_y]})
                                                                
                for i in node_array:
                    self.forces_LC6.update({i: [f_x, f_y]})
                
                self.forces_LC6 = {k: v for k, v in sorted(self.forces_LC6.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC6.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
                    
            elif self.Load_Case_ComboBox.currentIndex() == 6:
                # self.forces_LC7.update({node1:[f_x,f_y]})
            
                for i in node_array:
                    self.forces_LC7.update({i: [f_x, f_y]})
                
                self.forces_LC7 = {k: v for k, v in sorted(self.forces_LC7.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC7.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
                    
            elif self.Load_Case_ComboBox.currentIndex() == 7:
                # self.forces_LC8.update({node1:[f_x,f_y]})
                
                for i in node_array:
                    self.forces_LC8.update({i: [f_x, f_y]})
                
                self.forces_LC8 = {k: v for k, v in sorted(self.forces_LC8.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC8.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))

            elif self.Load_Case_ComboBox.currentIndex() == 8:
                # self.forces_LC9.update({node1:[f_x,f_y]})
                
                for i in node_array:
                    self.forces_LC9.update({i: [f_x, f_y]})
                                
                self.forces_LC9 = {k: v for k, v in sorted(self.forces_LC9.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC9.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))

            elif self.Load_Case_ComboBox.currentIndex() == 9:
                # self.forces_LC10.update({node1:[f_x,f_y]})
                
                for i in node_array:
                    self.forces_LC10.update({i: [f_x, f_y]})
                
                self.forces_LC10 = {k: v for k, v in sorted(self.forces_LC10.items(), key=lambda item: item[0])}

                self.Force_Table_Widget.setRowCount(0)

                # Loop all the nodes dictionary and replace/update the table widget
                for key, item in self.forces_LC10.items():
                    node1 = str(key)
                    f_x = str(item[0])
                    f_y = str(item[1])

                    # Add Items to Table Widget
                    rowPosition = self.Force_Table_Widget.rowCount()

                    # print(rowPosition)
                    self.Force_Table_Widget.insertRow(rowPosition)
                    self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node1))
                    self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                    self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
                    
            else:
                print("error")
                                       
            # Clear the Textboxes
            self.Force_Node_Number_LEdit.setText("")
            self.Force_Node_To_LEdit.setText("")
            # self.Force_X_LEdit.setText("")
            # self.Force_Y_LEdit.setText("")
            
            # Draw Truss
            self.Draw_Setup_Load_Case()
            # print(self.forces_LC1)

    def Remove_Force_Button_Func(self):
        # Grab Item from Highlighted Row
        # clicked = self.Force_Table_Widget.currentRow()
        clicked_row = self.Force_Table_Widget.selectionModel().selectedRows()

        # Get all row index
        indexes = []
        for row in clicked_row:
            indexes.append(row.row())
            
        # Reverse sort rows indexes
        indexes = sorted(indexes, reverse=True)
        
        # Forces TODO Remove forces to all load cases and update force pyqt table
        for rowidx in indexes:
            # bar = int(self.Force_Table_Widget.item(rowidx,0).text())
            # f_x = float(self.Force_Table_Widget.item(rowidx,1).text())
            # f_y = float(self.Force_Table_Widget.item(rowidx,2).text())
            # self.forces_LC1.update({bar: [f_x, f_y]})
            self.Force_Table_Widget.removeRow(rowidx)

        # Update Forces Dictionary based on PyQt Table
        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            self.forces_LC1 = {}
            self.Load_Case_ComboBox.setCurrentIndex(0)
        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            self.forces_LC2 = {}
            self.Load_Case_ComboBox.setCurrentIndex(1)
        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            self.forces_LC3 = {}
            self.Load_Case_ComboBox.setCurrentIndex(2)
        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            self.forces_LC4 = {}
            self.Load_Case_ComboBox.setCurrentIndex(3)
        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            self.forces_LC5 = {}
            self.Load_Case_ComboBox.setCurrentIndex(4)
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            self.forces_LC6 = {}
            self.Load_Case_ComboBox.setCurrentIndex(5)
        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            self.forces_LC7 = {}
            self.Load_Case_ComboBox.setCurrentIndex(6)
        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            self.forces_LC8 = {}
            self.Load_Case_ComboBox.setCurrentIndex(7)
        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            self.forces_LC9 = {}
            self.Load_Case_ComboBox.setCurrentIndex(8)
        else:
            self.forces_LC10 = {}
            self.Load_Case_ComboBox.setCurrentIndex(9)
        
        self.Draw_Setup_Load_Case()
        
        # print(self.forces_LC1)
    
    def Self_Weight_Func(self):
        if self.Self_Weight_LEdit.text() == "":
            print("Do not leave Self-Weight textboxes empty")
        else:
            # Grabe Item from LEdit Box
            unit_weight = float(self.Self_Weight_LEdit.text())
            
            self.Renumber_Nodes_Func()
            self.Renumber_Bars_Func()
            
            self.nodes = {}
            self.elements = {}
            self.areas = {}
            self.forces = {}
            self.supports = {}


            # Nodes
            for index in range(self.Nodes_Table_Widget.rowCount()):
                node = int(self.Nodes_Table_Widget.item(index,0).text())
                x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
                y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
                self.nodes.update({node: [x_coord,y_coord]})

            # Elements
            for index in range(self.Element_Table_Widget.rowCount()):
                bar = int(self.Element_Table_Widget.item(index,0).text())
                node_1 = int(self.Element_Table_Widget.item(index,1).text())
                node_2 = int(self.Element_Table_Widget.item(index,2).text())
                self.elements.update({bar:[node_1, node_2]})

            # Materials
            for index in range(self.Material_Table_Widget.rowCount()):
                bar = int(self.Material_Table_Widget.item(index,0).text())
                area = float(self.Material_Table_Widget.item(index,1).text())
                elasticity = float(self.Material_Table_Widget.item(index,2).text())
                self.areas.update({bar: area})
                self.elasticity.update({bar: elasticity})

            # Supports
            for index in range(self.Support_Table_Widget.rowCount()):
                node = int(self.Support_Table_Widget.item(index,0).text())
                x = int(self.Support_Table_Widget.item(index,1).text())
                y = int(self.Support_Table_Widget.item(index,2).text())
                self.supports.update({node: [x, y]})
                

            self.Truss_LC1 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC1)
            self.Truss_LC1.Apply_Selfweight(unit_weight)
                  
            self.forces_LC1 = self.Truss_LC1.forces
            
            self.Force_Table_Widget.setRowCount(0)
            
            for key, item in self.forces_LC1.items():
                node = str(key)
                f_x = str(item[0])
                f_y = str(item[1])

                # Add Items to Table Widget
                rowPosition = self.Force_Table_Widget.rowCount()

                # print(rowPosition)
                self.Force_Table_Widget.insertRow(rowPosition)
                self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
                self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
            
            self.Draw_Setup_Load_Case()
            
    ###### Support Function ######
    def Add_Support_Button_Func(self):
        if self.Support_Node_LEdit.text() == "":
            print("Do not leave Force textboxes empty")
        else:
            # Grabe Item from LEdit Box
            node = int(self.Support_Node_LEdit.text())
            x = self.X_Coord_ComboBox.currentText()
            y = self.Y_Coord_ComboBox.currentText()

            if x == "Yes":
                x = 1
            else:
                x = 0
            
            if y == "Yes":
                y = 1
            else:
                y = 0

            self.supports.update({node:[x,y]})
            self.supports = {k: v for k, v in sorted(self.supports.items(), key=lambda item: item[0])}
            print(self.supports)

            self.Support_Table_Widget.setRowCount(0)

            # Loop all the nodes dictionary and replace/update the table widget
            for key, item in self.supports.items():
                node = str(key)
                x = str(item[0])
                y = str(item[1])

                # Add Items to Table Widget
                rowPosition = self.Support_Table_Widget.rowCount()

                # print(rowPosition)
                self.Support_Table_Widget.insertRow(rowPosition)
                self.Support_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
                self.Support_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(x))
                self.Support_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(y))

            # Clear the Textboxes
            self.Support_Node_LEdit.setText("")

            # Draw Truss
            self.Draw_Setup_Load_Case()


    def Remove_Support_Button_Func(self):
        # Grab Item from Highlighted Row
        clicked = self.Support_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Support_Table_Widget.removeRow(clicked)

        # Supports
        self.supports = {}
        for index in range(self.Support_Table_Widget.rowCount()):
            node = int(self.Support_Table_Widget.item(index,0).text())
            x = int(self.Support_Table_Widget.item(index,1).text())
            y = int(self.Support_Table_Widget.item(index,2).text())
            self.supports.update({node: [x, y]})

        self.Draw_Setup_Load_Case()
        print(self.supports)
        
        
    ###### Truss Functions ######
    def Solve_Truss_Func(self):
        # Update all dictionaries from tables
        self.Renumber_Nodes_Func()
        self.Renumber_Bars_Func()
        
        self.nodes = {}
        self.elements = {}
        self.areas = {}
        
        self.supports = {}


        # Nodes
        for index in range(self.Nodes_Table_Widget.rowCount()):
            node = int(self.Nodes_Table_Widget.item(index,0).text())
            x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
            y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
            self.nodes.update({node: [x_coord,y_coord]})

        # Elements
        for index in range(self.Element_Table_Widget.rowCount()):
            bar = int(self.Element_Table_Widget.item(index,0).text())
            node_1 = int(self.Element_Table_Widget.item(index,1).text())
            node_2 = int(self.Element_Table_Widget.item(index,2).text())
            self.elements.update({bar:[node_1, node_2]})

        # Materials
        for index in range(self.Material_Table_Widget.rowCount()):
            bar = int(self.Material_Table_Widget.item(index,0).text())
            area = float(self.Material_Table_Widget.item(index,1).text())
            elasticity = float(self.Material_Table_Widget.item(index,2).text())
            self.areas.update({bar: area})
            self.elasticity.update({bar: elasticity})

        # Supports
        for index in range(self.Support_Table_Widget.rowCount()):
            node = int(self.Support_Table_Widget.item(index,0).text())
            x = int(self.Support_Table_Widget.item(index,1).text())
            y = int(self.Support_Table_Widget.item(index,2).text())
            self.supports.update({node: [x, y]})
            
        # Get Load Combination Factors from Load Combination Table
        # Load Combo 1
        Combo1_1 = float(self.Load_Combination_Table_Widget.item(0,0).text())
        Combo1_2 = float(self.Load_Combination_Table_Widget.item(1,0).text())
        Combo1_3 = float(self.Load_Combination_Table_Widget.item(2,0).text())
        Combo1_4 = float(self.Load_Combination_Table_Widget.item(3,0).text())
        Combo1_5 = float(self.Load_Combination_Table_Widget.item(4,0).text())
        Combo1_6 = float(self.Load_Combination_Table_Widget.item(5,0).text())
        Combo1_7 = float(self.Load_Combination_Table_Widget.item(6,0).text())
        Combo1_8 = float(self.Load_Combination_Table_Widget.item(7,0).text())
        Combo1_9 = float(self.Load_Combination_Table_Widget.item(8,0).text())
        Combo1_10 = float(self.Load_Combination_Table_Widget.item(9,0).text())
        
        # Load Combo 2
        Combo2_1 = float(self.Load_Combination_Table_Widget.item(0,1).text())
        Combo2_2 = float(self.Load_Combination_Table_Widget.item(1,1).text())
        Combo2_3 = float(self.Load_Combination_Table_Widget.item(2,1).text())
        Combo2_4 = float(self.Load_Combination_Table_Widget.item(3,1).text())
        Combo2_5 = float(self.Load_Combination_Table_Widget.item(4,1).text())
        Combo2_6 = float(self.Load_Combination_Table_Widget.item(5,1).text())
        Combo2_7 = float(self.Load_Combination_Table_Widget.item(6,1).text())
        Combo2_8 = float(self.Load_Combination_Table_Widget.item(7,1).text())
        Combo2_9 = float(self.Load_Combination_Table_Widget.item(8,1).text())
        Combo2_10 = float(self.Load_Combination_Table_Widget.item(9,1).text())
        
        # Load Combo 3
        Combo3_1 = float(self.Load_Combination_Table_Widget.item(0,2).text())
        Combo3_2 = float(self.Load_Combination_Table_Widget.item(1,2).text())
        Combo3_3 = float(self.Load_Combination_Table_Widget.item(2,2).text())
        Combo3_4 = float(self.Load_Combination_Table_Widget.item(3,2).text())
        Combo3_5 = float(self.Load_Combination_Table_Widget.item(4,2).text())
        Combo3_6 = float(self.Load_Combination_Table_Widget.item(5,2).text())
        Combo3_7 = float(self.Load_Combination_Table_Widget.item(6,2).text())
        Combo3_8 = float(self.Load_Combination_Table_Widget.item(7,2).text())
        Combo3_9 = float(self.Load_Combination_Table_Widget.item(8,2).text())
        Combo3_10 = float(self.Load_Combination_Table_Widget.item(9,2).text())

        # Load Combo 4
        Combo4_1 = float(self.Load_Combination_Table_Widget.item(0,3).text())
        Combo4_2 = float(self.Load_Combination_Table_Widget.item(1,3).text())
        Combo4_3 = float(self.Load_Combination_Table_Widget.item(2,3).text())
        Combo4_4 = float(self.Load_Combination_Table_Widget.item(3,3).text())
        Combo4_5 = float(self.Load_Combination_Table_Widget.item(4,3).text())
        Combo4_6 = float(self.Load_Combination_Table_Widget.item(5,3).text())
        Combo4_7 = float(self.Load_Combination_Table_Widget.item(6,3).text())
        Combo4_8 = float(self.Load_Combination_Table_Widget.item(7,3).text())
        Combo4_9 = float(self.Load_Combination_Table_Widget.item(8,3).text())
        Combo4_10 = float(self.Load_Combination_Table_Widget.item(9,3).text())

        # Load Combo 5
        Combo5_1 = float(self.Load_Combination_Table_Widget.item(0,4).text())
        Combo5_2 = float(self.Load_Combination_Table_Widget.item(1,4).text())
        Combo5_3 = float(self.Load_Combination_Table_Widget.item(2,4).text())
        Combo5_4 = float(self.Load_Combination_Table_Widget.item(3,4).text())
        Combo5_5 = float(self.Load_Combination_Table_Widget.item(4,4).text())
        Combo5_6 = float(self.Load_Combination_Table_Widget.item(5,4).text())
        Combo5_7 = float(self.Load_Combination_Table_Widget.item(6,4).text())
        Combo5_8 = float(self.Load_Combination_Table_Widget.item(7,4).text())
        Combo5_9 = float(self.Load_Combination_Table_Widget.item(8,4).text())
        Combo5_10 = float(self.Load_Combination_Table_Widget.item(9,4).text())

        # Load Combo 6
        Combo6_1 = float(self.Load_Combination_Table_Widget.item(0,5).text())
        Combo6_2 = float(self.Load_Combination_Table_Widget.item(1,5).text())
        Combo6_3 = float(self.Load_Combination_Table_Widget.item(2,5).text())
        Combo6_4 = float(self.Load_Combination_Table_Widget.item(3,5).text())
        Combo6_5 = float(self.Load_Combination_Table_Widget.item(4,5).text())
        Combo6_6 = float(self.Load_Combination_Table_Widget.item(5,5).text())
        Combo6_7 = float(self.Load_Combination_Table_Widget.item(6,5).text())
        Combo6_8 = float(self.Load_Combination_Table_Widget.item(7,5).text())
        Combo6_9 = float(self.Load_Combination_Table_Widget.item(8,5).text())
        Combo6_10 = float(self.Load_Combination_Table_Widget.item(9,5).text())
        
        # Load Combo 7
        Combo7_1 = float(self.Load_Combination_Table_Widget.item(0,6).text())
        Combo7_2 = float(self.Load_Combination_Table_Widget.item(1,6).text())
        Combo7_3 = float(self.Load_Combination_Table_Widget.item(2,6).text())
        Combo7_4 = float(self.Load_Combination_Table_Widget.item(3,6).text())
        Combo7_5 = float(self.Load_Combination_Table_Widget.item(4,6).text())
        Combo7_6 = float(self.Load_Combination_Table_Widget.item(5,6).text())
        Combo7_7 = float(self.Load_Combination_Table_Widget.item(6,6).text())
        Combo7_8 = float(self.Load_Combination_Table_Widget.item(7,6).text())
        Combo7_9 = float(self.Load_Combination_Table_Widget.item(8,6).text())
        Combo7_10 = float(self.Load_Combination_Table_Widget.item(9,6).text())
        
        # Load Combo 8
        Combo8_1 = float(self.Load_Combination_Table_Widget.item(0,7).text())
        Combo8_2 = float(self.Load_Combination_Table_Widget.item(1,7).text())
        Combo8_3 = float(self.Load_Combination_Table_Widget.item(2,7).text())
        Combo8_4 = float(self.Load_Combination_Table_Widget.item(3,7).text())
        Combo8_5 = float(self.Load_Combination_Table_Widget.item(4,7).text())
        Combo8_6 = float(self.Load_Combination_Table_Widget.item(5,7).text())
        Combo8_7 = float(self.Load_Combination_Table_Widget.item(6,7).text())
        Combo8_8 = float(self.Load_Combination_Table_Widget.item(7,7).text())
        Combo8_9 = float(self.Load_Combination_Table_Widget.item(8,7).text())
        Combo8_10 = float(self.Load_Combination_Table_Widget.item(9,7).text())
        
        # Load Combo 9
        Combo9_1 = float(self.Load_Combination_Table_Widget.item(0,8).text())
        Combo9_2 = float(self.Load_Combination_Table_Widget.item(1,8).text())
        Combo9_3 = float(self.Load_Combination_Table_Widget.item(2,8).text())
        Combo9_4 = float(self.Load_Combination_Table_Widget.item(3,8).text())
        Combo9_5 = float(self.Load_Combination_Table_Widget.item(4,8).text())
        Combo9_6 = float(self.Load_Combination_Table_Widget.item(5,8).text())
        Combo9_7 = float(self.Load_Combination_Table_Widget.item(6,8).text())
        Combo9_8 = float(self.Load_Combination_Table_Widget.item(7,8).text())
        Combo9_9 = float(self.Load_Combination_Table_Widget.item(8,8).text())
        Combo9_10 = float(self.Load_Combination_Table_Widget.item(9,8).text())
        
        # Load Combo 10
        Combo10_1 = float(self.Load_Combination_Table_Widget.item(0,9).text())
        Combo10_2 = float(self.Load_Combination_Table_Widget.item(1,9).text())
        Combo10_3 = float(self.Load_Combination_Table_Widget.item(2,9).text())
        Combo10_4 = float(self.Load_Combination_Table_Widget.item(3,9).text())
        Combo10_5 = float(self.Load_Combination_Table_Widget.item(4,9).text())
        Combo10_6 = float(self.Load_Combination_Table_Widget.item(5,9).text())
        Combo10_7 = float(self.Load_Combination_Table_Widget.item(6,9).text())
        Combo10_8 = float(self.Load_Combination_Table_Widget.item(7,9).text())
        Combo10_9 = float(self.Load_Combination_Table_Widget.item(8,9).text())
        Combo10_10 = float(self.Load_Combination_Table_Widget.item(9,9).text())
        
        # Convert forces load cases dictionaries to pandas dataframe
        forces_LC1_df = pd.DataFrame.from_dict(self.forces_LC1, orient='index', columns=['F_x','F_y'])
        forces_LC2_df = pd.DataFrame.from_dict(self.forces_LC2, orient='index', columns=['F_x','F_y'])
        forces_LC3_df = pd.DataFrame.from_dict(self.forces_LC3, orient='index', columns=['F_x','F_y'])
        forces_LC4_df = pd.DataFrame.from_dict(self.forces_LC4, orient='index', columns=['F_x','F_y'])
        forces_LC5_df = pd.DataFrame.from_dict(self.forces_LC5, orient='index', columns=['F_x','F_y'])
        forces_LC6_df = pd.DataFrame.from_dict(self.forces_LC6, orient='index', columns=['F_x','F_y'])
        forces_LC7_df = pd.DataFrame.from_dict(self.forces_LC7, orient='index', columns=['F_x','F_y'])
        forces_LC8_df = pd.DataFrame.from_dict(self.forces_LC8, orient='index', columns=['F_x','F_y'])
        forces_LC9_df = pd.DataFrame.from_dict(self.forces_LC9, orient='index', columns=['F_x','F_y'])
        forces_LC10_df = pd.DataFrame.from_dict(self.forces_LC10, orient='index', columns=['F_x','F_y'])
        
        # if forces_LC1_df.empty:
        #     forces_LC1_df = 0
        # if forces_LC2_df.empty:
        #     forces_LC2_df = 0
        # if forces_LC3_df.empty:
        #     forces_LC3_df = 0
        # if forces_LC4_df.empty:
        #     forces_LC4_df = 0
        # if forces_LC5_df.empty:
        #     forces_LC5_df = 0
        # if forces_LC6_df.empty:
        #     forces_LC6_df = 0
        # if forces_LC7_df.empty:
        #     forces_LC7_df = 0
        # if forces_LC8_df.empty:
        #     forces_LC8_df = 0
        # if forces_LC9_df.empty:
        #     forces_LC9_df = 0
        # if forces_LC10_df.empty:
        #     forces_LC10_df = 0
            
        force_Combo = [forces_LC1_df, forces_LC2_df, forces_LC3_df, forces_LC4_df, forces_LC5_df, forces_LC6_df, forces_LC7_df, forces_LC8_df, forces_LC9_df, forces_LC10_df]
        
        # Apply factors to Load Combinations
        # Load Combo 1
        Combo1 = [Combo1_1, Combo1_2, Combo1_3, Combo1_4, Combo1_5, Combo1_6, Combo1_7, Combo1_8, Combo1_9, Combo1_10]
        
        forces_Combo1 = pd.DataFrame()
        forces_Combo1_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo1[i] == 0:
                    pass
                else:
                    forces_Combo1 = Combo1[i] * j
                    forces_Combo1_prev = forces_Combo1
            elif Combo1[i] == 0:
                pass
            else:     
                if Combo1[i] == 0:
                    pass
                else:               
                    forces_Combo1 = forces_Combo1 + Combo1[i] * j
                    forces_Combo1 = forces_Combo1.fillna(forces_Combo1_prev)
                    forces_Combo1 = forces_Combo1.fillna(Combo1[i] * j)
                    forces_Combo1_prev = forces_Combo1
                
        forces_Combo1 = forces_Combo1.round(3)
                
        # Load Combo 1
        Combo2 = [Combo2_1, Combo2_2, Combo2_3, Combo2_4, Combo2_5, Combo2_6, Combo2_7, Combo2_8, Combo2_9, Combo2_10]
        
        forces_Combo2 = pd.DataFrame()
        forces_Combo2_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo2[i] == 0:
                    pass
                else:
                    forces_Combo2 = Combo2[i] * j
                    forces_Combo2_prev = forces_Combo2
            elif Combo2[i] == 0:
                pass
            else:     
                if Combo2[i] == 0:
                    pass
                else:               
                    forces_Combo2 = forces_Combo2 + Combo2[i] * j
                    forces_Combo2 = forces_Combo2.fillna(forces_Combo2_prev)
                    forces_Combo2 = forces_Combo2.fillna(Combo2[i] * j)
                    forces_Combo2_prev = forces_Combo2
                
        forces_Combo2 = forces_Combo2.round(3)

        # Load Combo 3
        Combo3 = [Combo3_1, Combo3_2, Combo3_3, Combo3_4, Combo3_5, Combo3_6, Combo3_7, Combo3_8, Combo3_9, Combo3_10]
        
        forces_Combo3 = pd.DataFrame()
        forces_Combo3_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo3[i] == 0:
                    pass
                else:
                    forces_Combo3 = Combo3[i] * j
                    forces_Combo3_prev = forces_Combo3
            elif Combo3[i] == 0:
                pass
            else:                    
                forces_Combo3 = forces_Combo3 + Combo3[i] * j
                forces_Combo3 = forces_Combo3.fillna(forces_Combo3_prev)
                forces_Combo3 = forces_Combo3.fillna(Combo3[i] * j)
                forces_Combo3_prev = forces_Combo3

        forces_Combo3 = forces_Combo3.round(3)

        # Load Combo 4
        Combo4 = [Combo4_1, Combo4_2, Combo4_3, Combo4_4, Combo4_5, Combo4_6, Combo4_7, Combo4_8, Combo4_9, Combo4_10]
        
        forces_Combo4 = pd.DataFrame()
        forces_Combo4_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo4[i] == 0:
                    pass
                else:
                    forces_Combo4 = Combo4[i] * j
                    forces_Combo4_prev = forces_Combo4
            elif Combo4[i] == 0:
                pass
            else:                    
                forces_Combo4 = forces_Combo4 + Combo4[i] * j
                forces_Combo4 = forces_Combo4.fillna(forces_Combo4_prev)
                forces_Combo4 = forces_Combo4.fillna(Combo4[i] * j)
                forces_Combo4_prev = forces_Combo4

        forces_Combo4 = forces_Combo4.round(3)

        # Load Combo 5
        Combo5 = [Combo5_1, Combo5_2, Combo5_3, Combo5_4, Combo5_5, Combo5_6, Combo5_7, Combo5_8, Combo5_9, Combo5_10]
        
        forces_Combo5 = pd.DataFrame()
        forces_Combo5_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo5[i] == 0:
                    pass
                else:
                    forces_Combo5 = Combo5[i] * j
                    forces_Combo5_prev = forces_Combo5
            elif Combo5[i] == 0:
                pass
            else:                    
                forces_Combo5 = forces_Combo5 + Combo5[i] * j
                forces_Combo5 = forces_Combo5.fillna(forces_Combo5_prev)
                forces_Combo5 = forces_Combo5.fillna(Combo5[i] * j)
                forces_Combo5_prev = forces_Combo5

        forces_Combo5 = forces_Combo5.round(3)

        # Load Combo 6
        Combo6 = [Combo6_1, Combo6_2, Combo6_3, Combo6_4, Combo6_5, Combo6_6, Combo6_7, Combo6_8, Combo6_9, Combo6_10]
        
        forces_Combo6 = pd.DataFrame()
        forces_Combo6_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo6[i] == 0:
                    pass
                else:
                    forces_Combo6 = Combo6[i] * j
                    forces_Combo6_prev = forces_Combo6
            elif Combo6[i] == 0:
                pass
            else:                    
                forces_Combo6 = forces_Combo6 + Combo6[i] * j
                forces_Combo6 = forces_Combo6.fillna(forces_Combo6_prev)
                forces_Combo6 = forces_Combo6.fillna(Combo6[i] * j)
                forces_Combo6_prev = forces_Combo6

        forces_Combo6 = forces_Combo6.round(3)

        # Load Combo 7
        Combo7 = [Combo7_1, Combo7_2, Combo7_3, Combo7_4, Combo7_5, Combo7_6, Combo7_7, Combo7_8, Combo7_9, Combo7_10]
        
        forces_Combo7 = pd.DataFrame()
        forces_Combo7_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo7[i] == 0:
                    pass
                else:
                    forces_Combo7 = Combo7[i] * j
                    forces_Combo7_prev = forces_Combo7
            elif Combo7[i] == 0:
                pass
            else:                    
                forces_Combo7 = forces_Combo7 + Combo7[i] * j
                forces_Combo7 = forces_Combo7.fillna(forces_Combo7_prev)
                forces_Combo7 = forces_Combo7.fillna(Combo7[i] * j)
                forces_Combo7_prev = forces_Combo7

        forces_Combo7 = forces_Combo7.round(3)

        # Load Combo 8
        Combo8 = [Combo8_1, Combo8_2, Combo8_3, Combo8_4, Combo8_5, Combo8_6, Combo8_7, Combo8_8, Combo8_9, Combo8_10]
        
        forces_Combo8 = pd.DataFrame()
        forces_Combo8_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo8[i] == 0:
                    pass
                else:
                    forces_Combo8 = Combo8[i] * j
                    forces_Combo8_prev = forces_Combo8
            elif Combo8[i] == 0:
                pass
            else:                    
                forces_Combo8 = forces_Combo8 + Combo8[i] * j
                forces_Combo8 = forces_Combo8.fillna(forces_Combo8_prev)
                forces_Combo8 = forces_Combo8.fillna(Combo8[i] * j)
                forces_Combo8_prev = forces_Combo8
                
        forces_Combo8 = forces_Combo8.round(3)

        # Load Combo 9
        Combo9 = [Combo9_1, Combo9_2, Combo9_3, Combo9_4, Combo9_5, Combo9_6, Combo9_7, Combo9_8, Combo9_9, Combo9_10]
        
        forces_Combo9 = pd.DataFrame()
        forces_Combo9_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo9[i] == 0:
                    pass
                else:
                    forces_Combo9 = Combo9[i] * j
                    forces_Combo9_prev = forces_Combo9
            elif Combo9[i] == 0:
                pass
            else:                    
                forces_Combo9 = forces_Combo9 + Combo9[i] * j
                forces_Combo9 = forces_Combo9.fillna(forces_Combo9_prev)
                forces_Combo9 = forces_Combo9.fillna(Combo9[i] * j)
                forces_Combo9_prev = forces_Combo9

        forces_Combo9 = forces_Combo9.round(3)
                
        # Load Combo 10
        Combo10 = [Combo10_1, Combo10_2, Combo10_3, Combo10_4, Combo10_5, Combo10_6, Combo10_7, Combo10_8, Combo10_9, Combo10_10]
        
        forces_Combo10 = pd.DataFrame()
        forces_Combo10_prev = pd.DataFrame()
        
        for i, j in enumerate(force_Combo):
            if i == 0:
                if Combo10[i] == 0:
                    pass
                else:
                    forces_Combo10 = Combo10[i] * j
                    forces_Combo10_prev = forces_Combo10
            elif Combo10[i] == 0:
                pass
            else:                    
                forces_Combo10 = forces_Combo10 + Combo10[i] * j
                forces_Combo10 = forces_Combo10.fillna(forces_Combo10_prev)
                forces_Combo10 = forces_Combo10.fillna(Combo10[i] * j)
                forces_Combo10_prev = forces_Combo10
                
        forces_Combo10 = forces_Combo10.round(3)
        
        # Convert Load Combos back to Dictionary
        self.forces_Combo1 = {}
        
        for i, row in forces_Combo1.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo1.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})

        self.forces_Combo2 = {}
        
        for i, row in forces_Combo2.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo2.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})

        self.forces_Combo3 = {}
        
        for i, row in forces_Combo3.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo3.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})

        self.forces_Combo4 = {}
        
        for i, row in forces_Combo4.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo4.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})

        self.forces_Combo5 = {}
        
        for i, row in forces_Combo5.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo5.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})

        self.forces_Combo6 = {}
        
        for i, row in forces_Combo6.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo6.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})
        
        self.forces_Combo7 = {}
        
        for i, row in forces_Combo7.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo7.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})

        self.forces_Combo8 = {}
        
        for i, row in forces_Combo8.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo8.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})

        self.forces_Combo9 = {}
        
        for i, row in forces_Combo9.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo9.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})
        self.forces_Combo10 = {}
        
        for i, row in forces_Combo10.iterrows():
            node = int(i)
            f_x = row['F_x']
            f_y = row['F_y']
            print(node, f_x, f_y)
            self.forces_Combo10.update({node: [np.round(float(f_x),3), np.round(float(f_y),3)]})
        
        
        # Solve Trusses
        self.Truss_LC1 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo1)
        self.Truss_LC1.Solve()
        
        self.Truss_LC2 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo2)
        self.Truss_LC2.Solve()
        
        self.Truss_LC3 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo3)
        self.Truss_LC3.Solve()
        
        self.Truss_LC4 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo4)
        self.Truss_LC4.Solve()
        
        self.Truss_LC5 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo5)
        self.Truss_LC5.Solve()
        
        self.Truss_LC6 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo6)
        self.Truss_LC6.Solve()
        
        self.Truss_LC7 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo7)
        self.Truss_LC7.Solve()
        
        self.Truss_LC8 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo8)
        self.Truss_LC8.Solve()
        
        self.Truss_LC9 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo9)
        self.Truss_LC9.Solve()
        
        self.Truss_LC10 = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo10)
        self.Truss_LC10.Solve()

        # Save Results
        # Load Combination 1
        self.df_displacements_LC1 = pd.DataFrame.from_dict(self.Truss_LC1.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC1 = pd.DataFrame.from_dict(self.Truss_LC1.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC1 = pd.DataFrame.from_dict(self.Truss_LC1.reactions_, orient='index', columns=['F_x','F_y'])

        # Load Combination 2
        self.df_displacements_LC2 = pd.DataFrame.from_dict(self.Truss_LC2.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC2 = pd.DataFrame.from_dict(self.Truss_LC2.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC2 = pd.DataFrame.from_dict(self.Truss_LC2.reactions_, orient='index', columns=['F_x','F_y'])

        # Load Combination 3
        self.df_displacements_LC3 = pd.DataFrame.from_dict(self.Truss_LC3.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC3 = pd.DataFrame.from_dict(self.Truss_LC3.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC3 = pd.DataFrame.from_dict(self.Truss_LC3.reactions_, orient='index', columns=['F_x','F_y'])
            
        # Load Combination 4
        self.df_displacements_LC4 = pd.DataFrame.from_dict(self.Truss_LC4.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC4 = pd.DataFrame.from_dict(self.Truss_LC4.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC4 = pd.DataFrame.from_dict(self.Truss_LC4.reactions_, orient='index', columns=['F_x','F_y'])

        # Load Combination 5
        self.df_displacements_LC5 = pd.DataFrame.from_dict(self.Truss_LC5.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC5 = pd.DataFrame.from_dict(self.Truss_LC5.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC5 = pd.DataFrame.from_dict(self.Truss_LC5.reactions_, orient='index', columns=['F_x','F_y'])

        # Load Combination 6
        self.df_displacements_LC6 = pd.DataFrame.from_dict(self.Truss_LC6.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC6 = pd.DataFrame.from_dict(self.Truss_LC6.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC6 = pd.DataFrame.from_dict(self.Truss_LC6.reactions_, orient='index', columns=['F_x','F_y'])

        # Load Combination 7
        self.df_displacements_LC7 = pd.DataFrame.from_dict(self.Truss_LC7.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC7 = pd.DataFrame.from_dict(self.Truss_LC7.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC7 = pd.DataFrame.from_dict(self.Truss_LC7.reactions_, orient='index', columns=['F_x','F_y'])

        # Load Combination 8
        self.df_displacements_LC8 = pd.DataFrame.from_dict(self.Truss_LC8.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC8 = pd.DataFrame.from_dict(self.Truss_LC8.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC8 = pd.DataFrame.from_dict(self.Truss_LC8.reactions_, orient='index', columns=['F_x','F_y'])

        # Load Combination 9
        self.df_displacements_LC9 = pd.DataFrame.from_dict(self.Truss_LC9.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC9 = pd.DataFrame.from_dict(self.Truss_LC9.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC9 = pd.DataFrame.from_dict(self.Truss_LC9.reactions_, orient='index', columns=['F_x','F_y'])

        # Load Combination 10
        self.df_displacements_LC10 = pd.DataFrame.from_dict(self.Truss_LC10.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces_LC10 = pd.DataFrame.from_dict(self.Truss_LC10.member_forces_, orient='index', columns=['Force'])
        self.df_reactions_LC10 = pd.DataFrame.from_dict(self.Truss_LC10.reactions_, orient='index', columns=['F_x','F_y'])
        
        self.df_member_lengths = pd.DataFrame.from_dict(self.Truss_LC1.member_lengths_, orient='index', columns=['Length'])

        with pd.ExcelWriter(file_name[0].split(".xlsx")[0] + "_Solved.xlsx") as writer:
            self.df_member_lengths.to_excel(writer, sheet_name='Member_Lengths')
            
            self.df_reactions_LC1.to_excel(writer, sheet_name='Reactions_LC1')
            self.df_displacements_LC1.to_excel(writer, sheet_name='Displacements_LC1')
            self.df_member_forces_LC1.to_excel(writer, sheet_name='Member Forces_LC1')
            
            self.df_reactions_LC2.to_excel(writer, sheet_name='Reactions_LC2')
            self.df_displacements_LC2.to_excel(writer, sheet_name='Displacements_LC2')
            self.df_member_forces_LC2.to_excel(writer, sheet_name='Member Forces_LC2')
            
            self.df_reactions_LC3.to_excel(writer, sheet_name='Reactions_LC3')
            self.df_displacements_LC3.to_excel(writer, sheet_name='Displacements_LC3')
            self.df_member_forces_LC3.to_excel(writer, sheet_name='Member Forces_LC3')
            
            self.df_reactions_LC4.to_excel(writer, sheet_name='Reactions_LC4')
            self.df_displacements_LC4.to_excel(writer, sheet_name='Displacements_LC4')
            self.df_member_forces_LC4.to_excel(writer, sheet_name='Member Forces_LC4')
            
            self.df_reactions_LC5.to_excel(writer, sheet_name='Reactions_LC5')
            self.df_displacements_LC5.to_excel(writer, sheet_name='Displacements_LC5')
            self.df_member_forces_LC5.to_excel(writer, sheet_name='Member Forces_LC5')
            
            self.df_reactions_LC6.to_excel(writer, sheet_name='Reactions_LC6')
            self.df_displacements_LC6.to_excel(writer, sheet_name='Displacements_LC6')
            self.df_member_forces_LC6.to_excel(writer, sheet_name='Member Forces_LC6')
            
            self.df_reactions_LC7.to_excel(writer, sheet_name='Reactions_LC7')
            self.df_displacements_LC7.to_excel(writer, sheet_name='Displacements_LC7')
            self.df_member_forces_LC7.to_excel(writer, sheet_name='Member Forces_LC7')
            
            self.df_reactions_LC8.to_excel(writer, sheet_name='Reactions_LC8')
            self.df_displacements_LC8.to_excel(writer, sheet_name='Displacements_LC8')
            self.df_member_forces_LC8.to_excel(writer, sheet_name='Member Forces_LC8')
            
            self.df_reactions_LC9.to_excel(writer, sheet_name='Reactions_LC9')
            self.df_displacements_LC9.to_excel(writer, sheet_name='Displacements_LC9')
            self.df_member_forces_LC9.to_excel(writer, sheet_name='Member Forces_LC9')
            
            self.df_reactions_LC10.to_excel(writer, sheet_name='Reactions_LC10')
            self.df_displacements_LC10.to_excel(writer, sheet_name='Displacements_LC10')
            self.df_member_forces_LC10.to_excel(writer, sheet_name='Member Forces_LC10')
            


        self.Reactions_Button.setEnabled(True)
        self.Displacement_Button.setEnabled(True)
        self.Axial_Force_Button.setEnabled(True)
        self.Load_Combination_Combo_Box.setEnabled(True)

        # save_file_name = file_name[0].split('xlsx')[0]
        # plt.savefig(save_file_name+'setup.png', dpi=300)

        # Update plot to Show Reactions
        plt.clf()
        # self.Post_Processing_Table.setRowCount(0)
        self.Draw_Truss_Reactions()
        self.canvas.draw()

        print("Truss Solved")
        self.statusBar.showMessage("Truss Solved")

    def Draw_Truss_Axial_Force_Map(self):
        plt.clf()
        self.Draw_Axial()
        self.canvas.draw()

        self.Post_Processing_Table.setColumnCount(3)
        self.Post_Processing_Table.setHorizontalHeaderLabels(['BAR', 'FORCE', 'LENGTH'])
        self.Post_Processing_Table.setRowCount(0)

        global file_name

        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC1')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC2')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC3')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC4')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC5')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC6')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC7')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC8')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC9')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass
            
        else:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces_LC10')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    bar = str(row[0])
                    force = str(row['Force'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(bar))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(force))
            except:
                pass
            
        # Member Lengths
        member_lengths_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member_Lengths')
        for index, row in member_lengths_sheet.iterrows():
            self.Post_Processing_Table.setItem(index, 2, QTableWidgetItem(str(row['Length'])))

    def Draw_Truss_Displacement(self):
        plt.clf()
        self.Draw_Displacements()
        self.canvas.draw()

        self.Post_Processing_Table.setColumnCount(3)
        self.Post_Processing_Table.setHorizontalHeaderLabels(['NODE', 'X', 'Y'])
        self.Post_Processing_Table.setRowCount(0)

        global file_name

        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC1')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC2')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC3')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC4')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC5')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC6')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC7')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC8')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC9')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 9:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements_LC10')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    X = str(row['X'])
                    Y = str(row['Y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(X))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(Y))
            except:
                pass

    def Draw_Truss_Reactions(self):
        plt.clf()
        self.Draw_Reactions()
        self.canvas.draw()

        self.Post_Processing_Table.setColumnCount(3)
        self.Post_Processing_Table.setHorizontalHeaderLabels(['NODE', 'FORCE X-DIR', 'FORCE Y-DIR'])
        self.Post_Processing_Table.setRowCount(0)

        global file_name

        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC1')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC2')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC3')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC4')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC5')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC6')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC7')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass

        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC8')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC9')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass
            
        elif self.Load_Combination_Combo_Box.currentIndex() == 9:
            try:
                reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions_LC10')

                # Reactions
                for index, row in reaction_sheet.iterrows():
                    node = str(row[0])
                    F_x = str(row['F_x'])
                    F_y = str(row['F_y'])

                    # Add Items to Table Widget
                    rowPosition = self.Post_Processing_Table.rowCount()

                    # print(rowPosition)
                    self.Post_Processing_Table.insertRow(rowPosition)
                    self.Post_Processing_Table.setItem(rowPosition, 0, QTableWidgetItem(node))
                    self.Post_Processing_Table.setItem(rowPosition, 1, QTableWidgetItem(F_x))
                    self.Post_Processing_Table.setItem(rowPosition, 2, QTableWidgetItem(F_y))
            except:
                pass

    def Draw_Setup_Load_Case(self):
        # self.Initialize_Plotting()
        # Update all dictionaries from tables
        self.Renumber_Nodes_Func()
        self.Renumber_Bars_Func()
        
        self.nodes = {}
        self.elements = {}
        self.areas = {}
        self.forces = {}
        self.supports = {}

        for index in range(self.Nodes_Table_Widget.rowCount()):
            node = int(self.Nodes_Table_Widget.item(index,0).text())
            x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
            y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
            self.nodes.update({node: [x_coord,y_coord]})

        # Elements
        for index in range(self.Element_Table_Widget.rowCount()):
            bar = int(self.Element_Table_Widget.item(index,0).text())
            node_1 = int(self.Element_Table_Widget.item(index,1).text())
            node_2 = int(self.Element_Table_Widget.item(index,2).text())
            self.elements.update({bar:[node_1, node_2]})

        # Materials
        for index in range(self.Material_Table_Widget.rowCount()):
            bar = int(self.Material_Table_Widget.item(index,0).text())
            area = float(self.Material_Table_Widget.item(index,1).text())
            elasticity = float(self.Material_Table_Widget.item(index,2).text())
            self.areas.update({bar: area})
            self.elasticity.update({bar: elasticity})
            
        # Forces

        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC1.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC1)
            # self.Load_Case_ComboBox.setCurrentIndex(0)
        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC2.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC2)
            # self.Load_Case_ComboBox.setCurrentIndex(1)
        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC3.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC3)
            # self.Load_Case_ComboBox.setCurrentIndex(2)
        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC4.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC4)
            # self.Load_Case_ComboBox.setCurrentIndex(3)
        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC5.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC5)
            # self.Load_Case_ComboBox.setCurrentIndex(4)
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC6.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC6)
            # self.Load_Case_ComboBox.setCurrentIndex(5)
        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC7.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC7)
            # self.Load_Case_ComboBox.setCurrentIndex(6)
        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC8.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC8)
            # self.Load_Case_ComboBox.setCurrentIndex(7)
        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC9.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC9)
            # self.Load_Case_ComboBox.setCurrentIndex(8)
        else:
            for index in range(self.Force_Table_Widget.rowCount()):
                node = int(self.Force_Table_Widget.item(index,0).text())
                f_x = float(self.Force_Table_Widget.item(index,1).text())
                f_y = float(self.Force_Table_Widget.item(index,2).text())
                self.forces_LC10.update({node: [f_x, f_y]})
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_LC10)
            # self.Load_Case_ComboBox.setCurrentIndex(9)
            


        # Supports
        for index in range(self.Support_Table_Widget.rowCount()):
            node = int(self.Support_Table_Widget.item(index,0).text())
            x = int(self.Support_Table_Widget.item(index,1).text())
            y = int(self.Support_Table_Widget.item(index,2).text())
            self.supports.update({node: [x, y]})

        # Update plot
        plt.clf()
        
        linewidth = float(self.Line_Width_LEdit.text())
        offset = float(self.Label_Offset_LEdit.text())
        length_of_arrow = float(self.Arrow_Length_LEdit.text())
        width_of_arrow = float(self.Arrow_Head_Size_LEdit.text())
        arrow_line_width = float(self.Arrow_Line_Width_LEdit.text())

        plt.rcParams.update({'font.size': float(self.Font_Size_LEdit.text())})
        self.Truss_Setup.Draw_Truss_Setup(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, width_of_arrow = width_of_arrow, arrow_line_width = arrow_line_width)
        
        
        self.canvas.draw()
        self.figure.tight_layout()

    # def Initialize_Truss_Components(self):
    #     nodes_sheet = pd.read_excel(file_name[0], sheet_name='Nodes')
    #     elements_sheet = pd.read_excel(file_name[0], sheet_name='Elements')
    #     materials_sheet = pd.read_excel(file_name[0], sheet_name='Materials')
    #     forces_sheet = pd.read_excel(file_name[0], sheet_name='Forces')
    #     supports_sheet = pd.read_excel(file_name[0], sheet_name='Supports')

    #     self.nodes = {}
    #     for i in range(len(nodes_sheet)):
    #         self.nodes.update({nodes_sheet['Node'][i]: [nodes_sheet['x_coord'][i], nodes_sheet['y_coord'][i]]})

    #     self.elements = {}
    #     for i in range(len(elements_sheet)):
    #         self.elements.update({elements_sheet['Element'][i]: [elements_sheet['Node_1'][i], elements_sheet['Node_2'][i]]})

    #     self.areas = {}
    #     for i in range(len(materials_sheet)):
    #         self.areas.update({materials_sheet['Element'][i]: materials_sheet['Area'][i]})

    #     self.elasticity = {}
    #     for i in range(len(materials_sheet)):
    #         self.elasticity.update({materials_sheet['Element'][i]: materials_sheet['Elasticity'][i]})

    #     self.forces_LC1 = {}
    #     for i in range(len(forces_sheet)):
    #         self.forces_LC1.update({forces_sheet['Node'][i]: [forces_sheet['F_x'][i], forces_sheet['F_y'][i]]})

    #     self.supports = {}
    #     for i in range(len(supports_sheet)):
    #         self.supports.update({supports_sheet['Node'][i]: [supports_sheet['X'][i], supports_sheet['Y'][i]]})
    
    def Draw_Setup_Load_Combo(self):
        # self.Initialize_Plotting()
        # Update all dictionaries from tables
        self.Renumber_Nodes_Func()
        self.Renumber_Bars_Func()
        
        self.nodes = {}
        self.elements = {}
        self.areas = {}
        self.forces = {}
        self.supports = {}

        for index in range(self.Nodes_Table_Widget.rowCount()):
            node = int(self.Nodes_Table_Widget.item(index,0).text())
            x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
            y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
            self.nodes.update({node: [x_coord,y_coord]})

        # Elements
        for index in range(self.Element_Table_Widget.rowCount()):
            bar = int(self.Element_Table_Widget.item(index,0).text())
            node_1 = int(self.Element_Table_Widget.item(index,1).text())
            node_2 = int(self.Element_Table_Widget.item(index,2).text())
            self.elements.update({bar:[node_1, node_2]})

        # Materials
        for index in range(self.Material_Table_Widget.rowCount()):
            bar = int(self.Material_Table_Widget.item(index,0).text())
            area = float(self.Material_Table_Widget.item(index,1).text())
            elasticity = float(self.Material_Table_Widget.item(index,2).text())
            self.areas.update({bar: area})
            self.elasticity.update({bar: elasticity})
            
        # Forces

        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo1)

        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo2)

        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo3)

        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo4)

        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo5)

        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo6)

        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo7)

        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo8)

        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo9)

        else:
            self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces_Combo10)
            
        # Supports
        for index in range(self.Support_Table_Widget.rowCount()):
            node = int(self.Support_Table_Widget.item(index,0).text())
            x = int(self.Support_Table_Widget.item(index,1).text())
            y = int(self.Support_Table_Widget.item(index,2).text())
            self.supports.update({node: [x, y]})

        # Update plot
        plt.clf()
        
        linewidth = float(self.Line_Width_LEdit.text())
        offset = float(self.Label_Offset_LEdit.text())
        length_of_arrow = float(self.Arrow_Length_LEdit.text())
        width_of_arrow = float(self.Arrow_Head_Size_LEdit.text())
        arrow_line_width = float(self.Arrow_Line_Width_LEdit.text())

        plt.rcParams.update({'font.size': float(self.Font_Size_LEdit.text())})
        self.Truss_Setup.Draw_Truss_Setup(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, width_of_arrow = width_of_arrow, arrow_line_width = arrow_line_width)
        
        
        self.canvas.draw()
        self.figure.tight_layout()

    # def Initialize_Truss_Components(self):
    #     nodes_sheet = pd.read_excel(file_name[0], sheet_name='Nodes')
    #     elements_sheet = pd.read_excel(file_name[0], sheet_name='Elements')
    #     materials_sheet = pd.read_excel(file_name[0], sheet_name='Materials')
    #     forces_sheet = pd.read_excel(file_name[0], sheet_name='Forces')
    #     supports_sheet = pd.read_excel(file_name[0], sheet_name='Supports')

    #     self.nodes = {}
    #     for i in range(len(nodes_sheet)):
    #         self.nodes.update({nodes_sheet['Node'][i]: [nodes_sheet['x_coord'][i], nodes_sheet['y_coord'][i]]})

    #     self.elements = {}
    #     for i in range(len(elements_sheet)):
    #         self.elements.update({elements_sheet['Element'][i]: [elements_sheet['Node_1'][i], elements_sheet['Node_2'][i]]})

    #     self.areas = {}
    #     for i in range(len(materials_sheet)):
    #         self.areas.update({materials_sheet['Element'][i]: materials_sheet['Area'][i]})

    #     self.elasticity = {}
    #     for i in range(len(materials_sheet)):
    #         self.elasticity.update({materials_sheet['Element'][i]: materials_sheet['Elasticity'][i]})

    #     self.forces_LC1 = {}
    #     for i in range(len(forces_sheet)):
    #         self.forces_LC1.update({forces_sheet['Node'][i]: [forces_sheet['F_x'][i], forces_sheet['F_y'][i]]})

    #     self.supports = {}
    #     for i in range(len(supports_sheet)):
    #         self.supports.update({supports_sheet['Node'][i]: [supports_sheet['X'][i], supports_sheet['Y'][i]]})

    ##### Matplotlib Functions #####

    def Draw_Truss_Setup(self):
        plt.rcParams.update({'font.size': float(self.Font_Size_LEdit.text())})
        
        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            self.forces = self.forces_LC1
            # self.Load_Case_ComboBox.setCurrentIndex(0)
        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            self.forces = self.forces_LC2
            # self.Load_Case_ComboBox.setCurrentIndex(1)
        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            self.forces = self.forces_LC3
            # self.Load_Case_ComboBox.setCurrentIndex(2)
        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            self.forces = self.forces_LC4
            # self.Load_Case_ComboBox.setCurrentIndex(3)
        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            self.forces = self.forces_LC5
            # self.Load_Case_ComboBox.setCurrentIndex(4)
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            self.forces = self.forces_LC6
            # self.Load_Case_ComboBox.setCurrentIndex(5)
        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            self.forces = self.forces_LC7
            # self.Load_Case_ComboBox.setCurrentIndex(6)
        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            self.forces = self.forces_LC8
            # self.Load_Case_ComboBox.setCurrentIndex(7)
        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            self.forces = self.forces_LC9
            # self.Load_Case_ComboBox.setCurrentIndex(8)
        elif self.Load_Combination_Combo_Box.currentIndex() == 9:
            self.forces = self.forces_LC10
            # self.Load_Case_ComboBox.setCurrentIndex(9)

        self.Force_Table_Widget.setRowCount(0)
                    
        # Loop all the force dictionary and replace/update the table widget
        for key, item in self.forces.items():
            node = str(key)
            f_x = str(item[0])
            f_y = str(item[1])

            # Add Items to Table Widget
            rowPosition = self.Force_Table_Widget.rowCount()

            # print(rowPosition)
            self.Force_Table_Widget.insertRow(rowPosition)
            self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
            self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
            self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
        
        # Draw Truss
        self.Draw_Setup_Load_Case()

    def Draw_Reactions(self):
        plt.rcParams.update({'font.size': float(self.Font_Size_LEdit.text())})
        linewidth = float(self.Line_Width_LEdit.text())
        offset = float(self.Label_Offset_LEdit.text())
        length_of_arrow = float(self.Arrow_Length_LEdit.text())
        width_of_arrow = float(self.Arrow_Head_Size_LEdit.text())
        arrow_line_width = float(self.Arrow_Line_Width_LEdit.text())
        
        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            self.Truss_LC1.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC1
            self.Load_Case_ComboBox.setCurrentIndex(0)
        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            self.Truss_LC2.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC2
            self.Load_Case_ComboBox.setCurrentIndex(1)
        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            self.Truss_LC3.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC3
            self.Load_Case_ComboBox.setCurrentIndex(2)
        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            self.Truss_LC4.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC4
            self.Load_Case_ComboBox.setCurrentIndex(3)
        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            self.Truss_LC5.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC5
            self.Load_Case_ComboBox.setCurrentIndex(4)
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            self.Truss_LC6.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC6
            self.Load_Case_ComboBox.setCurrentIndex(5)
        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            self.Truss_LC7.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC7
            self.Load_Case_ComboBox.setCurrentIndex(6)
        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            self.Truss_LC8.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.df_member_forces_LC8
            self.Load_Case_ComboBox.setCurrentIndex(7)
        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            self.Truss_LC9.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC9
            self.Load_Case_ComboBox.setCurrentIndex(8)
        else:
            self.Truss_LC10.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)
            self.forces = self.forces_LC10
            self.Load_Case_ComboBox.setCurrentIndex(9)
            
        self.Force_Table_Widget.setRowCount(0)
                    
        # Loop all the force dictionary and replace/update the table widget
        for key, item in self.forces.items():
            node = str(key)
            f_x = str(item[0])
            f_y = str(item[1])

            # Add Items to Table Widget
            rowPosition = self.Force_Table_Widget.rowCount()

            # print(rowPosition)
            self.Force_Table_Widget.insertRow(rowPosition)
            self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
            self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
            self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))

    def Draw_Displacements(self):
        plt.rcParams.update({'font.size': float(self.Font_Size_LEdit.text())})
        linewidth = float(self.Line_Width_LEdit.text())
        offset = float(self.Label_Offset_LEdit.text())
        # length_of_arrow = float(self.Arrow_Length_LEdit.text())
        # width_of_arrow = float(self.Arrow_Head_Size_LEdit.text())
        # arrow_line_width = float(self.Arrow_Line_Width_LEdit.text())
        magnification_factor = float(self.Displacement_Factor_LEdit.text())

        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            self.Truss_LC1.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC1
            self.Load_Case_ComboBox.setCurrentIndex(0)
        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            self.Truss_LC2.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC2
            self.Load_Case_ComboBox.setCurrentIndex(1)
        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            self.Truss_LC3.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC3
            self.Load_Case_ComboBox.setCurrentIndex(2)
        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            self.Truss_LC4.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC4
            self.Load_Case_ComboBox.setCurrentIndex(3)
        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            self.Truss_LC5.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC5
            self.Load_Case_ComboBox.setCurrentIndex(4)
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            self.Truss_LC6.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC6
            self.Load_Case_ComboBox.setCurrentIndex(5)
        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            self.Truss_LC7.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC7
            self.Load_Case_ComboBox.setCurrentIndex(6)
        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            self.Truss_LC8.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC8
            self.Load_Case_ComboBox.setCurrentIndex(7)
        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            self.Truss_LC9.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC9
            self.Load_Case_ComboBox.setCurrentIndex(8)
        else:
            self.Truss_LC10.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
            self.forces = self.forces_LC10
            self.Load_Case_ComboBox.setCurrentIndex(9)
            
        self.Force_Table_Widget.setRowCount(0)
                    
        # Loop all the force dictionary and replace/update the table widget
        for key, item in self.forces.items():
            node = str(key)
            f_x = str(item[0])
            f_y = str(item[1])

            # Add Items to Table Widget
            rowPosition = self.Force_Table_Widget.rowCount()

            # print(rowPosition)
            self.Force_Table_Widget.insertRow(rowPosition)
            self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
            self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
            self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))

    def Draw_Axial(self):
        plt.rcParams.update({'font.size': float(self.Font_Size_LEdit.text())})
            
        if self.Load_Combination_Combo_Box.currentIndex() == 0:
            self.Truss_LC1.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC1
            self.Load_Case_ComboBox.setCurrentIndex(0)
        elif self.Load_Combination_Combo_Box.currentIndex() == 1:
            self.Truss_LC2.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC2
            self.Load_Case_ComboBox.setCurrentIndex(1)
        elif self.Load_Combination_Combo_Box.currentIndex() == 2:
            self.Truss_LC3.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC3
            self.Load_Case_ComboBox.setCurrentIndex(2)
        elif self.Load_Combination_Combo_Box.currentIndex() == 3:
            self.Truss_LC4.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC4
            self.Load_Case_ComboBox.setCurrentIndex(3)
        elif self.Load_Combination_Combo_Box.currentIndex() == 4:
            self.Truss_LC5.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC5
            self.Load_Case_ComboBox.setCurrentIndex(4)
        elif self.Load_Combination_Combo_Box.currentIndex() == 5:
            self.Truss_LC6.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC6
            self.Load_Case_ComboBox.setCurrentIndex(5)
        elif self.Load_Combination_Combo_Box.currentIndex() == 6:
            self.Truss_LC7.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC7
            self.Load_Case_ComboBox.setCurrentIndex(6)
        elif self.Load_Combination_Combo_Box.currentIndex() == 7:
            self.Truss_LC8.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC8
            self.Load_Case_ComboBox.setCurrentIndex(7)
        elif self.Load_Combination_Combo_Box.currentIndex() == 8:
            self.Truss_LC9.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC9
            self.Load_Case_ComboBox.setCurrentIndex(8)
        else:
            self.Truss_LC10.Draw_Truss_Axial_Force_Map(color_bar_orientation = 'horizontal')
            self.forces = self.forces_LC10
            self.Load_Case_ComboBox.setCurrentIndex(9)
            
        self.Force_Table_Widget.setRowCount(0)
                    
        # Loop all the force dictionary and replace/update the table widget
        for key, item in self.forces.items():
            node = str(key)
            f_x = str(item[0])
            f_y = str(item[1])

            # Add Items to Table Widget
            rowPosition = self.Force_Table_Widget.rowCount()

            # print(rowPosition)
            self.Force_Table_Widget.insertRow(rowPosition)
            self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
            self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
            self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))

    def New_File_Func(self):
        
        self.Nodes_Table_Widget.setRowCount(0)
        self.Element_Table_Widget.setRowCount(0)
        self.Material_Table_Widget.setRowCount(0)
        self.Force_Table_Widget.setRowCount(0)
        self.Support_Table_Widget.setRowCount(0)
        self.Post_Processing_Table.setRowCount(0)
        
        for i in range(10):
            self.Load_Case_Table_Widget.setItem(i, 0, QTableWidgetItem(""))
        
        plt.clf()
        self.canvas.draw()

        del(self.nodes)
        del(self.elements)
        del(self.supports)
        del(self.forces_LC1)
        del(self.forces_LC2)
        del(self.forces_LC3)
        del(self.forces_LC4)
        del(self.forces_LC5)
        del(self.forces_LC6)
        del(self.forces_LC7)
        del(self.forces_LC8)
        del(self.forces_LC9)
        del(self.forces_LC10)
        del(self.elasticity)
        # del(self.cross_area)
        del(self.areas)
        
        gc.collect()
        
        self.nodes = {}
        self.elements = {}
        self.supports = {}
        self.forces_LC1 = {}
        self.forces_LC2 = {}
        self.forces_LC3 = {}
        self.forces_LC4 = {}
        self.forces_LC5 = {}
        self.forces_LC6 = {}
        self.forces_LC7 = {}
        self.forces_LC8 = {}
        self.forces_LC9 = {}
        self.forces_LC10 = {}
        self.elasticity = {}
        # self.cross_area = {}
        self.areas = {}
        self.load_case_index = 0
        
        self.Node_Number_From_LEdit.setText("1")
        self.Bar_Number_From_LEdit.setText("1")

        self.statusBar.showMessage("New File")
        
        title = "PySEAD Truss 2D"
        self.setWindowTitle(title)
        
        self.Reactions_Button.setEnabled(False)
        self.Displacement_Button.setEnabled(False)
        self.Axial_Force_Button.setEnabled(False)
        self.Load_Combination_Combo_Box.setEnabled(False)

    ##### Menu Functions #####

    def Save_Func(self):
        nodes_dict = {}
        elements_dict = {}
        materials_dict = {}
        forces_LC1_dict = {}
        forces_LC2_dict = {}
        forces_LC3_dict = {}
        forces_LC4_dict = {}
        forces_LC5_dict = {}
        forces_LC6_dict = {}
        forces_LC7_dict = {}
        forces_LC8_dict = {}
        forces_LC9_dict = {}
        forces_LC10_dict = {}
        supports_dict = {}
        load_case_dict = {}
        load_combo_dict = {}

        # try:
        # Nodes    
        for index in range(self.Nodes_Table_Widget.rowCount()):
            node = int(self.Nodes_Table_Widget.item(index,0).text())
            x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
            y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
            nodes_dict.update({index+1:[int(node), float(x_coord), float(y_coord)]})
        nodes_df = pd.DataFrame.from_dict(nodes_dict, orient='index', columns=['Node','x_coord','y_coord'])

        # Elements
        for index in range(self.Element_Table_Widget.rowCount()):
            bar = int(self.Element_Table_Widget.item(index,0).text())
            node_1 = int(self.Element_Table_Widget.item(index,1).text())
            node_2 = int(self.Element_Table_Widget.item(index,2).text())
            elements_dict.update({index+1:[int(bar), int(node_1), int(node_2)]})
        elements_df = pd.DataFrame.from_dict(elements_dict, orient='index', columns=['Element','Node_1','Node_2'])

        # Materials
        for index in range(self.Material_Table_Widget.rowCount()):
            bar = int(self.Material_Table_Widget.item(index,0).text())
            area = float(self.Material_Table_Widget.item(index,1).text())
            elasticity = float(self.Material_Table_Widget.item(index,2).text())
            materials_dict.update({index+1:[int(bar), float(area), float(elasticity)]})
        materials_df = pd.DataFrame.from_dict(materials_dict, orient='index', columns=['Element','Area','Elasticity'])
        
        # Load Cases
        for index in range(self.Load_Case_Table_Widget.rowCount()):
            load_case_dict.update({index+1:str(self.Load_Case_Table_Widget.item(index,0).text())})
        load_cases_df = pd.DataFrame.from_dict(load_case_dict, orient='index', columns=['Load Case Name'])
        
        # Load Combinations TODO
        
        # Forces
        # Load Case 1
        index = 1
        for key, item in self.forces_LC1.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC1_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC1_df = pd.DataFrame.from_dict(forces_LC1_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 2
        index = 1
        for key, item in self.forces_LC2.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC2_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC2_df = pd.DataFrame.from_dict(forces_LC2_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 3
        index = 1
        for key, item in self.forces_LC3.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC3_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC3_df = pd.DataFrame.from_dict(forces_LC3_dict, orient='index', columns=['Node','F_x','F_y'])
    
        # Load Case 4
        index = 1
        for key, item in self.forces_LC4.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC4_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC4_df = pd.DataFrame.from_dict(forces_LC4_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 5
        index = 1
        for key, item in self.forces_LC5.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC5_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC5_df = pd.DataFrame.from_dict(forces_LC5_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 6
        index = 1
        for key, item in self.forces_LC6.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC6_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC6_df = pd.DataFrame.from_dict(forces_LC6_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 7
        index = 1
        for key, item in self.forces_LC7.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC7_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC7_df = pd.DataFrame.from_dict(forces_LC7_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 8
        index = 1
        for key, item in self.forces_LC8.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC8_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC8_df = pd.DataFrame.from_dict(forces_LC8_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 9
        index = 1
        for key, item in self.forces_LC9.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC9_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC9_df = pd.DataFrame.from_dict(forces_LC9_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 10
        index = 1
        for key, item in self.forces_LC10.items():
            node = key
            f_x = item[0]
            f_y = item[1]
            forces_LC10_dict.update({index:[int(node), float(f_x), float(f_y)]})
            index+=1
        forces_LC10_df = pd.DataFrame.from_dict(forces_LC10_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Supports
        for index in range(self.Support_Table_Widget.rowCount()):
            node = int(self.Support_Table_Widget.item(index,0).text())
            x = int(self.Support_Table_Widget.item(index,1).text())
            y = int(self.Support_Table_Widget.item(index,2).text())
            supports_dict.update({index+1:[int(node), float(x), float(y)]})
        supports_df = pd.DataFrame.from_dict(supports_dict, orient='index', columns=['Node','X','Y'])
        
        # Load Combinations
        for index in range(self.Load_Combination_Table_Widget.rowCount()):
            C1 = float(self.Load_Combination_Table_Widget.item(index,0).text())
            C2 = float(self.Load_Combination_Table_Widget.item(index,1).text())
            C3 = float(self.Load_Combination_Table_Widget.item(index,2).text())
            C4 = float(self.Load_Combination_Table_Widget.item(index,3).text())
            C5 = float(self.Load_Combination_Table_Widget.item(index,4).text())
            C6 = float(self.Load_Combination_Table_Widget.item(index,5).text())
            C7 = float(self.Load_Combination_Table_Widget.item(index,6).text())
            C8 = float(self.Load_Combination_Table_Widget.item(index,7).text())
            C9 = float(self.Load_Combination_Table_Widget.item(index,8).text())
            C10 = float(self.Load_Combination_Table_Widget.item(index,9).text())
            load_combo_dict.update({index+1:[float(C1), float(C2), float(C3), float(C4), float(C5), float(C6),float(C7), float(C8), float(C9), float(C10)]})
        load_combo_dict_df = pd.DataFrame.from_dict(load_combo_dict, orient='index', columns=['Combo1','Combo2','Combo3','Combo4','Combo5','Combo6','Combo7','Combo8','Combo9','Combo10'])
        
        with pd.ExcelWriter(file_name[0]) as writer:
            nodes_df.to_excel(writer, sheet_name='Nodes')
            elements_df.to_excel(writer, sheet_name='Elements')
            materials_df.to_excel(writer, sheet_name='Materials')
            supports_df.to_excel(writer, sheet_name='Supports')
            load_cases_df.to_excel(writer, sheet_name='Load_Cases')
            load_combo_dict_df.to_excel(writer, sheet_name='Load_Combo')
            forces_LC1_df.to_excel(writer, sheet_name='Forces_LC1')
            forces_LC2_df.to_excel(writer, sheet_name='Forces_LC2')
            forces_LC3_df.to_excel(writer, sheet_name='Forces_LC3')
            forces_LC4_df.to_excel(writer, sheet_name='Forces_LC4')
            forces_LC5_df.to_excel(writer, sheet_name='Forces_LC5')
            forces_LC6_df.to_excel(writer, sheet_name='Forces_LC6')
            forces_LC7_df.to_excel(writer, sheet_name='Forces_LC7')
            forces_LC8_df.to_excel(writer, sheet_name='Forces_LC8')
            forces_LC9_df.to_excel(writer, sheet_name='Forces_LC9')
            forces_LC10_df.to_excel(writer, sheet_name='Forces_LC10')
        
        print("Saved")
        # except:
        #     self.statusBar.showMessage("Save Dialog Canceled") 

    def Save_As_Func(self):
        global file_name
        # try:
        file_name = QFileDialog.getSaveFileName(self, "Save File", "", "Excel File (*.xlsx);; All Files (*)")
        if file_name != "":
            self.Solve_Truss_Button.setEnabled(True)

        self.Save_Func()
        
        title = "PySEAD Truss 2D - " + file_name[0]
        self.setWindowTitle(title)

        # except:
            # print("Canceled Dialogue")
            # self.Solve_Truss_Button.setEnabled(False)

    def Open_File(self, nodes_sheet, elements_sheet, materials_sheet, forces_LC1_sheet, supports_sheet, load_cases_sheet, load_combo_sheet):
        try:
            # Nodes
            for index, row in nodes_sheet.iterrows():
                node = str(round(row['Node']))
                x_coord = str(row['x_coord'])
                y_coord = str(row['y_coord'])

                # Add Items to Table Widget
                rowPosition = self.Nodes_Table_Widget.rowCount()

                # print(rowPosition)
                self.Nodes_Table_Widget.insertRow(rowPosition)
                self.Nodes_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
                self.Nodes_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(x_coord))
                self.Nodes_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(y_coord))
            
            # Elements
            for index, row in elements_sheet.iterrows():
                element = str(round(row['Element']))
                node_1 = str(round(row['Node_1']))
                node_2 = str(round(row['Node_2']))

                # Add Items to Table Widget
                rowPosition = self.Element_Table_Widget.rowCount()

                # print(rowPosition)
                self.Element_Table_Widget.insertRow(rowPosition)
                self.Element_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(element))
                self.Element_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(node_1))
                self.Element_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(node_2))

            # Materials
            for index, row in materials_sheet.iterrows():
                element = str(round(row['Element']))
                area = str(row['Area'])
                elasticity = str(row['Elasticity'])

                # Add Items to Table Widget
                rowPosition = self.Material_Table_Widget.rowCount()

                # print(rowPosition)
                self.Material_Table_Widget.insertRow(rowPosition)
                self.Material_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(element))
                self.Material_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(area))
                self.Material_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(elasticity))
                
            # Load Cases
            for index, row in load_cases_sheet.iterrows():
                load_case = str(row['Load Case Name'])
                self.Load_Case_Table_Widget.setItem(index, 0, QTableWidgetItem(str(load_case)))

            # Load Combo
            for index, row in load_combo_sheet.iterrows():
                C1 = str(row['Combo1'])
                C2 = str(row['Combo2'])
                C3 = str(row['Combo3'])
                C4 = str(row['Combo4'])
                C5 = str(row['Combo5'])
                C6 = str(row['Combo6'])
                C7 = str(row['Combo7'])
                C8 = str(row['Combo8'])
                C9 = str(row['Combo9'])
                C10 = str(row['Combo10'])

                self.Load_Combination_Table_Widget.setItem(index, 0, QTableWidgetItem(C1))
                self.Load_Combination_Table_Widget.setItem(index, 1, QTableWidgetItem(C2))
                self.Load_Combination_Table_Widget.setItem(index, 2, QTableWidgetItem(C3))
                self.Load_Combination_Table_Widget.setItem(index, 3, QTableWidgetItem(C4))
                self.Load_Combination_Table_Widget.setItem(index, 4, QTableWidgetItem(C5))
                self.Load_Combination_Table_Widget.setItem(index, 5, QTableWidgetItem(C6))
                self.Load_Combination_Table_Widget.setItem(index, 6, QTableWidgetItem(C7))
                self.Load_Combination_Table_Widget.setItem(index, 7, QTableWidgetItem(C8))
                self.Load_Combination_Table_Widget.setItem(index, 8, QTableWidgetItem(C9))
                self.Load_Combination_Table_Widget.setItem(index, 9, QTableWidgetItem(C10))

            # Forces
            # Add Load Case 1 in Table
            for index, row in forces_LC1_sheet.iterrows():
                node = str(round(row['Node']))
                f_x = str(row['F_x'])
                f_y = str(row['F_y'])

                # Add Items to Table Widget
                rowPosition = self.Force_Table_Widget.rowCount()

                # print(rowPosition)
                self.Force_Table_Widget.insertRow(rowPosition)
                self.Force_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
                self.Force_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(f_x))
                self.Force_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(f_y))
            
            # Supports
            for index, row in supports_sheet.iterrows():
                node = str(round(row['Node']))
                x_support = str(row['X'])
                y_support = str(row['Y'])

                # Add Items to Table Widget
                rowPosition = self.Support_Table_Widget.rowCount()

                # print(rowPosition)
                self.Support_Table_Widget.insertRow(rowPosition)
                self.Support_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
                self.Support_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(x_support))
                self.Support_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(y_support))  
            # print(file_name[1])
            
            self.Draw_Setup_Load_Case()
        except:
            self.statusBar.showMessage("Canceled Dialogue")

    def Open_File_Func(self):
        self.New_File_Func()
        global file_name
        file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Excel File (*.xlsx);; All Files (*)")
        # print(file_name[0].split("xlsx"))
        try:
            nodes_sheet = pd.read_excel(file_name[0], sheet_name='Nodes')
            elements_sheet = pd.read_excel(file_name[0], sheet_name='Elements')
            materials_sheet = pd.read_excel(file_name[0], sheet_name='Materials')
            supports_sheet = pd.read_excel(file_name[0], sheet_name='Supports')
            forces_LC1_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC1')
            forces_LC2_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC2')
            forces_LC3_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC3')
            forces_LC4_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC4')
            forces_LC5_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC5')
            forces_LC6_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC6')
            forces_LC7_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC7')
            forces_LC8_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC8')
            forces_LC9_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC9')
            forces_LC10_sheet = pd.read_excel(file_name[0], sheet_name='Forces_LC10')
            load_cases_sheet = pd.read_excel(file_name[0], sheet_name='Load_Cases')
            load_combo_sheet = pd.read_excel(file_name[0], sheet_name='Load_Combo')
            
            # Save Dataframes into Dictionaries
            for _, row in forces_LC1_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC1.update({int(node): [float(f_x), float(f_y)]})
            
            for _, row in forces_LC2_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC2.update({int(node): [float(f_x), float(f_y)]})
            
            for _, row in forces_LC3_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC3.update({int(node): [float(f_x), float(f_y)]}) 
                
            for _, row in forces_LC4_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC4.update({int(node): [float(f_x), float(f_y)]})               
                
            for _, row in forces_LC5_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC5.update({int(node): [float(f_x), float(f_y)]})     
                    
            for _, row in forces_LC6_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC6.update({int(node): [float(f_x), float(f_y)]})   
                
            for _, row in forces_LC7_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC7.update({int(node): [float(f_x), float(f_y)]})        
                
            for _, row in forces_LC8_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC8.update({int(node): [float(f_x), float(f_y)]})   
                
            for _, row in forces_LC9_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC9.update({int(node): [float(f_x), float(f_y)]})           

            for _, row in forces_LC10_sheet.iterrows():
                node = row['Node']
                f_x = row['F_x']
                f_y = row['F_y']
                self.forces_LC10.update({int(node): [float(f_x), float(f_y)]}) 
                
            self.Open_File(nodes_sheet, elements_sheet, materials_sheet, forces_LC1_sheet, supports_sheet, load_cases_sheet, load_combo_sheet)

            self.Solve_Truss_Button.setEnabled(True)

            self.Node_row_Position = self.Nodes_Table_Widget.rowCount()
            self.Bar_row_Position = self.Element_Table_Widget.rowCount()

            self.Node_Number_From_LEdit.setText(str(self.Node_row_Position + 1))
            self.Bar_Number_From_LEdit.setText(str(self.Bar_row_Position + 1))
            
            title = "PySEAD Truss 2D - " + file_name[0]
            self.setWindowTitle(title)
        except:
            self.statusBar.showMessage("Cancelled Dialog")

    def Save_Figure_Func(self):
        figure_name = QFileDialog.getSaveFileName(self, "Save Figure", "", ".PNG (*.png);; All Files (*)")

        DPI = float(self.DPI_LEdit.text())
        # height = self.figure.get_figheight()
        # width = self.figure.get_figheight()
        
        # print(height)
        # print(width)
        
        # self.figure.set_figheight(4)  
        # self.figure.set_figwidth(8)
        
        plt.rcParams.update({'font.size': float(self.Font_Size_LEdit.text())})
        plt.savefig(figure_name[0], dpi = DPI, transparent=True, pad_inches = 0)

        # self.figure.set_figheight(height)
        # self.figure.set_figwidth(width) 
        
    def DarkMode_Menu_Func(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet())
        # apply_stylesheet(app, theme='dark_cyan.xml', extra=extra)
        plt.style.use('dark_background_pysead')
        plt.clf()
        self.canvas.draw()
    
    # def LightMode_Menu_Func(self):
    #     app.setStyleSheet("")
    #     # apply_stylesheet(app, theme='light_blue.xml', extra = extra)
    #     plt.clf()
    #     plt.style.use('fivethirtyeight')
        
    #     self.canvas.draw()
        
    def MaterialDark_Menu_Func(self):
        apply_stylesheet(app, theme='dark_cyan.xml', extra = extra, css_file='custom.css')
        plt.clf()
        plt.style.use('dark_background_pysead_materialdark')
        
        self.canvas.draw()
        
    def MaterialLight_Menu_Func(self):
        apply_stylesheet(app, theme='light_blue.xml', invert_secondary = True, extra = extra)
        # app.setStyleSheet("")
        plt.clf()
        plt.style.use('fivethirtyeight')
        
        self.canvas.draw()
        
    def Export_Nodes_HTML_Func(self):
        nodes_dict = {}
        elements_dict = {}
        materials_dict = {}
        forces_LC1_dict = {}
        forces_LC2_dict = {}
        forces_LC3_dict = {}
        forces_LC4_dict = {}
        forces_LC5_dict = {}
        forces_LC6_dict = {}
        forces_LC7_dict = {}
        forces_LC8_dict = {}
        forces_LC9_dict = {}
        forces_LC10_dict = {}
        supports_dict = {}
        load_case_dict = {}

        # try:
        # Nodes    
        for index in range(self.Nodes_Table_Widget.rowCount()):
            node = int(self.Nodes_Table_Widget.item(index,0).text())
            x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
            y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
            nodes_dict.update({index+1:[int(node), float(x_coord), float(y_coord)]})
        nodes_df = pd.DataFrame.from_dict(nodes_dict, orient='index', columns=['Node','x_coord','y_coord'])

        # Elements
        for index in range(self.Element_Table_Widget.rowCount()):
            bar = int(self.Element_Table_Widget.item(index,0).text())
            node_1 = int(self.Element_Table_Widget.item(index,1).text())
            node_2 = int(self.Element_Table_Widget.item(index,2).text())
            elements_dict.update({index+1:[int(bar), int(node_1), int(node_2)]})
        elements_df = pd.DataFrame.from_dict(elements_dict, orient='index', columns=['Element','Node_1','Node_2'])

        # Materials
        for index in range(self.Material_Table_Widget.rowCount()):
            bar = int(self.Material_Table_Widget.item(index,0).text())
            area = float(self.Material_Table_Widget.item(index,1).text())
            elasticity = float(self.Material_Table_Widget.item(index,2).text())
            materials_dict.update({index+1:[int(bar), float(area), float(elasticity)]})
        materials_df = pd.DataFrame.from_dict(materials_dict, orient='index', columns=['Element','Area','Elasticity'])
        
        # Load Cases
        for index in range(self.Load_Case_Table_Widget.rowCount()):
            load_case_dict.update({index+1:str(self.Load_Case_Table_Widget.item(index,0).text())})
        load_cases_df = pd.DataFrame.from_dict(load_case_dict, orient='index', columns=['Load Case Name'])
        
        # Forces
        # Load Case 1
        if bool(self.forces_LC1) == True:
            index = 1
            for key, item in self.forces_LC1.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC1_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC1_df = pd.DataFrame.from_dict(forces_LC1_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 2
        if bool(self.forces_LC2) == True:
            index = 1
            for key, item in self.forces_LC2.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC2_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC2_df = pd.DataFrame.from_dict(forces_LC2_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 3
        if bool(self.forces_LC3) == True:
            index = 1
            for key, item in self.forces_LC3.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC3_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC3_df = pd.DataFrame.from_dict(forces_LC3_dict, orient='index', columns=['Node','F_x','F_y'])
    
        # Load Case 4
        if bool(self.forces_LC4) == True:
            index = 1
            for key, item in self.forces_LC4.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC4_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC4_df = pd.DataFrame.from_dict(forces_LC4_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 5
        if bool(self.forces_LC5) == True:
            index = 1
            for key, item in self.forces_LC5.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC5_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC5_df = pd.DataFrame.from_dict(forces_LC5_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 6
        if bool(self.forces_LC6) == True:
            index = 1
            for key, item in self.forces_LC6.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC6_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC6_df = pd.DataFrame.from_dict(forces_LC6_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 7
        if bool(self.forces_LC7) == True:
            index = 1
            for key, item in self.forces_LC7.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC7_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC7_df = pd.DataFrame.from_dict(forces_LC7_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 8
        if bool(self.forces_LC8) == True:
            index = 1
            for key, item in self.forces_LC8.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC8_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC8_df = pd.DataFrame.from_dict(forces_LC8_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 9
        if bool(self.forces_LC9) == True:
            index = 1
            for key, item in self.forces_LC9.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC9_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC9_df = pd.DataFrame.from_dict(forces_LC9_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Load Case 10
        if bool(self.forces_LC10) == True:
            index = 1
            for key, item in self.forces_LC10.items():
                node = key
                f_x = item[0]
                f_y = item[1]
                forces_LC10_dict.update({index:[int(node), float(f_x), float(f_y)]})
                index+=1
            forces_LC10_df = pd.DataFrame.from_dict(forces_LC10_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Supports
        for index in range(self.Support_Table_Widget.rowCount()):
            node = int(self.Support_Table_Widget.item(index,0).text())
            x = int(self.Support_Table_Widget.item(index,1).text())
            y = int(self.Support_Table_Widget.item(index,2).text())
            supports_dict.update({index+1:[int(node), float(x), float(y)]})
        supports_df = pd.DataFrame.from_dict(supports_dict, orient='index', columns=['Node','X','Y'])
        
        file_name = QFileDialog.getSaveFileName(self, "Export to HTML", "", "HTML (*.html);; All Files (*)")
        with open(file_name[0], 'w') as writer:
            writer.write("<h1> PYSEAD TRUSS 2D REPORT </h1>")
            writer.write("<h2> Created by: Engr. Michael James C. Quidilla </h2>")
            writer.write("<br />")
            
            writer.write("<h1> Input Data </h1>")
            writer.write("<h2> Nodes </h2>")
            writer.write(nodes_df.to_html(index = False))
            writer.write("<br />")
            writer.write("<h2> Elements </h2>")
            writer.write(elements_df.to_html(index = False))
            writer.write("<br />")
            writer.write("<h2>Element Materials</h2>")
            writer.write(materials_df.to_html(index = False))
            writer.write("<br />")
            writer.write("<h2>Node Supports</h2>")
            writer.write(supports_df.to_html(index = False))
            writer.write("<br />")
            writer.write("<h2>Load Cases</h2>")
            writer.write(load_cases_df.to_html(index = False))
            writer.write("<br />")
            if bool(self.forces_LC1) == True:
                writer.write("<h2>Load Case 1</h2>")
                writer.write(forces_LC1_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC2) == True:
                writer.write("<h2>Load Case 2</h2>")
                writer.write(forces_LC2_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC3) == True:
                writer.write("<h2>Load Case 3</h2>")
                writer.write(forces_LC3_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC4) == True:
                writer.write("<h2>Load Case 4</h2>")
                writer.write(forces_LC4_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC5) == True:
                writer.write("<h2>Load Case 5</h2>")
                writer.write(forces_LC5_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC6) == True:
                writer.write("<h2>Load Case 6</h2>")
                writer.write(forces_LC6_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC7) == True:
                writer.write("<h2>Load Case 7</h2>")
                writer.write(forces_LC7_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC8) == True:
                writer.write("<h2>Load Case 8</h2>")
                writer.write(forces_LC8_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC9) == True:
                writer.write("<h2>Load Case 9</h2>")
                writer.write(forces_LC9_df.to_html(index = False))
                writer.write("<br />")
            if bool(self.forces_LC10) == True:
                writer.write("<h2>Load Case 10</h2>")
                writer.write(forces_LC10_df.to_html(index = False))
                writer.write("<br />")
            
        self.statusBar.showMessage("Exported to HTML")

    def Select_Func(self):
        print('select')
        self.GraphicsView_Widget.setDragMode(QGraphicsView.RubberBandDrag)

    def Pan_Func(self):
        print('pan').text
        self.GraphicsView_Widget.setDragMode(QGraphicsView.ScrollHandDrag)

    def Quit_Func(self):
        sys.exit()


    ###### Dialog Boxes ######
    def Import_CSV_Func(self):
        dialog = Import_CSV()
        result = dialog.exec()

        if result:
            try:
                Nodes_LEdit = dialog.findChild(QLineEdit, "Nodes_LEdit")
                Bars_LEdit = dialog.findChild(QLineEdit, "Bars_LEdit")
                Materials_LEdit = dialog.findChild(QLineEdit, "Materials_LEdit")
                Forces_LEdit = dialog.findChild(QLineEdit, "Forces_LEdit")
                Supports_LEdit = dialog.findChild(QLineEdit, "Supports_LEdit")
                
                nodes_sheet = pd.read_csv(Nodes_LEdit.text())
                elements_sheet = pd.read_csv(Bars_LEdit.text())
                materials_sheet = pd.read_csv(Materials_LEdit.text())
                forces_sheet = pd.read_csv(Forces_LEdit.text())
                supports_sheet = pd.read_csv(Supports_LEdit.text())

                self.Open_File(nodes_sheet, elements_sheet, materials_sheet, forces_sheet, supports_sheet)
                # self.Solve_Truss_Button.setEnabled(True)

                self.Node_row_Position = self.Nodes_Table_Widget.rowCount()
                self.Bar_row_Position = self.Element_Table_Widget.rowCount()

                self.Node_Number_From_LEdit.setText(str(self.Node_row_Position + 1))
                self.Bar_Number_From_LEdit.setText(str(self.Bar_row_Position + 1))

                self.Save_As_Func()
            except:
                self.statusBar.showMessage("Error Importing CSV")
                
    def About_Func(self):
        dialog = About()
        dialog.exec()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
    
        return os.path.join(base_path, relative_path)
    
###### Navigation Toolbar Customized #######
class NavigationToolbarCustom(NavigationToolbar):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ("Save","Pan","Zoom", "Home")]


if __name__ == "__main__":
    # Initialize the App
    # sys.argv += ['--style', 'Material']
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_cyan.xml', extra = extra, css_file='custom.css')
    UIWindow = UI()
    UIWindow.show()
    # app.setStyleSheet(qdarkstyle.load_stylesheet())

    if getattr(sys, 'frozen', False):
        # Close the splash screen. It does not matter when the call
        # to this function is made, the splash screen remains open until
        # this function is called or the Python program is terminated.
        pyi_splash.close()

    sys.exit(app.exec())
    
