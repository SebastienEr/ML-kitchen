#!/usr/bin/env bash
# demo_complet.sh - Démonstration complète de toutes les fonctionnalités

set -e

echo "🍳 Kitchen ML Planner v2.0 - Démonstration Complète"
echo "===================================================="
echo ""

# Vérification de l'environnement
echo "🔧 Vérification de l'environnement..."
if ! command -v python &> /dev/null; then
    echo "❌ Python n'est pas installé"
    exit 1
fi

pip install -q -r requirements.txt
echo "✅ Dépendances installées"
echo ""

# Création des dossiers
mkdir -p data/{raw_plans,structured,embeddings,exports} templates static

# 1. Génération des plans d'exemple
echo "🎬 1. Génération des plans d'exemple"
echo "-----------------------------------"
bash demo.sh
echo ""

# 2. Construction de l'index
echo "🧠 2. Construction de l'index vectoriel"
echo "--------------------------------------"
python embeddings/build_index.py
echo ""

# 3. Génération d'un plan personnalisé
echo "🤖 3. Génération d'un plan personnalisé"
echo "--------------------------------------"
python rag/generate_plan.py "Restaurant méditerranéen moderne avec terrasse, spécialité poissons grillés, 60 couverts, cuisine semi-ouverte"
echo ""

# 4. Validation de tous les plans
echo "✅ 4. Validation qualité de tous les plans"
echo "-----------------------------------------"
python validate.py
echo ""

# 5. Réparation automatique
echo "🔧 5. Réparation automatique des problèmes"
echo "-----------------------------------------"
python repair_plans.py --all
echo ""

# 6. Visualisation 3D
echo "🏗️ 6. Génération des visualisations 3D"
echo "--------------------------------------"
for plan in data/exports/plan_*.json; do
    if [ -f "$plan" ]; then
        echo "🎨 Rendu 3D de $(basename "$plan")..."
        python render_3d.py "$plan" --multiple
    fi
done
echo ""

# 7. Export CAD
echo "📐 7. Export CAD (DXF) de tous les plans"
echo "---------------------------------------"
python export_cad.py --all
echo ""

# 8. Estimation des coûts
echo "💰 8. Estimation des coûts détaillée"
echo "-----------------------------------"
for plan in data/exports/plan_*.json; do
    if [ -f "$plan" ]; then
        echo ""
        echo "💶 Estimation pour $(basename "$plan"):"
        echo "======================================"
        python cost_estimation.py "$plan" | head -25
        echo ""
    fi
done

# 9. Analyse HACCP
echo "🏥 9. Analyse HACCP (conformité sanitaire)"
echo "-----------------------------------------"
for plan in data/exports/plan_*.json; do
    if [ -f "$plan" ]; then
        echo ""
        echo "🔍 Analyse HACCP pour $(basename "$plan"):"
        echo "======================================="
        python haccp_analysis.py "$plan" | head -20
        echo ""
    fi
done

# 10. Résumé des fichiers générés
echo "📁 10. Résumé des fichiers générés"
echo "---------------------------------"
echo ""

echo "📊 STATISTIQUES FINALES"
echo "======================="
json_count=$(ls data/exports/*.json 2>/dev/null | wc -l | tr -d ' ')
png_count=$(ls data/exports/*.png 2>/dev/null | wc -l | tr -d ' ')
dxf_count=$(ls data/exports/*.dxf 2>/dev/null | wc -l | tr -d ' ')

echo "• Plans JSON générés: $json_count"
echo "• Visualisations PNG: $png_count"
echo "• Exports DXF: $dxf_count"
echo ""

echo "📂 FICHIERS DISPONIBLES"
echo "======================="
echo ""

if [ -d "data/exports" ]; then
    echo "📄 Plans JSON:"
    ls -la data/exports/*.json 2>/dev/null | awk '{print "   • " $9 " (" $5 " bytes)"}' || echo "   Aucun fichier JSON"
    echo ""
    
    echo "🎨 Visualisations 2D:"
    ls -la data/exports/*.png 2>/dev/null | grep -v "_3d_" | awk '{print "   • " $9 " (" $5 " bytes)"}' || echo "   Aucune visualisation 2D"
    echo ""
    
    echo "🏗️ Visualisations 3D:"
    ls -la data/exports/*_3d_*.png 2>/dev/null | awk '{print "   • " $9 " (" $5 " bytes)"}' || echo "   Aucune visualisation 3D"
    echo ""
    
    echo "📐 Exports CAD (DXF):"
    ls -la data/exports/*.dxf 2>/dev/null | awk '{print "   • " $9 " (" $5 " bytes)"}' || echo "   Aucun export DXF"
    echo ""
fi

echo "🌐 INTERFACE WEB"
echo "==============="
echo ""
echo "L'interface web est disponible via:"
echo "   python start_web.py"
echo ""
echo "Fonctionnalités web:"
echo "• Génération interactive de plans"
echo "• Visualisation en temps réel"
echo "• Téléchargement des résultats"
echo "• Validation automatique"
echo ""

echo "🎯 COMMANDES UTILES"
echo "=================="
echo ""
echo "Interface web:"
echo "   python start_web.py"
echo ""
echo "Pipeline complet:"
echo "   ./run_complete.sh"
echo ""
echo "Génération personnalisée:"
echo "   python rag/generate_plan.py \"Votre description\""
echo ""
echo "Validation:"
echo "   python validate.py"
echo ""
echo "Réparation:"
echo "   python repair_plans.py --all"
echo ""
echo "Export CAD:"
echo "   python export_cad.py data/exports/mon_plan.json"
echo ""
echo "Visualisation 3D:"
echo "   python render_3d.py data/exports/mon_plan.json --multiple"
echo ""
echo "Coûts:"
echo "   python cost_estimation.py data/exports/mon_plan.json"
echo ""
echo "HACCP:"
echo "   python haccp_analysis.py data/exports/mon_plan.json"
echo ""

echo "🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS !"
echo "======================================"
echo ""
echo "✨ Kitchen ML Planner v2.0 est maintenant prêt à l'emploi !"
echo ""
echo "📖 Consultez README_v2.md pour la documentation complète"
echo "🌐 Lancez python start_web.py pour l'interface graphique"
echo "🚀 Bonne génération de plans de cuisine !"
