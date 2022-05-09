# from PyQt5 import QtWidgets
from os import X_OK
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QTableWidget, QPushButton, QFrame, QAction, QTableWidgetItem, QHBoxLayout, QFileDialog
from PyQt5 import uic
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from pysead import Truss_2D

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #Global Variables
        global file_name
        file_name = ('C:/temp.xlsx',0)

        # Load the UI file
        uic.loadUi("GUI.ui", self)

        # Define our widgets
        # Button Widget
        self.Add_Node_Button = self.findChild(QPushButton, "Add_Node_Button")
        self.Update_Node_Button = self.findChild(QPushButton, "Update_Node_Button")
        self.Remove_Node_Button = self.findChild(QPushButton, "Remove_Node_Button")
        
        self.Add_Bar_Button = self.findChild(QPushButton, "Add_Bar_Button")
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
        
        self.Solve_Truss_Button = self.findChild(QPushButton, "Solve_Truss_Button")
        self.Setup_Button = self.findChild(QPushButton, "Setup_Button")
        self.Reactions_Button = self.findChild(QPushButton, "Reactions_Button")
        self.Axial_Force_Button = self.findChild(QPushButton, "Axial_Force_Button")
        self.Displacement_Button = self.findChild(QPushButton, "Displacement_Button")

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

        # Table Widget
        self.Nodes_Table_Widget = self.findChild(QTableWidget, "Nodes_Table_Widget")
        self.Element_Table_Widget = self.findChild(QTableWidget, "Element_Table_Widget")
        self.Material_Table_Widget = self.findChild(QTableWidget, "Material_Table_Widget")
        self.Force_Table_Widget = self.findChild(QTableWidget, "Force_Table_Widget")
        self.Support_Table_Widget = self.findChild(QTableWidget, "Support_Table_Widget")
        
        self.Post_Processing_Table = self.findChild(QTableWidget, "Post_Processing_Table")


        # Frame Widget
        self.Matplotlib_Frame = self.findChild(QFrame,"Matplotlib_Frame")
        self.Navigation_Frame = self.findChild(QFrame,"Navigation_Frame")

        # Put Matplotlib inside Matplotlib Frame
        self.horizontalLayout_Matplotlib = QHBoxLayout(self.Matplotlib_Frame)
        self.horizontalLayout_Matplotlib.setObjectName("Matplotlib_layout")
        self.figure = plt.figure(dpi=75)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.horizontalLayout_Matplotlib.addWidget(self.canvas)
        self.ax = plt.gca()

        self.horizontalLayout_Navigation = QHBoxLayout(self.Navigation_Frame)
        self.horizontalLayout_Navigation.setObjectName("Navigation_layout")
        self.horizontalLayout_Navigation.addWidget(NavigationToolbarCustom(self.canvas, self))

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
        self.Remove_Node_Button.clicked.connect(self.Remove_Node_Button_Func)
        self.Update_Node_Button.clicked.connect(self.Update_Node_Button_Func)

        # Elements
        self.Add_Bar_Button.clicked.connect(self.Add_Bar_Button_Func)
        self.Remove_Bar_Button.clicked.connect(self.Remove_Bar_Button_Func)
        self.Update_Bar_Button.clicked.connect(self.Update_Bar_Button_Func)

        # Solve
        self.Solve_Truss_Button.clicked.connect(self.Solve_Truss_Func)
        self.Setup_Button.clicked.connect(self.Draw_Setup)
        self.Reactions_Button.clicked.connect(self.Draw_Truss_Reactions)
        self.Axial_Force_Button.clicked.connect(self.Draw_Truss_Axial_Force_Map)
        self.Displacement_Button.clicked.connect(self.Draw_Truss_Displacement)



        # Menu Commands
        self.New_Menu.triggered.connect(self.New_File_Func)
        self.Open_Menu.triggered.connect(self.Open_File_Func)
        self.Save_As_Menu.triggered.connect(self.Save_As_Func)
        

        # Show the App
        self.show()
    
    def clicked(self):
        type(file_name[0])


    ###### Nodes Function ######
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

    def Update_Node_Button_Func(self):
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

    def Remove_Node_Button_Func(self):
        # Grab Item from Highlighted Row
        clicked = self.Nodes_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Nodes_Table_Widget.removeRow(clicked)

    ###### Elements Function ######
    def Add_Bar_Button_Func(self):
        # Grabe Item from LEdit Box
        bar = self.Bar_Number_LEdit.text()
        node_1 = self.Node_1_LEdit.text()
        node_2 = self.Node_2_LEdit.text()
        
        # Add Items to Table Widget
        rowPosition = self.Element_Table_Widget.rowCount()
        self.Element_Table_Widget.insertRow(rowPosition)
        self.Element_Table_Widget.setItem(rowPosition, 0, QTableWidgetItem(bar))
        self.Element_Table_Widget.setItem(rowPosition, 1, QTableWidgetItem(node_1))
        self.Element_Table_Widget.setItem(rowPosition, 2, QTableWidgetItem(node_2))

        # Clear the Textboxes
        self.Bar_Number_LEdit.setText("")
        self.Node_1_LEdit.setText("")
        self.Node_2_LEdit.setText("")

    def Update_Bar_Button_Func(self):
        # Grab Item from Highlighted Row
        clicked_row = self.Element_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Element_Table_Widget.removeRow(clicked_row)

        # Grab Items from Columns of the Selected Row
        bar = self.Bar_Number_LEdit.text()
        node_1 = self.Node_1_LEdit.text()
        node_2 = self.Node_2_LEdit.text()

        # Add Items to Table Widget
        self.Element_Table_Widget.insertRow(clicked_row)
        self.Element_Table_Widget.setItem(clicked_row, 0, QTableWidgetItem(bar))
        self.Element_Table_Widget.setItem(clicked_row, 1, QTableWidgetItem(node_1))
        self.Element_Table_Widget.setItem(clicked_row, 2, QTableWidgetItem(node_2))

        # Clear the Textboxes
        self.Bar_Number_LEdit.setText("")
        self.Node_1_LEdit.setText("")
        self.Node_2_LEdit.setText("")

    def Remove_Bar_Button_Func(self):
        # Grab Item from Highlighted Row
        clicked = self.Element_Table_Widget.currentRow()

        # Delete Highlighted Row
        self.Element_Table_Widget.removeRow(clicked)


    ###### Truss Functions ######
    def Solve_Truss_Func(self):
        plt.clf()
        self.Draw_Truss_Setup()
        self.canvas.draw()

        self.Initialize_Truss_Components()
        self.Truss = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)
        self.Truss.Solve()

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
        self.Initialize_Truss_Components()
        self.Truss = Truss_2D(nodes = self.nodes, supports = self.supports, cross_area = self.areas, elements = self.elements, elasticity = self.elasticity, forces = self.forces)

        linewidth = float(self.Line_Width_LEdit.text())
        offset = float(self.Label_Offset_LEdit.text())
        length_of_arrow = float(self.Arrow_Length_LEdit.text())
        width_of_arrow = float(self.Arrow_Head_Size_LEdit.text())
        arrow_line_width = float(self.Arrow_Line_Width_LEdit.text())

        self.Truss.Draw_Truss_Setup(linewidth = linewidth, offset = offset, length_of_arrow = length_of_arrow, width_of_arrow = width_of_arrow, arrow_line_width = arrow_line_width)

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
        # except:
        #     pass

    def Save_As_Func(self):
        global file_name
        file_name = QFileDialog.getSaveFileName(self, "Save File", "", "Excel File (*.xlsx);; All Files (*)")
        self.Save_Func()
        

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
            
        except:
            pass

class NavigationToolbarCustom(NavigationToolbar):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ("Save",)]

# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

