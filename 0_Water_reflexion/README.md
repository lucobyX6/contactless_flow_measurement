# Étude de la réflectivité de l'eau

## Organisation du répertoire : 

Le répertoire du projet est constitué de la manière suivante :
- ./0_Programs : Contient l'ensemble des programmes python et C++. 
- ./1_Pictures : Contient les résultats des expériences.
- ./2_Data : Contient les donneés brutes récupérées par durant les expériences. 

## Expériences :

L'objectif de ces expériences est de mesurer la **réflectivité de l'eau** vis à vis du rayon infrarouge émis par le capteur Tof. Deux expériences ont été réalisé, la première permet de découvrir l'impact du volume d'eau sur la réflectivité et la seconde la réflectivité dans un cas réel, directement sur le canal. 

Le code `Mean_on_distance_calculation_Xms.cpp` est le code envoyé dans le carte *STM32 L476RG* pour les deux expériences. Il suffit pour l'utiliser de copier son contenu dans le fichier `main.cpp` de votre projet.    

### Expérience 1 - Test de réflectivité dans une bassine

L'objectif de cette expérience était d'obtenir un premier aperçu de la variation de réflectivité induite par l'eau, en fonction du volume. L'image ci-dessous décrit le matériel de l'expérimentation.  

[image de l'expérience à ajouter]

La carte électronique génère au bout d'une dizaine de secondes une liste de 64 valeurs. Chaque valeur est la moyenne des résultats pour ce point sur 10s. Les résultats sont stockées dans le dossier `./2_Data`.   

Les résultats précédents sont traités par le programme python `E1_display_water_reflexion_results.py`. Ce dernier génère à partir de ces données des matrices. Elles sont stockées dans le dossier `./1_Pictures` avec le préfixe `E1_`.  

[image résultats à ajouter]

### Expérience 2 - Test de réflectivité dans le canal

Les résultats de l'expérience précédente ont révélé que plus il y avait d'eau, plus la réflectivité était faible.  

