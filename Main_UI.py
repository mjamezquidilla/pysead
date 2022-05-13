# from PyQt5 import QtWidgets
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import qdarkstyle
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg  # , NavigationToolbar2QT as NavigationToolbar
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Graphics_Scene import QDMGraphicsScene
from pysead import Truss_2D

plt.style.use('dark_background_pysead')

os.environ['QT_API'] = 'pyqt5'

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #Global Variables
        self.nodes = {}
        self.elements = {}
        self.supports = {}
        self.forces = {}
        self.elasticity = {}
        self.areas = {}



        # Load the UI file
        uic.loadUi("GUI.ui", self)

        # Define our widgets
        # Button Widget
        self.Add_Node_Button = self.findChild(QPushButton, "Add_Node_Button")
        self.Renumber_Nodes_Button = self.findChild(QPushButton, "Renumber_Nodes_Button")
        self.Remove_Node_Button = self.findChild(QPushButton, "Remove_Node_Button")
        
        self.Add_Bar_Button = self.findChild(QPushButton, "Add_Bar_Button")
        self.Renumber_Bar_Button = self.findChild(QPushButton, "Renumber_Bar_Button")
        self.Remove_Bar_Button = self.findChild(QPushButton, "Remove_Bar_Button")
        
        self.Update_Material_Button = self.findChild(QPushButton, "Update_Material_Button")
        
        self.Add_Force_Button = self.findChild(QPushButton, "Add_Force_Button")
        self.Remove_Force_Button = self.findChild(QPushButton, "Remove_Force_Button")
        
        self.Add_Support_Button = self.findChild(QPushButton, "Add_Support_Button")
        self.Remove_Support_Button = self.findChild(QPushButton, "Remove_Support_Button")
        
        self.Solve_Truss_Button = self.findChild(QPushButton, "Solve_Truss_Button")
        self.Setup_Button = self.findChild(QPushButton, "Setup_Button")
        self.Reactions_Button = self.findChild(QPushButton, "Reactions_Button")
        self.Axial_Force_Button = self.findChild(QPushButton, "Axial_Force_Button")
        self.Displacement_Button = self.findChild(QPushButton, "Displacement_Button")

        self.Save_Figure_Button = self.findChild(QPushButton, "Save_Figure_Button")

        # Line Edit Widget
        self.Node_Number_LEdit = self.findChild(QLineEdit, "Node_Number_LEdit")
        self.X_Coord_LEdit = self.findChild(QLineEdit, "X_Coord_LEdit")
        self.Y_Coord_LEdit = self.findChild(QLineEdit, "Y_Coord_LEdit")

        self.Bar_Number_LEdit = self.findChild(QLineEdit, "Bar_Number_LEdit")
        self.Node_1_LEdit = self.findChild(QLineEdit, "Node_1_LEdit")
        self.Node_2_LEdit = self.findChild(QLineEdit, "Node_2_LEdit")
        
        self.Displacement_Factor_LEdit = self.findChild(QLineEdit, "Displacement_Factor_LEdit")
        self.Line_Width_LEdit = self.findChild(QLineEdit, "Line_Width_LEdit")
        self.Label_Offset_LEdit = self.findChild(QLineEdit, "Label_Offset_LEdit")
        self.Arrow_Length_LEdit = self.findChild(QLineEdit, "Arrow_Length_LEdit")
        self.Arrow_Head_Size_LEdit = self.findChild(QLineEdit, "Arrow_Head_Size_LEdit")
        self.Arrow_Line_Width_LEdit = self.findChild(QLineEdit, "Arrow_Line_Width_LEdit")

        # Combo Box
        self.X_Coord_ComboBox = self.findChild(QComboBox, "X_Coord_ComboBox")
        self.Y_Coord_ComboBox = self.findChild(QComboBox, "Y_Coord_ComboBox")

        # Table Widget
        self.Nodes_Table_Widget = self.findChild(QTableWidget, "Nodes_Table_Widget")
        self.Element_Table_Widget = self.findChild(QTableWidget, "Element_Table_Widget")
        self.Material_Table_Widget = self.findChild(QTableWidget, "Material_Table_Widget")
        self.Force_Table_Widget = self.findChild(QTableWidget, "Force_Table_Widget")
        self.Support_Table_Widget = self.findChild(QTableWidget, "Support_Table_Widget")
        
        self.Post_Processing_Table = self.findChild(QTableWidget, "Post_Processing_Table")

        # Frame Widget
        self.Matplotlib_Frame = self.findChild(QFrame,"Matplotlib_Frame")
        # self.Navigation_Frame = self.findChild(QFrame,"Navigation_Frame")

        # Put Matplotlib inside Matplotlib Frame
        self.horizontalLayout_Matplotlib = QHBoxLayout(self.Matplotlib_Frame)
        self.horizontalLayout_Matplotlib.setObjectName("Matplotlib_layout")
        self.figure = plt.figure(dpi=75)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.horizontalLayout_Matplotlib.addWidget(self.canvas)
        self.ax = plt.gca()

        # self.horizontalLayout_Navigation = QHBoxLayout(self.Navigation_Frame)
        # self.horizontalLayout_Navigation.setObjectName("Navigation_layout")
        # self.horizontalLayout_Navigation.addWidget(NavigationToolbarCustom(self.canvas, self))

        # Graphics View
        self.grScene = QDMGraphicsScene()
        self.GraphicsView_Widget = self.findChild(QGraphicsView, 'graphicsView')
        self.GraphicsView_Widget.setScene(self.grScene)
        self.GraphicsView_Widget.scale(1,-1)

        # Menu Items
        self.New_Menu = self.findChild(QAction, "actionNew")
        self.Open_Menu = self.findChild(QAction, "actionOpen")
        self.Save_As_Menu = self.findChild(QAction, "actionSave_As")
        self.Quit_Menu = self.findChild(QAction, "actionQuit")

        self.DarkMode_Menu = self.findChild(QAction, "actionDarkMode")
        self.LightMode_Menu = self.findChild(QAction, "actionLightMode")

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

        # Run Commands

        # Button Commands
        # Nodes
        self.Add_Node_Button.clicked.connect(self.Add_Node_Button_Func)
        self.Remove_Node_Button.clicked.connect(self.Remove_Node_Button_Func)
        self.Renumber_Nodes_Button.clicked.connect(self.Renumber_Nodes_Func)

        # Elements
        self.Add_Bar_Button.clicked.connect(self.Add_Bar_Button_Func)
        self.Remove_Bar_Button.clicked.connect(self.Remove_Bar_Button_Func)
        self.Renumber_Bar_Button.clicked.connect(self.Renumber_Bars_Func)
        
        # Materials
        self.Update_Material_Button.clicked.connect(self.Update_Material_Button_Func)

        # Forces
        self.Add_Force_Button.clicked.connect(self.Add_Force_Button_Func)
        self.Remove_Force_Button.clicked.connect(self.Remove_Force_Button_Func)

        # Supports
        self.Add_Support_Button.clicked.connect(self.Add_Support_Button_Func)
        self.Remove_Support_Button.clicked.connect(self.Remove_Support_Button_Func)

        # Solve
        self.Solve_Truss_Button.clicked.connect(self.Solve_Truss_Func)
        self.Setup_Button.clicked.connect(self.Draw_Setup)
        self.Reactions_Button.clicked.connect(self.Draw_Truss_Reactions)
        self.Axial_Force_Button.clicked.connect(self.Draw_Truss_Axial_Force_Map)
        self.Displacement_Button.clicked.connect(self.Draw_Truss_Displacement)
        
        self.Save_Figure_Button.clicked.connect(self.Save_Figure_Func)

        # Menu Commands
        self.New_Menu.triggered.connect(self.New_File_Func)
        self.Open_Menu.triggered.connect(self.Open_File_Func)
        self.Save_As_Menu.triggered.connect(self.Save_As_Func)
        self.Quit_Menu.triggered.connect(self.Quit_Func)
        
        self.DarkMode_Menu.triggered.connect(self.DarkMode_Menu_Func)
        self.LightMode_Menu.triggered.connect(self.LightMode_Menu_Func)
        
        self.Node_row_Position = self.Nodes_Table_Widget.rowCount()
        self.Bar_row_Position = self.Element_Table_Widget.rowCount()

        # status bar
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Ready")

        # Show the App
        self.show()
    
    def clicked(self):
        type(file_name[0])


    ###### Nodes Function ######
    def Add_Node_Button_Func(self):
        # Check if all textbox is not empty
        if self.Node_Number_LEdit.text() == "" or self.X_Coord_LEdit.text() == "" or self.Y_Coord_LEdit.text() == "":
            print("Do not leave nodes textboxes empty")
        else:
            # Grabe Item from LEdit Box
            node = int(self.Node_Number_LEdit.text())
            x_coord = float(self.X_Coord_LEdit.text())
            y_coord = float(self.Y_Coord_LEdit.text())
            
            # self.node_number = int(node) + 1

            # # Add Items to Table Widget
            # self.Node_row_Position = self.Nodes_Table_Widget.rowCount()
            
            # # Clear the Textboxes
            self.Node_Number_LEdit.setText(str(int(node) + 1))
            self.X_Coord_LEdit.setText("")
            self.Y_Coord_LEdit.setText("")

            # Update the nodes and auto sort
            self.nodes.update({node: [x_coord, y_coord]})
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

            # Draw Truss
            self.Draw_Setup()
            print(self.nodes)

        
    def Remove_Node_Button_Func(self):
        # Grab Item from Highlighted Row
        clicked = self.Nodes_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Nodes_Table_Widget.removeRow(clicked)
        self.Renumber_Nodes_Func()
        self.Node_Number_LEdit.setText(str(int(self.Node_Number_LEdit.text()) - 1))

        # Reinitialize nodes dictionary and copy all data from table into dictionary        
        self.nodes = {}
        for index in range(self.Nodes_Table_Widget.rowCount()):
            node = int(self.Nodes_Table_Widget.item(index,0).text())
            x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
            y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
            self.nodes.update({index+1:[int(node), float(x_coord), float(y_coord)]})

        print(self.nodes)

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
            

    ###### Elements Function ######
    def Add_Bar_Button_Func(self):
        if self.Bar_Number_LEdit.text() == "" or self.Node_1_LEdit.text() == "" or self.Node_2_LEdit.text() == "":
            print("Do not leave nodes textboxes empty")
        else:
            # Grabe Item from LEdit Box
            bar = int(self.Bar_Number_LEdit.text())
            node_1 = int(self.Node_1_LEdit.text())
            node_2 = int(self.Node_2_LEdit.text())
            area = float(self.Area_LEdit.text())
            elasticity = float(self.Elasticity_LEdit.text())

            new_bar_number = bar + 1

            # Update the elements, areas, and elasticity and auto sort
            self.elements.update({bar: [node_1, node_2]})
            self.elements = {k: v for k, v in sorted(self.elements.items(), key=lambda item: item[0])}
            self.areas.update({bar: area})
            self.areas = {k: v for k, v in sorted(self.areas.items(), key=lambda item: item[0])}
            self.elasticity.update({bar: elasticity})
            self.elasticity = {k: v for k, v in sorted(self.elasticity.items(), key=lambda item: item[0])}


            # Remove the table items
            self.Element_Table_Widget.setRowCount(0)
            self.Material_Table_Widget.setRowCount(0)

            # Loop all the nodes dictionary and replace/update the table widget
            for key, item in self.elements.items():
                bar = str(key)
                node_1 = str(item[0])
                node_2 = str(item[1])

                # Add Items to Table Widget
                rowPosition = self.Element_Table_Widget.rowCount()

                # print(rowPosition)
                self.Element_Table_Widget.insertRow(rowPosition)
                self.Element_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(bar))
                self.Element_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(node_1))
                self.Element_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(node_2))

            for (key, area), (_, elasticity) in zip(self.areas.items(), self.elasticity.items()):
                bar = str(key)
                areas = str(area)
                elasticity = str(elasticity)

                rowPosition = self.Material_Table_Widget.rowCount()
                self.Material_Table_Widget.insertRow(rowPosition)
                self.Material_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(bar))
                self.Material_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(areas))
                self.Material_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(elasticity))

            # Clear the Textboxes
            self.Bar_Number_LEdit.setText(str(new_bar_number))
            self.Node_1_LEdit.setText("")
            self.Node_2_LEdit.setText("")

            self.Renumber_Bars_Func()

            # Draw Truss
            self.Draw_Setup()

            print(self.elements)
            print(self.areas)
            print(self.elasticity)

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

        self.Bar_Number_LEdit.setText(str(int(self.Bar_Number_LEdit.text())-1))
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
            
        # Draw Truss
        self.Draw_Setup()
        print(self.elements)
        print(self.areas)
        print(self.elasticity)

    ###### Materials Function ######
    def Update_Material_Button_Func(self):
        # Grab Item from Highlighted Row
        clicked_row = self.Material_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Material_Table_Widget.removeRow(clicked_row)

        # Grab Items from Columns of the Selected Row
        bar = self.Element_Table_Widget.item(clicked_row,0).text()
        area = self.Area_LEdit.text()
        elasticity = self.Elasticity_LEdit.text()

        # Add Items to Table Widget
        self.Material_Table_Widget.insertRow(clicked_row)
        self.Material_Table_Widget.setItem(clicked_row, 0, QTableWidgetItem(bar))
        self.Material_Table_Widget.setItem(clicked_row, 1, QTableWidgetItem(area))
        self.Material_Table_Widget.setItem(clicked_row, 2, QTableWidgetItem(elasticity))

    # def Remove_Material_Button_Func(self):
    #     # Grab Item from Highlighted Row
    #     clicked = self.Material_Table_Widget.currentRow()

    #     # Delete Highlighted Row
    #     self.Material_Table_Widget.removeRow(clicked)
    #     self.Element_Table_Widget.removeRow(clicked)

    ###### Forces Function ######
    def Add_Force_Button_Func(self):
        # Grabe Item from LEdit Box
        node = int(self.Force_Node_Number_LEdit.text())
        f_x = float(self.Force_X_LEdit.text())
        f_y = float(self.Force_Y_LEdit.text())

        self.forces.update({node:[f_x,f_y]})
        self.forces = {k: v for k, v in sorted(self.forces.items(), key=lambda item: item[0])}

        self.Force_Table_Widget.setRowCount(0)

        # Loop all the nodes dictionary and replace/update the table widget
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

        # Clear the Textboxes
        self.Force_Node_Number_LEdit.setText("")
        # self.Force_X_LEdit.setText("")
        # self.Force_Y_LEdit.setText("")

        # Draw Truss
        self.Draw_Setup()

        print(self.forces)

    def Remove_Force_Button_Func(self):
        # Grab Item from Highlighted Row
        clicked = self.Force_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Force_Table_Widget.removeRow(clicked)

        # Forces
        self.forces = {}
        for index in range(self.Force_Table_Widget.rowCount()):
            bar = int(self.Force_Table_Widget.item(index,0).text())
            f_x = float(self.Force_Table_Widget.item(index,1).text())
            f_y = float(self.Force_Table_Widget.item(index,2).text())
            self.forces.update({bar: [f_x, f_y]})

        print(self.forces)

    ###### Support Function ######
    def Add_Support_Button_Func(self):
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
        self.Draw_Setup()


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

        self.Draw_Setup()
        print(self.supports)

    ###### Truss Functions ######
    def Solve_Truss_Func(self):
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
        for index in range(self.Force_Table_Widget.rowCount()):
            bar = int(self.Force_Table_Widget.item(index,0).text())
            f_x = float(self.Force_Table_Widget.item(index,1).text())
            f_y = float(self.Force_Table_Widget.item(index,2).text())
            self.forces.update({bar: [f_x, f_y]})

        # Supports
        for index in range(self.Support_Table_Widget.rowCount()):
            node = int(self.Support_Table_Widget.item(index,0).text())
            x = int(self.Support_Table_Widget.item(index,1).text())
            y = int(self.Support_Table_Widget.item(index,2).text())
            self.supports.update({node: [x, y]})

        # Update plot
        plt.clf()
        self.Draw_Truss_Setup()
        self.canvas.draw()
        self.Post_Processing_Table.setRowCount(0)

        # Solve Truss
        self.Truss = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)
        self.Truss.Solve()

        # Save Results
        self.df_displacements = pd.DataFrame.from_dict(self.Truss.displacements_, orient='index', columns=['X','Y'])
        self.df_member_forces = pd.DataFrame.from_dict(self.Truss.member_forces_, orient='index', columns=['Force'])
        self.df_reactions = pd.DataFrame.from_dict(self.Truss.reactions_, orient='index', columns=['F_x','F_y'])

        with pd.ExcelWriter(file_name[0].split(".xlsx")[0] + "_Solved.xlsx") as writer:
            self.df_reactions.to_excel(writer, sheet_name='Reactions')
            self.df_displacements.to_excel(writer, sheet_name='Displacements')
            self.df_member_forces.to_excel(writer, sheet_name='Member Forces')

        self.Reactions_Button.setEnabled(True)
        self.Displacement_Button.setEnabled(True)
        self.Axial_Force_Button.setEnabled(True)

        # save_file_name = file_name[0].split('xlsx')[0]
        # plt.savefig(save_file_name+'setup.png', dpi=300)

        print("Truss Solved")

    def Draw_Truss_Axial_Force_Map(self):
        plt.clf()
        self.Draw_Axial()
        self.canvas.draw()

        self.Post_Processing_Table.setColumnCount(2)
        self.Post_Processing_Table.setHorizontalHeaderLabels(['BAR', 'FORCE'])
        self.Post_Processing_Table.setRowCount(0)

        global file_name

        try:
            reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Member Forces')

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

    def Draw_Truss_Displacement(self):
        plt.clf()
        self.Draw_Displacements()
        self.canvas.draw()

        self.Post_Processing_Table.setColumnCount(3)
        self.Post_Processing_Table.setHorizontalHeaderLabels(['NODE', 'X', 'Y'])
        self.Post_Processing_Table.setRowCount(0)

        global file_name

        try:
            reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Displacements')

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

        try:
            reaction_sheet = pd.read_excel(file_name[0].split(".xlsx")[0] + "_Solved.xlsx", sheet_name='Reactions')

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


    def Draw_Setup(self):
        # self.Initialize_Plotting()
        plt.clf()
        self.Draw_Truss_Setup()
        self.canvas.draw()

    def Initialize_Truss_Components(self):
        nodes_sheet = pd.read_excel(file_name[0], sheet_name='Nodes')
        elements_sheet = pd.read_excel(file_name[0], sheet_name='Elements')
        materials_sheet = pd.read_excel(file_name[0], sheet_name='Materials')
        forces_sheet = pd.read_excel(file_name[0], sheet_name='Forces')
        supports_sheet = pd.read_excel(file_name[0], sheet_name='Supports')

        self.nodes = {}
        for i in range(len(nodes_sheet)):
            self.nodes.update({nodes_sheet['Node'][i]: [nodes_sheet['x_coord'][i], nodes_sheet['y_coord'][i]]})

        self.elements = {}
        for i in range(len(elements_sheet)):
            self.elements.update({elements_sheet['Element'][i]: [elements_sheet['Node_1'][i], elements_sheet['Node_2'][i]]})

        self.areas = {}
        for i in range(len(materials_sheet)):
            self.areas.update({materials_sheet['Element'][i]: materials_sheet['Area'][i]})

        self.elasticity = {}
        for i in range(len(materials_sheet)):
            self.elasticity.update({materials_sheet['Element'][i]: materials_sheet['Elasticity'][i]})

        self.forces = {}
        for i in range(len(forces_sheet)):
            self.forces.update({forces_sheet['Node'][i]: [forces_sheet['F_x'][i], forces_sheet['F_y'][i]]})

        self.supports = {}
        for i in range(len(supports_sheet)):
            self.supports.update({supports_sheet['Node'][i]: [supports_sheet['X'][i], supports_sheet['Y'][i]]})

    ##### Matplotlib Functions #####

    def Draw_Truss_Setup(self):
        self.Truss_Setup = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)

        linewidth = float(self.Line_Width_LEdit.text())
        offset = float(self.Label_Offset_LEdit.text())
        length_of_arrow = float(self.Arrow_Length_LEdit.text())
        width_of_arrow = float(self.Arrow_Head_Size_LEdit.text())
        arrow_line_width = float(self.Arrow_Line_Width_LEdit.text())

        self.Truss_Setup.Draw_Truss_Setup(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, width_of_arrow = width_of_arrow, arrow_line_width = arrow_line_width)

    def Draw_Reactions(self):
        linewidth = float(self.Line_Width_LEdit.text())
        offset = float(self.Label_Offset_LEdit.text())
        length_of_arrow = float(self.Arrow_Length_LEdit.text())
        width_of_arrow = float(self.Arrow_Head_Size_LEdit.text())
        arrow_line_width = float(self.Arrow_Line_Width_LEdit.text())
        self.Truss.Draw_Reactions_(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, arrow_head_size = width_of_arrow, arrow_line_width = arrow_line_width)

    def Draw_Displacements(self):
        linewidth = float(self.Line_Width_LEdit.text())
        offset = float(self.Label_Offset_LEdit.text())
        # length_of_arrow = float(self.Arrow_Length_LEdit.text())
        # width_of_arrow = float(self.Arrow_Head_Size_LEdit.text())
        # arrow_line_width = float(self.Arrow_Line_Width_LEdit.text())
        magnification_factor = float(self.Displacement_Factor_LEdit.text())

        self.Truss.Draw_Truss_Displacements(linewidth = linewidth, magnification_factor = magnification_factor, offset = offset)
    
    def Draw_Axial(self):
        self.Truss.Draw_Truss_Axial_Force_Map()

    def New_File_Func(self):
        self.Nodes_Table_Widget.setRowCount(0)
        self.Element_Table_Widget.setRowCount(0)
        self.Material_Table_Widget.setRowCount(0)
        self.Force_Table_Widget.setRowCount(0)
        self.Support_Table_Widget.setRowCount(0)
        self.Post_Processing_Table.setRowCount(0)
        plt.clf()
        self.canvas.draw()

        self.nodes = {}
        self.elements = {}
        self.supports = {}
        self.forces = {}
        self.elasticity = {}
        self.cross_area = {}

        self.Node_Number_LEdit.setText("1")
        self.Bar_Number_LEdit.setText("1")

    ##### Menu Functions #####

    def Save_Func(self):
        nodes_dict = {}
        elements_dict = {}
        materials_dict = {}
        forces_dict = {}
        supports_dict = {}

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
        
        # Forces
        for index in range(self.Force_Table_Widget.rowCount()):
            node = int(self.Force_Table_Widget.item(index,0).text())
            f_x = float(self.Force_Table_Widget.item(index,1).text())
            f_y = float(self.Force_Table_Widget.item(index,2).text())
            forces_dict.update({index+1:[int(node), float(f_x), float(f_y)]})
        forces_df = pd.DataFrame.from_dict(forces_dict, orient='index', columns=['Node','F_x','F_y'])
        
        # Supports
        for index in range(self.Support_Table_Widget.rowCount()):
            node = int(self.Support_Table_Widget.item(index,0).text())
            x = int(self.Support_Table_Widget.item(index,1).text())
            y = int(self.Support_Table_Widget.item(index,2).text())
            supports_dict.update({index+1:[int(node), float(x), float(y)]})
        supports_df = pd.DataFrame.from_dict(supports_dict, orient='index', columns=['Node','X','Y'])
        
        with pd.ExcelWriter(file_name[0]) as writer:
            nodes_df.to_excel(writer, sheet_name='Nodes')
            elements_df.to_excel(writer, sheet_name='Elements')
            materials_df.to_excel(writer, sheet_name='Materials')
            forces_df.to_excel(writer, sheet_name='Forces')
            supports_df.to_excel(writer, sheet_name='Supports')
        
        print("Saved")
        # except:
        #     print("Canceled Dialogue")

    def Save_As_Func(self):
        global file_name
        # try:
        file_name = QFileDialog.getSaveFileName(self, "Save File", "", "Excel File (*.xlsx);; All Files (*)")
        if file_name != "":
            self.Solve_Truss_Button.setEnabled(True)

        self.Save_Func()

        # except:
            # print("Canceled Dialogue")
            # self.Solve_Truss_Button.setEnabled(False)

    def Open_File_Func(self):
        self.New_File_Func()
        global file_name
        file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Excel File (*.xlsx);; All Files (*)")
        # print(file_name[0].split("xlsx"))
        
        try:
            nodes_sheet = pd.read_excel(file_name[0], sheet_name='Nodes')
            elements_sheet = pd.read_excel(file_name[0], sheet_name='Elements')
            materials_sheet = pd.read_excel(file_name[0], sheet_name='Materials')
            forces_sheet = pd.read_excel(file_name[0], sheet_name='Forces')
            supports_sheet = pd.read_excel(file_name[0], sheet_name='Supports')

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

            # Forces
            for index, row in forces_sheet.iterrows():
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
            
            self.Solve_Truss_Button.setEnabled(True)

            self.Node_row_Position = self.Nodes_Table_Widget.rowCount()
            self.Bar_row_Position = self.Element_Table_Widget.rowCount()

            self.Node_Number_LEdit.setText(str(self.Node_row_Position + 1))
            self.Bar_Number_LEdit.setText(str(self.Bar_row_Position + 1))

            # print(self.elements)
        except:
            print("Canceled Dialogue")

    def Save_Figure_Func(self):
        figure_name = QFileDialog.getSaveFileName(self, "Save Figure", "", ".PNG (*.png);; All Files (*)")

        plt.savefig(figure_name[0], transparent=True, pad_inches = 0)

    def DarkMode_Menu_Func(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet())
        plt.style.use('dark_background_pysead')
        plt.clf()
        self.canvas.draw()
    
    def LightMode_Menu_Func(self):
        app.setStyleSheet("")
        plt.clf()
        plt.style.use('fivethirtyeight')
        
        self.canvas.draw()

    def Quit_Func(self):
        sys.exit()



###### Navigation Toolbar Customized #######
# class NavigationToolbarCustom(NavigationToolbar):
#     # only display the buttons we need
#     toolitems = [t for t in NavigationToolbar.toolitems if
#                  t[0] in ("Save",)]

# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()
app.setStyleSheet(qdarkstyle.load_stylesheet())

app.exec_()

