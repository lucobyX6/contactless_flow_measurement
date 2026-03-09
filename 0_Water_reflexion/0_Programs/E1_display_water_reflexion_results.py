import numpy as np
import matplotlib.pyplot as plt

# Values
no_water = np.array([
    [90, 98, 96, 132, 106, 82, 76, 75],
    [93, 112, 113, 85, 157, 154, 80, 80],
    [134, 90, 85, 82, 80, 79, 80, 94],
    [126, 88, 82, 79, 78, 76, 77, 80],
    [94, 113, 81, 79, 77, 75, 76, 78],
    [87, 84, 80, 77, 76, 75, 75, 78],
    [120, 82, 81, 78, 77, 76, 76, 76],
    [93, 83, 79, 78, 76, 76, 77, 79]
])

water_1_4L = np.array([
    [101, 205, 133, 98, 94, 126, 119, 90],
    [104, 143, 94, 115, 90, 121, 156, 88],
    [164, 98, 130, 191, 85, 255, 221, 115],
    [151, 96, 103, 98, 110, 84, 149, 127],
    [112, 92, 85, 79, 67, 68, 163, 86],
    [166, 92, 84, 106, 65, 79, 82, 86],
    [143, 89, 120, 83, 84, 81, 83, 150],
    [137, 91, 85, 85, 187, 118, 96, 96]
])

water_1_2L = np.array([
    [141, 124, 141, 136, 97, 94, 194, 96],
    [138, 103, 93, 89, 90, 117, 86, 90],
    [121, 99, 84, 177, 89, 128, 275, 87],
    [121, 107, 94, 80, 78, 102, 236, 89],
    [169, 100, 80, 55, 53, 228, 221, 108],
    [156, 90, 81, 141, 52, 78, 83, 115],
    [158, 89, 110, 81, 115, 94, 84, 113],
    [100, 92, 85, 84, 83, 84, 113, 127]
])

water_3_4L = np.array([
    [119, 163, 94, 136, 86, 145, 175, 98],
    [136, 98, 82, 77, 76, 170, 76, 88],
    [127, 89, 71, 221, 104, 178, 190, 76],
    [125, 84, 119, 66, 65, 72, 150, 85],
    [121, 123, 68, 45, 41, 215, 77, 104],
    [151, 81, 68, 45, 40, 69, 74, 80],
    [198, 80, 74, 70, 111, 100, 76, 110],
    [99, 85, 76, 75, 111, 75, 96, 135]
])

water_1L = np.array([
    [66, 67, 131, 57, 56, 61, 128, 99],
    [107, 55, 69, 44, 46, 64, 73, 70],
    [75, 47, 68, 128, 40, 96, 71, 78],
    [106, 44, 98, 41, 42, 44, 79, 81],
    [131, 57, 45, 29, 26, 107, 81, 80],
    [127, 52, 44, 25, 25, 56, 51, 50],
    [97, 52, 95, 85, 46, 47, 51, 86],
    [90, 53, 63, 50, 63, 58, 42, 69]
])

# Diff calculation
diff_1_4L = water_1_4L - no_water
diff_1_2L = water_1_2L - no_water
diff_3_4L = water_3_4L - no_water
diff_1L = water_1L - no_water

# Mean calculation
moy_1_4L = np.mean(diff_1_4L)
moy_1_2L = np.mean(diff_1_2L)
moy_3_4L = np.mean(diff_3_4L)
moy_1L = np.mean(diff_1L)

# Raw values
fig1, axes1 = plt.subplots(2, 2, figsize=(12, 10))
axes1 = axes1.ravel()
titres = ["Eau (1/4L)", "Eau (1/2L)", "Eau (3/4L)", "Eau (1L)"]
matrices = [water_1_4L, water_1_2L, water_3_4L, water_1L]
vmin_orig = min(matrice.min() for matrice in matrices)
vmax_orig = max(matrice.max() for matrice in matrices)

for i, (matrice, titre) in enumerate(zip(matrices, titres)):
    im = axes1[i].imshow(matrice, cmap='viridis', vmin=vmin_orig, vmax=vmax_orig)
    axes1[i].set_title(titre)
    fig1.colorbar(im, ax=axes1[i])

fig0 = plt.figure()
ax0 = fig0.add_subplot()

ax0.matshow(matrice, cmap='viridis', vmin=vmin_orig, vmax=vmax_orig)
ax0.set_title("Sans eau")
fig0.colorbar(im, ax=ax0)

# Diff values
fig2, axes2 = plt.subplots(2, 2, figsize=(12, 10))
axes2 = axes2.ravel()
titres_diff = [
    f"Différence (1/4 L - Sans eau)\nMoyenne: {moy_1_4L:.1f}",
    f"Différence (1/2 L - Sans eau)\nMoyenne: {moy_1_2L:.1f}",
    f"Différence (3/4 L - Sans eau)\nMoyenne: {moy_3_4L:.1f}",
    f"Différence (1 L - Sans eau)\nMoyenne: {moy_1L:.1f}"
]
matrices_diff = [diff_1_4L, diff_1_2L, diff_3_4L, diff_1L]
vmin_diff = min(matrice.min() for matrice in matrices_diff)
vmax_diff = max(matrice.max() for matrice in matrices_diff)

for i, (matrice_diff, titre_diff) in enumerate(zip(matrices_diff, titres_diff)):
    im = axes2[i].imshow(matrice_diff, cmap='coolwarm', vmin=vmin_diff, vmax=vmax_diff)
    axes2[i].set_title(titre_diff)
    fig2.colorbar(im, ax=axes2[i])

plt.tight_layout()
plt.show()
