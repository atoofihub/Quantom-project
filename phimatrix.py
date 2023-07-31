# imports
import time
import pandas as pd
import numpy as np
from itertools import product
import argparse


start_time = time.time()

# parser = argparse.ArgumentParser()
# parser.add_argument("-p")
# args = parser.parse_args()

parser = argparse.ArgumentParser(description='A test program.')

parser.add_argument("-l", "--print_string", help="Prints the supplied argument.", type=int)

args = parser.parse_args()

L = args.print_string


# L = 0
# # while L != 5 | L != 6:
# while True:
#     L = int(input("Hi! Please Enter the L:(L = 5,6) "))
#     if (L == 5):
#         break
#     elif(L == 6):
#         break


# define vertex_xyz function that get ""vertex number""" as input and calculate vertex coordinate and return ""x,y,z"" at the end
def vertex_xyz(Vertex_Number):
    z = 1
    if(Vertex_Number % 2 == 0):
        z = 0
        
    y = int( Vertex_Number // (2 * L) )
    x = int( (Vertex_Number % (2 * L) ) // 2 )
    
    return x,y,z

# define Qbit_from_vertex_corrdinate function that get ""vertex coordinate"" as input and find 3 link number and return 3 "link number" at the end
def Qbit_from_vertex_corrdinate(x,y,z):
    if z == 0:
        if x != 0 and y != 0:
            link_1 = 3*L*y + 3*x ; link_2 = 3*L*y + 3*x +1 ; link_3 = 3*L*y + 3*x - 1
        elif x == y:
            link_1 = 0 ; link_2 = 1 ; link_3 = 3*L - 1
        elif x != 0 and y == 0:
            link_1 = 3*L*y + 3*x ; link_2 = 3*L*y + 3*x +1 ; link_3 = 3*L*y + 3*x - 1
        elif x == 0 and y != 0:
            link_1 = 3*L*y + 3*x ; link_2 = 3*L*y + 3*x +1 ; link_3 = 3*L*(y + 1) + 3*x - 1
    elif z == 1:
        if x != (L-1) and y != (L-1):
            link_1 = 3*L*y + 3*x + 2 ; link_2 = 3*L*y + 3*x + 3*L + 3 ; link_3 = 3*L*y + 3*x + 1
        elif x == (L-1) and  y != (L-1):
            link_1 = 3*L*y + 3*x + 2 ; link_2 = 3*L*y + 3*L  ; link_3 = 3*L*y + 3*x + 1
        elif x != (L-1) and y == (L-1):
            link_1 = 3*L*y + 3*x + 2 ; link_2 =  3*x + 3 ; link_3 = 3*L*y + 3*x + 1
        elif x == y == (L-1) :
            link_1 = 3*L*y + 3*x + 2 ; link_2 = 0 ; link_3 = 3*L*y + 3*x + 1
    else : # error handling for function
        print("your z has not true value")
        return 0
    
    return link_1,link_2,link_3

outputdata = []
# main section for calculating eigenvalues for density matrix
for beta in range(1,10,1):
    beta = beta/10 # beta step is 0.1
    
    xl = pd.ExcelFile("L={}/total_configurations_{}_{}.xlsx".format(L,L,beta))
    sheet_names = xl.sheet_names
    # reading each sheets (there is 11 sheets in exel files)
    for i in range(11):
        df = pd.read_excel("L={}/total_configurations_{}_{}.xlsx".format(L,L,beta), sheet_name=i) # making data frame of sheets data
        data = (df.to_numpy())[:,1:] # deleting first column(beacause it is header)
        phikeys = list(product([-1,1], repeat=3)) # 8(2^3) modes for phi
        phi = {key: [] for key in phikeys} # making phi's dictionaey for 8 modes

        # loop for each row of data
        for j in range(data.shape[0]):
            for k in range(2 * L**2):
                Coor = vertex_xyz(k) # use vertex_xyz function(the input number resets every 2*L^2 times)
                LinkNum = sorted(Qbit_from_vertex_corrdinate(Coor[0],Coor[1],Coor[2])) # use Qbit_from_vertex_corrdinate function and sort list for better performance at np.delete() function

                Block = data[j,:] # Organize Block from data

                phi_key = tuple(Block[LinkNum]) # finding phi dictionary key of this block
                phi_data = phi[phi_key] # get the phi data that belongs to the block key

                Block = np.delete(Block, LinkNum) # make reduced block 
                Block = (''.join([str(item) for item in Block])).replace('-1','0') # replace -1 with 0 for making block number decimal

                phi_data.append(int(Block,2)) # making block number decimal and add the number to the phi dictionary

                phi.update({phi_key:phi_data}) # and update the dictionary value at the end
            
        # counting all items in each phi key
        decimal_phi = []
        for k in phikeys:
            unique, counts = np.unique(phi[k], return_counts=True)
            decimal_phi.append([unique,counts])

        # making density matrix
        phiMatrix = np.zeros((8,8))
        for k in range(len(phikeys)):
            for h in range(len(phikeys)):
                list_A = list(decimal_phi[k][0]) # get first phi list
                list_B = list(decimal_phi[h][0]) # get second phi list
                both = set(list_A).intersection(list_B) # finding intersection between first list and second list
                
                # finding indices of common items
                indices_A = [list_A.index(x) for x in both]
                indices_B = [list_B.index(x) for x in both]

                # doing dot product
                dotphi = sum(decimal_phi[k][1][indices_A] * decimal_phi[h][1][indices_B])
                phiMatrix[k,h] = dotphi

        phiMatrix_r = phiMatrix.reshape(-1,1)
        # and finding eigenvalues at the end 
        # eigenvalues, eigenvectors = np.linalg.eig(phiMatrix)
        # print({"PhiMatrix{}".format(k):phiMatrix_r[k,0] for k in range(64)})
        outputdict1 = {"PhiMatrix{}".format(k):phiMatrix_r[k,0] for k in range(64)}
        outputdict = {'L' : L, 'Beta' : beta, 'Sheet ID' : i,'Sheet Name' : sheet_names[i], 'N' : j+1}
        outputdict.update(outputdict1)
        # print(outputdict)
        outputdata.append(outputdict)
        # print({'L' : L, 'Beta' : beta, 'Sheet ID' : i,'Sheet Name' : sheet_names[i], 'N' : j+1, 'Eigen Values' : eigenvalues})

output = pd.DataFrame(outputdata)
output.to_csv("phimatrix_L{}.csv".format(L))
print("--- %s seconds ---" % (time.time() - start_time))