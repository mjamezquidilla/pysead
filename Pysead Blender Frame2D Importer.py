from pysead.Frame_2D import Member_2D, Frame_2D
import pandas as pd

nodes_sheet = pd.read_csv('nodes.csv')
elements_sheet = pd.read_csv('bar_elements.csv')
supports_sheet = pd.read_csv('supports.csv')
forces_sheet = pd.read_csv('nodal_loads.csv')

nodes_sheet['Node'] = nodes_sheet['Node'] + 1
elements_sheet['Element'] = elements_sheet['Element'] + 1
supports_sheet['Node'] = supports_sheet['Node'] + 1
forces_sheet['Node'] = forces_sheet['Node'] + 1

width = 0.300
depth = 0.500
fc = 21

area = width*depth
elasticity = 4700*(fc)**(1/2) * 1000
inertia = 1/12*width*depth**3

# Compile all members
member_list = []

for m in range(len(elements_sheet)): 
    # sort nodes
    node_1 = elements_sheet['Node_1'][m]+1
    node_2 = elements_sheet['Node_2'][m]+1

    element_node = sorted({node_1,node_2})
    # element_node = [node_1,node_2]

    globals()[f'M{m+1}'] = Member_2D(member_number=m+1, 
                                    area=area, 
                                    elasticity=elasticity, 
                                    inertia=inertia, 
                                    nodes={element_node[0]: [nodes_sheet['x_coord'][element_node[0]-1], nodes_sheet['y_coord'][element_node[0]-1]],
                                           element_node[1]: [nodes_sheet['x_coord'][element_node[1]-1], nodes_sheet['y_coord'][element_node[1]-1]]})
    string = f'M{m+1}'
    member_list.append(globals()[string])

# # Add selfweight per member
for member in member_list:
    member.Add_Self_Weight(1)
# M1.Add_Self_Weight(23.5)
# M3.Add_Self_Weight(23.5)

Frame = Frame_2D()
Frame.Compile_Frame_Member_Properties(member_list)

# Add Supports
support_array = [1,1,1]

supports={}
for i in range(len(supports_sheet)):
    supports.update({supports_sheet['Node'][i]: support_array})

Frame.supports = supports

# Add Nodal Forces
# forces_array = [10,0,0]

# forces={}
# for i in range(len(forces_sheet)):
#     forces.update({forces_sheet['Node'][i]: forces_array})

# Frame.Add_Load_Node(forces)