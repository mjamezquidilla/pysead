# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QTableWidget, QPushButton, QWidget, QFrame, QMenu, QAction, QTableWidgetItem, QHBoxLayout
from PyQt5 import uic
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from pysead import Truss_2D

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("GUI.ui", self)

        # Define our widgets
        # Button Widget
        self.Add_Node_Button = self.findChild(QPushButton, "Add_Node_Button")
        self.Update_Node_Button = self.findChild(QPushButton, "Update_Node_Button")
        self.Remove_Node_Button = self.findChild(QPushButton, "Remove_Node_Button")
        
        self.Add_Bar_Button = self.findChild(QPushButton, "Add_Node_Button")
        self.Update_Bar_Button = self.findChild(QPushButton, "Update_Bar_Button")
        self.Remove_Bar_Button = self.findChild(QPushButton, "Remove_Bar_Button")
        
        self.Add_Material_Button = self.findChild(QPushButton, "Add_Material_Button")
        self.Update_Material_Button = self.findChild(QPushButton, "Update_Material_Button")
        self.Remove_Material_Button = self.findChild(QPushButton, "Remove_Material_Button")
        
        self.Add_Force_Button = self.findChild(QPushButton, "Add_Force_Button")
        self.Update_Force_Button = self.findChild(QPushButton, "Update_Force_Button")
        self.Remove_Force_Button = self.findChild(QPushButton, "Remove_Force_Button")
        
        self.Add_Support_Button = self.findChild(QPushButton, "Add_Support_Button")
        self.Update_Support_Button = self.findChild(QPushButton, "Update_Support_Button")
        self.Remove_Support_Button = self.findChild(QPushButton, "Remove_Support_Button")
        
        self.Setup_Button = self.findChild(QPushButton, "Setup_Button")
        self.Reactions_Button = self.findChild(QPushButton, "Reactions_Button")
        self.Axial_Force_Button = self.findChild(QPushButton, "Axial_Force_Button")
        self.Displacement_Button = self.findChild(QPushButton, "Displacement_Button")

        # Line Edit Widget
        self.Node_Number_LEdit = self.findChild(QLineEdit, "Node_Number_LEdit")
        self.X_Coord_LEdit = self.findChild(QLineEdit, "X_Coord_LEdit")
        self.Y_Coord_LEdit = self.findChild(QLineEdit, "Y_Coord_LEdit")


        # Table Widget
        self.Nodes_Table_Widget = self.findChild(QTableWidget, "Nodes_Table_Widget")


        # Frame Widget
        self.Matplotlib_Frame = self.findChild(QFrame,"Matplotlib_Frame")

        # Put Matplotlib inside Matplotlib Frame
        self.horizontalLayout_Matplotlib = QHBoxLayout(self.Matplotlib_Frame)
        self.horizontalLayout_Matplotlib.setObjectName("Matplotlib_layout")
        self.figure = plt.figure(dpi=75)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.horizontalLayout_Matplotlib.addWidget(self.canvas)
        self.ax = plt.gca()

        # Menu Items
        self.New_Menu = self.findChild(QAction, "actionNew")
        self.Open_Menu = self.findChild(QAction, "actionOpen")
        self.Save_Menu = self.findChild(QAction, "actionSave")
        self.Save_As_Menu = self.findChild(QAction, "actionSave_As")
        self.Quit_Menu = self.findChild(QAction, "actionQuit")

        self.PySEAD_Truss_Menu = self.findChild(QAction, "actionPySEAD_Truss")

        # Run Commands

        # Button Commands
        # Nodes
        self.Add_Node_Button.clicked.connect(self.Add_Node_Button_Func)

        # Solve
        self.Setup_Button.clicked.connect(self.Draw_Setup)
        self.Reactions_Button.clicked.connect(self.Draw_Truss_Reactions)
        self.Axial_Force_Button.clicked.connect(self.Draw_Truss_Axial_Force_Map)
        self.Displacement_Button.clicked.connect(self.Draw_Truss_Displacement)



        # Menu Commands
        self.Open_Menu.triggered.connect(self.Open_File_Func)
        self.Save_Menu.triggered.connect(self.Save_File_Func)
        

        # Show the App
        self.show()
    
    def clicked(self):
        print("Hello")

    def Add_Node_Button_Func(self):
        # Grabe Item from LEdit Box
        node = self.Node_Number_LEdit.text()
        x_coord = self.X_Coord_LEdit.text()
        y_coord = self.Y_Coord_LEdit.text()
        
        # Add Items to Table Widget
        rowPosition = self.Nodes_Table_Widget.rowCount()
        self.Nodes_Table_Widget.insertRow(rowPosition)
        self.Nodes_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(node))
        self.Nodes_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(x_coord))
        self.Nodes_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(y_coord))

        # Clear the Textboxes
        self.Node_Number_LEdit.setText("")
        self.X_Coord_LEdit.setText("")
        self.Y_Coord_LEdit.setText("")

    def Update_Node_Button(self):
        # Grab Item from Highlighted Row
        clicked_row = self.Nodes_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Nodes_Table_Widget.removeRow(clicked_row)

        # Grab Items from Columns of the Selected Row
        node = self.Node_Number_LEdit.text()
        x_coord = self.X_Coord_LEdit.text()
        y_coord = self.Y_Coord_LEdit.text()

        # Add Items to Table Widget
        self.Nodes_Table_Widget.insertRow(clicked_row)
        self.Nodes_Table_Widget.setItem(clicked_row, 0, QTableWidgetItem(node))
        self.Nodes_Table_Widget.setItem(clicked_row, 1, QTableWidgetItem(x_coord))
        self.Nodes_Table_Widget.setItem(clicked_row, 2, QTableWidgetItem(y_coord))

        # Clear the Textboxes
        self.Node_Number_LEdit.setText("")
        self.X_Coord_LEdit.setText("")
        self.Y_Coord_LEdit.setText("")

    def Remove_Node_Button(self):
        # Grab Item from Highlighted Row
        clicked = self.Nodes_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Nodes_Table_Widget.removeRow(clicked)

    def Solve_Truss_Func(self):
        self.Initialize_Plotting()
        self.Draw_Truss_Setup()

        self.Initialize_Truss_Components()
        self.Truss = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)
        self.Truss.Solve()

        df_displacements = pd.DataFrame.from_dict(self.Truss.displacements_, orient='index', columns=['X','Y'])
        df_displacements.to_csv('C:\\Users\\mjame\\Desktop\\displacements.csv')

        df_member_forces = pd.DataFrame.from_dict(self.Truss.member_forces_, orient='index', columns=['Force'])
        df_member_forces.to_csv('C:\\Users\\mjame\\Desktop\\member_forces.csv')

        df_reactions = pd.DataFrame.from_dict(self.Truss.reactions_, orient='index', columns=['X','Y'])
        df_reactions.to_csv('C:\\Users\\mjame\\Desktop\\reactions.csv')

        # displacement_dict = {}
        # member_forces_dict = {}
        # reactions_dict = {}

        # try:
        #     # Nodes    
        #     for index in range(self.Nodes_Table_Widget.rowCount()):
        #         node = int(self.Nodes_Table_Widget.item(index,0).text())
        #         x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
        #         y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
        #         nodes_dict.update({index+1:[int(node), float(x_coord), float(y_coord)]})

        #     nodes_df = pd.DataFrame.from_dict(nodes_dict, orient='index', columns=['Nodes','X','Y'])
        #     nodes_df.to_csv('C:\\Users\\mjame\\Desktop\\Nodes_Gui.csv')

        print("Truss Solved")

    def Draw_Truss_Axial_Force_Map(self):
        self.Initialize_Truss_Components()
        self.Truss = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)
        self.Truss.Solve()

        self.Initialize_Plotting()
        self.Draw_Axial()

    def Draw_Truss_Displacement(self):
        self.Initialize_Truss_Components()
        self.Truss = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)
        self.Truss.Solve()

        self.Initialize_Plotting()
        self.Draw_Displacements()

    def Draw_Truss_Reactions(self):
        self.Initialize_Truss_Components()
        self.Truss = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)
        self.Truss.Solve()

        self.Initialize_Plotting()
        self.Draw_Reactions()

    def Draw_Setup(self):
        self.Initialize_Plotting()
        self.Draw_Truss_Setup()

    def Initialize_Truss_Components(self):
        nodes_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Nodes')
        elements_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Elements')
        materials_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Materials')
        forces_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Forces')
        supports_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Supports')

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

    # Matplotlib Functions
    def Initialize_Plotting(self):
        plt.close()
        self.horizontalLayout_Matplotlib.removeWidget(self.canvas)
        self.figure = plt.figure(dpi=75)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.horizontalLayout_Matplotlib.addWidget(self.canvas)
        self.ax = plt.gca()

    def Draw_Truss_Setup(self):
        self.Initialize_Truss_Components()
        self.Truss = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)
        self.Truss.Draw_Truss_Setup()

    def Draw_Reactions(self):
        self.Truss.Draw_Reactions_()

    def Draw_Displacements(self):
        self.Truss.Draw_Truss_Displacements()
    
    def Draw_Axial(self):
        self.Truss.Draw_Truss_Axial_Force_Map()

    def Save_File_Func(self):
        # # Loop through the listWidget and pull out each item and store into a dictionary
        nodes_dict = {}
        elements_dict = {}
        forces_dict = {}
        supports_dict = {}
        try:
            # Nodes    
            for index in range(self.Nodes_Table_Widget.rowCount()):
                node = int(self.Nodes_Table_Widget.item(index,0).text())
                x_coord = float(self.Nodes_Table_Widget.item(index,1).text())
                y_coord = float(self.Nodes_Table_Widget.item(index,2).text())
                nodes_dict.update({index+1:[int(node), float(x_coord), float(y_coord)]})

            nodes_df = pd.DataFrame.from_dict(nodes_dict, orient='index', columns=['Nodes','X','Y'])
            nodes_df.to_csv('C:\\Users\\mjame\\Desktop\\Nodes_Gui.csv')

            # Elements
            for index in range(self.Element_Table_Widget.rowCount()):
                bar = int(self.Element_Table_Widget.item(index,0).text())
                node_1 = int(self.Element_Table_Widget.item(index,1).text())
                node_2 = int(self.Element_Table_Widget.item(index,2).text())
                elements_dict.update({index+1:[int(bar), int(node_1), int(node_2)]})

            elements_df = pd.DataFrame.from_dict(elements_dict, orient='index', columns=['Element','Node_1','Node_2'])
            elements_df.to_csv('C:\\Users\\mjame\\Desktop\\bar_elements_Gui.csv')

        except:
            pass
        
    def Open_File_Func(self):
        # Loop through the listWidget and pull out each item and store into a dictionary
        try:
            nodes_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Nodes')
            elements_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Elements')
            materials_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Materials')
            forces_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Forces')
            supports_sheet = pd.read_excel('C:\\Users\\mjame\\Desktop\\GUI_Example.xlsx', sheet_name='Supports')

            # Nodes
            # nodes_sheet = pd.read_csv('C:\\Users\\mjame\\Desktop\\nodes.csv')
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
            # elements_df = pd.read_csv('C:\\Users\\mjame\\Desktop\\bar_elements.csv')
            for index, row in elements_sheet.iterrows():
                element = str(round(row['Element']))
                node_1 = str(row['Node_1'])
                node_2 = str(row['Node_2'])

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
            # forces_df = pd.read_csv('C:\\Users\\mjame\\Desktop\\forces.csv')
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
            # support_df = pd.read_csv('C:\\Users\\mjame\\Desktop\\supports.csv')
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
            
        except:
            pass

# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

