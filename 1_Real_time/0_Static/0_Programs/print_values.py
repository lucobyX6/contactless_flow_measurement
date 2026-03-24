# Librairies
import numpy as np
import matplotlib.pyplot as plt

# Read results file
file = open("contactless_flow_measurement/1_Real_time/0_Static/1_Data/Distance_problem/small_obj_far.txt", "r")
content = file.read()
file.close()

# Extract data
list = content.strip().split("\n")
split_list_x = [list[i].split(" ")[0][:-1] for i in range(len(list))]
split_list_y = [list[i].split(" ")[1][:-1] for i in range(len(list))]
split_list_z = [list[i].split(" ")[2] for i in range(len(list))]

# Transform in matrice
matrice_water = np.zeros((8,8))
for i in range(len(split_list_x)):
        matrice_water[int(split_list_x[i])][int(split_list_y[i])] = int(split_list_z[i])

# Display values
fig_raw, ax_raw = plt.subplots()

vmin_raw = 0
vmax_raw = 700

im_raw = ax_raw.imshow(matrice_water, cmap='coolwarm', vmin=vmin_raw, vmax=vmax_raw)
ax_raw.set_title("Measure near to the object")
fig_raw.colorbar(im_raw, ax=ax_raw) 

plt.tight_layout()
plt.show()