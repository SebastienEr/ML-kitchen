#!/bin/bash
# demo_interactif.sh - Démonstration complète du Kitchen Planner Interactif

echo "🎨 DÉMONSTRATION KITCHEN PLANNER INTERACTIF"
echo "==========================================="
echo ""

# Vérification des prérequis
echo "🔍 Vérification des prérequis..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Fichier requirements.txt introuvable"
    exit 1
fi

# Installation des dépendances si nécessaire
echo "📦 Installation des dépendances..."
pip install -r requirements.txt > /dev/null 2>&1

# Création des dossiers nécessaires
echo "📁 Création des dossiers..."
mkdir -p data/exports
mkdir -p templates

echo ""
echo "✅ Prérequis vérifiés avec succès !"
echo ""

# Affichage des fonctionnalités
echo "🎯 FONCTIONNALITÉS DISPONIBLES"
echo "=============================="
echo ""
echo "🏗️  ZONES DE PRÉPARATION"
echo "   • Légumerie (tables inox, éviers multiples, bacs gastro)"
echo "   • Préparation Froide (tables réfrigérées, planches de découpe)"
echo "   • Préparation Chaude (tables chauffantes, bain-marie)"
echo "   • Pâtisserie (four spécialisé, batteur, laminoir)"
echo "   • Boucherie (billot, scie à os, hachoir)"
echo ""
echo "🔥 ZONES DE CUISSON"
echo "   • Zone Cuisson Principale (fours, plaques, salamandre)"
echo "   • Grillade (grill, plancha, extracteur)"
echo "   • Friture (friteuses, filtration d'huile)"
echo "   • Wok (feux wok, évacuation vapeur)"
echo ""
echo "❄️  ZONES DE STOCKAGE"
echo "   • Chambre Froide Positive (+2°C à +4°C)"
echo "   • Chambre Froide Négative (-18°C)"
echo "   • Stockage Sec (étagères métalliques)"
echo "   • Cave à Vin (climatisation spécialisée)"
echo "   • Réserve (rayonnages, chariots)"
echo ""
echo "🧽 ZONES DE LAVAGE"
echo "   • Plonge Batterie (lave-vaisselle à capot)"
echo "   • Plonge Légumes (bacs spécialisés, douchette)"
echo "   • Laverie (lave-linge, séchoir)"
echo ""
echo "🍽️  ZONES DE SERVICE"
echo "   • Dressage (passe, lampes chauffantes)"
echo "   • Office (machine à café, réfrigérateur)"
echo "   • Bar (comptoir, tireuses, lave-verre)"
echo "   • Expédition (chariots, étiqueteuse)"
echo ""
echo "🧼 ZONES D'HYGIÈNE"
echo "   • Vestiaires (casiers, bancs, miroirs)"
echo "   • Sanitaires (WC, lavabos, distributeurs)"
echo "   • Lave-Mains (commande non manuelle)"
echo "   • Sas d'Hygiène (pédiluve, gel hydroalcoolique)"
echo ""
echo "⚙️  ZONES TECHNIQUES"
echo "   • Local Poubelles (conteneurs, ventilation)"
echo "   • Local Technique (tableau électrique, chaudière)"
echo "   • Réception (quai de déchargement, balance)"
echo "   • Bureau (ordinateur, armoire, coffre-fort)"
echo ""

echo "🎮 CONTRÔLES DISPONIBLES"
echo "========================"
echo ""
echo "📐 Configuration de la Pièce :"
echo "   • Largeur : 8m à 30m (curseur + saisie précise)"
echo "   • Profondeur : 6m à 25m (curseur + saisie précise)"
echo "   • Largeur Couloirs : 1m à 3m (respect normes HACCP)"
echo ""
echo "🎯 Sélection des Zones :"
echo "   • Cases à cocher pour chaque zone"
echo "   • Ajustement des tailles (min/max réalistes)"
echo "   • Couleurs visuelles pour identification"
echo "   • Liste d'équipements pour chaque zone"
echo ""
echo "📊 Statistiques Temps Réel :"
echo "   • Nombre de zones sélectionnées"
echo "   • Surface utile totale (zones de travail)"
echo "   • Surface couloirs (circulation)"
echo "   • Efficacité d'occupation (%)"
echo ""
echo "💾 Sauvegarde et Export :"
echo "   • Format JSON complet avec métadonnées"
echo "   • Image PNG haute résolution (300 DPI)"
echo "   • Téléchargement automatique"
echo ""

echo "🚀 LANCEMENT DE L'INTERFACE"
echo "============================"
echo ""
echo "1. L'interface va se lancer sur le port 5001"
echo "2. Votre navigateur s'ouvrira automatiquement"
echo "3. Commencez à personnaliser votre cuisine !"
echo ""

# Attendre confirmation
read -p "▶️  Appuyez sur Entrée pour lancer l'interface interactive..."

echo ""
echo "🎨 Lancement de l'interface interactive..."
echo ""
echo "📍 URL : http://localhost:5001"
echo "🔄 Pour arrêter : Ctrl+C"
echo ""

# Démarrage du serveur
python3 interactive_planner.py
