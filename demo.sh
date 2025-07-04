#!/usr/bin/env bash

# Demo script - Génère plusieurs exemples de plans

echo "🎯 Génération de plans de démonstration"
echo ""

# Plan 1: Restaurant compact
echo "📝 Génération plan compact..."
python -c "
import json
plan_compact = {
    'zones': [
        {'name': 'Réception', 'x': 0, 'y': 0, 'w': 2, 'h': 1},
        {'name': 'Stockage', 'x': 0, 'y': 1, 'w': 2, 'h': 2},
        {'name': 'Préparation', 'x': 2, 'y': 0, 'w': 3, 'h': 2},
        {'name': 'Cuisson', 'x': 5, 'y': 0, 'w': 3, 'h': 2},
        {'name': 'Service', 'x': 8, 'y': 0, 'w': 2, 'h': 1}
    ]
}
with open('data/exports/plan_compact.json', 'w') as f:
    json.dump(plan_compact, f, indent=2)
print('✅ Plan compact généré')
"

# Plan 2: Brasserie traditionnelle
echo "📝 Génération plan brasserie..."
python -c "
import json
plan_brasserie = {
    'zones': [
        {'name': 'Réception', 'x': 0, 'y': 0, 'w': 2, 'h': 1},
        {'name': 'Stockage Sec', 'x': 0, 'y': 1, 'w': 2, 'h': 1},
        {'name': 'Stockage Froid', 'x': 0, 'y': 2, 'w': 2, 'h': 1},
        {'name': 'Préparation', 'x': 2, 'y': 0, 'w': 4, 'h': 2},
        {'name': 'Grillade', 'x': 6, 'y': 0, 'w': 2, 'h': 2},
        {'name': 'Friture', 'x': 8, 'y': 0, 'w': 2, 'h': 1},
        {'name': 'Dressage', 'x': 8, 'y': 1, 'w': 2, 'h': 1},
        {'name': 'Plonge', 'x': 2, 'y': 2, 'w': 4, 'h': 1},
        {'name': 'Bar', 'x': 6, 'y': 2, 'w': 4, 'h': 1}
    ]
}
with open('data/exports/plan_brasserie.json', 'w') as f:
    json.dump(plan_brasserie, f, indent=2)
print('✅ Plan brasserie généré')
"

# Plan 3: Restaurant gastronomique
echo "📝 Génération plan gastronomique..."
python -c "
import json
plan_gastro = {
    'zones': [
        {'name': 'Réception', 'x': 0, 'y': 0, 'w': 2, 'h': 1},
        {'name': 'Stockage Sec', 'x': 0, 'y': 1, 'w': 2, 'h': 1},
        {'name': 'Stockage Froid', 'x': 0, 'y': 2, 'w': 2, 'h': 1},
        {'name': 'Légumerie', 'x': 2, 'y': 0, 'w': 2, 'h': 2},
        {'name': 'Préparation Froide', 'x': 4, 'y': 0, 'w': 3, 'h': 1},
        {'name': 'Préparation Chaude', 'x': 4, 'y': 1, 'w': 3, 'h': 1},
        {'name': 'Cuisson Principale', 'x': 7, 'y': 0, 'w': 3, 'h': 2},
        {'name': 'Pâtisserie', 'x': 10, 'y': 0, 'w': 2, 'h': 1},
        {'name': 'Dressage', 'x': 10, 'y': 1, 'w': 2, 'h': 1},
        {'name': 'Plonge Batterie', 'x': 2, 'y': 2, 'w': 3, 'h': 1},
        {'name': 'Plonge Vaisselle', 'x': 5, 'y': 2, 'w': 3, 'h': 1},
        {'name': 'Expédition', 'x': 8, 'y': 2, 'w': 4, 'h': 1}
    ]
}
with open('data/exports/plan_gastronomique.json', 'w') as f:
    json.dump(plan_gastro, f, indent=2)
print('✅ Plan gastronomique généré')
"

echo ""
echo "🎨 Génération des visualisations..."

# Génère les images pour chaque plan
for plan_type in "compact" "brasserie" "gastronomique"; do
    python -c "
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

plan_type = '$plan_type'
with open(f'data/exports/plan_{plan_type}.json', 'r') as f:
    plan = json.load(f)

zones = plan.get('zones', [])
fig, ax = plt.subplots(figsize=(14, 10))
colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 
          'lightpink', 'lightgray', 'lightcyan', 'wheat', 'lavender',
          'mistyrose', 'honeydew', 'aliceblue']

max_x = max_y = 0

for i, zone in enumerate(zones):
    name = zone.get('name', f'Zone {i+1}')
    x = zone.get('x', 0)
    y = zone.get('y', 0)
    w = zone.get('w', 1)
    h = zone.get('h', 1)
    
    max_x = max(max_x, x + w)
    max_y = max(max_y, y + h)
    
    color = colors[i % len(colors)]
    
    rect = patches.Rectangle(
        (x, y), w, h,
        linewidth=2, 
        edgecolor='black', 
        facecolor=color,
        alpha=0.7
    )
    ax.add_patch(rect)
    
    ax.text(
        x + w/2, y + h/2, 
        name,
        ha='center', va='center',
        fontsize=8, weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9)
    )

ax.set_xlim(-0.5, max_x + 0.5)
ax.set_ylim(-0.5, max_y + 0.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_xlabel('Position X (mètres)', fontsize=12)
ax.set_ylabel('Position Y (mètres)', fontsize=12)
ax.set_title(f'Cuisine {plan_type.title()} - {len(zones)} zones', fontsize=16, weight='bold')

plt.tight_layout()
plt.savefig(f'data/exports/plan_{plan_type}.png', dpi=300, bbox_inches='tight')
plt.close()

print(f'✅ Plan {plan_type} visualisé')
"
done

echo ""
echo "✨ Démonstration terminée !"
echo "📁 Plans générés :"
echo "   - data/exports/plan_compact.json/.png"
echo "   - data/exports/plan_brasserie.json/.png" 
echo "   - data/exports/plan_gastronomique.json/.png"
