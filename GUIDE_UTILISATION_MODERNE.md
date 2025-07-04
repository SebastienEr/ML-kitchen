# 🍳 Kitchen Planner Pro - Guide Utilisateur Complet

## 🚀 Interface Modernisée et Interactive

### 📋 **Table des Matières**
1. [Vue d'ensemble](#vue-densemble)
2. [Interface utilisateur](#interface-utilisateur)
3. [Fonctionnalités principales](#fonctionnalités-principales)
4. [Drag & Drop avancé](#drag--drop-avancé)
5. [Cotations et mesures](#cotations-et-mesures)
6. [Simulation avec cuisiniers](#simulation-avec-cuisiniers)
7. [Validation HACCP](#validation-haccp)
8. [Raccourcis clavier](#raccourcis-clavier)
9. [Export et sauvegarde](#export-et-sauvegarde)
10. [Dépannage](#dépannage)

---

## 🔍 Vue d'ensemble

**Kitchen Planner Pro** est une interface web moderne et interactive pour concevoir des cuisines professionnelles. L'application offre :

- **Drag & Drop intelligent** avec magnétisme automatique
- **Cotations en temps réel** avec dimensions précises
- **Simulation avec petits cuisiniers** animés
- **Validation HACCP automatique** selon les normes
- **Battements de portes** et couloirs de circulation
- **Export professionnel** (JSON + PNG haute résolution)

---

## 🖥️ Interface utilisateur

### **Layout Principal**
```
┌─────────────────────────────────────────────┐
│              🍳 Kitchen Planner Pro         │ ← Header
├─────────────┬───────────────────────────────┤
│   Sidebar   │        Canvas Principal       │
│             │                               │
│ 🔥 Cuisson  │     [Zone de conception]      │
│ ❄️ Réfrigé. │                               │
│ 🚿 Lavage   │     📏 Cotations             │
│ 🥄 Prépara. │     👨‍🍳 Cuisiniers            │
│             │     🚪 Portes                │
│ 📊 Stats    │                               │
└─────────────┴───────────────────────────────┘
            📋 Toolbar flottant
```

### **Zones principales**

1. **Header** : Boutons d'action globaux
2. **Sidebar** : Catalogue d'équipements et statistiques
3. **Canvas** : Zone de conception avec grille magnétique
4. **Propriétés** : Panel latéral pour éditer les éléments
5. **Toolbar** : Outils de dessin et mesure

---

## ⭐ Fonctionnalités principales

### **1. Gestion des équipements**

#### **Catégories disponibles :**
- 🔥 **Cuisson** : Four, plancha, friteuse, grill
- ❄️ **Réfrigération** : Frigo, congélateur, cellule, cave
- 🚿 **Lavage** : Plonge, lave-vaisselle, évier, bac
- 🥄 **Préparation** : Table, billot, plan, étagère

#### **Propriétés modifiables :**
- **Dimensions** : Largeur × Hauteur (en cm)
- **Position** : Coordonnées X, Y précises
- **Nom** : Libellé personnalisé
- **Rotation** : Orientation (0°, 90°, 180°, 270°)

### **2. Interface de conception**

#### **Grille magnétique**
- **Pas de 20cm** pour placement précis
- **Attraction automatique** vers les guides
- **Alignement intelligent** entre équipements

#### **Détection de collision**
- **Alerte visuelle** en temps réel
- **Repositionnement automatique** si nécessaire
- **Respect des distances HACCP**

---

## 🎯 Drag & Drop avancé

### **Glisser-déposer depuis la sidebar**

1. **Sélectionner** un équipement dans la sidebar
2. **Maintenir** le clic et faire glisser vers le canvas
3. **Relâcher** à l'emplacement désiré
4. L'équipement se **place automatiquement** sur la grille

### **Déplacement sur le canvas**

```
🖱️ Clic + glisser     → Déplacement libre
⚏ Grille activée      → Magnétisme automatique
🔍 Collision détectée  → Alerte + repositionnement
📏 Dimensions          → Affichage en temps réel
```

### **Redimensionnement**

- **Poignées** aux 4 coins de chaque équipement
- **Contraintes** : dimensions min/max respectées
- **Proportions** : maintien du ratio si souhaité
- **Mise à jour** automatique des cotations

---

## 📏 Cotations et mesures

### **Affichage des dimensions**

#### **Activation :**
- Bouton **📏 Cotations** dans le header
- Raccourci clavier : **`D`**

#### **Informations affichées :**
- **Largeur** de chaque équipement (en cm)
- **Hauteur** de chaque équipement (en cm)
- **Distances** entre éléments
- **Couloirs** et zones de circulation

### **Types de mesures**

| Type | Description | Affichage |
|------|-------------|-----------|
| **Équipement** | Dimensions L×H | `120×80 cm` |
| **Distance** | Entre 2 éléments | `↔ 85 cm` |
| **Couloir** | Largeur passage | `Couloir: 120 cm` |
| **Surface** | Zone totale | `4.2 m²` |

### **Normes HACCP**

- **Couloir minimum** : 120 cm de large
- **Distance cuisson/froid** : 100 cm minimum
- **Battement de porte** : 90 cm de dégagement
- **Accès d'urgence** : 80 cm minimum

---

## 👨‍🍳 Simulation avec cuisiniers

### **Ajout de cuisiniers**

#### **Méthodes :**
1. Bouton **👨‍🍳 Ajouter Cuisinier** dans le header
2. Placement automatique dans une zone libre
3. Déplacement par glisser-déposer

### **Animations et comportements**

#### **Mouvements automatiques :**
- **Déplacement aléatoire** toutes les 3-8 secondes
- **Évitement des équipements** et murs
- **Changement d'humeur** occasionnel

#### **Interactions :**
- **Double-clic** : Déclenche animation de marche
- **Clic droit** : Menu contextuel spécialisé
- **Glisser-déposer** : Repositionnement manuel

### **Indicateurs visuels**

```
👨‍🍳 → Cuisinier heureux
😊 → Satisfait du layout
🤔 → Réfléchit à l'organisation
😅 → Stressé (problème détecté)
🙂 → Neutre
```

### **Analyse ergonomique**

L'application calcule automatiquement :
- **Distances de déplacement** moyennes
- **Zones de congestion** potentielles
- **Efficacité des flux** de travail
- **Temps de parcours** estimés

---

## ✅ Validation HACCP

### **Contrôles automatiques**

#### **Sécurité alimentaire :**
- ✅ Séparation **cuisson/réfrigération**
- ✅ Marche en avant respectée
- ✅ Zones de contamination isolées
- ✅ Accès de nettoyage suffisants

#### **Circulation :**
- ✅ Largeur des couloirs (min 120cm)
- ✅ Sorties de secours dégagées
- ✅ Flux logiques du personnel
- ✅ Livraisons/évacuation distinctes

#### **Ergonomie :**
- ✅ Distances de travail optimales
- ✅ Hauteurs de plan adaptées
- ✅ Éclairage des postes
- ✅ Ventilation adéquate

### **Système d'alertes**

#### **Types de violations :**

| Niveau | Couleur | Description | Action |
|--------|---------|-------------|--------|
| 🔴 **Erreur** | Rouge | Violation majeure | Correction obligatoire |
| 🟡 **Attention** | Orange | Amélioration souhaitable | Recommandation |
| 🟢 **Conforme** | Vert | Aux normes | Validation |

#### **Affichage des alertes :**
- **Surbrillance** des éléments problématiques
- **Tooltip** avec message explicatif
- **Suggestion** de correction automatique
- **Score d'efficacité** mis à jour

---

## ⌨️ Raccourcis clavier

### **Actions globales**

| Raccourci | Action |
|-----------|--------|
| `Ctrl + S` | Sauvegarder le layout |
| `Ctrl + Z` | Annuler la dernière action |
| `Ctrl + Y` | Rétablir |
| `Ctrl + A` | Sélectionner tout |
| `Ctrl + D` | Dupliquer la sélection |

### **Navigation et affichage**

| Raccourci | Action |
|-----------|--------|
| `G` | Activer/désactiver la grille |
| `M` | Magnétisme on/off |
| `D` | Afficher/masquer les cotations |
| `H` | Validation HACCP |
| `Espace` | Ajouter un cuisinier |

### **Sélection et édition**

| Raccourci | Action |
|-----------|--------|
| `Échap` | Désélectionner tout |
| `Suppr` | Supprimer la sélection |
| `F2` | Renommer l'élément |
| `Ctrl + Clic` | Sélection multiple |
| `↑↓←→` | Déplacer précisément |

### **Outils de dessin**

| Raccourci | Action |
|-----------|--------|
| `S` | Outil sélection |
| `W` | Outil mur |
| `O` | Outil porte |
| `C` | Outil couloir |
| `R` | Outil mesure |

---

## 💾 Export et sauvegarde

### **Sauvegarde automatique**

- **Sauvegarde locale** dans le navigateur
- **Historique** des 50 dernières actions
- **Récupération** automatique au rechargement

### **Export professionnel**

#### **Formats disponibles :**

1. **JSON** : Métadonnées complètes
   ```json
   {
     "layout": { ... },
     "metadata": {
       "timestamp": "2025-07-04T10:30:00Z",
       "efficiency": 87.5,
       "violations": [],
       "stats": { ... }
     }
   }
   ```

2. **PNG haute résolution** : Image du layout
   - Résolution : 1200×800 pixels
   - Cotations incluses
   - Légende automatique
   - Échelle proportionnelle

#### **Contenu de l'export :**
- **Plan complet** avec équipements
- **Cotations et mesures** précises
- **Cuisiniers** et leurs positions
- **Statistiques** de performance
- **Violations HACCP** détectées
- **Suggestions** d'amélioration

### **Import de layouts**

- **Glisser-déposer** de fichiers JSON
- **Restauration** complète de l'état
- **Validation** automatique à l'import
- **Mise à jour** des statistiques

---

## 🛠️ Fonctionnalités avancées

### **Menu contextuel (clic droit)**

Sur un équipement :
- 🔄 **Dupliquer**
- 🔄 **Rotation** (90°)
- ⚙️ **Propriétés** détaillées
- ⬆️ **Premier plan**
- ⬇️ **Arrière-plan**
- 🗑️ **Supprimer**

### **Modes d'affichage**

#### **Vue thermique**
- **Zones chaudes** en rouge (cuisson)
- **Zones froides** en bleu (réfrigération)
- **Gradient de température** visible

#### **Vue flux de travail**
- **Connexions** entre équipements
- **Chemins optimaux** suggérés
- **Goulots d'étranglement** identifiés

### **Mini-carte**

- **Vue d'ensemble** en temps réel
- **Navigation rapide** dans les grands layouts
- **Zoom et panoramique** intégrés

---

## 🔧 Dépannage

### **Problèmes courants**

#### **L'équipement ne se place pas**
- ✅ Vérifier qu'il n'y a pas de collision
- ✅ Activer la grille magnétique (`G`)
- ✅ Zoom suffisant pour voir les détails

#### **Les cotations ne s'affichent pas**
- ✅ Activer les cotations (`D`)
- ✅ Sélectionner au moins un équipement
- ✅ Vérifier le niveau de zoom

#### **Performance lente**
- ✅ Réduire le nombre d'équipements
- ✅ Fermer les autres onglets
- ✅ Actualiser la page

#### **Sauvegarde ne fonctionne pas**
- ✅ Vérifier les cookies autorisés
- ✅ Espace de stockage disponible
- ✅ Navigateur compatible

### **Compatibilité navigateurs**

| Navigateur | Version min | Support |
|------------|-------------|---------|
| Chrome | 90+ | ✅ Complet |
| Firefox | 88+ | ✅ Complet |
| Safari | 14+ | ✅ Complet |
| Edge | 90+ | ✅ Complet |

### **Configuration recommandée**

- **Résolution** : 1920×1080 minimum
- **RAM** : 4 GB minimum
- **Connexion** : Non requise (fonctionne hors ligne)

---

## 📞 Support et assistance

### **Assistance technique**
- **Documentation** : Ce guide complet
- **Exemples** : Layouts de démonstration inclus
- **Tutoriels** : Vidéos et guides pas-à-pas

### **Mises à jour**
- **Auto-actualisation** des nouvelles fonctionnalités
- **Notifications** des améliorations
- **Compatibilité** ascendante garantie

---

## 🎯 Conseils pour bien commencer

### **Première utilisation**

1. **Familiarisez-vous** avec l'interface
2. **Testez** le drag & drop avec quelques équipements
3. **Activez les cotations** pour voir les dimensions
4. **Ajoutez des cuisiniers** pour la simulation
5. **Exportez** votre premier layout

### **Bonnes pratiques**

- **Commencer par les gros équipements** (fours, chambres froides)
- **Respecter les flux logiques** (réception → stockage → préparation → cuisson → service)
- **Prévoir les couloirs** dès le début
- **Tester avec des cuisiniers** pour valider l'ergonomie
- **Sauvegarder régulièrement** pendant la conception

### **Optimisation des layouts**

1. **Grouper par fonction** (zones homogènes)
2. **Minimiser les déplacements** du personnel
3. **Respecter les normes HACCP** (validation automatique)
4. **Prévoir l'évolutivité** (espaces modulables)
5. **Tester différentes configurations** (historique des versions)

---

*Kitchen Planner Pro - Conception professionnelle de cuisines industrielles*
*Version 2.0 - Interface modernisée et interactive*
