# 🍳 Kitchen ML Planner v2.0

Pipeline ML local pour générer automatiquement des agencements de cuisine professionnels à partir de plans PDF et d'un brief utilisateur.

## 🚀 Lancement rapide

```bash
# Installation des dépendances
pip install -r requirements.txt

# Interface web (recommandé)
python start_web.py

# Pipeline complet en ligne de commande
./run_complete.sh
```

## ✨ Fonctionnalités principales

- 📄 **Parsing PDF automatique** : Extraction des équipements et zones depuis vos plans existants
- 🧠 **Recherche sémantique** : Index FAISS pour retrouver les plans similaires 
- 🎯 **Génération intelligente** : Plans optimisés selon votre brief
- 🎨 **Visualisation 2D/3D** : Plans colorés avec zones nommées
- 🌐 **Interface web interactive** : Dashboard moderne et intuitif
- 📐 **Export CAD (DXF)** : Compatible AutoCAD, FreeCAD, QCAD
- 💰 **Estimation des coûts** : Budget détaillé par zone
- 🏥 **Analyse HACCP** : Conformité sanitaire automatique
- 🔧 **Réparation automatique** : Correction des chevauchements
- ✅ **Validation qualité** : Détection des problèmes

## 🌐 Interface Web

L'interface web offre une expérience utilisateur moderne et intuitive :

```bash
python start_web.py
# Ouvre automatiquement http://localhost:5000
```

**Fonctionnalités web :**
- Génération de plans en temps réel
- Visualisation interactive
- Téléchargement des résultats
- Plans d'exemple intégrés
- Validation automatique

## 🎯 Types de cuisine supportés

### 🏠 Cuisine Compacte (20m²)
```json
{
  "zones": 5,
  "surface": "20m²",
  "usage": "Petite restauration, food trucks"
}
```

### 🍽️ Brasserie (30m²)
```json
{
  "zones": 9,
  "surface": "30m²", 
  "usage": "Restaurant 50-80 couverts"
}
```

### ⭐ Gastronomique (36m²)
```json
{
  "zones": 12,
  "surface": "36m²",
  "usage": "Haute gastronomie, service premium"
}
```

## 📋 Workflow du pipeline

### 1. 📄 Ingestion des plans PDF
```bash
python ingest/parse_plans.py
```
- Extraction automatique des équipements et zones
- Support des plans architecturaux standards
- Génération de JSON structurés

### 2. 🔍 Indexation vectorielle
```bash
python embeddings/build_index.py
```
- Embeddings sémantiques avec `all-MiniLM-L6-v2`
- Index FAISS pour recherche rapide
- Support de milliers de plans

### 3. 🤖 Génération RAG
```bash
python rag/generate_plan.py "Restaurant italien moderne"
```
- Recherche des plans les plus pertinents
- Génération adaptée au brief utilisateur
- Plans optimisés pour cuisines professionnelles

### 4. 🎨 Visualisation
```bash
# Visualisation 2D
python modules/draw_plan.py plan.json plan.png

# Visualisation 3D (multiple vues)
python render_3d.py plan.json --multiple
```

## 🚀 Fonctionnalités avancées

### 📐 Export CAD (DXF)
```bash
# Export un plan spécifique
python export_cad.py data/exports/plan_brasserie.json

# Export tous les plans
python export_cad.py --all
```
**Compatible avec :** AutoCAD, FreeCAD, QCAD, SketchUp

### 💰 Estimation des coûts
```bash
python cost_estimation.py data/exports/plan_brasserie.json
```

**Analyse détaillée :**
- Coût par zone (équipements + installation)
- Infrastructure (électricité, plomberie, ventilation)
- Certifications HACCP
- Budget total avec imprévu

### 🏥 Analyse HACCP
```bash
python haccp_analysis.py data/exports/plan_brasserie.json
```

**Vérifications :**
- ✅ Principe de marche en avant
- ✅ Séparation chaud/froid
- ✅ Proximité des zones de lavage
- ✅ Accessibilité du stockage
- 📋 Points critiques de contrôle (CCP)

### 🔧 Réparation automatique
```bash
# Répare un plan spécifique
python repair_plans.py data/exports/mon_plan.json

# Répare tous les plans
python repair_plans.py --all
```

### ✅ Validation qualité
```bash
python validate.py
```

**Contrôles :**
- Détection des chevauchements
- Validation des surfaces
- Métriques de qualité
- Recommandations d'optimisation

## 📁 Structure du projet

```
kitchen_ml_planner/
├── 🌐 start_web.py             # Interface web
├── 🔄 run_complete.sh          # Pipeline complet
├── 🎬 demo.sh                  # Plans d'exemple
├── ✅ validate.py              # Validation qualité
├── 🔧 repair_plans.py          # Réparation automatique
├── 📐 export_cad.py            # Export DXF
├── 🏗️ render_3d.py             # Visualisation 3D
├── 💰 cost_estimation.py       # Estimation coûts
├── 🏥 haccp_analysis.py        # Analyse HACCP
├── 📋 requirements.txt         # Dépendances Python
├── 📖 README_v2.md             # Documentation
│
├── 📂 templates/               # Interface web
│   └── index.html
├── 📂 static/                  # Ressources web
│
├── 📂 data/
│   ├── 📂 raw_plans/          # PDFs sources
│   ├── 📂 structured/         # JSON extraits
│   ├── 📂 embeddings/         # Index FAISS
│   └── 📂 exports/            # Plans générés
│       ├── *.json             # Plans JSON
│       ├── *.png              # Visualisations 2D
│       ├── *.dxf              # Export CAD
│       └── *_3d_*.png         # Visualisations 3D
│
├── 📂 ingest/                 # Parsing PDF
├── 📂 embeddings/             # Indexation vectorielle
├── 📂 rag/                    # Génération RAG
└── 📂 modules/                # Visualisation 2D
```

## 💻 Installation et configuration

### Prérequis
- Python 3.8+
- pip (gestionnaire de packages Python)
- 4GB RAM minimum
- 1GB espace disque

### Installation automatique
```bash
git clone <votre-repo>
cd kitchen_ml_planner
pip install -r requirements.txt
```

### Installation manuelle
```bash
pip install pymupdf sentence-transformers faiss-cpu matplotlib gpt4all numpy flask
```

## 📝 Utilisation détaillée

### Mode interface web (recommandé)
```bash
python start_web.py
```
1. Ouvrez http://localhost:5000
2. Décrivez votre cuisine dans le formulaire
3. Choisissez le type et la surface
4. Cliquez sur "Générer le plan"
5. Téléchargez les résultats

### Mode ligne de commande
```bash
# Pipeline complet
./run_complete.sh

# Génération personnalisée
python rag/generate_plan.py "Restaurant japonais 25 couverts"

# Visualisation spécifique
python render_3d.py data/exports/mon_plan.json --multiple
```

## 🎯 Format des plans générés

```json
{
  "zones": [
    {
      "name": "Préparation Froide",
      "x": 2,      // Position X (mètres)
      "y": 0,      // Position Y (mètres)
      "w": 3,      // Largeur (mètres)
      "h": 2       // Hauteur (mètres)
    }
  ]
}
```

## 📊 Zones supportées

| Zone | Description | Équipements typiques | Surface moy. |
|------|-------------|---------------------|--------------|
| **Réception** | Arrivée marchandises | Balance, tables de contrôle | 2-4m² |
| **Stockage Sec** | Produits secs | Étagères métalliques | 4-8m² |
| **Stockage Froid** | Chambre froide | Réfrigération, étagères | 6-12m² |
| **Préparation Froide** | Sans cuisson | Tables inox, éviers | 8-15m² |
| **Préparation Chaude** | Avec cuisson | Tables chauffantes | 6-12m² |
| **Cuisson** | Zone principale | Fours, plaques, friteuses | 10-20m² |
| **Dressage** | Finition plats | Passe-plats, lampes | 4-8m² |
| **Plonge** | Nettoyage | Lave-vaisselle industriel | 6-10m² |
| **Service** | Expédition | Réchauds, chariots | 4-8m² |

## 🎛️ Personnalisation avancée

### Modifier les types de zones
```python
# Dans rag/generate_plan.py
CUSTOM_ZONES = [
    {"name": "Ma Zone", "x": 0, "y": 0, "w": 2, "h": 1}
]
```

### Adapter l'analyse HACCP
```python
# Dans haccp_analysis.py
CUSTOM_RULES = {
    "ma_regle": {
        "description": "Ma règle personnalisée",
        "critical": True
    }
}
```

### Personnaliser les coûts
```python
# Dans cost_estimation.py
CUSTOM_COSTS = {
    "Ma Zone": {
        "base": 1500,  # €/m²
        "equipment": ["Mon équipement"]
    }
}
```

## 📈 Métriques et KPI

### Qualité des plans
- Score de conformité HACCP (0-100%)
- Détection des chevauchements
- Optimisation des flux
- Ratios de surface

### Performance
- Génération : < 5 secondes
- Validation : < 1 seconde
- Visualisation 3D : < 10 secondes
- Export CAD : < 2 secondes

## 🔧 Résolution de problèmes

### Erreur d'import
```bash
pip install --upgrade -r requirements.txt
```

### Plans vides
```bash
# Régénère les plans d'exemple
bash demo.sh
```

### Chevauchements détectés
```bash
# Réparation automatique
python repair_plans.py --all
```

### Interface web inaccessible
```bash
# Vérification du port
lsof -i :5000
# Changement de port si nécessaire
python web_interface.py --port 8080
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajoute nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Sentence Transformers](https://www.sbert.net/) pour les embeddings
- [FAISS](https://faiss.ai/) pour la recherche vectorielle
- [Matplotlib](https://matplotlib.org/) pour les visualisations
- [Flask](https://flask.palletsprojects.com/) pour l'interface web

---

**Kitchen ML Planner v2.0** - Générez des cuisines professionnelles optimisées en quelques secondes ! 🚀🍳
