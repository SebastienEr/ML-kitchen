# 🎨 Guide d'Utilisation - Kitchen Planner Interactif

## Vue d'Ensemble

Le Kitchen Planner Interactif vous permet de créer des plans de cuisine professionnelle entièrement personnalisés en temps réel. Sélectionnez les zones spécifiques dont vous avez besoin, ajustez leurs tailles, et obtenez un plan optimisé automatiquement.

## 🚀 Lancement Rapide

```bash
cd kitchen_ml_planner
python interactive_planner.py
```

Ouvrez ensuite votre navigateur à l'adresse : **http://localhost:5001**

## 🎯 Fonctionnalités Principales

### 1. Sélection de Zones Avancée

L'interface propose **40+ types de zones** organisées en 8 catégories :

#### 🏗️ Zones de Préparation
- **Légumerie** : Tables inox, éviers multiples, bacs gastro, éplucheuse
- **Préparation Froide** : Tables réfrigérées, éviers, planches de découpe
- **Préparation Chaude** : Tables chauffantes, bain-marie, mixeurs
- **Pâtisserie** : Four à pâtisserie, batteur, laminoir, chambre de pousse
- **Boucherie** : Billot, scie à os, hachoir, chambre froide dédiée

#### 🔥 Zones de Cuisson
- **Zone Cuisson Principale** : Fours, plaques, salamandre, hotte
- **Grillade** : Grill, plancha, extracteur spécialisé
- **Friture** : Friteuses, filtration d'huile, ventilation renforcée
- **Wok** : Feux wok, évacuation vapeur, tables adjacentes

#### ❄️ Zones de Stockage
- **Chambre Froide Positive** : Groupe froid, étagères inox, thermomètre
- **Chambre Froide Négative** : Groupe froid -18°C, alarme température
- **Stockage Sec** : Étagères métalliques, contenants hermétiques
- **Cave à Vin** : Climatisation vin, casiers, éclairage LED
- **Réserve** : Rayonnages, chariots, zone déballage

#### 🧽 Zones de Lavage
- **Plonge Batterie** : Lave-vaisselle à capot, bacs de trempage
- **Plonge Légumes** : Bacs spécialisés, douchette, tables de tri
- **Laverie** : Lave-linge, séchoir, rangement linge

#### 🍽️ Zones de Service
- **Dressage** : Passe, lampes chauffantes, tables de dressage
- **Office** : Machine à café, réfrigérateur, micro-ondes
- **Bar** : Comptoir, tireuses, lave-verre, réfrigération
- **Expédition** : Chariots, étiqueteuse, balance

#### 🧼 Zones d'Hygiène
- **Vestiaires** : Casiers, bancs, miroirs
- **Sanitaires** : WC, lavabos, distributeurs
- **Lave-Mains** : Lave-mains à commande non manuelle
- **Sas d'Hygiène** : Lave-mains, distributeur gel, pédiluve

#### ⚙️ Zones Techniques
- **Local Poubelles** : Conteneurs, point d'eau, ventilation
- **Local Technique** : Tableau électrique, chaudière, ventilation
- **Réception** : Quai de déchargement, balance, tables de contrôle
- **Bureau** : Bureau, ordinateur, armoire, coffre-fort

### 2. Configuration des Dimensions

#### Contrôles de la Pièce
- **Largeur** : 8m à 30m (curseur + saisie précise)
- **Profondeur** : 6m à 25m (curseur + saisie précise)
- **Largeur Couloirs** : 1m à 3m (curseur + saisie précise)

#### Tailles des Zones
- Chaque zone a des **limites min/max réalistes**
- Ajustement par incréments de 0.5m²
- **Couleurs visuelles** pour identification rapide

### 3. Génération de Plan en Temps Réel

#### Algorithme d'Optimisation
- **Placement automatique** évitant les chevauchements
- **Optimisation de l'espace** avec ratio 3:2 par défaut
- **Respect des couloirs** pour circulation HACCP
- **Adaptation dynamique** aux contraintes de taille

#### Visualisation Instantanée
- **Plan 2D haute résolution** (300 DPI)
- **Couleurs par catégorie** pour identification rapide
- **Surface affichée** pour chaque zone
- **Grille de référence** avec dimensions

### 4. Statistiques Avancées

L'interface calcule automatiquement :
- **Nombre de zones** sélectionnées
- **Surface utile totale** (zones de travail)
- **Surface couloirs** (circulation)
- **Efficacité d'occupation** (% surface utile)

### 5. Sauvegarde et Export

#### Formats Disponibles
- **JSON** : Plan complet avec métadonnées
- **PNG** : Image haute résolution du plan
- **Téléchargement automatique** après sauvegarde

#### Données Sauvegardées
```json
{
  "zones": [
    {
      "name": "Légumerie",
      "x": 0, "y": 0, "w": 4.8, "h": 2.5,
      "color": "#90EE90",
      "equipment": ["Tables inox", "Éviers multiples", ...]
    }
  ],
  "statistics": {
    "zones_count": 8,
    "total_surface": 67.3,
    "corridor_surface": 32.7,
    "efficiency": 67.3
  }
}
```

## 🎮 Utilisation Étape par Étape

### Étape 1 : Configuration de Base
1. Ajustez les **dimensions de la pièce** avec les curseurs
2. Définissez la **largeur des couloirs** (1.5m recommandé)
3. Observez la mise à jour en temps réel

### Étape 2 : Sélection des Zones
1. **Cochez les zones** que vous souhaitez inclure
2. **Ajustez les tailles** selon vos besoins
3. Consultez la **liste d'équipements** pour chaque zone

### Étape 3 : Génération du Plan
1. Cliquez sur **"Générer le Plan"**
2. Visualisez le **plan optimisé** instantanément
3. Consultez les **statistiques** d'efficacité

### Étape 4 : Personnalisation
1. **Modifiez les tailles** si nécessaire
2. **Ajoutez/supprimez des zones** dynamiquement
3. **Régénérez** automatiquement le plan

### Étape 5 : Sauvegarde
1. Cliquez sur **"💾 Sauvegarder"**
2. Nommez votre plan
3. **Téléchargement automatique** du fichier JSON

## 🏆 Bonnes Pratiques

### Dimensionnement Optimal
- **Légumerie** : 6-8m² pour restaurant moyen
- **Cuisson principale** : 15-20m² minimum
- **Chambres froides** : 8-12m² selon volume d'activité
- **Plonge** : 9-12m² pour lave-vaisselle à capot

### Circulation HACCP
- **Couloirs** : 1.5m minimum pour respect HACCP
- **Zone sale/propre** : Séparer plonge et préparation
- **Flux unidirectionnel** : De la réception au service

### Efficacité d'Espace
- **Objectif** : 65-75% d'efficacité d'occupation
- **Surface couloirs** : 25-35% de l'espace total
- **Zones prioritaires** : Cuisson et préparation froide

## 🔧 Dépannage

### Problèmes Courants
- **Plan vide** : Vérifiez que des zones sont sélectionnées
- **Zones qui se chevauchent** : Réduisez les tailles ou agrandissez la pièce
- **Erreur de génération** : Vérifiez la console du navigateur

### Support
- Consultez les logs dans la console du navigateur (F12)
- Vérifiez que le serveur fonctionne sur le port 5001
- Redémarrez le serveur en cas de problème persistant

## 🚀 Intégration avec les Autres Outils

Cette interface s'intègre parfaitement avec :
- **Validation automatique** (`validate.py`)
- **Export CAD** (`export_cad.py`) 
- **Visualisation 3D** (`render_3d.py`)
- **Analyse coûts** (`cost_estimation.py`)
- **Conformité HACCP** (`haccp_analysis.py`)

---

*Interface développée pour une personnalisation complète et professionnelle des cuisines commerciales.*
