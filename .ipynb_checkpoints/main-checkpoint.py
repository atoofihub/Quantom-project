import pandas as pd
import numpy as np
from itertools import product

L = 5

def vertex_xyz(Vertex_Number):
    z = 1
    if(Vertex_Number % 2 == 0):
        z = 0
        
    y = int( Vertex_Number // (2 * L) )
    
    x = int( (Vertex_Number % (2 * L) ) // 2 )
    
    return x,y,z

def vertex_number(x,y,z):
    return 2*x + 2*L*y + z

def Qbit_from_vertex_corrdinate(x,y,z):
    
    spine_1 = 0
    spine_2 = 0
    spine_3 = 0
    
    if z == 0:
        
        if x != 0 and y != 0:
            spine_1 = 3*L*y + 3*x ; spine_2 = 3*L*y + 3*x +1 ; spine_3 = 3*L*y + 3*x - 1;
             
        elif x == y:
            spine_1 = 0 ; spine_2 = 1 ; spine_3 = 3*L - 1;
             
        elif x != 0 and y == 0:
            spine_1 = 3*L*y + 3*x ; spine_2 = 3*L*y + 3*x +1 ; spine_3 = 3*L*y + 3*x - 1;
             
        elif x == 0 and y != 0:
            spine_1 = 3*L*y + 3*x ; spine_2 = 3*L*y + 3*x +1 ; spine_3 = 3*L*(y + 1) + 3*x - 1;
        
        
    elif z == 1:
        
        if x != (L-1) and y != (L-1):
            spine_1 = 3*L*y + 3*x + 2 ; spine_2 = 3*L*y + 3*x + 3*L + 3 ; spine_3 = 3*L*y + 3*x + 1;
             
        elif x == (L-1) and  y != (L-1):
            spine_1 = 3*L*y + 3*x + 2 ; spine_2 = 3*L*y + 3*L  ; spine_3 = 3*L*y + 3*x + 1;
             
        elif x != (L-1) and y == (L-1):
            spine_1 = 3*L*y + 3*x + 2 ; spine_2 =  3*x + 3 ; spine_3 = 3*L*y + 3*x + 1;

        elif x == y == (L-1) :
            spine_1 = 3*L*y + 3*x + 2 ; spine_2 = 0 ; spine_3 = 3*L*y + 3*x + 1;
             
    else : 
        print("your z has not true value")
        return 0
    
    return spine_1,spine_2,spine_3

for beta in range(1,10,1):
    beta = beta/10
    
    keyList = list(product([-1,1], repeat=3))
    Phi = {key: [] for key in keyList}
    
    for i in range(11):
        df_sheet_index = pd.read_excel("L=5/total_configurations_5_{}.xlsx".format(beta), sheet_name=i)
        data = df_sheet_index.to_numpy()
        data = data[:,1:]

        ReducedBlocks = []
        for j in range(data.shape[0]):
            Coor = vertex_xyz(j%50)
            LinkNum = sorted(Qbit_from_vertex_corrdinate(Coor[0],Coor[1],Coor[2]))

            Block = data[j,:]
            # print(Phi[tuple(Block[LinkNum])])
            ReducedBlocks.append(np.delete(Block, LinkNum))

        ReducedBlocks = np.array(ReducedBlocks)