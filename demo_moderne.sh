#!/bin/bash

# 🍳 Kitchen Planner Pro - Script de Démonstration Moderne
# Interface interactive avec drag & drop, cotations, et simulation

echo "🍳 Kitchen Planner Pro - Démonstration Interactive"
echo "=================================================="
echo ""

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'attente interactive
wait_for_user() {
    echo ""
    echo -e "${CYAN}[Appuyez sur Entrée pour continuer...]${NC}"
    read -r
}

# Fonction pour afficher les fonctionnalités
show_feature() {
    echo -e "${GREEN}✅ $1${NC}"
    echo -e "   $2"
    echo ""
}

# Introduction
echo -e "${PURPLE}🎯 NOUVELLE INTERFACE MODERNISÉE${NC}"
echo "================================="
echo ""
echo "Cette démonstration présente toutes les nouvelles fonctionnalités :"
echo ""
show_feature "Drag & Drop Intelligent" "Glissez-déposez avec magnétisme automatique"
show_feature "Cotations en Temps Réel" "Dimensions et mesures précises"
show_feature "Simulation Cuisiniers" "Petits personnages animés pour tester l'ergonomie"
show_feature "Validation HACCP" "Contrôles automatiques des normes"
show_feature "Battements de Portes" "Zones de dégagement visualisées"
show_feature "Export Professionnel" "JSON + Images haute résolution"

wait_for_user

# Vérification des prérequis
echo -e "${BLUE}🔍 Vérification des prérequis...${NC}"
echo ""

# Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python installé: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3 requis${NC}"
    exit 1
fi

# Flask
if python3 -c "import flask" 2>/dev/null; then
    FLASK_VERSION=$(python3 -c "import flask; print(flask.__version__)" 2>/dev/null)
    echo -e "${GREEN}✅ Flask installé: $FLASK_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Installation de Flask...${NC}"
    pip3 install flask
fi

# Pillow pour la génération d'images
if python3 -c "import PIL" 2>/dev/null; then
    echo -e "${GREEN}✅ Pillow installé${NC}"
else
    echo -e "${YELLOW}⚠️  Installation de Pillow...${NC}"
    pip3 install Pillow
fi

echo ""
echo -e "${GREEN}🎉 Tous les prérequis sont satisfaits !${NC}"

wait_for_user

# Préparation de l'environnement
echo -e "${BLUE}🛠️  Préparation de l'environnement...${NC}"
echo ""

# Création des dossiers nécessaires
mkdir -p data/exports
mkdir -p static
mkdir -p templates

echo -e "${GREEN}✅ Dossiers créés${NC}"

# Vérification des fichiers
FILES_TO_CHECK=(
    "modern_kitchen_planner_app.py"
    "templates/modern_kitchen_planner.html"
    "static/advanced-planner.js"
    "static/advanced-styles.css"
)

echo ""
echo -e "${BLUE}📁 Vérification des fichiers...${NC}"

for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(ls -lh "$file" | awk '{print $5}')
        echo -e "${GREEN}✅ $file ($SIZE)${NC}"
    else
        echo -e "${RED}❌ $file manquant${NC}"
    fi
done

wait_for_user

# Lancement de l'application
echo -e "${PURPLE}🚀 Lancement de Kitchen Planner Pro...${NC}"
echo ""

echo "Configuration de l'application :"
echo "• URL: http://localhost:5003"
echo "• Mode debug: Activé"
echo "• Interface: Moderne et interactive"
echo ""

# Test de disponibilité du port
if lsof -ti:5003 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Le port 5003 est déjà utilisé${NC}"
    echo "Arrêt du processus existant..."
    kill -9 $(lsof -ti:5003) 2>/dev/null || true
    sleep 2
fi

echo -e "${GREEN}🎯 Lancement de l'application...${NC}"
echo ""

# Lancement en arrière-plan
python3 modern_kitchen_planner_app.py &
APP_PID=$!

# Attendre que l'application démarre
echo "⏳ Démarrage en cours..."
sleep 3

# Vérifier si l'application est démarrée
if curl -s http://localhost:5003 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Application démarrée avec succès !${NC}"
else
    echo -e "${RED}❌ Erreur au démarrage${NC}"
    kill $APP_PID 2>/dev/null || true
    exit 1
fi

wait_for_user

# Guide d'utilisation interactif
echo -e "${PURPLE}📖 Guide d'utilisation interactif${NC}"
echo "================================="
echo ""

echo -e "${CYAN}🎯 FONCTIONNALITÉS PRINCIPALES${NC}"
echo ""

echo "1️⃣  DRAG & DROP INTELLIGENT"
echo "   • Glissez les équipements depuis la sidebar"
echo "   • Placement automatique sur la grille"
echo "   • Magnétisme et alignement automatique"
echo "   • Détection de collision en temps réel"
echo ""

echo "2️⃣  COTATIONS ET MESURES"
echo "   • Bouton 📏 'Cotations' dans le header"
echo "   • Dimensions affichées en temps réel"
echo "   • Distances entre équipements"
echo "   • Largeur des couloirs de circulation"
echo ""

echo "3️⃣  SIMULATION AVEC CUISINIERS"
echo "   • Bouton 👨‍🍳 'Ajouter Cuisinier'"
echo "   • Personnages animés qui se déplacent"
echo "   • Double-clic pour animation spéciale"
echo "   • Test ergonomique des flux de travail"
echo ""

echo "4️⃣  VALIDATION HACCP"
echo "   • Contrôles automatiques des normes"
echo "   • Alertes visuelles pour violations"
echo "   • Score d'efficacité en temps réel"
echo "   • Suggestions d'amélioration"
echo ""

wait_for_user

echo -e "${CYAN}⌨️  RACCOURCIS CLAVIER${NC}"
echo ""

echo "• Ctrl + S  → Sauvegarder"
echo "• Ctrl + Z  → Annuler"
echo "• Ctrl + Y  → Rétablir"
echo "• G         → Grille magnétique"
echo "• D         → Afficher cotations"
echo "• Suppr     → Supprimer sélection"
echo "• Échap     → Désélectionner"
echo ""

echo -e "${CYAN}🖱️  INTERACTIONS SOURIS${NC}"
echo ""

echo "• Clic gauche        → Sélectionner"
echo "• Clic + glisser     → Déplacer"
echo "• Clic droit         → Menu contextuel"
echo "• Double-clic        → Propriétés"
echo "• Molette            → Zoom"
echo "• Poignées d'angle   → Redimensionner"
echo ""

wait_for_user

echo -e "${CYAN}🏗️  ÉTAPES DE CONCEPTION${NC}"
echo ""

echo "1. 📋 PLANIFICATION"
echo "   → Définir les besoins et contraintes"
echo "   → Choisir la taille de la cuisine"
echo ""

echo "2. 🏗️  STRUCTURE"
echo "   → Placer les murs et cloisons"
echo "   → Définir les portes et passages"
echo "   → Marquer les couloirs principaux"
echo ""

echo "3. 🔥 ÉQUIPEMENTS LOURDS"
echo "   → Fours, chambres froides"
echo "   → Gros électroménager"
echo "   → Respecter les distances HACCP"
echo ""

echo "4. 🥄 ÉQUIPEMENTS SECONDAIRES"
echo "   → Tables de préparation"
echo "   → Étagères et rangements"
echo "   → Éviers et points d'eau"
echo ""

echo "5. 👨‍🍳 VALIDATION ERGONOMIQUE"
echo "   → Ajouter des cuisiniers"
echo "   → Tester les déplacements"
echo "   → Optimiser les flux"
echo ""

echo "6. 💾 FINALISATION"
echo "   → Activer les cotations"
echo "   → Vérifier la conformité HACCP"
echo "   → Exporter le plan final"
echo ""

wait_for_user

# Exemples de layouts prédéfinis
echo -e "${PURPLE}🎨 Exemples de layouts prédéfinis${NC}"
echo "================================="
echo ""

echo "L'application inclut plusieurs exemples :"
echo ""

echo "🏪 BRASSERIE TRADITIONNELLE"
echo "• Surface: 40-60 m²"
echo "• Grill, plancha, friteuse"
echo "• Zone de lavage optimisée"
echo "• Bar et service intégrés"
echo ""

echo "🍽️  RESTAURANT GASTRONOMIQUE"
echo "• Surface: 80-120 m²"
echo "• Multiple fours et stations"
echo "• Chambre froide et cellule"
echo "• Zone pâtisserie séparée"
echo ""

echo "☕ CAFÉ-RESTAURANT"
echo "• Surface: 25-40 m²"
echo "• Compact et fonctionnel"
echo "• Machine à café professionnelle"
echo "• Préparation rapide"
echo ""

wait_for_user

# Fonctionnalités avancées
echo -e "${PURPLE}⚡ Fonctionnalités avancées${NC}"
echo "=========================="
echo ""

echo "🎯 OPTIMISATION AUTOMATIQUE"
echo "• Algorithme de placement intelligent"
echo "• Regroupement par zones fonctionnelles"
echo "• Minimisation des déplacements"
echo ""

echo "📊 ANALYSE DE PERFORMANCE"
echo "• Score d'efficacité en temps réel"
echo "• Calcul des surfaces et volumes"
echo "• Analyse des flux de circulation"
echo ""

echo "🔍 MODES D'AFFICHAGE"
echo "• Vue thermique (chaud/froid)"
echo "• Vue flux de travail"
echo "• Mode technique (cotations)"
echo ""

echo "📱 EXPORT MULTI-FORMAT"
echo "• JSON avec métadonnées complètes"
echo "• PNG haute résolution"
echo "• Intégration future: DXF, PDF"
echo ""

wait_for_user

# Instructions de test
echo -e "${GREEN}🧪 Instructions de test${NC}"
echo "======================="
echo ""

echo "Maintenant, testez l'application :"
echo ""

echo "1️⃣  Ouvrez votre navigateur sur: ${CYAN}http://localhost:5003${NC}"
echo ""

echo "2️⃣  Faites glisser un four depuis la sidebar vers le canvas"
echo ""

echo "3️⃣  Cliquez sur 📏 'Cotations' pour voir les dimensions"
echo ""

echo "4️⃣  Ajoutez un cuisinier avec 👨‍🍳 'Ajouter Cuisinier'"
echo ""

echo "5️⃣  Double-cliquez sur le cuisinier pour l'animer"
echo ""

echo "6️⃣  Cliquez droit sur un équipement pour le menu contextuel"
echo ""

echo "7️⃣  Testez les raccourcis clavier (G pour grille, D pour cotations)"
echo ""

echo "8️⃣  Exportez votre création avec 📥 'Exporter'"
echo ""

wait_for_user

# Surveillance des logs
echo -e "${BLUE}📋 Surveillance de l'application${NC}"
echo ""

echo "L'application est maintenant en cours d'exécution."
echo "Vous pouvez:"
echo ""
echo "• Utiliser l'interface web: http://localhost:5003"
echo "• Consulter les logs en temps réel"
echo "• Arrêter avec Ctrl+C dans ce terminal"
echo ""

echo -e "${YELLOW}💡 Conseils d'utilisation:${NC}"
echo ""
echo "• Commencez par les gros équipements"
echo "• Utilisez la grille magnétique (G)"
echo "• Testez avec des cuisiniers"
echo "• Respectez les alertes HACCP"
echo "• Sauvegardez régulièrement"
echo ""

# Fonction de monitoring simple
monitor_app() {
    echo -e "${CYAN}📊 Monitoring de l'application...${NC}"
    echo "Press 'q' to quit monitoring"
    echo ""
    
    while true; do
        if ! kill -0 $APP_PID 2>/dev/null; then
            echo -e "${RED}❌ L'application s'est arrêtée${NC}"
            break
        fi
        
        # Vérifier si l'utilisateur veut quitter
        read -t 5 -n 1 key 2>/dev/null
        if [[ $key == "q" ]]; then
            break
        fi
        
        echo -n "."
    done
}

echo ""
echo -e "${GREEN}🎉 Démonstration terminée !${NC}"
echo ""
echo "L'application reste active. Options:"
echo ""
echo "• [M] Surveiller l'application"
echo "• [S] Arrêter l'application"
echo "• [Q] Quitter sans arrêter"
echo ""

read -p "Votre choix (M/S/Q): " choice

case $choice in
    [Mm]* )
        monitor_app
        ;;
    [Ss]* )
        echo "Arrêt de l'application..."
        kill $APP_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Application arrêtée${NC}"
        ;;
    [Qq]* )
        echo "L'application continue en arrière-plan."
        echo "Pour l'arrêter plus tard: kill $APP_PID"
        ;;
    * )
        echo "Option non reconnue. L'application continue."
        ;;
esac

echo ""
echo -e "${PURPLE}🍳 Merci d'avoir testé Kitchen Planner Pro !${NC}"
echo ""
echo "Pour plus d'informations:"
echo "• Guide complet: GUIDE_UTILISATION_MODERNE.md"
echo "• Code source: modern_kitchen_planner_app.py"
echo "• Documentation: README.md"
echo ""

exit 0
