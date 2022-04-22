class Blender_Importer:
    def __init__(self) -> None:
        pass

    def Import_Truss3D(self):
        import pandas as pd
        nodes_sheet = pd.read_csv('nodes.csv')
        elements_sheet = pd.read_csv('bar_elements.csv')
        supports_sheet = pd.read_csv('supports.csv')

        nodes = {}
        for i in range(len(nodes_sheet)):
            nodes.update({nodes_sheet['Node'][i]: [nodes_sheet['x_coord'][i], nodes_sheet['y_coord'][i]]})

        elements = {}
        for i in range(len(elements_sheet)):
            elements.update({elements_sheet['Element'][i]: [elements_sheet['Node_1'][i], elements_sheet['Node_2'][i]]})

        supports = {}
        support_array = [1,1,1]

        for i in range(len(supports_sheet)):
            supports.update({supports_sheet['Node'][i]: support_array})
        
        return(nodes, elements, supports)