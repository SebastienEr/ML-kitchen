#!/usr/bin/env bash
# run_complete.sh - Pipeline complet avec toutes les fonctionnalités avancées

set -e

echo "🍳 Kitchen ML Planner - Pipeline Complet v2.0"
echo "=============================================="
echo ""

# Vérification de l'environnement
echo "🔧 Vérification de l'environnement..."
if ! command -v python &> /dev/null; then
    echo "❌ Python n'est pas installé"
    exit 1
fi

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip install -q -r requirements.txt

# Création des dossiers
mkdir -p data/{raw_plans,structured,embeddings,exports} templates static

echo "✅ Environnement prêt"
echo ""

# Étape 1: Parsing des PDFs
echo "📄 Étape 1: Parsing des plans PDF"
echo "--------------------------------"
if [ -d "data/raw_plans" ] && [ "$(ls -A data/raw_plans 2>/dev/null)" ]; then
    echo "🔍 Plans PDF trouvés, parsing en cours..."
    python ingest/parse_plans.py
else
    echo "ℹ️  Aucun plan PDF trouvé, génération de plans d'exemple..."
    bash demo.sh
fi
echo ""

# Étape 2: Construction de l'index vectoriel
echo "🧠 Étape 2: Construction de l'index vectoriel"
echo "--------------------------------------------"
python embeddings/build_index.py
echo ""

# Étape 3: Génération de plan avec RAG
echo "🤖 Étape 3: Génération de plan avec RAG"
echo "--------------------------------------"
echo "🔄 Génération d'un plan personnalisé..."
python rag/generate_plan.py "Restaurant moderne avec cuisine ouverte, spécialité grillades et cuisine méditerranéenne, 40 couverts"
echo ""

# Étape 4: Visualisation 2D
echo "🎨 Étape 4: Visualisation du plan"
echo "--------------------------------"
if [ -f "data/exports/generated_plan.json" ]; then
    python modules/draw_plan.py data/exports/generated_plan.json data/exports/plan_visu.png
    echo "✅ Plan visualisé: data/exports/plan_visu.png"
else
    echo "❌ Aucun plan généré à visualiser"
fi
echo ""

# Étape 5: Validation qualité
echo "✅ Étape 5: Validation qualité"
echo "-----------------------------"
python validate.py
echo ""

# Étape 6: Réparation si nécessaire
echo "🔧 Étape 6: Réparation automatique"
echo "---------------------------------"
python repair_plans.py --all
echo ""

# Étape 7: Export CAD
echo "📐 Étape 7: Export CAD (DXF)"
echo "---------------------------"
python export_cad.py --all
echo ""

# Étape 8: Estimation des coûts
echo "💰 Étape 8: Estimation des coûts"
echo "-------------------------------"
for plan in data/exports/*.json; do
    if [ -f "$plan" ]; then
        echo "💶 Estimation pour $(basename "$plan"):"
        python cost_estimation.py "$plan" | head -20
        echo ""
    fi
done

echo "🎉 PIPELINE TERMINÉ AVEC SUCCÈS !"
echo "================================="
echo ""
echo "📁 Fichiers générés:"
echo "   • Plans JSON: data/exports/*.json"
echo "   • Visualisations: data/exports/*.png"
echo "   • Export CAD: data/exports/*.dxf"
echo ""
echo "🌐 Interface web disponible:"
echo "   python start_web.py"
echo ""
echo "🔧 Commandes utiles:"
echo "   • Interface web: python start_web.py"
echo "   • Réparation: python repair_plans.py --all"
echo "   • Validation: python validate.py"
echo "   • Export CAD: python export_cad.py <plan.json>"
echo "   • Coûts: python cost_estimation.py <plan.json>"
echo "   • Plans démo: bash demo.sh"
