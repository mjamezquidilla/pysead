import numpy as np 
import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')
plt.rcParams['hatch.color'] = 'white'
print("Positive Values for forces: right, up (righthand rule)")
print("Negative moment = clockwise, Positive moment = counter-clockwise (righthand rule)")
print("For adding Local Member Load: Axial Load is always parallel to the member local axis")
print("For adding Local Member Load: Loading is always point downward towards the frame element and is considered positive")
print("Member Forces: at left end to right end (based on local axis) - [Axial, Shear, Bending]. Local Axis is governed for positive/negative values. Right is positive, upward is positive, counterclockwise is positive")
print("Frame Reactions: [horizontal, vertical, Moment]. horizontal - right is positive, vertical - upward is positive, moment - counterclockwise is positive")


class Member_2D:
    def __init__(self, member_number, nodes, area, elasticity, inertia):
        self.member_number = member_number
        self.nodes = nodes
        self.area = area
        self.inertia = inertia
        self.elasticity = elasticity


        self.node_list = []
        for node in nodes:
            self.node_list.append(node)

        # compute length of member
        coordinates = []
        for node in nodes:
            coordinates.append(nodes[node])
        x1 = coordinates[0][0]
        y1 = coordinates[0][1]
        x2 = coordinates[1][0]
        y2 = coordinates[1][1]
        self.length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # create empty force vectors for each node
        self.forces = {}
        for node in nodes:
            self.forces.update({node: [0,0,0]})

        # Create Shear and Moment numpy arrays
        division_spacing = 0.2
        self.x_array = np.linspace(0,self.length,int(np.ceil(self.length)/division_spacing))
        self.axial = np.zeros(int(np.ceil(self.length)/division_spacing))
        self.shear = np.zeros(int(np.ceil(self.length)/division_spacing))
        self.moment = np.zeros(int(np.ceil(self.length)/division_spacing))


    def Add_Load_Axial_Uniform(self, w):
        L = self.length
        beginning_axial = w * L / 2
        end_axial = w * L / 2
        
        self.forces[self.node_list[0]][0] += beginning_axial
        self.forces[self.node_list[1]][0] += end_axial

        # Axial Values
        axial_values = self.x_array.copy()
        for index, _ in enumerate(axial_values):
            axial_values[index] = beginning_axial

        self.axial += axial_values        


    def Add_Self_Weight(self, unit_weight):
        w = unit_weight * self.area

        nodes = self.nodes
        coordinates = []
        for node in nodes:
            coordinates.append(nodes[node])
        x1 = coordinates[0][0]
        y1 = coordinates[0][1]
        x2 = coordinates[1][0]
        y2 = coordinates[1][1]
        L = self.length
        
        c = (x2 - x1) / L
        s = (y2 - y1) / L

        w1 = w * c
        
        if y2 > y1:
            w2 = -w * s
        else:
            w2 = w * s

        self.Add_Load_Full_Uniform(w1)
        self.Add_Load_Axial_Uniform(w2)


    def Add_load_Axial(self, P, a):
        L = self.length
        beginning_axial = P * (L - a) / L
        end_axial = P * (a) / L
        self.forces[self.node_list[0]][0] += beginning_axial
        self.forces[self.node_list[1]][0] += end_axial
        
        # Axial Values
        axial_values = self.x_array.copy()
        for index, _ in enumerate(axial_values):
            axial_values[index] = beginning_axial

        self.axial += axial_values


    def Add_Load_Point(self, P, a):
        L = self.length
        beginning_moment = P * (L-a)**2 * a / L**2
        end_moment = -P * (L-a) * a**2 / L**2
        beginning_shear = P * (L-a) / L
        end_shear = P * a / L
        self.forces[self.node_list[0]][2] += beginning_moment
        self.forces[self.node_list[1]][2] += end_moment
        self.forces[self.node_list[0]][1] += - beginning_shear
        self.forces[self.node_list[1]][1] += - end_shear

        # Shear Values
        shear_values = self.x_array.copy()
        for index, shear_value in enumerate(shear_values):
            if shear_value < a:
                shear_values[index] = P * (L-a) / L
            else:
                shear_values[index] = P * (L-a) / L - P

        self.shear += shear_values

        # Moment Values
        moment_values = self.x_array.copy()
        for index, moment_value in enumerate(moment_values):
            if moment_value < a:
                moment_values[index] = P * (L-a) / L * moment_value
            else:
                moment_values[index] = P * (L-a) / L * moment_value - P * (moment_value - a)

        self.moment += moment_values        


    def Add_Load_Full_Uniform(self, w):
        L = self.length
        beginning_moment = w * L**2 / 12
        end_moment = -w * L**2 / 12
        beginning_shear = w * L / 2
        end_shear = w * L / 2
        self.forces[self.node_list[0]][2] += beginning_moment
        self.forces[self.node_list[1]][2] += end_moment
        self.forces[self.node_list[0]][1] += - beginning_shear
        self.forces[self.node_list[1]][1] += - end_shear

        shear_values = self.x_array.copy()
        for index, shear_value in enumerate(shear_values):
            shear_values[index] = beginning_shear - w * shear_value
        
        moment_values = self.x_array.copy()
        for index, moment_value in enumerate(moment_values):
            moment_values[index] = beginning_moment - beginning_shear * moment_value + w * moment_value**2 / 2

        self.shear += shear_values
        self.moment += moment_values


    def Add_Load_Moment(self,M,a):
        L = self.length
        b = L - a
        beginning_moment = M * b * (2*a-b) / L**2
        end_moment = M * a * (2*b-a) / L**2
        self.forces[self.node_list[0]][2] += beginning_moment
        self.forces[self.node_list[1]][2] += end_moment

        moment_values = self.x_array.copy()
        for index, _ in enumerate(moment_values):
            moment_values[index] = beginning_moment
        self.moment += moment_values


    def Add_Load_Partial_Uniform(self, w, a, b):
        L = self.length
        beginning_moment = w * L**2 / 12 * (6*(b/L)**2 - 8*(b/L)**3 + 3*(b/L)**4)
        end_moment = -w * L**2 / 12 * (6*(a/L)**2 - 8*(a/L)**3 + 3*(a/L)**4)
        beginning_shear = w * (b-a) / L * ((b-a)/2 + (L-b))
        end_shear = w * (b-a) / L * ((b-a)/2 + a)
        self.forces[self.node_list[0]][2] += beginning_moment
        self.forces[self.node_list[1]][2] += end_moment
        self.forces[self.node_list[0]][1] += - beginning_shear
        self.forces[self.node_list[1]][1] += - end_shear

        # Shear Values
        shear_values = self.x_array.copy()
        for index, shear_value in enumerate(shear_values):
            if shear_value < a:
                shear_values[index] = (w * (b-a) / L * ((b-a)/2 + (L-b)))
            elif shear_value >= a and shear_value < b :
                shear_values[index] = (w * (b-a) / L * ((b-a)/2 + (L-b))) - w*(shear_value - a)
            else:
                shear_values[index] = (w * (b-a) / L * ((b-a)/2 + (L-b))) - w*(b - a)

        self.shear += shear_values

        # Moment Values
        moment_values = self.x_array.copy()
        for index, moment_value in enumerate(moment_values):
            if moment_value < a:
                moment_values[index] = (w * (b-a) / L * ((b-a)/2 + (L-b))) * moment_value
            elif moment_value >= a and moment_value < b :
                moment_values[index] = (w * (b-a) / L * ((b-a)/2 + (L-b))) * moment_value - w*(moment_value - a)**2 / 2
            else:
                moment_values[index] = (w * (b-a) / L * ((b-a)/2 + (L-b))) * moment_value - w * (b - a) * ((b-a)/2 + (moment_value - b))

        self.moment += moment_values

    def Plot_Axial_Diagram(self, figure_size=[10,5]):
        plt.figure(figsize=figure_size)
        plt.plot(self.x_array,self.axial)
        plt.fill_between(self.x_array, 0, self.axial, hatch = '/', alpha = 0.1)
        plt.xlim([0, self.length])
        plt.ylabel('Axial')
        plt.xlabel('Length')
        plt.title('Axial Diagram of Member {}'.format(self.member_number))
        plt.tight_layout()
        plt.show()


    # Plot Shear Diagram
    def Plot_Shear_Diagram(self, figure_size=[10,5]):
        plt.figure(figsize=figure_size)
        plt.plot(self.x_array,self.shear)
        plt.fill_between(self.x_array, 0, self.shear, hatch = '/', alpha = 0.1)
        plt.xlim([0, self.length])
        plt.ylabel('Shear')
        plt.xlabel('Length')
        plt.title('Shear Diagram of Member {}'.format(self.member_number))
        plt.tight_layout()
        plt.show()

    # Plot Moment Diagram
    def Plot_Moment_Diagram(self, figure_size = [10,5]):
        plt.figure(figsize=figure_size)
        plt.plot(self.x_array,self.moment)
        plt.fill_between(self.x_array, 0, self.moment, hatch = '/', alpha = 0.1)
        plt.xlim([0, self.length])
        plt.ylabel('Moment')
        plt.xlabel('Length')
        plt.title('Moment Diagram of Member {}'.format(self.member_number))
        plt.tight_layout()
        plt.show()


    def Resolve_Forces_into_Components(self):
        # solve for angle
        nodes = self.nodes

        coordinates = []
        for node in nodes:
            coordinates.append(nodes[node])
        x1 = coordinates[0][0]
        y1 = coordinates[0][1]
        x2 = coordinates[1][0]
        y2 = coordinates[1][1]
        L = self.length
        
        c = (x2 - x1) / L
        s = (y2 - y1) / L

        FA_1 = self.forces[self.node_list[0]][0] 
        FA_2 = self.forces[self.node_list[1]][0] 
        FV_1 = self.forces[self.node_list[0]][1] 
        FV_2 = self.forces[self.node_list[1]][1] 
        M_1 = self.forces[self.node_list[0]][2] 
        M_2 = self.forces[self.node_list[1]][2] 

        if y2 >= y1:
            FV1_x = -FV_1 * s
            FV2_x = -FV_2 * s
        else: 
            FV1_x = -FV_1 * s
            FV2_x = -FV_2 * s

        FA_1_x = FA_1 * c
        FA_1_y = FA_1 * s
        FA_2_x = FA_2 * c
        FA_2_y = FA_2 * s

        FV1_y = FV_1 * c
        FV2_y = FV_2 * c

        self.resolved_forces = {}
        
        for node in nodes:
            self.resolved_forces.update({node: [0,0,0]})
        
        self.resolved_forces[self.node_list[0]][0] = FV1_x + FA_1_x
        self.resolved_forces[self.node_list[0]][1] = FV1_y + FA_1_y
        self.resolved_forces[self.node_list[0]][2] = - M_1
        self.resolved_forces[self.node_list[1]][0] = FV2_x + FA_2_x
        self.resolved_forces[self.node_list[1]][1] = FV2_y + FA_2_y
        self.resolved_forces[self.node_list[1]][2] = - M_2


    def Add_Shear_At_Left_Support(self, shear):
        shear_values = self.x_array.copy()
        for index, _ in enumerate(shear_values):
            shear_values[index] = shear
        self.shear += shear_values

        moment_values = self.x_array.copy()
        for index, moment_value in enumerate(moment_values):
            moment_values[index] = -shear * moment_value
        self.moment += moment_values

    def Add_Moment_At_Left_Support(self, moment):
        moment_values = self.x_array.copy()
        for index, _ in enumerate(moment_values):
            moment_values[index] = moment
        self.moment += moment_values


    def Add_Axial_At_Left_Support(self, axial):
        axial_values = self.x_array.copy()
        for index, _ in enumerate(axial_values):
            axial_values[index] = axial
        self.axial += axial_values


    def Plot_Diagrams(self, figure_size = [10,10]):
        fig, axs = plt.subplots(3, 1)
        fig.set_figheight(figure_size[0])
        fig.set_figwidth(figure_size[1])

        # Plot Axial Diagram
        axs[0].plot(self.x_array,self.axial)
        axs[0].plot(self.x_array,self.axial)
        axs[0].fill_between(self.x_array, 0, self.axial, hatch = '/', alpha = 0.1)
        axs[0].set_xlim([0, self.length])
        axs[0].set_ylabel('Axial')
        axs[0].set_xlabel('Length')
        axs[0].set_title('Axial Diagram of Member {}'.format(self.member_number))

        # Plot Shear Diagram
        axs[1].plot(self.x_array,self.shear)
        axs[1].plot(self.x_array,self.shear)
        axs[1].fill_between(self.x_array, 0, self.shear, hatch = '/', alpha = 0.1)
        axs[1].set_xlim([0, self.length])
        axs[1].set_ylabel('Shear')
        axs[1].set_xlabel('Length')
        axs[1].set_title('Shear Diagram of Member {}'.format(self.member_number))
        
        # Plot Moment Diagram
        axs[2].plot(self.x_array,self.moment)
        axs[2].plot(self.x_array,self.moment)
        axs[2].fill_between(self.x_array, 0, self.moment, hatch = '/', alpha = 0.1)
        axs[2].set_xlim([0, self.length])
        axs[2].set_ylabel('Moment')
        axs[2].set_xlabel('Length')
        axs[2].set_title('Moment Diagram of Member {}'.format(self.member_number))
 
        plt.tight_layout()
        plt.show()




class Frame_2D:
    
    def __init__(self):
        '''
        Initializes Frame class object. User should be aware of its units for consistency of solution.
        
        Parameters
        ----------
        
        nodes: dictionary 
               nodal name/mark followed by the [x,y] coordinate in an array form.
        
        elements: dictionary
                  member or element name followed by the connecting nodes in a form of an array.
                  
        supports: dictionary
                  applies supports at the node name/mark followed by the an array support condition as follows:
                  if array == [1,1]: Pin support
                  if array == [0,1]: Roller support free to move abot the x-axis
                  if array == [1,0]: Roller support free to move abot the y-axis
                  
        forces: dictionary
                applies forces at the node name/mark, followed by an array of [x,y] coordinate. Positive values for x-axis indicate right direction. Positive values for y-axis indicate up direction
        
        elasticities dictionary
                    member's modulus of elasticities. Member's name/mark followed by its modulus of elasticities
                    
        areas: dictionary
                    member's cross-sectional area. Member's name/mark followed by its cross-sectional area
                  
        '''
        self.nodes = {}
        self.elements = {}
        self.supports = {}
        self.forces = {}
        self.elasticities = {}
        self.areas = {}
        self.inertias = {}


    def Compile_Frame_Member_Properties(self, members_list):
        # Compile all nodes
        nodes = {}
        for member in members_list:
            nodes.update(member.nodes)
        
        # Compile all elements
        elements = {}
        for member in members_list:
            elements.update({member.member_number: [member.node_list[0], member.node_list[1]]})
        
        # Compile all areas
        areas = {}
        for member in members_list:
            areas.update({member.member_number: member.area})

        # Compile all inertias
        inertias = {}
        for member in members_list:
            inertias.update({member.member_number: member.inertia})
        
        # Compile all elasticities
        elasticities = {}
        for member in members_list:
            elasticities.update({member.member_number: member.elasticity})

        # Compile all local member forces
        local_member_forces = []
        for member in members_list:
            local_member_forces.append([v for v in member.forces.values()])

        __local_member_forces_dict = {key: [0,0,0,0,0,0] for key in range(1,len(local_member_forces)+1)}
        for i, force in enumerate(local_member_forces):
            __local_member_forces_dict.update({i+1: np.array([force[0][0], -force[0][1], force[0][2], force[1][1], -force[1][1], force[1][2]])})
        
        # Compile all load forces
        forces = {key: [0,0,0] for key in nodes}
        for member in members_list:
            member.Resolve_Forces_into_Components()
            member_forces_temp = member.resolved_forces

            for key in forces: 
                if key in member_forces_temp: 
                    forces[key][0] += member_forces_temp[key][0] 
                    forces[key][1] += member_forces_temp[key][1] 
                    forces[key][2] += member_forces_temp[key][2] 

        forces = {k: v for k, v in sorted(forces.items(), key=lambda item: item[0])}

        self.nodes = nodes
        self.elements = elements
        self.forces = forces
        self.elasticities = elasticities
        self.areas = areas
        self.inertias = inertias
        self.local_member_forces = __local_member_forces_dict
        self.members_list = members_list

    
    def Add_Load_Node(self, nodal_load):
        forces = self.forces
        for key in forces: 
            if key in nodal_load:
                forces[key][0] += nodal_load[key][0] 
                forces[key][1] += nodal_load[key][1] 
                forces[key][2] += nodal_load[key][2] 
        self.forces.update(forces)


    def Member_Lengths(self, element, nodes, elements):
        from_point = elements[element][0]
        to_point = elements[element][1]
        from_node = nodes[from_point]
        to_node = nodes[to_point]

        x1 = from_node[0]
        y1 = from_node[1]
        x2 = to_node[0]
        y2 = to_node[1]
        
        L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return L


    def Assemble_Stiffness_Matrix(self, element, areas, nodes, elements, elasticities, inertias):
        from_point = elements[element][0]
        to_point = elements[element][1]
        from_node = nodes[from_point]
        to_node = nodes[to_point]

        x1 = from_node[0]
        y1 = from_node[1]
        x2 = to_node[0]
        y2 = to_node[1]
        
        L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        c = (x2 - x1)/L
        s = (y2 - y1)/L

        A = areas[element]
        I = inertias[element]
        E = elasticities[element]
        
        k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,      0],
                                    [0,          12,    6*L,         0,   -12,    6*L],
                                    [0,         6*L, 4*L**2,         0,  -6*L, 2*L**2],
                                    [-A*L**2/I,   0,      0,  A*L**2/I,     0,      0],
                                    [0,         -12,   -6*L,         0,    12,   -6*L],
                                    [0,         6*L, 2*L**2,         0,  -6*L, 4*L**2]])

        T = np.array([[c, s, 0 , 0, 0, 0],
                    [-s, c, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, c, s, 0],
                    [0, 0, 0, -s, c, 0],
                    [0, 0, 0, 0, 0, 1]])

        K = np.transpose(T).dot(k).dot(T)

        return K


    def Assemble_Global_Stiffness(self, K, k, i, j):
        dofs = [3*i-3, 3*i-2, 3*i-1, 3*j-3, 3*j-2, 3*j-1]
        K[np.ix_(dofs,dofs)] += k
        return K


    def Support_Vector(self, restrained_dofs, nodes):
        dofs = np.zeros([3 * len(nodes)])

        for dof in restrained_dofs:
            dofs[dof * 3 - 3] = restrained_dofs[dof][0]
            dofs[dof * 3 - 2] = restrained_dofs[dof][1]
            dofs[dof * 3 - 1] = restrained_dofs[dof][2]

        support_vector = []

        for i, dof in enumerate(dofs):
            if dof == 1:
                support_vector.append(i + 1)

        return support_vector


    def Apply_Boundary_Conditions(self, support_vector, K_global):
        dofs = []

        for j in support_vector:
            dofs.append(j - 1)

        k = np.delete(K_global, obj = dofs, axis = 0)
        k_new = np.delete(k, obj = dofs, axis = 1)
        return k_new


    def Assemble_Force_Vector(self, forces, support_vector, nodes):
        # Create force vector
        f = np.zeros([3 * len(nodes)])

        # extracts forces along x and y
        for force in forces:
            f[force * 3 - 3] = forces[force][0]
            f[force * 3 - 2] = forces[force][1]
            f[force * 3 - 1] = forces[force][2]

        # create dof list
        dofs = []

        # loops and appends restrained dofs and appends it to the list dof
        for j in support_vector:
            dofs.append(j-1)

        # removes force vector unecessary rows
        f_new = np.delete(f, obj = dofs, axis = 0)
        return f_new


    def Frame_Global_Displacement(self, displacements, Support_Vector, nodes):
        # Create New Support Vector in python indexing
        support_vector_new = [x - 1 for x in Support_Vector]

        # Create Displacement Vector
        displacement_vector = np.zeros(3*len(nodes))

        # Creating global displacement vector that looks for all elements in the support vector and replacing the with value of 0 of that particular index
        j = 0

        # Looping displacement vectors indexes and looks for any of the value within the array "Support_Vector". Replaces with 0 if the value of the index is equal to any of the support vector.
        for i, _ in enumerate(displacement_vector):
            if np.any(np.in1d(support_vector_new, i)):
                displacement_vector[i] = 0
            else:
                displacement_vector[i] = displacements[j]
                j += 1

        return displacement_vector


    def Solve_Reactions(self, K_global, displacement_vector):
        return np.round(K_global.dot(displacement_vector),5)


    def Element_Displacement(self, element_number, global_displacement, elements):
        fromNode = elements[element_number][0]
        toNode = elements[element_number][1]

        u = [3 * fromNode - 2, 3 * fromNode - 1, 3 * fromNode, 
            3 * toNode - 2, 3 * toNode - 1, 3 * toNode]

        # u.sort()

        elem_displacements = []

        for _, u_node in enumerate(u):
            elem_displacements.append(global_displacement[u_node - 1])

        return elem_displacements


    def Solve_Member_Force(self, element, element_displacements, areas, nodes, elements, elasticities, inertias):
        from_point = elements[element][0]
        to_point = elements[element][1]
        from_node = nodes[from_point]
        to_node = nodes[to_point]

        x1 = from_node[0]
        y1 = from_node[1]
        x2 = to_node[0]
        y2 = to_node[1]
        
        L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        c = (x2 - x1)/L
        s = (y2 - y1)/L

        A = areas[element]
        I = inertias[element]
        E = elasticities[element]
        u = element_displacements[element-1]
        
        k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,      0],
                                    [0,          12,    6*L,         0,   -12,    6*L],
                                    [0,         6*L, 4*L**2,         0,  -6*L, 2*L**2],
                                    [-A*L**2/I,   0,      0,  A*L**2/I,     0,      0],
                                    [0,         -12,   -6*L,         0,    12,   -6*L],
                                    [0,         6*L, 2*L**2,         0,  -6*L, 4*L**2]])

        T = np.array([[c, s, 0 , 0, 0, 0],
                    [-s, c, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, c, s, 0],
                    [0, 0, 0, -s, c, 0],
                    [0, 0, 0, 0, 0, 1]])


        member_force = k.dot(T).dot(u)
        return member_force

    def Displacements(self, displacements):

        displacements = {key + 1: displacements[key] for (key, _) in enumerate(displacements + 1)}

        displacements_dict = {}
        
        for displacement in range(1,int(len(displacements)/3 + 1)):
            displacements_dict.update({displacement: [displacements[3 * displacement - 2], displacements[3 * displacement - 1], displacements[3 * displacement] ]})

        return displacements_dict

    def Solve(self):
        '''
        Solves the 2D Frame.
        
        Output Parameters
        -----------------
        
        displacements_: dictionary
                        global displacement of each node. name of each node accompanied by its displacement values along x and y respectively 
        
        reactions_: dictionary
                    global reactions of the Frame. name of each node accompanied by its force values along x and y respectively 
        
        member_forces_: dictionary
                        member forces of the Frame. name of each member accompanied by its force values. positive (+) values are in tension and negative (-) values are in compression
        
        member_stresses_: dictionary
                          member stresses of the Frame. name of each member accompanied by its stress values. positive (+) values are in tension and negative (-) values are in compression
                          
        K_global: numpy array
                  returns the Global Stiffness Matrix of the Frame
        
        '''       
        
        nodes = self.nodes
        elements = self.elements
        supports = self.supports
        forces = self.forces
        elasticities = self.elasticities
        areas = self.areas
        inertias = self.inertias
        
        # Step 1: Get all Member Lengths
        member_lengths = []

        for element in elements:
            L = self.Member_Lengths(element, nodes, elements)
            member_lengths.append(L)

        # Step 2: Assemble Stiffness Matrix for All members
        k_elems = []

        for element in elements:
            k_elems.append(self.Assemble_Stiffness_Matrix(element, areas, nodes, elements, elasticities, inertias))

        # Step 3: Assemble Global Stiffness Matrix
        K_global = np.zeros([3*len(nodes), 3*len(nodes)])

        for i, _ in enumerate(k_elems):
            K_global = self.Assemble_Global_Stiffness(K_global, k_elems[i], elements[i+1][0], elements[i+1][1])

        # Step 4: Apply Boundary conditions to reduce the Global Stiffness Matrix 
        Support_Vector = self.Support_Vector(supports, nodes)
        K_new = self.Apply_Boundary_Conditions(Support_Vector, K_global)

        # Step 5: Reduce Force Vector
        f_new = self.Assemble_Force_Vector(forces, Support_Vector, nodes)

        # Step 6: Solve for Displacement
        displacements = np.linalg.inv(K_new).dot(f_new.transpose())

        # Step 7: Create Global Displacement Vector
        global_displacements = self.Frame_Global_Displacement(displacements, Support_Vector, nodes)

        # Step 8: Solve for Reactions 
        reactions = self.Solve_Reactions(K_global, global_displacements)

        # Step 9: Solve Member Displacements
        element_displacements = []

        for element in elements:
            element_displacements.append(self.Element_Displacement(element, global_displacements, elements))

        # Step 10A: Solve Member Forces
        solved_member_forces = []

        for element in elements:
            solved_member_forces.append(self.Solve_Member_Force(element, element_displacements, areas, nodes, elements, elasticities, inertias))
        solved_member_forces = {key: solved_member_forces[key-1] for key in elements}


        # Storing of Variables lists
        self.displacements_ = self.Displacements(global_displacements)
        self.reactions_ = self.__Reactions(reactions, supports)
        self.K_global_ = K_global

        # Member Lengths
        lengths = {}
        for key, length in enumerate(member_lengths):
            lengths.update({key+1: length})
        self.member_lengths_ = lengths

        # Solved Member Forces
        self.solved_member_forces = solved_member_forces
        
        # Updated Local Member Forces
        new_member_forces_dict = {}
        for key in solved_member_forces:
            new_member_forces = solved_member_forces[key] + self.local_member_forces[key]
            new_member_forces_dict.update({key: new_member_forces})
        self.local_member_forces_solved_ = new_member_forces_dict

        # Step 11: Update Local Member Forces to its Member Class
        self.Update_Member_Local_Forces()
    
    def Update_Member_Local_Forces(self):
        for element, member in enumerate(self.members_list):
            member.Add_Axial_At_Left_Support(self.solved_member_forces[element + 1][0])
            member.Add_Shear_At_Left_Support(self.solved_member_forces[element + 1][1])
            member.Add_Moment_At_Left_Support(self.solved_member_forces[element + 1][2])


    def Draw_Frame_Setup(self, figure_size = None, linewidth = 2, offset = 0.12, length_of_arrow = 1.0, width_of_arrow = 0.05, arrow_line_width = 2, grid = True):
        '''
        Draws the Truss as initialized by the class
        
        Parameters
        ----------
        
        figure_size: array
                    size of the plot's figure in x, y heights.
        length_of_arrow: float
                        length of force vector arrow. default value is 1.0
        width_of_arrow: float
                        width of force vector arrow head. default value is 0.1
        arrow_line_width: float
                        width of force vector line. default value is 2.0
        grid: boolean
              activates gridlines. default value is False
        '''
        
        
        nodes = self.nodes
        elements = self.elements
        supports = self.supports
        forces = self.forces      

        plt.figure(figsize = figure_size)
        plt.grid(grid)
       
        # plotting nodes and members
        for element in elements:
            from_node = elements[element][0]
            to_node = elements[element][1]
            from_point = nodes[from_node]
            to_point = nodes[to_node]
            x1 = from_point[0]
            y1 = from_point[1]
            x2 = to_point[0]
            y2 = to_point[1]
            plt.plot([x1,x2],[y1,y2], marker = 'o', color = 'black', zorder = 5, linewidth = linewidth)

        # plotting supports
        for support in supports:

            support_x = supports[support][0]
            support_y = supports[support][1]
            support_z = supports[support][2]

            x = nodes[support][0]
            y = nodes[support][1]

            if support_x == 1 and support_y == 1 and support_z == 1:
                plt.scatter(x, y, marker = 's', s = 200, c='r', zorder = 2)
            elif support_x == 1 and support_y == 1 and support_z == 0:
                plt.scatter(x, y, marker = '^', s = 200, c='r', zorder = 2)
            else: 
                plt.scatter(x, y, marker = 'o', s = 200, c='y', zorder = 2)
    
        # plotting node labels
        # offset = 0.12
        
        for node in nodes:
            plt.annotate(node, (nodes[node][0]+offset, nodes[node][1]+offset), zorder = 10, c='black')
            
        # plotting member labels
        for element in elements:
            fromNode = elements[element][0]
            toNode = elements[element][1]
            from_point = nodes[fromNode]
            to_point = nodes[toNode]
            
            middlePoint = [abs((to_point[0] - from_point[0])/2) + min(from_point[0], to_point[0]), 
                           abs((to_point[1] - from_point[1])/2) + min(from_point[1], to_point[1])]
            
            plt.annotate(element, (middlePoint[0], middlePoint[1]), zorder = 10, c = 'b')
            
        # plotting force vectors
        # loop all x-direction forces
        for force in forces:
            x = nodes[force][0]
            y = nodes[force][1]

            f_x = np.round(forces[force][0],2)

            # plot arrow x-direction
            if f_x > 0:
                plt.arrow(x - length_of_arrow, y, length_of_arrow, 0, 
                          shape = 'full', head_width = width_of_arrow, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                plt.annotate(f_x, ((x - length_of_arrow), y + 0.1), c='red')
                plt.scatter(x - length_of_arrow, y, c='white')
            elif f_x < 0:
                plt.arrow(x + length_of_arrow, y, -length_of_arrow, 0, 
                          shape = 'full', head_width = width_of_arrow, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                plt.annotate(f_x, ((x + length_of_arrow), y + 0.1), c='red')
                plt.scatter(x + length_of_arrow,y, c='white')
            else:
                pass

        # loop all y-direction forces
        for force in forces:
            x = nodes[force][0]
            y = nodes[force][1]

            f_y = np.round(forces[force][1],2)

            # plot arrow y-direction
            if f_y > 0:
                plt.arrow(x, y - length_of_arrow, 0, length_of_arrow,
                          shape = 'full', head_width = width_of_arrow, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                plt.annotate(f_y, (x + 0.1, (y - length_of_arrow)), c='red') 
                plt.scatter(x,y - length_of_arrow, c='white')
            elif f_y < 0:
                plt.arrow(x, y + length_of_arrow, 0, -length_of_arrow, 
                          shape = 'full', head_width = width_of_arrow, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                plt.annotate(f_y, (x + 0.1, (y + length_of_arrow)), c='red')
                plt.scatter(x,y + length_of_arrow, c='white')
            else:
                pass
            
        plt.show()



    def Draw_Frame_Displacements(self, linewidth = 2, magnification_factor = 100, figure_size = None, offset = 0.12):
        '''
        Draws the Truss displacements after solving the truss
        
        Parameters
        ----------
        
        figure_size: array
                    size of the plot's figure in x, y heights.
        length_of_arrow: float
                        length of force vector arrow. default value is 1.0
        width_of_arrow: float
                        width of force vector arrow head. default value is 0.1
        arrow_line_width: float
                        width of force vector line. default value is 2.0
        '''

        nodes = self.nodes
        elements = self.elements
        supports = self.supports

        new_nodes = {}
        for _ in self.displacements_:
            for node in nodes:
                x_dist = self.displacements_[node][0] * magnification_factor + nodes[node][0]
                y_dist = self.displacements_[node][1] * magnification_factor + nodes[node][1]
                new_nodes.update({node: [x_dist, y_dist]})

        plt.figure(figsize = figure_size)
       
        # Plotting Old nodes
        # plotting nodes and members
        for element in dict(elements):
            from_node = elements[element][0]
            to_node = elements[element][1]
            from_point = nodes[from_node]
            to_point = nodes[to_node]
            x1 = from_point[0]
            y1 = from_point[1]
            x2 = to_point[0]
            y2 = to_point[1]
            plt.plot([x1,x2],[y1,y2], marker = 'o', color = 'black', zorder = 5, linestyle = '--', alpha = 0.10, linewidth = linewidth)
    
        # Plotting New nodes
        # plotting nodes and members
        for element in dict(elements):
            from_node = elements[element][0]
            to_node = elements[element][1]
            from_point = new_nodes[from_node]
            to_point = new_nodes[to_node]
            x1 = from_point[0]
            y1 = from_point[1]
            x2 = to_point[0]
            y2 = to_point[1]
            plt.plot([x1,x2],[y1,y2], marker = 'o', color = 'black', zorder = 5, linewidth = linewidth)

        # plotting supports
        for support in supports:

            support_x = supports[support][0]
            support_y = supports[support][1]
            support_z = supports[support][2]

            x = new_nodes[support][0]
            y = new_nodes[support][1]

            if support_x == 1 and support_y == 1 and support_z == 1:
                plt.scatter(x, y, marker = 's', s = 200, c='r', zorder = 2)
            elif support_x == 1 and support_y == 1 and support_z == 0:
                plt.scatter(x, y, marker = '^', s = 200, c='r', zorder = 2)
            else: 
                plt.scatter(x, y, marker = 'o', s = 200, c='y', zorder = 2)
    
        # plotting node labels
        # offset = 0.12
        
        for node in new_nodes:
            plt.annotate(node, (new_nodes[node][0]+offset, new_nodes[node][1]+offset), zorder = 10, c='black')
            
        # plotting member labels
        for element in elements:
            fromNode = elements[element][0]
            toNode = elements[element][1]
            from_point = new_nodes[fromNode]
            to_point = new_nodes[toNode]
            
            middlePoint = [abs((to_point[0] - from_point[0])/2) + min(from_point[0], to_point[0]), 
                           abs((to_point[1] - from_point[1])/2) + min(from_point[1], to_point[1])]
            
            plt.annotate(element, (middlePoint[0], middlePoint[1]), zorder = 10, c = 'b')

        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.show()

    def __Reactions(self, reactions, supports):

        forces_dict = {key + 1: reactions[key] for (key, _) in enumerate(reactions + 1)}

        reactions_dict = {}
        for support in supports:
            reactions_dict.update({support: [forces_dict[3 * support - 2], forces_dict[3 * support-1], forces_dict[3 * support]]})

        return reactions_dict