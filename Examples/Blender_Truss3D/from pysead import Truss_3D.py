from pysead import Truss_3D
import pandas as pd


def pysead_blender_importer():
    nodes_sheet = pd.read_csv('nodes.csv')
    elements_sheet = pd.read_csv('bar_elements.csv')
    supports_sheet = pd.read_csv('supports.csv')
    forces_sheet = pd.read_csv('nodal_loads.csv')

    nodes = {}
    for i in range(len(nodes_sheet)):
        nodes.update({nodes_sheet['Node'][i]+1: [nodes_sheet['x_coord'][i], nodes_sheet['y_coord'][i], nodes_sheet['z_coord'][i]]})

    elements = {}
    for i in range(len(elements_sheet)):
        elements.update({elements_sheet['Element'][i]+1: [elements_sheet['Node_1'][i]+1, elements_sheet['Node_2'][i]+1]})

    support_array = [1,1,1]

    supports={}
    for i in range(len(supports_sheet)):
        supports.update({supports_sheet['Node'][i]+1: support_array})

    forces_array = [10,0,0]

    forces={}
    for i in range(len(forces_sheet)):
        forces.update({forces_sheet['Node'][i]+1: forces_array})
    
    return(nodes, elements, supports, forces)

nodes, elements, supports, forces = pysead_blender_importer()


areas = {key: 0.002 for key in elements}
elasticity = {key: 200_000_000 for key in elements}

Truss = Truss_3D(nodes=nodes,
                elements=elements,
                supports=supports,
                forces=forces,
                elasticity=elasticity,
                cross_area=areas)

# %%
Truss.Draw_Truss_Setup()

# %%
Truss.Solve()

# %%
Truss.reactions_

# %%
Truss.Draw_Truss_Displacements(magnification_factor=10)

# %%
Truss.displacements_

# %%



