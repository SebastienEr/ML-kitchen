# 🍳 Kitchen Planner Pro - Interface Modernisée

> **Planificateur de cuisine professionnel avec interface web interactive, drag & drop intelligent, cotations en temps réel, simulation avec cuisiniers animés et validation HACCP automatique.**

## 🚀 Nouveautés de l'interface modernisée

### ✨ **Fonctionnalités révolutionnaires**

- **🎯 Drag & Drop Intelligent** - Glissez-déposez avec magnétisme automatique et détection de collision
- **📏 Cotations en Temps Réel** - Dimensions, mesures et distances affichées instantanément  
- **👨‍🍳 Simulation Cuisiniers** - Petits personnages animés pour tester l'ergonomie des flux
- **✅ Validation HACCP** - Contrôles automatiques des normes sanitaires et de sécurité
- **🚪 Battements de Portes** - Zones de dégagement et couloirs de circulation visualisés
- **📱 Interface Responsive** - Design moderne adaptatif pour tous les écrans

## 🖥️ Capture d'écran

```
┌─────────────────────────────────────────────────────────────┐
│ 🍳 Kitchen Planner Pro     [📏] [👨‍🍳] [⚏] [✅] [💾] [📥] │
├─────────────┬───────────────────────────────────────────────┤
│ 🔥 CUISSON  │                                               │
│ ┌─────────┐ │  ┌──────┐    ┌──────┐         👨‍🍳              │
│ │🔥 Four  │ │  │ Four │120 │Frigo │60       ↕               │
│ │🍳Plancha│ │  │  x80 │cm  │ x120 │cm       85cm            │
│ │🍟Friteuse│ │  └──────┘    └──────┘         ↕               │
│ │🥩 Grill │ │                                               │
│ └─────────┘ │  ←─── 150cm ────→  ⬅──────── Couloir ──────→  │
│             │                                               │
│ ❄️ FROID    │              ┌──────────┐                     │
│ 🚿 LAVAGE   │              │  Plonge  │                     │
│ 🥄 PRÉPARA. │              │ 120x60cm │                     │
│             │              └──────────┘                     │
│ 📊 STATS    │                                               │
│ Surface:4.2m│              Efficacité: 87% ✅               │
│ Équip.: 5   │                                               │
│ Chefs: 2    │                                               │
└─────────────┴───────────────────────────────────────────────┘
                    [🖱️] [🧱] [🚪] [🛤️] [📏] [🗑️]
```

## 🎯 Démarrage rapide

### **Installation et lancement**

```bash
# Cloner le projet
git clone <repository-url>
cd kitchen_ml_planner

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application moderne
python modern_kitchen_planner_app.py

# Ouvrir dans le navigateur
# http://localhost:5003
```

### **Ou utiliser le script de démonstration**

```bash
# Script de démonstration interactif
./demo_moderne.sh

# Suit le guide d'utilisation pas-à-pas
# Montre toutes les fonctionnalités
# Lance l'application automatiquement
```

## 🎨 Interface utilisateur

### **Layout principal**

- **Header** : Actions globales (cotations, export, sauvegarde)
- **Sidebar** : Catalogue d'équipements par catégorie + statistiques
- **Canvas** : Zone de conception avec grille magnétique
- **Toolbar** : Outils de dessin flottants
- **Propriétés** : Panel latéral pour éditer les éléments sélectionnés

### **Équipements disponibles**

| Catégorie | Équipements | Caractéristiques |
|-----------|-------------|------------------|
| 🔥 **Cuisson** | Four, Plancha, Friteuse, Grill | Puissance, température max |
| ❄️ **Réfrigération** | Frigo, Congélateur, Cellule, Cave | Plage de température |
| 🚿 **Lavage** | Plonge, Lave-vaisselle, Évier, Bac | Consommation d'eau |
| 🥄 **Préparation** | Table, Billot, Plan, Étagère | Surface de travail |

## ⚡ Fonctionnalités avancées

### **🎯 Drag & Drop Intelligent**

- **Magnétisme automatique** sur grille 20cm
- **Détection de collision** en temps réel
- **Placement automatique** en cas de conflit
- **Alignement intelligent** entre équipements
- **Guides visuels** pour le positionnement

### **📏 Cotations et Mesures**

- **Dimensions automatiques** de chaque équipement
- **Distances entre éléments** calculées
- **Largeur des couloirs** vérifiée
- **Surface totale** mise à jour en temps réel
- **Conformité HACCP** validée

### **👨‍🍳 Simulation avec Cuisiniers**

- **Personnages animés** qui se déplacent
- **Mouvements aléatoires** réalistes
- **Changements d'humeur** selon l'ergonomie
- **Test des flux** de circulation
- **Double-clic** pour animations spéciales

### **✅ Validation HACCP Automatique**

- **Séparation cuisson/froid** (min 100cm)
- **Largeur des couloirs** (min 120cm)
- **Battements de portes** (dégagement 90cm)
- **Marche en avant** respectée
- **Score d'efficacité** calculé en temps réel

## ⌨️ Raccourcis clavier

### **Actions globales**
- `Ctrl + S` - Sauvegarder
- `Ctrl + Z` - Annuler
- `Ctrl + Y` - Rétablir
- `Ctrl + A` - Sélectionner tout
- `Ctrl + D` - Dupliquer

### **Navigation**
- `G` - Grille magnétique
- `D` - Cotations
- `M` - Magnétisme
- `H` - Validation HACCP
- `Espace` - Ajouter cuisinier

### **Édition**
- `Suppr` - Supprimer sélection
- `Échap` - Désélectionner
- `F2` - Renommer
- `↑↓←→` - Déplacer précisément

## 🛠️ API et endpoints

### **Endpoints disponibles**

```python
GET  /                     # Interface principale
GET  /api/equipment        # Base de données équipements
POST /api/validate         # Validation HACCP
POST /api/optimize         # Optimisation automatique
POST /api/export           # Export JSON + PNG
POST /api/suggestions      # Suggestions d'amélioration
GET  /download/<filename>  # Téléchargement fichiers
```

### **Format des données**

```json
{
  "layout": {
    "equipment": [
      {
        "type": "four",
        "name": "🔥 Four",
        "x": 100, "y": 150,
        "width": 120, "height": 80,
        "category": "cuisson"
      }
    ],
    "chefs": [
      { "x": 250, "y": 200, "mood": "happy" }
    ]
  },
  "metadata": {
    "efficiency": 87.5,
    "violations": [],
    "stats": { "total_surface": 4.2 }
  }
}
```

## 📊 Métriques et analyses

### **Calculs automatiques**

- **Surface totale** : Somme des équipements en m²
- **Efficacité** : Score basé sur l'organisation et les violations HACCP
- **Compacité** : Regroupement par zones fonctionnelles
- **Ergonomie** : Distances moyennes de déplacement

### **Violations HACCP détectées**

- ❌ **Erreurs** : Violations majeures (chevauchements, distances critiques)
- ⚠️ **Avertissements** : Améliorations recommandées (couloirs, organisation)
- ✅ **Conformité** : Respect des normes sanitaires

## 🎨 Modes d'affichage

### **Vue standard**
- Équipements avec couleurs par catégorie
- Cotations et dimensions visibles
- Cuisiniers animés

### **Vue thermique**
- Zones chaudes (rouge) - équipements de cuisson
- Zones froides (bleu) - réfrigération
- Gradient de température visualisé

### **Vue flux de travail**
- Connexions entre équipements
- Chemins optimaux suggérés
- Goulots d'étranglement identifiés

## 💾 Export et sauvegarde

### **Formats d'export**

1. **JSON** - Métadonnées complètes du layout
2. **PNG** - Image haute résolution (1200×800px)
3. **Futur** - DXF (CAO), PDF (impression)

### **Contenu exporté**

- Plan complet avec équipements positionnés
- Cotations et mesures précises
- Positions des cuisiniers
- Statistiques de performance
- Violations HACCP et suggestions
- Timestamp et métadonnées

### **Sauvegarde automatique**

- Stockage local dans le navigateur
- Historique des 50 dernières actions
- Récupération automatique au rechargement
- Undo/Redo illimité

## 🏗️ Architecture technique

### **Frontend**
- **HTML5** - Structure sémantique
- **CSS3** - Animations et responsive design
- **JavaScript ES6+** - Logique interactive avancée
- **Canvas API** - Rendu graphique optimisé

### **Backend**
- **Flask** - Serveur web Python
- **Pillow** - Génération d'images
- **JSON** - Sérialisation des données
- **RESTful API** - Endpoints standardisés

### **Algorithmes**

- **Détection de collision** - Intersection de rectangles
- **Magnétisme** - Attraction vers grille et guides
- **Optimisation** - Placement automatique par zones
- **Validation HACCP** - Règles métier intégrées

## 🔧 Configuration et personnalisation

### **Variables d'environnement**

```python
# Configuration serveur
HOST = '0.0.0.0'
PORT = 5003
DEBUG = True

# Paramètres grille
GRID_SIZE = 20  # cm
MAGNETIC_DISTANCE = 30  # px

# Règles HACCP
MIN_CORRIDOR_WIDTH = 120  # cm
MIN_COOKING_COLD_DISTANCE = 100  # cm
DOOR_CLEARANCE = 90  # cm
```

### **Personnalisation équipements**

```python
EQUIPMENT_DATABASE = {
    'custom_equipment': {
        'name': '🔧 Équipement Custom',
        'category': 'custom',
        'default_width': 100,
        'default_height': 60,
        'color': '#ff6b6b',
        'description': 'Équipement personnalisé'
    }
}
```

## 📱 Compatibilité

### **Navigateurs supportés**
- ✅ Chrome 90+
- ✅ Firefox 88+  
- ✅ Safari 14+
- ✅ Edge 90+

### **Résolutions recommandées**
- 💻 Desktop : 1920×1080 min
- 📱 Tablet : 1024×768 min
- 📞 Mobile : Interface adaptative

### **Performances**
- ⚡ Démarrage : < 2 secondes
- 🎯 Réactivité : 60 FPS
- 💾 Mémoire : < 100 MB
- 🌐 Hors ligne : Fonctionnel

## 🎓 Guides et tutoriels

### **Démarrage**
1. **GUIDE_UTILISATION_MODERNE.md** - Guide complet illustré
2. **demo_moderne.sh** - Démonstration interactive
3. **Exemples inclus** - Layouts prédéfinis

### **Pour développeurs**
- **API Documentation** - Endpoints et formats
- **Code commenté** - Architecture détaillée
- **Tests unitaires** - Validation fonctionnelle

## 🤝 Contribution

### **Structure du projet**

```
kitchen_ml_planner/
├── modern_kitchen_planner_app.py  # Backend Flask
├── templates/
│   └── modern_kitchen_planner.html  # Interface web
├── static/
│   ├── advanced-planner.js         # Logique frontend
│   └── advanced-styles.css         # Styles avancés
├── data/exports/                   # Fichiers exportés
└── GUIDE_UTILISATION_MODERNE.md   # Documentation
```

### **Ajout de fonctionnalités**

1. **Équipements** : Modifier `EQUIPMENT_DATABASE`
2. **Règles HACCP** : Mettre à jour `HACCP_RULES`
3. **Styles** : Éditer `advanced-styles.css`
4. **Logique** : Enrichir `advanced-planner.js`

## 📞 Support

### **Documentation**
- 📖 Guide utilisateur complet
- 🎥 Tutoriels vidéo (à venir)
- 💬 FAQ et dépannage

### **Problèmes courants**
- **Performance lente** : Réduire le nombre d'éléments, fermer autres onglets
- **Sauvegarde échoue** : Vérifier cookies, espace stockage
- **Cotations invisibles** : Activer avec bouton 📏 ou touche `D`

---

## 🎯 Roadmap

### **Version 2.1** (Prochaine)
- 🎨 Thèmes personnalisables
- 📐 Outils de mesure avancés
- 🔄 Import/Export DXF
- 📱 Application mobile native

### **Version 2.2**
- 🤖 IA pour optimisation automatique
- ☁️ Sauvegarde cloud
- 👥 Collaboration en temps réel
- 📊 Analytics avancées

### **Version 3.0**
- 🥽 Vue 3D immersive
- 🎮 Mode réalité virtuelle
- 📈 Simulation de rentabilité
- 🌍 Multi-langues

---

**Kitchen Planner Pro** - *Révolutionnez la conception de vos cuisines professionnelles* 🍳✨

*Interface modernisée avec drag & drop intelligent, cotations temps réel et simulation cuisiniers*
