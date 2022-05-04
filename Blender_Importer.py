def Import_Truss3D(nodes_filename = "nodes.csv", elements_filename = "bar_elements.csv", supports_filename = "supports.csv", nodal_loads_filename = "nodal_loads.csv"):
    '''
    returns nodes, elements, supports, and forces as dictionaries from the Blender Add-on

    Parameters
    ----------
        
        nodes: dictionary 
               nodal name/mark followed by the [x,y] coordinate in an array form.
        
        elements: dictionary
                  member or element name followed by the connecting nodes in a form of an array.
                  
        supports: dictionary
                  applies supports at the node name/mark followed by the an array support condition as follows:
                  array is assumed to be pinned [1,1,1], that is, no translation occurs in x/y/z direction.
                  
        forces: dictionary
                applies forces at the node name/mark, followed by an array of [x,y,z] coordinate. Z-coordinate upward is positive

    '''
    import pandas as pd
    nodes_sheet = pd.read_csv(nodes_filename)
    elements_sheet = pd.read_csv(elements_filename)
    supports_sheet = pd.read_csv(supports_filename)
    forces_sheet = pd.read_csv(nodal_loads_filename)

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

    forces_array = [10,0,-10]

    forces={}
    for i in range(len(forces_sheet)):
        forces.update({forces_sheet['Node'][i]+1: forces_array})
    
    return(nodes, elements, supports, forces)