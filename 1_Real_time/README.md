# Acquisition et traitement des données du capteur en temps réel

## Organisation du répertoire : 

Le répertoire du projet est constitué de la manière suivante :
.
├── 0_Static : Contient les pré-codes pour tester les fonctionnalités sur des données statiques avant l'implémentation dynamique.  
│   ├── 0_Programs : Algorithme C++ et Python
│   ├── 1_Data : Données récoltées pour tester les foncionnalités
│   └── 2_Pictures : Matrices résultats.  
├── 1_Dynamic : Contient les codes d'acquisition et de traitement en temps réel. 
│   ├── 0_Without_obj_detect : Acquisition en temps réel et affichage sans traitement dans une matrice 3D.
│   ├── 1_With_obj_detect : Acquisition en temps réel, identification des objets puis affichage dans une matrice 3D.
│   ├── 2_With_distances_between_points : Acquisition en temps réel, identification des objets puis affichage dans une matrice 3D en prenant en considération la résolution.
│   └── 3_With_rotation : Acquisition en temps réel, identification des objets puis affichage dans une matrice 3D avec la rotation autour d'un axe.