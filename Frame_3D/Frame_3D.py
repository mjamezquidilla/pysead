#%%
import numpy as np 

def assemble_local_stiffness_matrix(L: float, A: float, Iz:float, Iy:float, J:float, E:float, G:float) -> np.ndarray:
    '''
    Assembles the local stiffness matrix of a 3D beam
    L - Length of Beam
    A - Cross-sectional Area of the beam
    Iz - Major Direction of the beam's moment of inertia 
    Iy - Minor Direction of the beam's moment of inertia
    J - Polar Moment of Inertia of the beam
    E - Modulus of Elasticity of the beam
    G - Shear Modulus of the beam
    '''
    
    K1 = A * L**2
    K2 = 12 * Iz
    K3 = 6 * L * Iz
    K4 = 12 * Iy
    K5 = -6*L*Iy
    K6 = G*J*L**2/E
    K7 = -6*L*Iy 
    K8 = 4*L**2*Iy
    K9 = 6*L*Iz
    K10 = 4*L**2*Iz

    k1 = np.zeros((6,6))

    k1[0,0] = K1
    k1[1,1] = K2
    k1[5,1] = K3 
    k1[2,2] = K4
    k1[4,2] = K5 
    k1[3,3] = K6 
    k1[2,4] = K7 
    k1[4,4] = K8 
    k1[1,5] = K9 
    k1[5,5] = K10
    
    k2 = np.zeros((6,6))

    k2[0,0] = -K1
    k2[1,1] = -K2
    k2[5,1] = K3 
    k2[2,2] = -K4
    k2[4,2] = K5 
    k2[3,3] = -K6 
    k2[2,4] = -K7 
    k2[4,4] = K8 /2
    k2[1,5] = -K9 
    k2[5,5] = K10 / 2

    top_row = np.hstack([k1,k2])
    bottom_row = np.hstack([k2,k1])
    K = np.vstack([top_row,bottom_row])
    K_beam = E / L**3 * K
    return K_beam

def transformation_matrix(Xb: float,Yb: float,Zb: float,Xe: float,Ye: float,Ze: float, angle: float) -> np.ndarray:
    '''
    Computes the transformation matrix of the local beam axis to the global axis
    Xb - beginning of the beam x-coordinate based on the global axis
    Yb - beginning of the beam y-coordinate based on the global axis
    Zb - beginning of the beam z-coordinate based on the global axis
    Xe - end of the beam x-coordinate based on the global axis
    Ye - end of the beam y-coordinate based on the global axis
    Ze - end of the beam z-coordinate based on the global axis
    angle - relative angle of the beam based on its own beam axis from 0 to 90 degrees. Clockwise rotation is positive. (degrees)
    '''
    L = np.sqrt((Xe - Xb)**2 + (Ye - Yb)**2 + (Ze - Zb)**2)
    
    # 1st row 
    rxX = (Xe - Xb) / L 
    rxY = (Ye - Yb) / L
    rxZ = (Ze - Zb) / L

    if Xe == Xb and Ze == Zb:
        if Ye > Yb:
            r = np.array([[0, rxY, 0],
                        [-rxY* np.cos(np.deg2rad(angle)), 0, np.sin(np.deg2rad(angle))],
                        [rxY*np.sin(np.deg2rad(angle)), 0, np.cos(np.deg2rad(angle))]])

        else:
            r = np.array([[0, rxY, 0],
                        [rxY* np.cos(np.deg2rad(angle)), 0, -np.sin(np.deg2rad(angle))],
                        [-rxY*np.sin(np.deg2rad(angle)), 0, -np.cos(np.deg2rad(angle))]])

    else:
        # 2nd row
        ryX = (-rxX * rxY * np.cos(np.deg2rad(angle)) - rxZ * np.sin(np.deg2rad(angle))) / (np.sqrt(rxX**2 + rxZ**2))
        ryY = np.sqrt(rxX**2 + rxZ**2) * np.cos(np.deg2rad(angle))
        ryZ = (-rxY * rxZ * np.cos(np.deg2rad(angle)) + rxX * np.sin(np.deg2rad(angle))) / (np.sqrt(rxX**2 + rxZ**2))

        # 3rd row
        rzX = (rxX * rxY * np.sin(np.deg2rad(angle)) - rxZ * np.cos(np.deg2rad(angle))) / (np.sqrt(rxX**2 + rxZ**2))
        rzY = -np.sqrt(rxX**2 + rxZ**2) * np.sin(np.deg2rad(angle))
        rzZ = (rxY * rxZ * np.sin(np.deg2rad(angle)) + rxX * np.cos(np.deg2rad(angle))) / (np.sqrt(rxX**2 + rxZ**2))

        # construct transformation matrix
        r = np.array([[rxX, rxY, rxZ],
                      [ryX, ryY, ryZ],
                      [rzX, rzY, rzZ]])
        
    zero_matrix = np.zeros((3,3))
    first_row = np.hstack([r,zero_matrix, zero_matrix, zero_matrix])
    second_row = np.hstack([zero_matrix, r, zero_matrix, zero_matrix])
    third_row = np.hstack([zero_matrix, zero_matrix, r, zero_matrix])
    fourth_row = np.hstack([zero_matrix, zero_matrix, zero_matrix, r])

    R = np.vstack([first_row, second_row, third_row, fourth_row])

    return R

def assemble_global_stiffness_matrix(k: np.ndarray, r: np.ndarray):
    '''
    Computes the global stiffness matrix of a beam
    k - local stiffness matrix
    r - transformation matrix
    '''
    return np.transpose(r) @ k @ r



#%%
# k1 = assemble_local_stiffness_matrix(L = 240, A = 32.9, Iz=716, Iy=236, J=15.1, E=29_000, G=11_500)
# r1 = transformation_matrix(-20,0,0,0,0,0,0)
# print(r1)
# K1= assemble_global_stiffness_matrix(k1,r1)
# print(K1)
#
#
# k2 = assemble_local_stiffness_matrix(L = 240, A = 32.9, Iz=716, Iy=236, J=15.1, E=29_000, G=11_500)
# r2 = transformation_matrix(0,-20,0,0,0,0,90)
# print(k2)
# print(r2)
# K2= assemble_global_stiffness_matrix(k2,r2)
# print(K2)
#
#
# k3 = assemble_local_stiffness_matrix(L = 240, A = 32.9, Iz=716, Iy=236, J=15.1, E=29_000, G=11_500)
r3 = transformation_matrix(0,0,-20,0,0,0,30)
print(r3)
# K3= assemble_global_stiffness_matrix(k3,r3)
# print(K3)

# %%
