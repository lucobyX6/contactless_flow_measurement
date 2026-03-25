# Librairies
import numpy as np
import matplotlib.pyplot as plt

# Read results file
file_0L = open("contactless_flow_measurement/0_Water_reflexion/2_Data/reflectance_no_water.txt", "r")
content_0L = file_0L.read()
file_0L.close()

file_1L = open("contactless_flow_measurement/0_Water_reflexion/2_Data/reflectance_1L.txt", "r")
content_1L = file_1L.read()
file_1L.close()

file_2L = open("contactless_flow_measurement/0_Water_reflexion/2_Data/reflectance_2L.txt", "r")
content_2L = file_2L.read()
file_2L.close()

# Extract data
list_0L = content_0L.strip().split("\n")
split_list_x_0L = [list_0L[i].split(" ")[0][:-1] for i in range(len(list_0L))]
split_list_y_0L = [list_0L[i].split(" ")[1][:-1] for i in range(len(list_0L))]
split_list_z_0L = [list_0L[i].split(" ")[2] for i in range(len(list_0L))]

list_1L = content_1L.strip().split("\n")
split_list_x_1L = [list_1L[i].split(" ")[0][:-1] for i in range(len(list_1L))]
split_list_y_1L = [list_1L[i].split(" ")[1][:-1] for i in range(len(list_1L))]
split_list_z_1L = [list_1L[i].split(" ")[2] for i in range(len(list_1L))]

list_2L = content_2L.strip().split("\n")
split_list_x_2L = [list_2L[i].split(" ")[0][:-1] for i in range(len(list_2L))]
split_list_y_2L = [list_2L[i].split(" ")[1][:-1] for i in range(len(list_2L))]
split_list_z_2L = [list_2L[i].split(" ")[2] for i in range(len(list_2L))]

# Transform in matrice
matrice_0L = np.zeros((8,8))
for i in range(len(split_list_x_0L)):
        matrice_0L[int(split_list_x_0L[i])][int(split_list_y_0L[i])] = int(split_list_z_0L[i])

matrice_1L = np.zeros((8,8))
for i in range(len(split_list_x_1L)):
        matrice_1L[int(split_list_x_1L[i])][int(split_list_y_1L[i])] = int(split_list_z_1L[i])

matrice_2L = np.zeros((8,8))
for i in range(len(split_list_x_2L)):
        matrice_2L[int(split_list_x_2L[i])][int(split_list_y_2L[i])] = int(split_list_z_2L[i])

# Raw values
fig1, axes1 = plt.subplots(1,3)
axes1 = axes1.ravel()
titles = ["Water (0L)", "Water (1L)", "Water (2L)"]
matrices = [matrice_0L, matrice_1L, matrice_2L]
vmin_orig = 0
vmax_orig = 100

for i, (matrice, titre) in enumerate(zip(matrices, titles)):
    im = axes1[i].imshow(matrice, cmap='coolwarm', vmin=vmin_orig, vmax=vmax_orig)
    axes1[i].set_title(titre)
    fig1.colorbar(im, ax=axes1[i], fraction=0.046, pad=0.04)

plt.tight_layout()
plt.show()
