# Librairies
import numpy as np
import matplotlib.pyplot as plt


threshold = 20 # Threshold to detect object
group = 1 # Group counter
find = False # No neighbor with a group

# Read results file
f = open("contactless_flow_measurement/1_Real_time/0_Static/1_Data/E3_Second_pos_obj.txt" ,"r")
content = f.read()
f.close()

# Extract data
list = content.strip().split("\n")

split_list_x = [list[i].split(" ")[0][:-1] for i in range(len(list))]
split_list_y = [list[i].split(" ")[1][:-1] for i in range(len(list))]
split_list_z = [list[i].split(" ")[2] for i in range(len(list))]

# Transfrom in matrice
matrice = np.zeros((8,8))

for i in range(len(split_list_x)):
        matrice[int(split_list_x[i])][int(split_list_y[i])] = int(split_list_z[i])

# Distance matrice before obj identification
vmin = 0
vmax = 700

fig0 = plt.figure()
ax0 = fig0.add_subplot()

im = ax0.matshow(matrice, cmap='viridis', vmin=vmin, vmax=vmax)
ax0.set_title("Raw values - position 2")
fig0.colorbar(im, ax=ax0)
plt.savefig("contactless_flow_measurement/1_Real_time/0_Static/2_Pictures/raw_pos2.png")

# Identify object
matrice_objects = np.zeros((8,8))

diff = np.zeros((3,3))

for row in range(len(matrice)):
    for col in range(len(matrice[0])):
        
        # A point is in neighborhood (threshold) ? 
        if(row-1 < 0 or col-1 < 0):
            diff[0][0] = 9999 
        else:
            diff[0][0] = np.abs(matrice[row][col] - matrice[row-1][col-1])

        if(row-1 < 0):
            diff[0][1] = 9999
        else:
            diff[0][1] = np.abs(matrice[row][col] - matrice[row-1][col])

        if(row-1 < 0 or col+1 > len(matrice[0])-1):
            diff[0][2] = 9999
        else:
            diff[0][2] = np.abs(matrice[row][col] - matrice[row-1][col+1])

        if(col-1 < 0):
            diff[1][0] = 9999
        else:
            diff[1][0] = np.abs(matrice[row][col] - matrice[row][col-1])

        diff[1][1] = -1

        if(col+1 > len(matrice[0])-1):
            diff[1][2] = 9999
        else:
            diff[1][2] = np.abs(matrice[row][col] - matrice[row][col+1])

        if(row+1 > len(matrice)-1 or col-1 < 0):
            diff[2][0] = 9999
        else:
            diff[2][0] = np.abs(matrice[row][col] - matrice[row+1][col-1])

        if(row+1 > len(matrice)-1):
            diff[2][1] = 9999
        else:
            diff[2][1] = np.abs(matrice[row][col] - matrice[row+1][col])

        if(row+1 > len(matrice[0])-1 or col+1 > len(matrice)-1):
            diff[2][2] = 9999
        else:
            diff[2][2] = np.abs(matrice[row][col] - matrice[row+1][col+1])

        # This neighbor has a group ? 
        for i in range(len(diff)):
            for j in range(len(diff[0])):
                value = diff[i][j]
                if((value != 9999 and value !=-1) and value < threshold): 
                    print(matrice_objects[row+i-1][col+j-1])
                    if(matrice_objects[row+i-1][col+j-1] !=0):
                        matrice_objects[row][col] = matrice_objects[row+i-1][col+j-1]
                        find = True

        # If no, assign an arbitrary group  
        if(find == False):
            # Création d'un nouveau groupe
            matrice_objects[row][col] = group
            group +=1
        else:
            find = False

# Display objects
fig1 = plt.figure()
ax1 = fig1.add_subplot()

vmin_obj = min(obj.min() for obj in matrice_objects)
vmax_obj = max(obj.max() for obj in matrice_objects)

im1 = ax1.matshow(matrice_objects, vmin=vmin_obj, vmax=vmax_obj)
ax1.set_title("Objets")       
fig1.colorbar(im1, ax=ax1)    

plt.tight_layout()
plt.show()