from enum import auto
from PyQt5 import QtCore, QtGui, QtWidgets
# from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pysead import Truss_2D

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Setup Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 768)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 768))

        # Setup Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Setup Left Frame
        self.Left_Frame = QtWidgets.QFrame(self.centralwidget)
        self.Left_Frame.setGeometry(QtCore.QRect(10, 10, 371, 711))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Left_Frame.sizePolicy().hasHeightForWidth())
        self.Left_Frame.setSizePolicy(sizePolicy)
        self.Left_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Left_Frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Left_Frame.setObjectName("Left_Frame")

        # Tab Widget
        self.Tab_Widget = QtWidgets.QTabWidget(self.Left_Frame)
        self.Tab_Widget.setGeometry(QtCore.QRect(10, 10, 351, 691))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tab_Widget.sizePolicy().hasHeightForWidth())
        self.Tab_Widget.setSizePolicy(sizePolicy)
        self.Tab_Widget.setObjectName("Tab_Widget")

        # Nodes Tab
        self.Nodes_Tab = QtWidgets.QWidget()
        self.Nodes_Tab.setObjectName("Nodes_Tab")
        self.Add_Remove_Group = QtWidgets.QGroupBox(self.Nodes_Tab)
        self.Add_Remove_Group.setGeometry(QtCore.QRect(0, 560, 341, 111))
        self.Add_Remove_Group.setObjectName("Add_Remove_Group")
        self.gridLayoutWidget = QtWidgets.QWidget(self.Add_Remove_Group)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 321, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.Add_Remove_Grid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.Add_Remove_Grid.setContentsMargins(5, 0, 5, 0)
        self.Add_Remove_Grid.setObjectName("Add_Remove_Grid")
        self.X_Coord_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.X_Coord_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.X_Coord_Label.setObjectName("X_Coord_Label")
        self.Add_Remove_Grid.addWidget(self.X_Coord_Label, 0, 1, 1, 1)
        self.X_Coord_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.X_Coord_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.X_Coord_LEdit.setObjectName("X_Coord_LEdit")
        self.Add_Remove_Grid.addWidget(self.X_Coord_LEdit, 1, 1, 1, 1)
        self.Node_Number_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Node_Number_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Node_Number_LEdit.setObjectName("Node_Number_LEdit")
        self.Add_Remove_Grid.addWidget(self.Node_Number_LEdit, 1, 0, 1, 1)
        self.Y_Coord_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Y_Coord_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Y_Coord_LEdit.setObjectName("Y_Coord_LEdit")
        self.Add_Remove_Grid.addWidget(self.Y_Coord_LEdit, 1, 2, 1, 1)
        self.Y_Coord_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Y_Coord_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Y_Coord_Label.setObjectName("Y_Coord_Label")
        self.Add_Remove_Grid.addWidget(self.Y_Coord_Label, 0, 2, 1, 1)
        self.Node_Number_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Node_Number_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Node_Number_Label.setObjectName("Node_Number_Label")
        self.Add_Remove_Grid.addWidget(self.Node_Number_Label, 0, 0, 1, 1)

        self.Add_Node_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda: Add_Node_Button(self) )
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Add_Node_Button.sizePolicy().hasHeightForWidth())
        self.Add_Node_Button.setSizePolicy(sizePolicy)
        self.Add_Node_Button.setObjectName("Add_Node_Button")
        self.Add_Remove_Grid.addWidget(self.Add_Node_Button, 2, 0, 1, 1)

        self.Update_Node_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda: Update_Node_Button(self))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Update_Node_Button.sizePolicy().hasHeightForWidth())
        self.Update_Node_Button.setSizePolicy(sizePolicy)
        self.Update_Node_Button.setObjectName("Update_Node_Button")
        self.Add_Remove_Grid.addWidget(self.Update_Node_Button, 2, 1, 1, 1)

        self.Remove_Node_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda: Remove_Node_Button(self))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Remove_Node_Button.sizePolicy().hasHeightForWidth())
        self.Remove_Node_Button.setSizePolicy(sizePolicy)
        self.Remove_Node_Button.setObjectName("Remove_Node_Button")
        self.Add_Remove_Grid.addWidget(self.Remove_Node_Button, 2, 2, 1, 1)
        self.Nodes_Table_Group = QtWidgets.QGroupBox(self.Nodes_Tab)
        self.Nodes_Table_Group.setGeometry(QtCore.QRect(0, 10, 341, 541))
        self.Nodes_Table_Group.setObjectName("Nodes_Table_Group")
        self.Nodes_Table_Widget = QtWidgets.QTableWidget(self.Nodes_Table_Group)
        self.Nodes_Table_Widget.setGeometry(QtCore.QRect(10, 20, 321, 511))
        self.Nodes_Table_Widget.setAlternatingRowColors(True)
        self.Nodes_Table_Widget.setRowCount(0)
        self.Nodes_Table_Widget.setObjectName("Nodes_Table_Widget")
        self.Nodes_Table_Widget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Nodes_Table_Widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Nodes_Table_Widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Nodes_Table_Widget.setHorizontalHeaderItem(2, item)
        self.Tab_Widget.addTab(self.Nodes_Tab, "")

        # Elements Tab
        self.Elements_Tab = QtWidgets.QWidget()
        self.Elements_Tab.setObjectName("Elements_Tab")
        self.Add_Remove_Bars_Group = QtWidgets.QGroupBox(self.Elements_Tab)
        self.Add_Remove_Bars_Group.setGeometry(QtCore.QRect(0, 560, 341, 111))
        self.Add_Remove_Bars_Group.setObjectName("Add_Remove_Bars_Group")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.Add_Remove_Bars_Group)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 321, 81))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.Add_Remove_Bars_Grid = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.Add_Remove_Bars_Grid.setContentsMargins(5, 0, 5, 0)
        self.Add_Remove_Bars_Grid.setObjectName("Add_Remove_Bars_Grid")
        self.Node_1_Label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.Node_1_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Node_1_Label.setObjectName("Node_1_Label")
        self.Add_Remove_Bars_Grid.addWidget(self.Node_1_Label, 0, 1, 1, 1)
        self.Node_1_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.Node_1_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Node_1_LEdit.setObjectName("Node_1_LEdit")
        self.Add_Remove_Bars_Grid.addWidget(self.Node_1_LEdit, 1, 1, 1, 1)
        self.Bar_Number_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.Bar_Number_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Bar_Number_LEdit.setObjectName("Bar_Number_LEdit")
        self.Add_Remove_Bars_Grid.addWidget(self.Bar_Number_LEdit, 1, 0, 1, 1)
        self.Node_2_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.Node_2_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Node_2_LEdit.setObjectName("Node_2_LEdit")
        self.Add_Remove_Bars_Grid.addWidget(self.Node_2_LEdit, 1, 2, 1, 1)
        self.Node_2_Label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.Node_2_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Node_2_Label.setObjectName("Node_2_Label")
        self.Add_Remove_Bars_Grid.addWidget(self.Node_2_Label, 0, 2, 1, 1)
        self.Bar_Number_Label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.Bar_Number_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Bar_Number_Label.setObjectName("Bar_Number_Label")
        self.Add_Remove_Bars_Grid.addWidget(self.Bar_Number_Label, 0, 0, 1, 1)
        self.Add_Bar_Button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Add_Bar_Button.sizePolicy().hasHeightForWidth())
        self.Add_Bar_Button.setSizePolicy(sizePolicy)
        self.Add_Bar_Button.setObjectName("Add_Bar_Button")
        self.Add_Remove_Bars_Grid.addWidget(self.Add_Bar_Button, 2, 0, 1, 1)
        self.Update_Bar_Button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Update_Bar_Button.sizePolicy().hasHeightForWidth())
        self.Update_Bar_Button.setSizePolicy(sizePolicy)
        self.Update_Bar_Button.setObjectName("Update_Bar_Button")
        self.Add_Remove_Bars_Grid.addWidget(self.Update_Bar_Button, 2, 1, 1, 1)
        self.Remove_Bar_Button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Remove_Bar_Button.sizePolicy().hasHeightForWidth())
        self.Remove_Bar_Button.setSizePolicy(sizePolicy)
        self.Remove_Bar_Button.setObjectName("Remove_Bar_Button")
        self.Add_Remove_Bars_Grid.addWidget(self.Remove_Bar_Button, 2, 2, 1, 1)
        self.Element_Table_Group = QtWidgets.QGroupBox(self.Elements_Tab)
        self.Element_Table_Group.setGeometry(QtCore.QRect(0, 10, 341, 541))
        self.Element_Table_Group.setObjectName("Element_Table_Group")
        self.Element_Table_Widget = QtWidgets.QTableWidget(self.Element_Table_Group)
        self.Element_Table_Widget.setGeometry(QtCore.QRect(10, 20, 321, 511))
        self.Element_Table_Widget.setAlternatingRowColors(True)
        self.Element_Table_Widget.setRowCount(0)
        self.Element_Table_Widget.setObjectName("Element_Table_Widget")
        self.Element_Table_Widget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Element_Table_Widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Element_Table_Widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Element_Table_Widget.setHorizontalHeaderItem(2, item)
        self.Tab_Widget.addTab(self.Elements_Tab, "")

        # Material Tab
        self.Materials_Tab = QtWidgets.QWidget()
        self.Materials_Tab.setObjectName("Materials_Tab")
        self.Add_Remove_Material_Group = QtWidgets.QGroupBox(self.Materials_Tab)
        self.Add_Remove_Material_Group.setGeometry(QtCore.QRect(0, 560, 341, 111))
        self.Add_Remove_Material_Group.setObjectName("Add_Remove_Material_Group")
        self.gridLayoutWidget_6 = QtWidgets.QWidget(self.Add_Remove_Material_Group)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(10, 20, 321, 81))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.Add_Remove_Material_Grid = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.Add_Remove_Material_Grid.setContentsMargins(5, 0, 5, 0)
        self.Add_Remove_Material_Grid.setObjectName("Add_Remove_Material_Grid")
        self.Area_Label = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.Area_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Area_Label.setObjectName("Area_Label")
        self.Add_Remove_Material_Grid.addWidget(self.Area_Label, 0, 1, 1, 1)
        self.Area_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.Area_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Area_LEdit.setObjectName("Area_LEdit")
        self.Add_Remove_Material_Grid.addWidget(self.Area_LEdit, 1, 1, 1, 1)
        self.Bar_Number_Material_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.Bar_Number_Material_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Bar_Number_Material_LEdit.setObjectName("Bar_Number_Material_LEdit")
        self.Add_Remove_Material_Grid.addWidget(self.Bar_Number_Material_LEdit, 1, 0, 1, 1)
        self.Elasticity_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.Elasticity_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Elasticity_LEdit.setObjectName("Elasticity_LEdit")
        self.Add_Remove_Material_Grid.addWidget(self.Elasticity_LEdit, 1, 2, 1, 1)
        self.Elasticity_Label = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.Elasticity_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Elasticity_Label.setObjectName("Elasticity_Label")
        self.Add_Remove_Material_Grid.addWidget(self.Elasticity_Label, 0, 2, 1, 1)
        self.Bar_Number_Material_Label = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.Bar_Number_Material_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Bar_Number_Material_Label.setObjectName("Bar_Number_Material_Label")
        self.Add_Remove_Material_Grid.addWidget(self.Bar_Number_Material_Label, 0, 0, 1, 1)
        self.Add_Material_Button = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Add_Material_Button.sizePolicy().hasHeightForWidth())
        self.Add_Material_Button.setSizePolicy(sizePolicy)
        self.Add_Material_Button.setObjectName("Add_Material_Button")
        self.Add_Remove_Material_Grid.addWidget(self.Add_Material_Button, 2, 0, 1, 1)
        self.Update_Material_Button = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Update_Material_Button.sizePolicy().hasHeightForWidth())
        self.Update_Material_Button.setSizePolicy(sizePolicy)
        self.Update_Material_Button.setObjectName("Update_Material_Button")
        self.Add_Remove_Material_Grid.addWidget(self.Update_Material_Button, 2, 1, 1, 1)
        self.Remove_Material_Button = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Remove_Material_Button.sizePolicy().hasHeightForWidth())
        self.Remove_Material_Button.setSizePolicy(sizePolicy)
        self.Remove_Material_Button.setObjectName("Remove_Material_Button")
        self.Add_Remove_Material_Grid.addWidget(self.Remove_Material_Button, 2, 2, 1, 1)
        self.Material_Table_Group = QtWidgets.QGroupBox(self.Materials_Tab)
        self.Material_Table_Group.setGeometry(QtCore.QRect(0, 10, 341, 541))
        self.Material_Table_Group.setObjectName("Material_Table_Group")
        self.Material_Table_Widget = QtWidgets.QTableWidget(self.Material_Table_Group)
        self.Material_Table_Widget.setGeometry(QtCore.QRect(10, 20, 321, 511))
        self.Material_Table_Widget.setAlternatingRowColors(True)
        self.Material_Table_Widget.setRowCount(0)
        self.Material_Table_Widget.setObjectName("Material_Table_Widget")
        self.Material_Table_Widget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Material_Table_Widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Material_Table_Widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Material_Table_Widget.setHorizontalHeaderItem(2, item)
        self.Tab_Widget.addTab(self.Materials_Tab, "")

        # Force Tab
        self.Force_Tab = QtWidgets.QWidget()
        self.Force_Tab.setObjectName("Force_Tab")
        self.Force_Table_Group = QtWidgets.QGroupBox(self.Force_Tab)
        self.Force_Table_Group.setGeometry(QtCore.QRect(0, 10, 341, 541))
        self.Force_Table_Group.setObjectName("Force_Table_Group")
        self.Force_Table_Widget = QtWidgets.QTableWidget(self.Force_Table_Group)
        self.Force_Table_Widget.setGeometry(QtCore.QRect(10, 20, 321, 511))
        self.Force_Table_Widget.setAlternatingRowColors(True)
        self.Force_Table_Widget.setRowCount(0)
        self.Force_Table_Widget.setObjectName("Force_Table_Widget")
        self.Force_Table_Widget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Force_Table_Widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Force_Table_Widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Force_Table_Widget.setHorizontalHeaderItem(2, item)
        self.Add_Remove_Forces_Group = QtWidgets.QGroupBox(self.Force_Tab)
        self.Add_Remove_Forces_Group.setGeometry(QtCore.QRect(0, 560, 341, 111))
        self.Add_Remove_Forces_Group.setObjectName("Add_Remove_Forces_Group")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.Add_Remove_Forces_Group)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 20, 321, 81))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.Add_Remove_Forces_Grid = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.Add_Remove_Forces_Grid.setContentsMargins(5, 0, 5, 0)
        self.Add_Remove_Forces_Grid.setObjectName("Add_Remove_Forces_Grid")
        self.Force_X_Label = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.Force_X_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Force_X_Label.setObjectName("Force_X_Label")
        self.Add_Remove_Forces_Grid.addWidget(self.Force_X_Label, 0, 1, 1, 1)
        self.Force_X_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.Force_X_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Force_X_LEdit.setObjectName("Force_X_LEdit")
        self.Add_Remove_Forces_Grid.addWidget(self.Force_X_LEdit, 1, 1, 1, 1)
        self.Force_Node_Number_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.Force_Node_Number_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Force_Node_Number_LEdit.setObjectName("Force_Node_Number_LEdit")
        self.Add_Remove_Forces_Grid.addWidget(self.Force_Node_Number_LEdit, 1, 0, 1, 1)
        self.Force_Y_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.Force_Y_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Force_Y_LEdit.setObjectName("Force_Y_LEdit")
        self.Add_Remove_Forces_Grid.addWidget(self.Force_Y_LEdit, 1, 2, 1, 1)
        self.Force_Y_Label = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.Force_Y_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Force_Y_Label.setObjectName("Force_Y_Label")
        self.Add_Remove_Forces_Grid.addWidget(self.Force_Y_Label, 0, 2, 1, 1)
        self.Force_Node_Number_Label = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.Force_Node_Number_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Force_Node_Number_Label.setObjectName("Force_Node_Number_Label")
        self.Add_Remove_Forces_Grid.addWidget(self.Force_Node_Number_Label, 0, 0, 1, 1)
        self.Add_Force_Button = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Add_Force_Button.sizePolicy().hasHeightForWidth())
        self.Add_Force_Button.setSizePolicy(sizePolicy)
        self.Add_Force_Button.setObjectName("Add_Force_Button")
        self.Add_Remove_Forces_Grid.addWidget(self.Add_Force_Button, 2, 0, 1, 1)
        self.Update_Force_Button = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Update_Force_Button.sizePolicy().hasHeightForWidth())
        self.Update_Force_Button.setSizePolicy(sizePolicy)
        self.Update_Force_Button.setObjectName("Update_Force_Button")
        self.Add_Remove_Forces_Grid.addWidget(self.Update_Force_Button, 2, 1, 1, 1)
        self.Remove_Force_Button = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Remove_Force_Button.sizePolicy().hasHeightForWidth())
        self.Remove_Force_Button.setSizePolicy(sizePolicy)
        self.Remove_Force_Button.setObjectName("Remove_Force_Button")
        self.Add_Remove_Forces_Grid.addWidget(self.Remove_Force_Button, 2, 2, 1, 1)
        self.Tab_Widget.addTab(self.Force_Tab, "")

        # Supports Tab
        self.Supports_Tab = QtWidgets.QWidget()
        self.Supports_Tab.setObjectName("Supports_Tab")
        self.Support_Table_Group = QtWidgets.QGroupBox(self.Supports_Tab)
        self.Support_Table_Group.setGeometry(QtCore.QRect(0, 10, 341, 541))
        self.Support_Table_Group.setObjectName("Support_Table_Group")
        self.Support_Table_Widget = QtWidgets.QTableWidget(self.Support_Table_Group)
        self.Support_Table_Widget.setGeometry(QtCore.QRect(10, 20, 321, 511))
        self.Support_Table_Widget.setAlternatingRowColors(True)
        self.Support_Table_Widget.setRowCount(0)
        self.Support_Table_Widget.setObjectName("Support_Table_Widget")
        self.Support_Table_Widget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Support_Table_Widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Support_Table_Widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Support_Table_Widget.setHorizontalHeaderItem(2, item)
        self.Add_Remove_Supports_Group = QtWidgets.QGroupBox(self.Supports_Tab)
        self.Add_Remove_Supports_Group.setGeometry(QtCore.QRect(0, 560, 341, 111))
        self.Add_Remove_Supports_Group.setObjectName("Add_Remove_Supports_Group")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.Add_Remove_Supports_Group)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 321, 81))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.Add_Remove_Supports_Grid = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.Add_Remove_Supports_Grid.setContentsMargins(5, 0, 5, 0)
        self.Add_Remove_Supports_Grid.setObjectName("Add_Remove_Supports_Grid")
        self.X_Coord_Support_Label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.X_Coord_Support_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.X_Coord_Support_Label.setObjectName("X_Coord_Support_Label")
        self.Add_Remove_Supports_Grid.addWidget(self.X_Coord_Support_Label, 0, 1, 1, 1)
        self.Support_Node_LEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.Support_Node_LEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Support_Node_LEdit.setObjectName("Support_Node_LEdit")
        self.Add_Remove_Supports_Grid.addWidget(self.Support_Node_LEdit, 1, 0, 1, 1)
        self.Y_Coord_Support_Label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.Y_Coord_Support_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Y_Coord_Support_Label.setObjectName("Y_Coord_Support_Label")
        self.Add_Remove_Supports_Grid.addWidget(self.Y_Coord_Support_Label, 0, 2, 1, 1)
        self.Support_Node_Label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.Support_Node_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Support_Node_Label.setObjectName("Support_Node_Label")
        self.Add_Remove_Supports_Grid.addWidget(self.Support_Node_Label, 0, 0, 1, 1)
        self.Add_Support_Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Add_Support_Button.sizePolicy().hasHeightForWidth())
        self.Add_Support_Button.setSizePolicy(sizePolicy)
        self.Add_Support_Button.setObjectName("Add_Support_Button")
        self.Add_Remove_Supports_Grid.addWidget(self.Add_Support_Button, 2, 0, 1, 1)
        self.Update_Support_Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Update_Support_Button.sizePolicy().hasHeightForWidth())
        self.Update_Support_Button.setSizePolicy(sizePolicy)
        self.Update_Support_Button.setObjectName("Update_Support_Button")
        self.Add_Remove_Supports_Grid.addWidget(self.Update_Support_Button, 2, 1, 1, 1)

        self.Remove_Support_Button = QtWidgets.QPushButton(self.gridLayoutWidget_3, clicked = lambda: Draw_Setup(self))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Remove_Support_Button.sizePolicy().hasHeightForWidth())
        self.Remove_Support_Button.setSizePolicy(sizePolicy)
        self.Remove_Support_Button.setObjectName("Remove_Support_Button")
        self.Add_Remove_Supports_Grid.addWidget(self.Remove_Support_Button, 2, 2, 1, 1)
        self.X_Coord_ComboBox = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.X_Coord_ComboBox.setObjectName("X_Coord_ComboBox")
        self.X_Coord_ComboBox.addItem("")
        self.X_Coord_ComboBox.addItem("")
        self.Add_Remove_Supports_Grid.addWidget(self.X_Coord_ComboBox, 1, 1, 1, 1)
        self.Y_Coord_ComboBox = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.Y_Coord_ComboBox.setObjectName("Y_Coord_ComboBox")
        self.Y_Coord_ComboBox.addItem("")
        self.Y_Coord_ComboBox.addItem("")
        self.Add_Remove_Supports_Grid.addWidget(self.Y_Coord_ComboBox, 1, 2, 1, 1)
        self.Tab_Widget.addTab(self.Supports_Tab, "")

        # Solve Tab
        self.Solve_Tab = QtWidgets.QWidget()
        self.Solve_Tab.setObjectName("Solve_Tab")
        self.Post_Processing_Group = QtWidgets.QGroupBox(self.Solve_Tab)
        self.Post_Processing_Group.setGeometry(QtCore.QRect(0, 100, 341, 551))
        self.Post_Processing_Group.setObjectName("Post_Processing_Group")
        self.Post_Processing_Table = QtWidgets.QTableWidget(self.Post_Processing_Group)
        self.Post_Processing_Table.setGeometry(QtCore.QRect(10, 20, 321, 451))
        self.Post_Processing_Table.setAlternatingRowColors(True)
        self.Post_Processing_Table.setObjectName("Post_Processing_Table")
        self.Post_Processing_Table.setColumnCount(0)
        self.Post_Processing_Table.setRowCount(0)
        self.Show_Group = QtWidgets.QGroupBox(self.Post_Processing_Group)
        self.Show_Group.setGeometry(QtCore.QRect(0, 480, 341, 71))
        self.Show_Group.setObjectName("Show_Group")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.Show_Group)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 321, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.Show_Grid = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Show_Grid.setContentsMargins(0, 0, 0, 0)
        self.Show_Grid.setObjectName("Show_Grid")

        self.Reactions_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget, clicked = lambda: Draw_Truss_Reactions(self))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Reactions_Button.sizePolicy().hasHeightForWidth())
        self.Reactions_Button.setSizePolicy(sizePolicy)
        self.Reactions_Button.setObjectName("Reactions_Button")
        self.Show_Grid.addWidget(self.Reactions_Button)

        self.Axial_Force_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget, clicked = lambda: Draw_Truss_Axial_Force_Map(self))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Axial_Force_Button.sizePolicy().hasHeightForWidth())
        self.Axial_Force_Button.setSizePolicy(sizePolicy)
        self.Axial_Force_Button.setObjectName("Axial_Force_Button")
        self.Show_Grid.addWidget(self.Axial_Force_Button)

        self.Displacement_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget, clicked = lambda: Draw_Truss_Displacement(self))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Displacement_Button.sizePolicy().hasHeightForWidth())
        self.Displacement_Button.setSizePolicy(sizePolicy)
        self.Displacement_Button.setObjectName("Displacement_Button")
        self.Show_Grid.addWidget(self.Displacement_Button)

        self.Solve_Truss_Group = QtWidgets.QGroupBox(self.Solve_Tab)
        self.Solve_Truss_Group.setGeometry(QtCore.QRect(0, 10, 341, 81))
        self.Solve_Truss_Group.setObjectName("Solve_Truss_Group")

        self.Solve_Truss_Button = QtWidgets.QPushButton(self.Solve_Truss_Group, clicked = lambda: Solve_Truss(self))
        self.Solve_Truss_Button.setGeometry(QtCore.QRect(20, 20, 301, 51))
        self.Solve_Truss_Button.setObjectName("Solve_Truss_Button")
        self.Tab_Widget.addTab(self.Solve_Tab, "")

        # Matplotlib Frame
        self.Matplotlib_Frame = QtWidgets.QFrame(self.centralwidget)
        self.Matplotlib_Frame.setGeometry(QtCore.QRect(390, 10, 881, 711))
        self.Matplotlib_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Matplotlib_Frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Matplotlib_Frame.setObjectName("Matplotlib_Frame")
        
        self.horizontalLayout_Matplotlib = QtWidgets.QHBoxLayout(self.Matplotlib_Frame)
        self.horizontalLayout_Matplotlib.setObjectName("Matplotlib_layout")

        self.figure = plt.figure(dpi=75)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.horizontalLayout_Matplotlib.addWidget(self.canvas)
        self.ax = plt.gca()
        # self.Plot()

        # Main Menu Drop Down
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionOpen")

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.open_file)

        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.save_file)

        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionPySEAD_Truss = QtWidgets.QAction(MainWindow)
        self.actionPySEAD_Truss.setObjectName("actionPySEAD_Truss")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actionPySEAD_Truss)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.Tab_Widget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def Add_Node_Button(self):
            # Grabe Item from LEdit Box
            node = self.Node_Number_LEdit.text()
            x_coord = self.X_Coord_LEdit.text()
            y_coord = self.Y_Coord_LEdit.text()
            
            # Add Items to Table Widget
            rowPosition = self.Nodes_Table_Widget.rowCount()
            self.Nodes_Table_Widget.insertRow(rowPosition)
            self.Nodes_Table_Widget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(node))
            self.Nodes_Table_Widget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(x_coord))
            self.Nodes_Table_Widget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(y_coord))

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
            self.Nodes_Table_Widget.setItem(clicked_row, 0, QtWidgets.QTableWidgetItem(node))
            self.Nodes_Table_Widget.setItem(clicked_row, 1, QtWidgets.QTableWidgetItem(x_coord))
            self.Nodes_Table_Widget.setItem(clicked_row, 2, QtWidgets.QTableWidgetItem(y_coord))

            # Clear the Textboxes
            self.Node_Number_LEdit.setText("")
            self.X_Coord_LEdit.setText("")
            self.Y_Coord_LEdit.setText("")

        def Remove_Node_Button(self):
            # Grab Item from Highlighted Row
            clicked = self.Nodes_Table_Widget.currentRow()

            # Delete Highlighted Row
            self.Nodes_Table_Widget.removeRow(clicked)

        def Solve_Truss(self):
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
            self.Initialize_Plotting()
            self.Draw_Axial()

        def Draw_Truss_Displacement(self):
            self.Initialize_Plotting()
            self.Draw_Displacements()

        def Draw_Truss_Reactions(self):
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
   
    # Menu Items functions

    def save_file(self):
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
    
    def open_file(self):
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
                self.Nodes_Table_Widget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(node))
                self.Nodes_Table_Widget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(x_coord))
                self.Nodes_Table_Widget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(y_coord))
            
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
                self.Element_Table_Widget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(element))
                self.Element_Table_Widget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(node_1))
                self.Element_Table_Widget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(node_2))

            # Materials
            for index, row in materials_sheet.iterrows():
                element = str(round(row['Element']))
                area = str(row['Area'])
                elasticity = str(row['Elasticity'])

                # Add Items to Table Widget
                rowPosition = self.Material_Table_Widget.rowCount()

                # print(rowPosition)
                self.Material_Table_Widget.insertRow(rowPosition)
                self.Material_Table_Widget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(element))
                self.Material_Table_Widget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(area))
                self.Material_Table_Widget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(elasticity))

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
                self.Force_Table_Widget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(node))
                self.Force_Table_Widget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(f_x))
                self.Force_Table_Widget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(f_y))
            
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
                self.Support_Table_Widget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(node))
                self.Support_Table_Widget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(x_support))
                self.Support_Table_Widget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(y_support))  
            
        except:
            pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Add_Remove_Group.setTitle(_translate("MainWindow", "Add / Update / Remove Nodes to Table"))
        self.X_Coord_Label.setText(_translate("MainWindow", "X Coordinate"))
        self.Y_Coord_Label.setText(_translate("MainWindow", "Y Coordinate"))
        self.Node_Number_Label.setText(_translate("MainWindow", "Node Number"))
        self.Add_Node_Button.setText(_translate("MainWindow", "Add Node"))
        self.Update_Node_Button.setText(_translate("MainWindow", "Update Selected"))
        self.Remove_Node_Button.setText(_translate("MainWindow", "Remove Selected"))
        self.Nodes_Table_Group.setTitle(_translate("MainWindow", "Nodes Table"))
        item = self.Nodes_Table_Widget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NODE"))
        item = self.Nodes_Table_Widget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "X"))
        item = self.Nodes_Table_Widget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Y"))
        self.Tab_Widget.setTabText(self.Tab_Widget.indexOf(self.Nodes_Tab), _translate("MainWindow", "Nodes"))
        self.Add_Remove_Bars_Group.setTitle(_translate("MainWindow", "Add / Update / Remove Bars to Table"))
        self.Node_1_Label.setText(_translate("MainWindow", "Node 1"))
        self.Node_2_Label.setText(_translate("MainWindow", "Node 2"))
        self.Bar_Number_Label.setText(_translate("MainWindow", "Bar Number"))
        self.Add_Bar_Button.setText(_translate("MainWindow", "Add Bar"))
        self.Update_Bar_Button.setText(_translate("MainWindow", "Update Selected"))
        self.Remove_Bar_Button.setText(_translate("MainWindow", "Remove Selected"))
        self.Element_Table_Group.setTitle(_translate("MainWindow", "Elements Table"))
        item = self.Element_Table_Widget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "BAR"))
        item = self.Element_Table_Widget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "NODE 1"))
        item = self.Element_Table_Widget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "NODE 2"))
        self.Tab_Widget.setTabText(self.Tab_Widget.indexOf(self.Elements_Tab), _translate("MainWindow", "Elements"))
        self.Add_Remove_Material_Group.setTitle(_translate("MainWindow", "Add / Update / Remove Materials to Table"))
        self.Area_Label.setText(_translate("MainWindow", "Cross-sectional Area"))
        self.Elasticity_Label.setText(_translate("MainWindow", "Elasticity"))
        self.Bar_Number_Material_Label.setText(_translate("MainWindow", "Bar Number"))
        self.Add_Material_Button.setText(_translate("MainWindow", "Add Material"))
        self.Update_Material_Button.setText(_translate("MainWindow", "Update Selected"))
        self.Remove_Material_Button.setText(_translate("MainWindow", "Remove Selected"))
        self.Material_Table_Group.setTitle(_translate("MainWindow", "Materials Table"))
        item = self.Material_Table_Widget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "BAR"))
        item = self.Material_Table_Widget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "CROSS AREA"))
        item = self.Material_Table_Widget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "ELASTICITY"))
        self.Tab_Widget.setTabText(self.Tab_Widget.indexOf(self.Materials_Tab), _translate("MainWindow", "Materials"))
        self.Force_Table_Group.setTitle(_translate("MainWindow", "Forces Table"))
        item = self.Force_Table_Widget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NODE"))
        item = self.Force_Table_Widget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "FORCE X DIR"))
        item = self.Force_Table_Widget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "FORCE Y DIR"))
        self.Add_Remove_Forces_Group.setTitle(_translate("MainWindow", "Add / Update / Remove Forces to Table"))
        self.Force_X_Label.setText(_translate("MainWindow", "Force X-Direction"))
        self.Force_Y_Label.setText(_translate("MainWindow", "Force Y-Direction"))
        self.Force_Node_Number_Label.setText(_translate("MainWindow", "Node Number"))
        self.Add_Force_Button.setText(_translate("MainWindow", "Add Force"))
        self.Update_Force_Button.setText(_translate("MainWindow", "Update Selected"))
        self.Remove_Force_Button.setText(_translate("MainWindow", "Remove Selected"))
        self.Tab_Widget.setTabText(self.Tab_Widget.indexOf(self.Force_Tab), _translate("MainWindow", "Forces"))
        self.Support_Table_Group.setTitle(_translate("MainWindow", "Supports Table"))
        item = self.Support_Table_Widget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NODE"))
        item = self.Support_Table_Widget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "PINNED X"))
        item = self.Support_Table_Widget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "PINNED Y"))
        self.Add_Remove_Supports_Group.setTitle(_translate("MainWindow", "Add / Update / Remove Supports to Table"))
        self.X_Coord_Support_Label.setText(_translate("MainWindow", "X Coordinate"))
        self.Y_Coord_Support_Label.setText(_translate("MainWindow", "Y Coordinate"))
        self.Support_Node_Label.setText(_translate("MainWindow", "Node Number"))
        self.Add_Support_Button.setText(_translate("MainWindow", "Add Support"))
        self.Update_Support_Button.setText(_translate("MainWindow", "Update Selected"))
        self.Remove_Support_Button.setText(_translate("MainWindow", "Remove Selected"))
        self.X_Coord_ComboBox.setItemText(0, _translate("MainWindow", "Yes"))
        self.X_Coord_ComboBox.setItemText(1, _translate("MainWindow", "No"))
        self.Y_Coord_ComboBox.setItemText(0, _translate("MainWindow", "Yes"))
        self.Y_Coord_ComboBox.setItemText(1, _translate("MainWindow", "No"))
        self.Tab_Widget.setTabText(self.Tab_Widget.indexOf(self.Supports_Tab), _translate("MainWindow", "Supports"))
        self.Post_Processing_Group.setTitle(_translate("MainWindow", "Post Processing"))
        self.Show_Group.setTitle(_translate("MainWindow", "Show"))
        self.Reactions_Button.setText(_translate("MainWindow", "Reactions"))
        self.Axial_Force_Button.setText(_translate("MainWindow", "Axial Force"))
        self.Displacement_Button.setText(_translate("MainWindow", "Displacement"))
        self.Solve_Truss_Group.setTitle(_translate("MainWindow", "Solve Truss"))
        self.Solve_Truss_Button.setText(_translate("MainWindow", "Solve Truss"))
        self.Tab_Widget.setTabText(self.Tab_Widget.indexOf(self.Solve_Tab), _translate("MainWindow", "Solve"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionQuit.setText(_translate("MainWindow", "Quir"))
        self.actionPySEAD_Truss.setText(_translate("MainWindow", "PySEAD Truss"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.Tab_Widget.setCurrentIndex(0)
    MainWindow.show()
    sys.exit(app.exec_())

