import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.patches import Arc, RegularPolygon
from numpy import radians as rad
# plt.style.use('fivethirtyeight')
# plt.rcParams['hatch.color'] = 'white'
# print("Positive Values for forces: right, up (righthand rule)")
# print("Negative moment = clockwise, Positive moment = counter-clockwise (righthand rule)")
# print("For adding Local Member Load: Axial Load is always parallel to the member local axis")
# print("For adding Local Member Load: Loading is always point downward towards the frame element and is considered positive")
# print("Member Forces: at left end to right end (based on local axis) - [Axial, Shear, Bending]. Local Axis is governed for positive/negative values. Right is positive, upward is positive, counterclockwise is positive")
# print("Frame Reactions: [horizontal, vertical, Moment]. horizontal - right is positive, vertical - upward is positive, moment - counterclockwise is positive")
# print("Frame Moment Release: All elements that is connected to the same release node should be released at node end of the element")


class Member_2D:
    def __init__(self, member_number, area, elasticity, inertia, nodes = {}, moment_release = [0,0], no_of_divs = 11):
        self.member_number = member_number
        self.area = area
        self.inertia = inertia
        self.elasticity = elasticity
        self.moment_release_left = moment_release[0]
        self.moment_release_right = moment_release[1]
        self.no_of_divs = no_of_divs
        self.points_of_interest = []
        self.uniform_full_load = []
        self.point_load = []
        self.uniform_axial_load = []
        self.self_weight = []
        self.uniform_full_load_fx = []
        self.uniform_full_load_fy = []
        
        # Check if nodes dictionary is not empty
        if nodes:
            self.nodes = nodes
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
            self.division_spacing = self.length/no_of_divs
            self.x_array = np.linspace(0,self.length,int(np.ceil(self.length)/self.division_spacing))
            self.axial = np.zeros(int(np.ceil(self.length)/self.division_spacing))
            self.shear = np.zeros(int(np.ceil(self.length)/self.division_spacing))
            self.moment = np.zeros(int(np.ceil(self.length)/self.division_spacing))

            # Plotting Member Releases
            self.__Release_Node_Coordinates()

    def Compile_Member_Forces(self):
        # Reinitialize forces dictionary
        self.forces = {}
        for node in self.nodes:
            self.forces.update({node: [0,0,0]})
        
        # Insert the points of interest into x_array
        for a in self.points_of_interest:
            index = np.searchsorted(self.x_array, a)
            self.x_array = np.insert(self.x_array, index, a)
            
            before = np.searchsorted(self.x_array, a-0.001)
            self.x_array = np.insert(self.x_array, before, a-0.001)
            
            after = np.searchsorted(self.x_array, a+0.001)
            self.x_array = np.insert(self.x_array, after, a+0.001)

        # Re-initialize axial, shear, and moment arrays based on length of x_array
        self.axial = np.zeros(len(self.x_array))
        self.shear = np.zeros(len(self.x_array))
        self.moment = np.zeros(len(self.x_array))
        # Recompute the axial, moment and shear values based on new x_array
        for p in self.point_load:
            self.Add_Load_Point(p[0], p[1])
        
        for w in self.uniform_full_load:
            self.Add_Load_Full_Uniform(w, False)
            
        for a in self.uniform_axial_load:
            self.Add_Load_Axial_Uniform(a)

        for w in self.self_weight:
            self.Add_Self_Weight(w)

        for w in self.uniform_full_load_fx:
            self.Add_Load_Full_Uniform_Fx(w)

        for w in self.uniform_full_load_fy:
            self.Add_Load_Full_Uniform_Fy(w)

    def __Release_Node_Coordinates(self):
        nodes = self.nodes
        moment_release = [self.moment_release_left, self.moment_release_right]

        nodes_coordinate_List = []

        for node in nodes:
            nodes_coordinate_List.append(nodes[node].copy())

        self.release_node_coordinates = []

        for i, _ in enumerate(moment_release):
            if moment_release[i] == 1:
                self.release_node_coordinates.append(nodes_coordinate_List[i])

        self.release_node_coordinates = self.release_node_coordinates

        # compute length of member
        coordinates = []
        for node in nodes:
            coordinates.append(nodes[node])
        x1 = coordinates[0][0]
        y1 = coordinates[0][1]
        x2 = coordinates[1][0]
        y2 = coordinates[1][1]
        self.length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        c = (x2 - x1) / self.length
        s = (y2 - y1) / self.length

        node_vert = self.length * 0.1 * s
        node_hor = self.length * 0.1 * c

        if moment_release[0] == 1 and moment_release[1] == 0:
            self.release_node_coordinates[0][0] += node_hor
            self.release_node_coordinates[0][1] += node_vert
        elif moment_release[0] == 0 and moment_release[1] == 1:
            self.release_node_coordinates[0][0] -= node_hor
            self.release_node_coordinates[0][1] -= node_vert
        elif moment_release[0] == 1 and moment_release[1] == 1:
            self.release_node_coordinates[0][0] += node_hor
            self.release_node_coordinates[0][1] += node_vert
            self.release_node_coordinates[1][0] -= node_hor
            self.release_node_coordinates[1][1] -= node_vert
            

    def Add_Nodes_To_Element(self, element, nodes):
        from_node = element[0]
        to_node = element[1]
        from_point = nodes[from_node]
        to_point = nodes[to_node]

        self.nodes = {from_node: from_point, to_node: to_point}
        self.node_list = []
        for node in self.nodes:
            self.node_list.append(node)

        # compute length of member
        coordinates = []
        for node in self.nodes:
            coordinates.append(nodes[node])
        x1 = coordinates[0][0]
        y1 = coordinates[0][1]
        x2 = coordinates[1][0]
        y2 = coordinates[1][1]
        self.length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # create empty force vectors for each node
        self.forces = {}
        for node in self.nodes:
            self.forces.update({node: [0,0,0]})

        # Create Shear and Moment numpy arrays
        self.division_spacing = self.length/self.no_of_divs
        self.x_array = np.linspace(0,self.length,int(np.ceil(self.length)/self.division_spacing))
        self.axial = np.zeros(int(np.ceil(self.length)/self.division_spacing))
        self.shear = np.zeros(int(np.ceil(self.length)/self.division_spacing))
        self.moment = np.zeros(int(np.ceil(self.length)/self.division_spacing))

        self.__Release_Node_Coordinates()


    def Add_Load_Axial_Uniform(self, w, skip_part = False): # OKAY!
        L = self.length
        beginning_axial = w * L / 2
        end_axial = w * L / 2
        
        self.forces[self.node_list[0]][0] += beginning_axial
        self.forces[self.node_list[1]][0] += end_axial

        # Axial Values
        axial_values = self.x_array.copy()
        for index, x in enumerate(axial_values):
            axial_values[index] = w*x - beginning_axial

        self.axial += axial_values        

        if not skip_part:
            if not w in self.uniform_axial_load:
                self.uniform_axial_load.append(w)

    def Add_Self_Weight(self, unit_weight): # OKAY!
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
        
        if x2 >= x1 and y2 >= y1: # 1st quadrant
            w1 = w * c
            w2 = -w * s
        elif x2 <= x1 and y2 >= y1: # 2nd quadrant
            w1 = w * c
            w2 = -w * s
        elif x2 <= x1 and y2 <= y1: # 3rd quadrant
            w1 = -w * c
            w2 = w * s
        else: # 4th quadrant
            w1 = w * c
            w2 = -w * s

        self.Add_Load_Full_Uniform(w1, True)
        self.Add_Load_Axial_Uniform(w2, True)
        
        if not unit_weight in self.self_weight:
            self.self_weight.append(unit_weight)


    def Add_Load_Full_Uniform_Fy(self, w): # OKAY!
        nodes = self.nodes
        coordinates = []
        for node in nodes:
            coordinates.append(nodes[node])
        x1 = coordinates[0][0]
        y1 = coordinates[0][1]
        x2 = coordinates[1][0]
        y2 = coordinates[1][1]
        L = self.length
        
        if x2 <= x1 and y2 <= y1:
            x2new = x1
            x1new = x2
            x2 = x2new
            x1 = x1new
            y2new = y1
            y1new = y2
            y2 = y2new
            y1 = y1new
        
        c = (x2 - x1) / L
        s = (y2 - y1) / L

        w1 = w * c
        w2 = -w * s 

        self.Add_Load_Full_Uniform(-w1, True)
        self.Add_Load_Axial_Uniform(-w2, True)
        
        if not w in self.uniform_full_load_fy:
            self.uniform_full_load_fy.append(w)

    
    def Add_Load_Full_Uniform_Fx(self, w): # OKAY!
        nodes = self.nodes
        coordinates = []
        for node in nodes:
            coordinates.append(nodes[node])
        x1 = coordinates[0][0]
        y1 = coordinates[0][1]
        x2 = coordinates[1][0]
        y2 = coordinates[1][1]
        L = self.length
        
        if x2 <= x1 and y2 <= y1:
            x2new = x1
            x1new = x2
            x2 = x2new
            x1 = x1new
            y2new = y1
            y1new = y2
            y2 = y2new
            y1 = y1new
            
        c = (x2 - x1) / L
        s = (y2 - y1) / L

        w1 = w * s        
        w2 = w * c 

        self.Add_Load_Full_Uniform(w1, True)
        self.Add_Load_Axial_Uniform(w2, True)
    
        if not w in self.uniform_full_load_fx:
            self.uniform_full_load_fx.append(w)


    def Add_Load_Point(self, P, a): # OKAY
        L = self.length
        beginning_moment = P * (L-a)**2 * a / L**2
        end_moment = -P * a**2 * (L-a)/L**2
        beginning_shear = (P*(L-a) + beginning_moment + end_moment) / L
        end_shear = (-P*a + end_moment + beginning_moment) / L

        if self.moment_release_left == 1 and self.moment_release_right == 0:
            beginning_shear = (beginning_shear - 3 / (2*L) * beginning_moment)
            end_shear = (-end_shear + 3 / (2*L) * beginning_moment)
            end_moment = end_moment - 1 / 2 * beginning_moment
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
            self.forces[self.node_list[1]][2] += end_moment
        elif self.moment_release_left == 0 and self.moment_release_right == 1:
            beginning_shear = (beginning_shear - 3 / (2*L) * end_moment)
            end_shear = (-end_shear + 3 / (2*L) * end_moment)
            beginning_moment = beginning_moment - 1 / 2 * end_moment
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
            self.forces[self.node_list[0]][2] += beginning_moment
        elif self.moment_release_right == 1 and self.moment_release_right == 1:
            beginning_shear = (beginning_shear - 1 / L * (beginning_moment + end_moment))
            end_shear = (-end_shear + 1 / L * (beginning_moment + end_moment))
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
        else:
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += end_shear
            self.forces[self.node_list[0]][2] += beginning_moment
            self.forces[self.node_list[1]][2] += end_moment


        # Shear Values
        shear_values = self.x_array.copy()
        for index, x in enumerate(self.x_array):
            if x <= a:
                shear_values[index] = beginning_shear
            else:
                shear_values[index] = beginning_shear - P

        self.shear += shear_values

        # Moment Values
        if self.moment_release_left == 1:
            beginning_moment = 0

        moment_values = self.x_array.copy()
        for index, x in enumerate(self.x_array):
            if x <= a:
                moment_values[index] = beginning_moment  - beginning_shear * x
            else:
                moment_values[index] = beginning_moment  - beginning_shear * x + P * (x - a)
        self.moment += moment_values    

        if not a in self.points_of_interest:
            self.points_of_interest.append(a)
            self.point_load.append([P,a])
   
   
    def Add_Load_Full_Uniform(self, w, skip_part=False): # OKAY!
        L = self.length
        
        beginning_moment = w * L**2 / 12
        end_moment = -w * L**2 / 12
        beginning_shear = w * L / 2
        end_shear = w * L / 2
    
        if self.moment_release_left == 1 and self.moment_release_right == 0:
            beginning_shear = (beginning_shear - 3 / (2*L) * beginning_moment)
            end_shear = (end_shear + 3 / (2*L) * beginning_moment)
            end_moment = end_moment - 1 / 2 * beginning_moment
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
            self.forces[self.node_list[1]][2] += end_moment
        elif self.moment_release_left == 0 and self.moment_release_right == 1:
            beginning_shear = (beginning_shear - 3 / (2*L) * end_moment)
            end_shear = (end_shear + 3 / (2*L) * end_moment)
            beginning_moment = beginning_moment - 1 / 2 * end_moment
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
            self.forces[self.node_list[0]][2] += beginning_moment
        elif self.moment_release_right == 1 and self.moment_release_right == 1:
            beginning_shear = (beginning_shear - 1 / L * (beginning_moment + end_moment))
            end_shear = (end_shear + 1 / L * (beginning_moment + end_moment))
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
        else:
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
            self.forces[self.node_list[0]][2] += beginning_moment
            self.forces[self.node_list[1]][2] += end_moment
        
        # Shear Values
        shear_values = self.x_array.copy()
        for index, shear_value in enumerate(shear_values):
            shear_values[index] = beginning_shear - w * shear_value
        
        # Moment Values
        if self.moment_release_left == 1:
            beginning_moment = 0
        moment_values = self.x_array.copy()
        for index, moment_value in enumerate(moment_values):
            moment_values[index] = beginning_moment - beginning_shear * moment_value + w * moment_value**2 / 2

        self.shear += shear_values
        self.moment += moment_values
        
        if not skip_part:
            if not w in self.uniform_full_load:
                self.uniform_full_load.append(w)


    # def Add_Load_Moment(self,M,a): #TODO Recheck values for all quadrants
    #     L = self.length
    #     b = L - a
    #     beginning_moment = M * b * (2*a-b) / L**2
    #     end_moment = M * a * (2*b-a) / L**2

    #     if self.moment_release_left == 1 and self.moment_release_right == 0:
    #         end_moment = end_moment - 1 / 2 * beginning_moment
    #         self.forces[self.node_list[1]][2] += end_moment
    #     elif self.moment_release_left == 0 and self.moment_release_right == 1:
    #         beginning_moment = beginning_moment - 1 / 2 * end_moment
    #         self.forces[self.node_list[0]][2] += beginning_moment
    #     elif self.moment_release_right == 1 and self.moment_release_right == 1:
    #         pass
    #     else:
    #         self.forces[self.node_list[0]][2] += beginning_moment
    #         self.forces[self.node_list[1]][2] += end_moment

        
    #     # Moment Values
    #     if self.moment_release_left == 1:
    #         beginning_moment = 0
    #     moment_values = self.x_array.copy()
    #     for index, _ in enumerate(moment_values):
    #         moment_values[index] = beginning_moment
    #     self.moment += moment_values


    def Add_Load_Partial_Uniform(self, w, a, b): #TODO Recheck values for all quadrants
        L = self.length
        beginning_moment = w*L**2/12 * (6*(b/L)**2 - 8*(b/L)**3 + 3*(b/L)**4) - w*L**2/12 * (6*(a/L)**2 - 8*(a/L)**3 + 3*(a/L)**4)
        end_moment =  - w*L**2/12 * (4*(b/L)**3 - 3*(b/L)**4) + w*L**2/12 * (4*(a/L)**3 - 3*(a/L)**4)
        beginning_shear = w * (b-a) / L * ((b-a)/2 + (L-b)) 
        end_shear = w * (b-a) / L * ((b-a)/2 + a) 

        if self.moment_release_left == 1 and self.moment_release_right == 0:
            beginning_shear = (beginning_shear - 3 / (2*L) * beginning_moment)
            end_shear = (end_shear + 3 / (2*L) * beginning_moment)
            end_moment = end_moment - 1 / 2 * beginning_moment
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
            self.forces[self.node_list[1]][2] += end_moment
        elif self.moment_release_left == 0 and self.moment_release_right == 1:
            beginning_shear = (beginning_shear - 3 / (2*L) * end_moment)
            end_shear = (end_shear + 3 / (2*L) * end_moment)
            beginning_moment = beginning_moment - 1 / 2 * end_moment
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
            self.forces[self.node_list[0]][2] += beginning_moment
        elif self.moment_release_right == 1 and self.moment_release_right == 1:
            beginning_shear = (beginning_shear - 1 / L * (beginning_moment + end_moment))
            end_shear = (end_shear + 1 / L * (beginning_moment + end_moment))
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
        else:
            self.forces[self.node_list[0]][1] += - beginning_shear
            self.forces[self.node_list[1]][1] += - end_shear
            self.forces[self.node_list[0]][2] += beginning_moment
            self.forces[self.node_list[1]][2] += end_moment

        # Shear Values
        shear_values = self.x_array.copy()
        for index, shear_value in enumerate(shear_values):
            if shear_value < a:
                shear_values[index] = beginning_shear
            elif shear_value >= a and shear_value < b :
                shear_values[index] = beginning_shear - w*(shear_value - a)
            else:
                shear_values[index] = beginning_shear - w*(b - a)

        self.shear += shear_values

        # Moment Values
        # if self.moment_release_left == 1:
        #     beginning_moment = 0
        moment_values = self.x_array.copy()
        for index, moment_value in enumerate(moment_values): #TODO FIX MOMENT VALUES
            if moment_value < a:
                moment_values[index] = beginning_moment - beginning_shear * moment_value
            elif moment_value >= a and moment_value < b :
                moment_values[index] = beginning_moment - beginning_shear * moment_value + w*(moment_value - a)**2 / 2
            else:
                moment_values[index] = beginning_moment - beginning_shear * moment_value + w * (b - a) * ((b-a)/2 + (moment_value - b))

        self.moment += moment_values


    def Plot_Axial_Diagram(self, figure_size=[10,5], show_annoation = True): # OKAY

        range = int(np.ceil(self.length)/self.division_spacing)
        x_array = np.linspace(0,1,range)

        plt.figure(figsize=figure_size)
        plt.plot(x_array,self.axial, marker='o')
        plt.fill_between(x_array, 0, self.axial, hatch = '/', alpha = 0.1)
        plt.xlim([-0.1, 1.1])
        # plt.plot(self.x_array,self.axial, marker='o')
        # plt.fill_between(self.x_array, 0, self.axial, hatch = '/', alpha = 0.1)
        # plt.xlim([0, self.length])
        plt.ylabel('Axial')
        plt.xlabel('Length ratio, Length = {}'.format(self.length))
        plt.title('Axial Diagram of Member {}'.format(self.member_number))

        if show_annoation:
            for i, text in enumerate(self.axial):
                plt.annotate(round(text,2), (x_array[i], self.axial[i]))

        plt.tight_layout()
        plt.show()



    # Plot Shear Diagram
    def Plot_Shear_Diagram(self, figure_size=[10,5], show_annotation = True):
        
        range = int(np.ceil(self.length)/self.division_spacing)
        x_array = np.linspace(0,1,range)

        plt.figure(figsize=figure_size)
        plt.plot(x_array,self.shear, marker='o')
        plt.fill_between(x_array, 0, self.shear, hatch = '/', alpha = 0.1)
        plt.xlim([-0.1, 1.1])
        # plt.plot(self.x_array,self.shear, marker='o')
        # plt.fill_between(self.x_array, 0, self.shear, hatch = '/', alpha = 0.1)
        # plt.xlim([0, self.length])
        plt.ylabel('Shear')
        plt.xlabel('Length ratio, Length = {}'.format(self.length))
        plt.title('Shear Diagram of Member {}'.format(self.member_number))

        if show_annotation:
            for i, text in enumerate(self.shear):
                plt.annotate(round(text,2), (x_array[i], self.shear[i]))
        
        plt.xticks(x_array)
        plt.tight_layout()
        plt.show()


    # Plot Moment Diagram
    def Plot_Moment_Diagram(self, figure_size = [10,5], show_annotation = True):

        range = int(np.ceil(self.length)/self.division_spacing)
        x_array = np.linspace(0,1,range)

        plt.figure(figsize=figure_size)
        plt.plot(x_array,-self.moment, marker='o')
        plt.fill_between(x_array, 0, -self.moment, hatch = '/', alpha = 0.1)
        plt.xlim([-0.1, 1.1])
        # plt.plot(self.x_array,-self.moment, marker='o')
        # plt.fill_between(self.x_array, 0, -self.moment, hatch = '/', alpha = 0.1)
        # plt.xlim([0, self.length])
        plt.ylabel('Moment')
        plt.xlabel('Length ratio, Length = {}'.format(self.length))
        plt.title('Moment Diagram of Member {}'.format(self.member_number))

        if show_annotation:
            for i, text in enumerate(self.moment):
                plt.annotate(round(-text,2), (x_array[i], -self.moment[i]))

        plt.xticks(x_array)
        plt.tight_layout()
        plt.show()


    def Resolve_Forces_into_Components(self): # OKAY!
        self.Compile_Member_Forces()
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

        if y2 >= y1 and x2 >= x1: # 0 to 90 degrees
            c = (x2 - x1) / L
            s = (y2 - y1) / L
        elif y2 >= y1 and x1 >= x2: # 91 to 180 degrees
            c = (x2 - x1) / L
            s = (y2 - y1) / L
        elif y1 >= y2 and x1 >= x2: # 181 to 270 degrees
            c = (x1 - x2) / L
            s = (y1 - y2) / L            
        else: # 271 to 360 degrees
            c = (x2 - x1) / L
            s = (y2 - y1) / L 

        FA_1 = self.forces[self.node_list[0]][0] 
        FA_2 = self.forces[self.node_list[1]][0] 
        FV_1 = self.forces[self.node_list[0]][1] 
        FV_2 = self.forces[self.node_list[1]][1] 
        M_1 = self.forces[self.node_list[0]][2] 
        M_2 = self.forces[self.node_list[1]][2] 

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
        
        self.resolved_forces[self.node_list[1]][0] = FV2_x + FA_2_x
        self.resolved_forces[self.node_list[1]][1] = FV2_y + FA_2_y

        if x2 >= x1 and y2 >= y1: # 0 to 90 degrees
            self.resolved_forces[self.node_list[0]][2] = - M_1
            self.resolved_forces[self.node_list[1]][2] = - M_2
        elif x1 >= x2 and y2 >= y1: # 91 to 180 degrees
            self.resolved_forces[self.node_list[0]][2] = - M_1
            self.resolved_forces[self.node_list[1]][2] = - M_2
        elif x1 >= x2 and y1 >= y2: # 181 to 270 degrees
            self.resolved_forces[self.node_list[0]][2] = - M_1
            self.resolved_forces[self.node_list[1]][2] = - M_2
        else: # 271 to 359
            self.resolved_forces[self.node_list[0]][2] = - M_1
            self.resolved_forces[self.node_list[1]][2] = - M_2

    def Reaction_Add_Shear_At_Left_Support(self, shear): # OKAY
        shear_values = self.x_array.copy()
        for index, _ in enumerate(shear_values):
            shear_values[index] = shear
        self.shear += shear_values

        moment_values = self.x_array.copy()
        for index, moment_value in enumerate(moment_values):
            moment_values[index] = -shear * moment_value
        self.moment += moment_values


    def Reaction_Add_Moment_At_Left_Support(self, moment): # OKAY
        moment_values = self.x_array.copy()
        for index, _ in enumerate(moment_values):
            moment_values[index] = moment
        self.moment += moment_values


    def Reaction_Add_Axial_At_Left_Support(self, axial): # OKAY
        axial_values = self.x_array.copy()
        for index, _ in enumerate(axial_values):
            axial_values[index] = axial
        self.axial += axial_values


    def Plot_Diagrams(self, figure_size = [15,10], show_annotation = True): # OKAY
        fig, axs = plt.subplots(3, 1)
        fig.set_figheight(figure_size[0])
        fig.set_figwidth(figure_size[1])

        # range = int(np.ceil(self.length)/self.division_spacing)
        # x_array_relative = np.linspace(0,1,range)
        x_array_relative = self.x_array / np.ceil(self.length)

        # Plot Axial Diagram
        axs[0].plot(x_array_relative,self.axial, marker = 'o')
        axs[0].fill_between(x_array_relative, 0, self.axial, hatch = '/', alpha = 0.1)
        axs[0].set_xlim([-0.1,1.1])
        axs[0].set_ylabel('Axial')
        axs[0].set_xlabel('Length ratio, Length = {}'.format(self.length))
        axs[0].set_title('Axial Diagram of Member {}'.format(self.member_number))
        
        if show_annotation == True:
            for i, text in enumerate(self.axial):
                axs[0].annotate(round(text,2), (x_array_relative[i], self.axial[i]))

        axs[0].margins(0.2)

        # Plot Shear Diagram
        axs[1].plot(x_array_relative,self.shear, marker = 'o')
        axs[1].fill_between(x_array_relative, 0, self.shear, hatch = '/', alpha = 0.1)
        axs[1].set_xlim([-0.1,1.1])
        axs[1].set_ylabel('Shear')
        axs[1].set_xlabel('Length ratio, Length = {}'.format(self.length))
        axs[1].set_title('Shear Diagram of Member {}'.format(self.member_number))

        if show_annotation == True:
            for i, text in enumerate(self.shear):
                axs[1].annotate(round(text,2), (x_array_relative[i], self.shear[i]))
        
        axs[1].margins(0.2)

        # Plot Moment Diagram
        axs[2].plot(x_array_relative,-self.moment, marker = 'o')
        axs[2].fill_between(x_array_relative, 0, -self.moment, hatch = '/', alpha = 0.1)
        axs[2].set_xlim([-0.1,1.1])
        axs[2].set_ylabel('Moment')
        axs[2].set_xlabel('Length ratio, Length = {}'.format(self.length))
        axs[2].set_title('Moment Diagram of Member {}'.format(self.member_number))

        if show_annotation == True:
            for i, text in enumerate(self.moment):
                axs[2].annotate(round(-text,2), (x_array_relative[i], -self.moment[i]))
        
        axs[2].margins(0.2)
        
        plt.tight_layout()
        plt.show()

    def Summary(self): # OKAY
        self.moment_max = -np.max(self.moment)
        self.moment_min = -np.min(self.moment)
        self.moment_at_left = -self.moment[0]
        self.moment_at_right = -self.moment[-1]
        
        self.shear_max = np.max(self.shear)
        self.shear_min = np.min(self.shear)
        self.shear_at_left = self.shear[0]
        self.shear_at_right = self.shear[-1]
        
        print("At Left End:")
        print("Axial: {}".format(self.axial[0]))
        print("Shear: {}".format(self.shear_at_left))
        print("Moment: {}".format(self.moment_at_left))
        print()
        print("At Right End:")
        print("Axial: {}".format(self.axial[-1]))
        print("Shear: {}".format(self.shear_at_right))
        print("Moment: {}".format(self.moment_at_right))
        print()
        print("Minimum and Maximum")
        print("Minimum Shear: {}".format(self.shear_min))
        print("Maximum Shear: {}".format(self.shear_max))
        print("Minimum Moment: {}".format(self.moment_min))
        print("Maximum Moment: {}".format(self.moment_max))
        
    # def Assemble_Member_Stiffness_Matrix(self):
    #     # moment_releases_left = self.member_moment_releases[element][0]
    #     # moment_releases_right = self.member_moment_releases[element][1]
        
    #     # from_point = elements[element][0]
    #     # to_point = elements[element][1]
    #     # from_node = nodes[from_point]
    #     # to_node = nodes[to_point]
        
    #     # compute length of member
    #     coordinates = []
    #     for node in self.nodes:
    #         coordinates.append(self.nodes[node])
    #     x1 = coordinates[0][0]
    #     y1 = coordinates[0][1]
    #     x2 = coordinates[1][0]
    #     y2 = coordinates[1][1]
        
    #     L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #     c = (x2 - x1)/L
    #     s = (y2 - y1)/L

    #     A = self.area
    #     I = self.inertia
    #     E = self.elasticity

    #     # if moment_releases_left == 1 and moment_releases_right == 1:
    #     #     k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,      0],
    #     #                                 [0,            0,      0,         0,     0,      0],
    #     #                                 [0,            0,      0,         0,     0,      0],
    #     #                                 [-A*L**2/I,    0,      0,  A*L**2/I,     0,      0],
    #     #                                 [0,            0,      0,         0,     0,      0],
    #     #                                 [0,            0,      0,         0,     0,      0]])
        
    #     # elif moment_releases_left == 1 and moment_releases_right == 0:
    #     #     k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,     0],
    #     #                                 [0,          3,        0,         0,   -3,    3*L],
    #     #                                 [0,          0,        0,         0,    0,      0],
    #     #                                 [-A*L**2/I,   0,       0,  A*L**2/I,    0,      0],
    #     #                                 [0,         -3,        0,         0,    3,    -3*L],
    #     #                                 [0,         3*L,       0,         0,  -3*L, 3*L**2]])
        
    #     # elif moment_releases_left == 0 and moment_releases_right == 1:
    #     #     k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,    0,    0],
    #     #                                 [0,            3,    3*L,         0,   -3,    0],
    #     #                                 [0,          3*L, 3*L**2,         0, -3*L,    0],
    #     #                                 [-A*L**2/I,   0,       0,  A*L**2/I,    0,    0],
    #     #                                 [0,          -3,    -3*L,         0,    3,    0],
    #     #                                 [0,           0,       0,         0,    0,    0]])

    #     # else:
    #     k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,      0],
    #                                 [0,          12,    6*L,         0,   -12,    6*L],
    #                                 [0,         6*L, 4*L**2,         0,  -6*L, 2*L**2],
    #                                 [-A*L**2/I,   0,      0,  A*L**2/I,     0,      0],
    #                                 [0,         -12,   -6*L,         0,    12,   -6*L],
    #                                 [0,         6*L, 2*L**2,         0,  -6*L, 4*L**2]])
        
    #     T = np.array([[c, s, 0 , 0, 0, 0],
    #                 [-s, c, 0, 0, 0, 0],
    #                 [0, 0, 1, 0, 0, 0],
    #                 [0, 0, 0, c, s, 0],
    #                 [0, 0, 0, -s, c, 0],
    #                 [0, 0, 0, 0, 0, 1]])

    #     K = np.transpose(T).dot(k).dot(T)

    #     return K        
        

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
            __local_member_forces_dict.update({i+1: np.array([force[0][0], -force[0][1], force[0][2], force[1][0], -force[1][1], force[1][2]])})
        
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

        # Compile all member releases
        member_moment_releases = {}
        for member in members_list:
            member_moment_releases.update({member.member_number: [member.moment_release_left, member.moment_release_right]})

        # Compile all member release coordinates for plotting
        moment_releases_coordinates = []
        for member in members_list:
            for m in member.release_node_coordinates:
                moment_releases_coordinates.append(m)

        self.nodes = nodes
        self.elements = elements
        self.forces = forces
        self.elasticities = elasticities
        self.areas = areas
        self.inertias = inertias
        self.local_member_forces = __local_member_forces_dict
        self.members_list = members_list
        self.member_moment_releases = member_moment_releases
        self.moment_releases_coordinates = moment_releases_coordinates

    
    def Add_Load_Node(self, nodal_load):
        forces = self.forces
        for key in forces: 
            if key in nodal_load:
                forces[key][0] += nodal_load[key][0] 
                forces[key][1] += nodal_load[key][1] 
                forces[key][2] += nodal_load[key][2] 
        self.forces.update(forces)


    def __Member_Lengths(self, element, nodes, elements):
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


    def __Assemble_Stiffness_Matrix(self, element, areas, nodes, elements, elasticities, inertias):
        moment_releases_left = self.member_moment_releases[element][0]
        moment_releases_right = self.member_moment_releases[element][1]
        
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

        if moment_releases_left == 1 and moment_releases_right == 1:
            k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,      0],
                                        [0,            0,      0,         0,     0,      0],
                                        [0,            0,      0,         0,     0,      0],
                                        [-A*L**2/I,    0,      0,  A*L**2/I,     0,      0],
                                        [0,            0,      0,         0,     0,      0],
                                        [0,            0,      0,         0,     0,      0]])
        
        elif moment_releases_left == 1 and moment_releases_right == 0:
            k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,      0],
                                        [0,            3,      0,         0,    -3,    3*L],
                                        [0,            0,      0,         0,     0,      0],
                                        [-A*L**2/I,    0,      0,  A*L**2/I,     0,      0],
                                        [0,           -3,      0,         0,     3,   -3*L],
                                        [0,          3*L,      0,         0,  -3*L, 3*L**2]])
        
        elif moment_releases_left == 0 and moment_releases_right == 1:
            k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,    0,    0],
                                        [0,            3,    3*L,         0,   -3,    0],
                                        [0,          3*L, 3*L**2,         0, -3*L,    0],
                                        [-A*L**2/I,   0,       0,  A*L**2/I,    0,    0],
                                        [0,          -3,    -3*L,         0,    3,    0],
                                        [0,           0,       0,         0,    0,    0]])

        else:
            k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,      0],
                                        [0,           12,    6*L,         0,   -12,    6*L],
                                        [0,          6*L, 4*L**2,         0,  -6*L, 2*L**2],
                                        [-A*L**2/I,    0,      0,  A*L**2/I,     0,      0],
                                        [0,          -12,   -6*L,         0,    12,   -6*L],
                                        [0,          6*L, 2*L**2,         0,  -6*L, 4*L**2]])
        
        T = np.array([[c, s, 0 , 0, 0, 0],
                     [-s, c, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, c, s, 0],
                     [0, 0, 0, -s, c, 0],
                     [0, 0, 0, 0, 0, 1]])

        K = np.transpose(T).dot(k).dot(T)

        return K


    def __Assemble_Global_Stiffness(self, K, k, i, j):
        dofs = [3*i-3, 3*i-2, 3*i-1, 3*j-3, 3*j-2, 3*j-1]
        K[np.ix_(dofs,dofs)] += k
        return K


    def __Support_Vector(self, restrained_dofs, nodes):
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


    def __Apply_Boundary_Conditions(self, support_vector, K_global):
        dofs = []

        for j in support_vector:
            dofs.append(j - 1)

        k = np.delete(K_global, obj = dofs, axis = 0)
        k_new = np.delete(k, obj = dofs, axis = 1)
        return k_new


    def __Assemble_Force_Vector(self, forces, support_vector, nodes):
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


    def __Frame_Global_Displacement(self, displacements, Support_Vector, nodes):
        # Create New Support Vector in python indexing
        support_vector_new = [x - 1 for x in Support_Vector]

        # Create Displacement Vector
        displacement_vector = np.zeros(3*len(nodes))

        # Creating global displacement vector that looks for all elements in the support vector and replacing the with value of 0 of that particular index
        j = 0

        # Looping displacement vectors indexes and looks for any of the value within the array "Support_Vector". Replaces with 0 if the value of the index is equal to any of the support vector.
        for i, _ in enumerate(displacement_vector):
            if np.any(np.isin(support_vector_new, i)):
                displacement_vector[i] = 0
            else:
                displacement_vector[i] = displacements[j]
                j += 1

        return displacement_vector


    def __Solve_Reactions(self, K_global, displacement_vector):
        return (K_global.dot(displacement_vector))


    def __Element_Displacement(self, element_number, global_displacement, elements):
        fromNode = elements[element_number][0]
        toNode = elements[element_number][1]

        u = [3 * fromNode - 2, 3 * fromNode - 1, 3 * fromNode, 
            3 * toNode - 2, 3 * toNode - 1, 3 * toNode]

        # u.sort()

        elem_displacements = []

        for _, u_node in enumerate(u):
            elem_displacements.append(global_displacement[u_node - 1])

        return elem_displacements


    def __Solve_Member_Force(self, element, element_displacements, areas, nodes, elements, elasticities, inertias):
        moment_releases_left = self.member_moment_releases[element][0]
        moment_releases_right = self.member_moment_releases[element][1]

        from_point = elements[element][0]
        to_point = elements[element][1]
        from_node = nodes[from_point]
        to_node = nodes[to_point]

        x1 = from_node[0]
        y1 = from_node[1]
        x2 = to_node[0]
        y2 = to_node[1]
        
        L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        if y2 >= y1 and x2 >= x1: # 0 to 90 degrees
            c = (x2 - x1) / L
            s = (y2 - y1) / L
        elif y2 >= y1 and x1 >= x2: # 91 to 180 degrees
            c = (x1 - x2) / L
            s = (y2 - y1) / L
        elif y1 >= y2 and x1 >= x2: # 181 to 270 degrees
            c = (x1 - x2) / L
            s = (y1 - y2) / L            
        else: # 271 to 360 degrees
            c = (x2 - x1) / L
            s = (y1 - y2) / L 
        
        
        # c = (x2 - x1)/L
        # s = (y2 - y1)/L

        A = areas[element]
        I = inertias[element]
        E = elasticities[element]
        u = element_displacements[element-1]
        

        if moment_releases_left == 1 and moment_releases_right == 1:
            k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,      0],
                                        [0,            0,      0,         0,     0,      0],
                                        [0,            0,      0,         0,     0,      0],
                                        [-A*L**2/I,    0,      0,  A*L**2/I,     0,      0],
                                        [0,            0,      0,         0,     0,      0],
                                        [0,            0,      0,         0,     0,      0]])
        
        elif moment_releases_left == 1 and moment_releases_right == 0:
            k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,     0,     0],
                                        [0,          3,        0,         0,   -3,    3*L],
                                        [0,          0,        0,         0,    0,      0],
                                        [-A*L**2/I,   0,       0,  A*L**2/I,    0,      0],
                                        [0,         -3,        0,         0,    3,    -3*L],
                                        [0,         3*L,       0,         0,  -3*L, 3*L**2]])
        
        elif moment_releases_left == 0 and moment_releases_right == 1:
            k = E * I / L**3 * np.array([[A*L**2/I,    0,      0, -A*L**2/I,    0,    0],
                                        [0,            3,    3*L,         0,   -3,    0],
                                        [0,          3*L, 3*L**2,         0, -3*L,    0],
                                        [-A*L**2/I,   0,       0,  A*L**2/I,    0,    0],
                                        [0,          -3,    -3*L,         0,    3,    0],
                                        [0,           0,       0,         0,    0,    0]])

        else:
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

    def __Displacements(self, displacements):

        displacements = {key + 1: displacements[key] for (key, _) in enumerate(displacements + 1)}

        displacements_dict = {}
        
        for displacement in range(1,int(len(displacements)/3 + 1)):
            displacements_dict.update({displacement: [float(displacements[3 * displacement - 2]), float(displacements[3 * displacement - 1]), float(displacements[3 * displacement]) ]})

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
            L = self.__Member_Lengths(element, nodes, elements)
            member_lengths.append(L)

        # Step 2: Assemble Stiffness Matrix for All members
        k_elems = []

        for element in elements:
            k_elems.append(self.__Assemble_Stiffness_Matrix(element, areas, nodes, elements, elasticities, inertias))

        # Step 3: Assemble Global Stiffness Matrix
        K_global = np.zeros([3*len(nodes), 3*len(nodes)])

        for i, _ in enumerate(k_elems):
            K_global = self.__Assemble_Global_Stiffness(K_global, k_elems[i], elements[i+1][0], elements[i+1][1])

        # Step 4: Apply Boundary conditions to reduce the Global Stiffness Matrix 
        Support_Vector = self.__Support_Vector(supports, nodes)
        K_new = self.__Apply_Boundary_Conditions(Support_Vector, K_global)

        # Step 5: Reduce Force Vector
        f_new = self.__Assemble_Force_Vector(forces, Support_Vector, nodes)

        # Step 6: Solve for Displacement
        # Remove all columns and rows with all 0 for stiffness matrix and forces
        zero_index = np.where(~K_new.any(axis=0))[0]
        K_new = np.delete(K_new, obj = zero_index, axis = 0)
        K_new = np.delete(K_new, obj = zero_index, axis = 1)
        f_new = np.delete(f_new, obj = zero_index, axis = 0)

        displacements = np.linalg.inv(K_new).dot(f_new.transpose())
        displacements = np.insert(displacements, zero_index, 0)

        # Step 7: Create Global Displacement Vector
        global_displacements = self.__Frame_Global_Displacement(displacements, Support_Vector, nodes)

        # Step 8: Solve for Reactions 
        forces_for_reactions = []
        for force in self.forces:
            for i in range(3):
                forces_for_reactions.append(self.forces[force][i])

        forces_for_reactions = np.array(forces_for_reactions)
        reactions = self.__Solve_Reactions(K_global, global_displacements) - forces_for_reactions

        # Step 9: Solve Member Displacements
        element_displacements = []

        for element in elements:
            element_displacements.append(self.__Element_Displacement(element, global_displacements, elements))

        # Step 10A: Solve Member Forces
        solved_member_forces = []

        for element in elements:
            solved_member_forces.append(self.__Solve_Member_Force(element, element_displacements, areas, nodes, elements, elasticities, inertias))
        solved_member_forces = {key: solved_member_forces[key-1] for key in elements}


        # Storing of Variables lists
        self.displacements_ = self.__Displacements(global_displacements)
        self.displacements_array_ = global_displacements
        self.reactions_ = self.__Reactions(reactions, supports)
        self.K_global_ = K_global
        self.K_reduced_ = K_new
        self.F_reduced_ = f_new
        self.element_displacements_ = element_displacements
        self.forces_for_reactions_ = forces_for_reactions

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
        self.__Update_Member_Local_Forces()
    
    def __Update_Member_Local_Forces(self):
        for element, member in enumerate(self.members_list):
            member.Reaction_Add_Axial_At_Left_Support(self.solved_member_forces[element + 1][0])
            member.Reaction_Add_Shear_At_Left_Support(self.solved_member_forces[element + 1][1])
            member.Reaction_Add_Moment_At_Left_Support(self.solved_member_forces[element + 1][2])


    def Draw_Frame_Setup(self, figure_size = None, linewidth = 2, offset = 0.12, length_of_arrow = 1.0, arrow_head_size = 0.05, arrow_line_width = 2, grid = True, node_size = 10, radius_of_arc = 0.2):
        '''
        Draws the Truss as initialized by the class
        
        Parameters
        ----------
        
        figure_size: array
                    size of the plot's figure in x, y heights.
        length_of_arrow: float
                        length of force vector arrow. default value is 1.0
        arrow_head_width: float
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
        areas = self.areas
        moment_releases_coordinates = self.moment_releases_coordinates

        average_area = []
        for area in areas:
            average_area.append(areas[area])
        average_area = np.array(average_area)
        average_area = np.average(average_area)

        plt.figure(figsize = figure_size)
        plt.grid(grid)
        ax = plt.gca()
       
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
            ax.plot([x1,x2],[y1,y2], marker = 'o', color = 'black', zorder = 5, linewidth = linewidth * areas[element] / average_area, markersize = node_size)

        # plotting supports
        for support in supports:

            support_x = supports[support][0]
            support_y = supports[support][1]
            support_z = supports[support][2]

            x = nodes[support][0]
            y = nodes[support][1]

            if support_x == 1 and support_y == 1 and support_z == 1:
                ax.scatter(x, y, marker = 's', s = 200, c='r', zorder = 2)
            elif support_x == 1 and support_y == 1 and support_z == 0:
                ax.scatter(x, y, marker = '^', s = 200, c='r', zorder = 2)
            else: 
                ax.scatter(x, y, marker = 'o', s = 200, c='y', zorder = 2)
    
        # plotting node labels
        # offset = 0.12
        
        for node in nodes:
            ax.annotate(node, (nodes[node][0]+offset, nodes[node][1]+offset), zorder = 10, c='black')
            
        # plotting member labels
        for element in elements:
            fromNode = elements[element][0]
            toNode = elements[element][1]
            from_point = nodes[fromNode]
            to_point = nodes[toNode]
            
            middlePoint = [abs((to_point[0] - from_point[0])/2) + min(from_point[0], to_point[0]), 
                           abs((to_point[1] - from_point[1])/2) + min(from_point[1], to_point[1])]
            
            ax.annotate(element, (middlePoint[0], middlePoint[1]), zorder = 10, c = 'b')
            
        # plotting force vectors
        # loop all x-direction forces
        for force in forces:
            x = nodes[force][0]
            y = nodes[force][1]

            f_x = np.round(forces[force][0],2)
            f_y = np.round(forces[force][1],2)
            M_x = np.round(forces[force][2],2)

            # plot arrow x-direction
            if f_x > 0:
                ax.arrow(x - length_of_arrow, y, length_of_arrow, 0, 
                          shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                ax.annotate(f_x, ((x - length_of_arrow), y + offset), c='red')
                ax.scatter(x - length_of_arrow, y, c='white')
            elif f_x < 0:
                ax.arrow(x + length_of_arrow, y, -length_of_arrow, 0, 
                          shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                ax.annotate(f_x, ((x + length_of_arrow), y + offset), c='red')
                ax.scatter(x + length_of_arrow,y, c='white')
            else:
                pass

            # plot arrow y-direction
            if f_y > 0:
                ax.arrow(x, y - length_of_arrow, 0, length_of_arrow,
                          shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                ax.annotate(f_y, (x + offset, (y - length_of_arrow)), c='red') 
                ax.scatter(x,y - length_of_arrow, c='white')
            elif f_y < 0:
                ax.arrow(x, y + length_of_arrow, 0, -length_of_arrow, 
                          shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                ax.annotate(f_y, (x + offset, (y + length_of_arrow)), c='red')
                ax.scatter(x,y + length_of_arrow, c='white')
            else:
                pass

            # plot moment arrows
            if M_x > 0:
                self.__drawCirc(ax,radius_of_arc,x,y,0,180,lw=arrow_line_width,direction="Positive")
                ax.annotate(M_x, (x, (y + radius_of_arc/1.5)), c='green')
            elif M_x < 0:
                self.__drawCirc(ax,radius_of_arc,x,y,0,180,lw=arrow_line_width,direction="Negative")
                ax.annotate(M_x, (x, (y + radius_of_arc/1.5)), c='green')
            else:
                pass
            
        # Plot Member Release Coordinates
        for member_release in moment_releases_coordinates:
            ax.scatter(member_release[0], member_release[1], color = 'lime', s = node_size * 10, zorder = 20)

        ax.axis('equal')
        plt.show()


    def Draw_Frame_Displacements_(self, linewidth = 2, magnification_factor = 100, figure_size = None, offset = 0.12):
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
        plt.axis('equal')
        plt.show()

    def __Reactions(self, reactions, supports):

        forces_dict = {key + 1: reactions[key] for (key, _) in enumerate(reactions + 1)}

        reactions_dict = {}
        for support in supports:
            reactions_dict.update({support: [float(forces_dict[3 * support - 2]), 
                                             float(forces_dict[3 * support-1]), 
                                             float(forces_dict[3 * support])]})

        return reactions_dict

    def __drawCirc(self, ax,radius,centX,centY,angle_,theta2_,color_='green',lw=2,direction="Positive"):
        # Arc
        arc = Arc((centX,centY),radius,radius,angle=angle_,
            theta1=0,theta2=theta2_,capstyle='round',linestyle='-',lw=lw,color=color_)
        ax.add_patch(arc)


        # Create the arrow head
        startX = centX-(radius/2)*np.cos(rad(theta2_+angle_))
        startY = centY-(radius/2)*np.sin(rad(theta2_+angle_))
        endX=centX+(radius/2)*np.cos(rad(theta2_+angle_)) #Do trig to determine end position
        endY=centY+(radius/2)*np.sin(rad(theta2_+angle_))

        if direction=="Positive":
            ax.add_patch(                    #Create triangle as arrow head
                RegularPolygon(
                    xy=(endX, endY),            # (x,y)
                    numVertices=3,                       # number of vertices
                    radius=radius/9,                # radius
                    orientation=rad(angle_+theta2_),     # orientation
                    color=color_
                )
            )
        else:
            ax.add_patch(                    #Create triangle as arrow head
                RegularPolygon(
                    xy=(startX, startY),            # (x,y)
                    numVertices=3,                       # number of vertices
                    radius=radius/9,                # radius
                    orientation=rad(angle_+theta2_),     # orientation
                    color=color_
                )
            )
        # ax.set_xlim([centX-radius,centY+radius]) and ax.set_ylim([centY-radius,centY+radius]) 
        # Make sure you keep the axes scaled or else arrow will distort

    def Draw_Reactions_(self, figure_size = None, linewidth = 2, offset = 0.12, length_of_arrow = 1.0, arrow_head_size = 0.05, arrow_line_width = 2, grid = True, node_size = 10, radius_of_arc = 0.2, show_ext_forces = False):
        '''
        Draws the Truss as initialized by the class
        
        Parameters
        ----------
        
        figure_size: array
                    size of the plot's figure in x, y heights.
        length_of_arrow: float
                        length of force vector arrow. default value is 1.0
        arrow_head_width: float
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
        areas = self.areas
        moment_releases_coordinates = self.moment_releases_coordinates
        reactions = self.reactions_

        average_area = []
        for area in areas:
            average_area.append(areas[area])
        average_area = np.array(average_area)
        average_area = np.average(average_area)

        plt.figure(figsize = figure_size)
        plt.grid(grid)
        ax = plt.gca()
       
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
            ax.plot([x1,x2],[y1,y2], marker = 'o', color = 'black', zorder = 5, linewidth = linewidth * areas[element] / average_area, markersize = node_size)

        # plotting supports
        for support in supports:

            support_x = supports[support][0]
            support_y = supports[support][1]
            support_z = supports[support][2]

            x = nodes[support][0]
            y = nodes[support][1]

            if support_x == 1 and support_y == 1 and support_z == 1:
                ax.scatter(x, y, marker = 's', s = 200, c='r', zorder = 2)
            elif support_x == 1 and support_y == 1 and support_z == 0:
                ax.scatter(x, y, marker = '^', s = 200, c='r', zorder = 2)
            else: 
                ax.scatter(x, y, marker = 'o', s = 200, c='y', zorder = 2)

        
    
        # plotting node labels
        # offset = 0.12
        
        for node in nodes:
            ax.annotate(node, (nodes[node][0]+offset, nodes[node][1]+offset), zorder = 10, c='black')
            
        # plotting member labels
        # for element in elements:
        #     fromNode = elements[element][0]
        #     toNode = elements[element][1]
        #     from_point = nodes[fromNode]
        #     to_point = nodes[toNode]
            
        #     middlePoint = [abs((to_point[0] - from_point[0])/2) + min(from_point[0], to_point[0]), 
        #                    abs((to_point[1] - from_point[1])/2) + min(from_point[1], to_point[1])]
            
        #     ax.annotate(element, (middlePoint[0], middlePoint[1]), zorder = 10, c = 'b')
            
        # plotting force vectors
        # loop all x-direction forces
        if show_ext_forces == True:
            for force in forces:
                x = nodes[force][0]
                y = nodes[force][1]

                f_x = np.round(forces[force][0],2)
                f_y = np.round(forces[force][1],2)
                M_x = np.round(forces[force][2],2)

                # plot arrow x-direction
                if f_x > 0:
                    ax.arrow(x - length_of_arrow, y, length_of_arrow, 0, 
                            shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                            linewidth = arrow_line_width)
                    ax.annotate(f_x, ((x - length_of_arrow), y + offset), c='red')
                    ax.scatter(x - length_of_arrow, y, c='white')
                elif f_x < 0:
                    ax.arrow(x + length_of_arrow, y, -length_of_arrow, 0, 
                            shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                            linewidth = arrow_line_width)
                    ax.annotate(f_x, ((x + length_of_arrow), y + offset), c='red')
                    ax.scatter(x + length_of_arrow,y, c='white')
                else:
                    pass

                # plot arrow y-direction
                if f_y > 0:
                    ax.arrow(x, y - length_of_arrow, 0, length_of_arrow,
                            shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                            linewidth = arrow_line_width)
                    ax.annotate(f_y, (x + offset, (y - length_of_arrow)), c='red') 
                    ax.scatter(x,y - length_of_arrow, c='white')
                elif f_y < 0:
                    ax.arrow(x, y + length_of_arrow, 0, -length_of_arrow, 
                            shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                            linewidth = arrow_line_width)
                    ax.annotate(f_y, (x + offset, (y + length_of_arrow)), c='red')
                    ax.scatter(x,y + length_of_arrow, c='white')
                else:
                    pass

                # plot moment arrows
                if M_x > 0:
                    self.__drawCirc(ax,radius_of_arc,x,y,0,180,lw=arrow_line_width,direction="Positive")
                    ax.annotate(M_x, (x, (y + radius_of_arc/1.5)), c='green')
                elif M_x < 0:
                    self.__drawCirc(ax,radius_of_arc,x,y,0,180,lw=arrow_line_width,direction="Negative")
                    ax.annotate(M_x, (x, (y + radius_of_arc/1.5)), c='green')
                else:
                    pass
            
        # Plot Member Release Coordinates
        for member_release in moment_releases_coordinates:
            ax.scatter(member_release[0], member_release[1], color = 'lime', s = node_size * 10, zorder = 20)

        # plotting support vectors
        # loop all x-direction forces
        for reaction in reactions:
            x = nodes[reaction][0]
            y = nodes[reaction][1]

            f_x = np.round(reactions[reaction][0],2)
            f_y = np.round(reactions[reaction][1],2)
            M_x = np.round(reactions[reaction][2],2)

            # plot arrow x-direction
            if f_x > 0:
                ax.arrow(x - length_of_arrow, y, length_of_arrow, 0, 
                          shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                ax.annotate(f_x, ((x - length_of_arrow), y + offset), c='red')
                ax.scatter(x - length_of_arrow, y, c='white')
            elif f_x < 0:
                ax.arrow(x + length_of_arrow, y, -length_of_arrow, 0, 
                          shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                ax.annotate(f_x, ((x + length_of_arrow), y + offset), c='red')
                ax.scatter(x + length_of_arrow,y, c='white')
            else:
                pass

            # plot arrow y-direction
            if f_y > 0:
                ax.arrow(x, y - length_of_arrow, 0, length_of_arrow,
                          shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                ax.annotate(f_y, (x + offset, (y - length_of_arrow)), c='red') 
                ax.scatter(x,y - length_of_arrow, c='white')
            elif f_y < 0:
                ax.arrow(x, y + length_of_arrow, 0, -length_of_arrow, 
                          shape = 'full', head_width = arrow_head_size, length_includes_head = True, color='r', zorder = 15,
                          linewidth = arrow_line_width)
                ax.annotate(f_y, (x + offset, (y + length_of_arrow)), c='red')
                ax.scatter(x,y + length_of_arrow, c='white')
            else:
                pass

            # plot moment arrows
            if M_x > 0:
                self.__drawCirc(ax,radius_of_arc,x,y,0,180,lw=arrow_line_width,direction="Positive")
                ax.annotate(M_x, (x, (y + radius_of_arc/1.5)), c='green')
            elif M_x < 0:
                self.__drawCirc(ax,radius_of_arc,x,y,0,180,lw=arrow_line_width,direction="Negative")
                ax.annotate(M_x, (x, (y + radius_of_arc/1.5)), c='green')
            else:
                pass

        ax.axis('equal')
        plt.show()
       
       
    def Draw_Moment_Diagram(self, figure_size = None, show_labels=False, grid=True, scale_factor=50, linewidth = 2, node_size = 10, dpi = 100):
    
        nodes = self.nodes
        elements = self.elements
        supports = self.supports      
        areas = self.areas
        linewidth = linewidth
        node_size = node_size
        
        average_area = []
        for area in areas:
            average_area.append(areas[area])
        average_area = np.array(average_area)
        average_area = np.average(average_area)
    
        plt.figure(figsize=figure_size, dpi=dpi)
        plt.grid(grid)
        ax = plt.gca()
        scale_factor = scale_factor

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
            ax.plot([x1,x2],[y1,y2], marker = 'o', 
                    color = 'black', zorder = 5, 
                    linewidth = linewidth * areas[element] / average_area, 
                    markersize = node_size)
            middlePoint = [abs((to_point[0] - from_point[0])/2) + min(from_point[0], to_point[0]), 
                abs((to_point[1] - from_point[1])/2) + min(from_point[1], to_point[1])]
            ax.annotate(element, (middlePoint[0], middlePoint[1]), zorder = 10, c = 'b') 
            
        for member in self.members_list:
            x = []
            y = []
            for _, array in member.nodes.items():
                x.append(array[0])
                y.append(array[1])

            # Rotation angle (in degrees)
            theta_deg = np.arctan2(y[1]-y[0],x[1]-x[0]) * 180 / np.pi
            theta_rad = np.deg2rad(theta_deg)  # convert to radians

            # Translation (dx, dy)
            dx = x[0]
            dy = y[0]
            
            # Scale factor
            scaled_member_moment = member.moment / scale_factor

            # Apply rotation
            x_rot = (member.x_array * np.cos(theta_rad) - scaled_member_moment * np.sin(theta_rad))
            y_rot = (member.x_array * np.sin(theta_rad) + scaled_member_moment * np.cos(theta_rad))

            # Apply translation
            x_final = x_rot + dx
            y_final = y_rot + dy
            
            # insert
            x_final = np.insert(x_final, 0, x[0])
            last_fron_end_index = len(x_final)
            x_final = np.insert(x_final, last_fron_end_index, x[-1])

            y_final = np.insert(y_final, 0, y[0])
            last_fron_end_index = len(y_final)
            y_final = np.insert(y_final, last_fron_end_index, y[-1])

            # Plot
            ax.plot(x_final, y_final, 'b-', linewidth = linewidth * areas[element] / average_area)
            
            moment = np.insert(member.moment, 0, x[0])
            last_fron_end_index = len(moment)
            moment = np.insert(moment, last_fron_end_index, x[-1])
            
            if show_labels:
                first = 0
                last = int(len(moment) - 1)
                for i, text in enumerate(moment):
                    if i != first and i != last:
                        plt.annotate(round(text,2), (x_final[i], y_final[i]))
            
            # plotting supports
            for support in supports:

                support_x = supports[support][0]
                support_y = supports[support][1]
                support_z = supports[support][2]

                x = nodes[support][0]
                y = nodes[support][1]

                if support_x == 1 and support_y == 1 and support_z == 1:
                    ax.scatter(x, y, marker = 's', s = 200, c='r', zorder = 2)
                elif support_x == 1 and support_y == 1 and support_z == 0:
                    ax.scatter(x, y, marker = '^', s = 200, c='r', zorder = 2)
                else: 
                    ax.scatter(x, y, marker = 'o', s = 200, c='y', zorder = 2)

        ax.axis('equal')
        ax.grid(True)

        plt.show()


    def Draw_Shear_Diagram(self, figure_size = None, show_labels=False, grid=True, scale_factor=50, linewidth = 2, node_size = 10, dpi = 100):
    
        nodes = self.nodes
        elements = self.elements
        supports = self.supports      
        areas = self.areas
        linewidth = linewidth
        node_size = node_size
        
        average_area = []
        for area in areas:
            average_area.append(areas[area])
        average_area = np.array(average_area)
        average_area = np.average(average_area)
    
        plt.figure(figsize=figure_size, dpi=dpi)
        plt.grid(grid)
        ax = plt.gca()
        scale_factor = scale_factor

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
            ax.plot([x1,x2],[y1,y2], marker = 'o', 
                    color = 'black', zorder = 5, 
                    linewidth = linewidth * areas[element] / average_area, 
                    markersize = node_size)
            middlePoint = [abs((to_point[0] - from_point[0])/2) + min(from_point[0], to_point[0]), 
                abs((to_point[1] - from_point[1])/2) + min(from_point[1], to_point[1])]
            ax.annotate(element, (middlePoint[0], middlePoint[1]), zorder = 10, c = 'b') 

        for member in self.members_list:
            x = []
            y = []
            for _, array in member.nodes.items():
                x.append(array[0])
                y.append(array[1])

            # Rotation angle (in degrees)
            theta_deg = np.arctan2(y[1]-y[0],x[1]-x[0]) * 180 / np.pi
            theta_rad = np.deg2rad(theta_deg)  # convert to radians

            # Translation (dx, dy)
            dx = x[0]
            dy = y[0]
            
            # Scale factor
            scaled_member_shear = member.shear / scale_factor

            # Apply rotation
            x_rot = (member.x_array * np.cos(theta_rad) - scaled_member_shear * np.sin(theta_rad))
            y_rot = (member.x_array * np.sin(theta_rad) + scaled_member_shear * np.cos(theta_rad))

            # Apply translation
            x_final = x_rot + dx
            y_final = y_rot + dy
            
            # insert
            x_final = np.insert(x_final, 0, x[0])
            last_fron_end_index = len(x_final)
            x_final = np.insert(x_final, last_fron_end_index, x[-1])

            y_final = np.insert(y_final, 0, y[0])
            last_fron_end_index = len(y_final)
            y_final = np.insert(y_final, last_fron_end_index, y[-1])

            # Plot
            ax.plot(x_final, y_final, 'm-', linewidth = linewidth * areas[element] / average_area)
            
            shear = np.insert(member.shear, 0, x[0])
            last_fron_end_index = len(shear)
            shear = np.insert(shear, last_fron_end_index, x[-1])
            
            if show_labels:
                first = 0
                last = int(len(shear) - 1)
                for i, text in enumerate(shear):
                    if i != first and i != last:
                        plt.annotate(round(text,2), (x_final[i], y_final[i]))
            
            # plotting supports
            for support in supports:

                support_x = supports[support][0]
                support_y = supports[support][1]
                support_z = supports[support][2]

                x = nodes[support][0]
                y = nodes[support][1]

                if support_x == 1 and support_y == 1 and support_z == 1:
                    ax.scatter(x, y, marker = 's', s = 200, c='r', zorder = 2)
                elif support_x == 1 and support_y == 1 and support_z == 0:
                    ax.scatter(x, y, marker = '^', s = 200, c='r', zorder = 2)
                else: 
                    ax.scatter(x, y, marker = 'o', s = 200, c='y', zorder = 2)

        ax.axis('equal')
        ax.grid(True)

        plt.show()


    def Draw_Axial_Diagram(self, figure_size = None, show_labels=False, grid=True, scale_factor=300, linewidth = 2, node_size = 10, dpi=100):
    
        nodes = self.nodes
        elements = self.elements
        supports = self.supports      
        areas = self.areas
        linewidth = linewidth
        node_size = node_size
        
        average_area = []
        for area in areas:
            average_area.append(areas[area])
        average_area = np.array(average_area)
        average_area = np.average(average_area)
    
        plt.figure(figsize=figure_size, dpi=dpi)
        plt.grid(grid)
        ax = plt.gca()
        scale_factor = scale_factor

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
            ax.plot([x1,x2],[y1,y2], marker = 'o', 
                    color = 'black', zorder = 5, 
                    linewidth = linewidth * areas[element] / average_area, 
                    markersize = node_size)
            middlePoint = [abs((to_point[0] - from_point[0])/2) + min(from_point[0], to_point[0]), 
                abs((to_point[1] - from_point[1])/2) + min(from_point[1], to_point[1])]
            ax.annotate(element, (middlePoint[0], middlePoint[1]), zorder = 10, c = 'b') 

        for member in self.members_list:
            x = []
            y = []
            for _, array in member.nodes.items():
                x.append(array[0])
                y.append(array[1])

            # Rotation angle (in degrees)
            theta_deg = np.arctan2(y[1]-y[0],x[1]-x[0]) * 180 / np.pi
            theta_rad = np.deg2rad(theta_deg)  # convert to radians

            # Translation (dx, dy)
            dx = x[0]
            dy = y[0]
            
            # Scale factor
            scaled_member_axial = member.axial / scale_factor

            # Apply rotation
            x_rot = (member.x_array * np.cos(theta_rad) - scaled_member_axial * np.sin(theta_rad))
            y_rot = (member.x_array * np.sin(theta_rad) + scaled_member_axial * np.cos(theta_rad))

            # Apply translation
            x_final = x_rot + dx
            y_final = y_rot + dy
            
            # insert
            x_final = np.insert(x_final, 0, x[0])
            last_fron_end_index = len(x_final)
            x_final = np.insert(x_final, last_fron_end_index, x[-1])

            y_final = np.insert(y_final, 0, y[0])
            last_fron_end_index = len(y_final)
            y_final = np.insert(y_final, last_fron_end_index, y[-1])

            # Plot
            ax.plot(x_final, y_final, 'r-', linewidth = linewidth * areas[element] / average_area)
            
            axial = np.insert(member.axial, 0, x[0])
            last_fron_end_index = len(axial)
            axial = np.insert(axial, last_fron_end_index, x[-1])
            
            if show_labels:
                first = 0
                last = int(len(axial) - 1)
                for i, text in enumerate(axial):
                    if i != first and i != last:
                        plt.annotate(round(text,2), (x_final[i], y_final[i]))
            
            # plotting supports
            for support in supports:

                support_x = supports[support][0]
                support_y = supports[support][1]
                support_z = supports[support][2]

                x = nodes[support][0]
                y = nodes[support][1]

                if support_x == 1 and support_y == 1 and support_z == 1:
                    ax.scatter(x, y, marker = 's', s = 200, c='r', zorder = 2)
                elif support_x == 1 and support_y == 1 and support_z == 0:
                    ax.scatter(x, y, marker = '^', s = 200, c='r', zorder = 2)
                else: 
                    ax.scatter(x, y, marker = 'o', s = 200, c='y', zorder = 2)

        ax.axis('equal')
        ax.grid(True)

        plt.show()
