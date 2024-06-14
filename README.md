uHDR V6.0

Prérequis
---------
Version de python >= 11.0
Installation des packages de python :
pip install -r requirements.txt

Installation d'un visualisateur d'image HDR :
Ouvrir le microsoft store, rechercher "hdr viewer" puis installer "HDR + WCG Image Viewer"

Lancement du logiciel
----------
Rendez vous dans le répertoire uHDR puis
python uHDR.py

HDRImageViewer s'ouvre automatiquement. Ne le fermez pas mais appuyez sur la touche echap pour quitter le mode plein écran. Laissez le tourner en arrière plan.

# uHDR

## Description

uHDR est un logiciel open source d’édition d’images HDR. Bien que des versions stables soient disponibles, il est toujours en développement pour amélioration. uHDR possède un pipeline graphique complet dédié intégralement aux traitements à grande gamme de luminance (HDR : High Dynamic Range).

## Version actuelle : uHDR v6

- **Publication** : 2020
- **Licence** : GNU version 3
- **Développé pour** : Python 3.9
- **Mise à jour mineure** : 2024 (compatibilité avec Python 3.12)
- **Auteurs** : Rémi Cozot, Rémi Synave

### Architecture de uHDR v6

1. **uhdrCore** : Regroupe toutes les fonctionnalités de traitement et d'édition d'images.
2. **guiQt** : Gère l'interface graphique.
3. **preferences** : Gère les préférences utilisateur.

## Mise à jour majeure : uHDR v7

### Changements majeurs

- Refonte totale du code de l’IHM vers le modèle Qt : signaux et événements.
- Renforcement du typage : abandon du type Self pour les annotations de type classiques.
- Finalisation de la documentation.
- Parallélisation légère complète.

### Objectif de la version 7

Finaliser la migration de la version 6 vers la version 7.

## Livrables attendus

1. **Code de l’application**
2. **Document de suivi du projet**
3. **Compte-rendu des modifications réalisées** (conception, code, jeux d'essais…)
4. **Revue finale du projet**

## Critères d'évaluation

1. **Fluidité de l’interface** : pas de « freeze ».
2. **Robustesse à la montée en charge** : nombre maximal d’images 4K HDR sans plantage de l’application.
3. **Absence de bugs**
4. **Nombre de fonctionnalités intégrées dans la v7**
5. **Qualité de la documentation en anglais**

### Documentation

- Clarté des documents.
- Précision des informations.
- Orthographe.

## Conseil

Prenez le temps de tester le logiciel dans sa version 6. Testez un maximum de fonctionnalités et étudiez bien le code de l’existant avant de commencer à programmer. Lisez le README.

## Lien vers le dépôt git

[Dépôt git de uHDR](https://gogs.univ-littoral.fr/synave/uHDR)

La version 7 se trouve dans une branche.

---

### Auteurs

- **Rémi Cozot** : remi.cozot@univ-littoral.fr
- **Rémi Synave** : remi.synave@univ-littoral.fr

*Date : 6 juin 2024*
