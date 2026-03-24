# Projet recherche 2026 - Capteur de débit d'eau sans contact

Ce projet s'inscrit dans le cursus d'ingénieur ISMIN (_Ingénieur Systèmes Microélectronique et Informatique_). 

**Étudiants :**
- Lucas VINCENT
- Reem AL HADDAD

## Contexte

En France, 12% de l'irrigation est réalisée par irrigation gravitaire. Ce procédé repose sur un réseau de canaux de tailles diverses qui distribue l'eau grâce à la différence d'altitude entre l'amont et l'aval. Cette technique ancestrale a notamment permis d'irriguer des terres arides dans le sud de la France, comme la *La Plaine de La Crau*. 

Le dérèglement climatique nous impose de repenser notre utilisation de l’eau. De manière à raisonner son usage et mettre en place les mesures adaptés, il est nécessaire d'établir une surveillance préalable de ces canaux. Pour obtenir le maximum d'informations à l'échelle la plus large possible, les chercheurs déploient des réseaux de capteurs intelligents le long des cours d'eau.

Traditionnellement, les systèmes employés sont mécaniques et immergés. Cependant, les canaux sont des
milieux à ciel ouvert où transitent une multitude de débris, dont des branches, des feuilles ou des sédiments. Ces perturbations rendent les capteurs immergés peu efficaces, car elles peuvent les bloquer ou les endommager. 

L'alternative actuelle est d'utiliser des capteurs basés sur la technologie radar, entre 10 et 80GHz. Ces derniers sont peu sensibles à la qualité de l'eau ou la présence d'algues et de sédiments. Ils admettent aussi une excellente précision et un faible entretien.
Cependant, les objets en surface ou la turbulence des eaux affectent la fiabilité des résultat. De plus, le prix de ces capteurs pouvant atteindre plusieurs milliers d'euros, est un frein à leur déploiement à grande échelle. 

## Capteurs actuellement utilisé

Ce projet est une exploration de l'intérêt d'un capteur `Time-of-flight` dans l'acquisition du débit d'eau pour les canaux. Sur le papier, il représente une alternative peu coûteuse financièrement et énergétiquement par rapport aux solutions à base de technologies radars actuellement développées. Cependant, nos recherches révèlent que son usage dans ce milieu est complexe

Ce travail est inspiré de la vidéo [Turn a Time-of-Flight Sensor into a 3D Scanner](https://www.youtube.com/watch?v=s32OUzhjf4U). 

**Matériel utilisé :**
- Carte `Nucleo - STM32 L476RG`
- Capteur TOF `VL53L5CX` avec module SATEL
- Servomoteur `Microservo 9g`

**Documentation :**  \
[1] VL53L8CX Datasheet, ST Microelectronics, 22 December 2022 . [En ligne]. Disponible suivant ce [lien](https://www.st.com/resource/en/datasheet/vl53l8cx.pdf)

[2] SparkFun_VL53L5CX_Library, SparkFun Electronics, No publication date. [En ligne]. Disponible suivant ce [lien](https://github.com/sparkfun/SparkFun_VL53L5CX_Arduino_Library)

[3] NUCLEO-L476RG Pinout, ST Microelectronics, No publication date. [En ligne]. Disponible suivant ce [lien](https://os.mbed.com/platforms/ST-Nucleo-L476RG/#overview)

## Arborescence du projet

Le projet est découpé en deux parties, l'étude de la réflectivité de l'eau et l'acquisition et le traitement de données en temps réel. 

- ./0_Water_reflexion : Expériences sur la réflectance de l'eau. 
- ./1_Real_time : Acquisition en temps réel des données du capteurs, traitement et affichage dynamique. 
- ./2_3D_Object : Ensemble des modélisations 3D réalisées en support du projet. 

## Conclusions

- L'eau absorbe les ondes infrarouges émisent par le capteur. Cette absorption est d'autant plus présente que le volume d'eau est important. Dans un canal l'absorption est totale empêchant la prise de mesure à la surface de l'eau. Cette problématique oblige à détecter des objets en surface pour mesurer leur vitesse, plutôt que la surface de l'eau. 

- La résolution du capteur dépend de la distance. Les lasers infrarouges sont émis avec un angle de 5,625° les uns par rapport aux autres. Ainsi, plus la distance est importante, plus la distance entre deux points de mesure est grande. De plus, plus la précision décroit avec la distance. Ces deux phénomènes cumulés impactent la capacité à détecter des formes ou un objet à moyenne (1m) ou longue distance (2m). 

- Si le capteur est placé sur un moteur asservi, comme un servomoteur, il peut acquérir un plus grand nombre de points proche les uns des autres. Cette méthode permet de réduire la résolution et peut donc potentiellement corriger la problématique identifiée précédemment. 

## Ouverture 

Il existe une technologie similaire au TOF en rotation nommé le LiDAR (light detection and ranging). Ce dernier admet une meilleure résolution, permet une rotation à 360° avec une haute fréquence d'acquisition et une technologie déjà fortement déployée dans l'industrie, notamment en navigation autonome. Cette piste semble donc être une nouvelle voie prometteuse d'analyse. Le capteur pourrait être placé au dessus du canal. Pour obtenir la vitesse de l'eau en surface, il mesurerait la vitesse des feuilles et branchages flottants. Pour mesurer la hauteur d'eau, il étudierait la berge et chercherait un saut de réflectance.
