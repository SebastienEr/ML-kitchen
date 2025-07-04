#!/usr/bin/env python3
# interactive_planner.py - Interface interactive avancée pour la personnalisation des plans

import json
import os
import base64
import sys
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kitchen_interactive_planner_2025'

# Base de données complète des équipements de cuisine
EQUIPMENT_DATABASE = {
    "zones_preparation": {
        "Légumerie": {"min_size": 4, "max_size": 12, "default": 6, "color": "#90EE90", "equipment": ["Tables inox", "Éviers multiples", "Bacs gastro", "Éplucheuse"]},
        "Préparation Froide": {"min_size": 6, "max_size": 20, "default": 10, "color": "#ADD8E6", "equipment": ["Tables réfrigérées", "Éviers", "Planches de découpe", "Couteaux"]},
        "Préparation Chaude": {"min_size": 4, "max_size": 15, "default": 8, "color": "#FFB6C1", "equipment": ["Tables chauffantes", "Bain-marie", "Mixeurs", "Robot coupe"]},
        "Pâtisserie": {"min_size": 8, "max_size": 25, "default": 12, "color": "#DDA0DD", "equipment": ["Four à pâtisserie", "Batteur", "Laminoir", "Chambre de pousse"]},
        "Boucherie": {"min_size": 6, "max_size": 18, "default": 10, "color": "#F08080", "equipment": ["Billot", "Scie à os", "Hachoir", "Chambre froide dédiée"]}
    },
    "zones_cuisson": {
        "Zone Cuisson Principale": {"min_size": 10, "max_size": 30, "default": 15, "color": "#FFA07A", "equipment": ["Fours", "Plaques de cuisson", "Salamandre", "Hotte"]},
        "Grillade": {"min_size": 4, "max_size": 12, "default": 6, "color": "#CD853F", "equipment": ["Grill", "Plancha", "Extracteur spécialisé"]},
        "Friture": {"min_size": 2, "max_size": 8, "default": 4, "color": "#DAA520", "equipment": ["Friteuses", "Filtration d'huile", "Ventilation renforcée"]},
        "Wok": {"min_size": 3, "max_size": 8, "default": 5, "color": "#FF6347", "equipment": ["Feux wok", "Évacuation vapeur", "Tables adjacentes"]}
    },
    "zones_stockage": {
        "Chambre Froide Positive": {"min_size": 4, "max_size": 20, "default": 8, "color": "#87CEEB", "equipment": ["Groupe froid", "Étagères inox", "Thermomètre"]},
        "Chambre Froide Négative": {"min_size": 3, "max_size": 15, "default": 6, "color": "#4682B4", "equipment": ["Groupe froid -18°C", "Étagères", "Alarme température"]},
        "Stockage Sec": {"min_size": 4, "max_size": 25, "default": 8, "color": "#F5DEB3", "equipment": ["Étagères métalliques", "Contenants hermétiques", "Hygrométrie"]},
        "Cave à Vin": {"min_size": 4, "max_size": 20, "default": 8, "color": "#800080", "equipment": ["Climatisation vin", "Casiers", "Éclairage LED"]},
        "Réserve": {"min_size": 6, "max_size": 30, "default": 12, "color": "#D2B48C", "equipment": ["Rayonnages", "Chariots", "Zone déballage"]}
    },
    "zones_lavage": {
        "Plonge Batterie": {"min_size": 6, "max_size": 15, "default": 9, "color": "#B0C4DE", "equipment": ["Lave-vaisselle à capot", "Bacs de trempage", "Tables d'égouttage"]},
        "Plonge Légumes": {"min_size": 3, "max_size": 8, "default": 5, "color": "#AFEEEE", "equipment": ["Bacs spécialisés", "Douchette", "Tables de tri"]},
        "Laverie": {"min_size": 4, "max_size": 12, "default": 6, "color": "#E0FFFF", "equipment": ["Lave-linge", "Séchoir", "Rangement linge"]}
    },
    "zones_service": {
        "Dressage": {"min_size": 4, "max_size": 15, "default": 8, "color": "#F0E68C", "equipment": ["Passe", "Lampes chauffantes", "Tables de dressage"]},
        "Office": {"min_size": 3, "max_size": 10, "default": 6, "color": "#FFFACD", "equipment": ["Machine à café", "Réfrigérateur", "Micro-ondes"]},
        "Bar": {"min_size": 6, "max_size": 20, "default": 10, "color": "#CD853F", "equipment": ["Comptoir", "Tireuses", "Lave-verre", "Réfrigération"]},
        "Expédition": {"min_size": 3, "max_size": 10, "default": 5, "color": "#DDA0DD", "equipment": ["Chariots", "Étiqueteuse", "Balance"]}
    },
    "zones_hygiene": {
        "Vestiaires": {"min_size": 6, "max_size": 20, "default": 10, "color": "#F5F5F5", "equipment": ["Casiers", "Bancs", "Miroirs"]},
        "Sanitaires": {"min_size": 4, "max_size": 12, "default": 6, "color": "#FFFAF0", "equipment": ["WC", "Lavabos", "Distributeurs"]},
        "Lave-Mains": {"min_size": 1, "max_size": 3, "default": 2, "color": "#F0F8FF", "equipment": ["Lave-mains à commande non manuelle", "Savon", "Essuie-mains"]},
        "Sas d'Hygiène": {"min_size": 2, "max_size": 6, "default": 3, "color": "#F8F8FF", "equipment": ["Lave-mains", "Distributeur gel", "Pédiluve"]}
    },
    "zones_technique": {
        "Local Poubelles": {"min_size": 4, "max_size": 15, "default": 8, "color": "#696969", "equipment": ["Conteneurs", "Point d'eau", "Ventilation"]},
        "Local Technique": {"min_size": 3, "max_size": 12, "default": 6, "color": "#A9A9A9", "equipment": ["Tableau électrique", "Chaudière", "Ventilation"]},
        "Réception": {"min_size": 4, "max_size": 15, "default": 8, "color": "#D3D3D3", "equipment": ["Quai de déchargement", "Balance", "Tables de contrôle"]},
        "Bureau": {"min_size": 6, "max_size": 20, "default": 10, "color": "#E6E6FA", "equipment": ["Bureau", "Ordinateur", "Armoire", "Coffre-fort"]}
    },
    "equipements_speciaux": {
        "Fenêtre": {"min_size": 0, "max_size": 0, "default": 0, "color": "#87CEFA", "equipment": ["Châssis", "Ventilation naturelle"]},
        "Porte": {"min_size": 0, "max_size": 0, "default": 0, "color": "#DEB887", "equipment": ["Porte battante", "Ferme-porte"]},
        "Couloir": {"min_size": 2, "max_size": 10, "default": 3, "color": "#F5F5DC", "equipment": ["Circulation", "Éclairage"]}
    }
}

def calculate_optimal_layout(selected_zones, room_dimensions, corridor_width):
    """Calcule un agencement optimal des zones sélectionnées."""
    
    total_width, total_height = room_dimensions
    zones = []
    
    if not selected_zones:
        return {"zones": zones}
    
    # Tri des zones par taille décroissante pour optimiser l'agencement
    sorted_zones = sorted(selected_zones.items(), key=lambda x: x[1]['size'], reverse=True)
    
    # Algorithme de placement optimisé
    x, y = 0, 0
    row_height = 0
    max_width = total_width - corridor_width
    
    for zone_name, zone_config in sorted_zones:
        zone_info = get_zone_info(zone_name)
        if not zone_info:
            continue
            
        size = zone_config['size']
        # Calcul des dimensions optimales (ratio 3:2 par défaut)
        width = min(size * 0.6, max_width)
        height = size / width if width > 0 else 1
        
        # Vérifie si la zone tient sur la ligne actuelle
        if x + width > max_width:
            # Nouvelle ligne
            x = 0
            y += row_height + corridor_width
            row_height = 0
        
        # Vérifie si on dépasse la hauteur totale
        if y + height > total_height - corridor_width:
            # Réduit la hauteur si nécessaire
            height = max(1, total_height - y - corridor_width)
            width = size / height if height > 0 else size
        
        zones.append({
            "name": zone_name,
            "x": round(x, 1),
            "y": round(y, 1),
            "w": round(width, 1),
            "h": round(height, 1),
            "color": zone_info.get('color', '#E6E6FA'),
            "equipment": zone_info.get('equipment', [])
        })
        
        x += width + corridor_width / 2
        row_height = max(row_height, height)
    
    return {"zones": zones}

def get_zone_info(zone_name):
    """Récupère les informations d'une zone depuis la base de données."""
    for category, zones in EQUIPMENT_DATABASE.items():
        if zone_name in zones:
            return zones[zone_name]
    return None

@app.route('/')
def index():
    """Page principale avec l'interface interactive."""
    return render_template('interactive_planner.html')

@app.route('/api/equipment-database')
def api_equipment_database():
    """API pour récupérer la base de données d'équipements."""
    return jsonify(EQUIPMENT_DATABASE)

@app.route('/api/generate-interactive', methods=['POST'])
def api_generate_interactive():
    """API pour générer un plan à partir de la sélection interactive."""
    try:
        data = request.get_json()
        
        selected_zones = data.get('zones', {})
        room_width = float(data.get('room_width', 15))
        room_height = float(data.get('room_height', 10))
        corridor_width = float(data.get('corridor_width', 1.5))
        
        # Génère l'agencement optimal
        plan_data = calculate_optimal_layout(
            selected_zones, 
            (room_width, room_height), 
            corridor_width
        )
        
        # Calcule les statistiques
        total_surface = sum(z['w'] * z['h'] for z in plan_data['zones'])
        corridor_surface = (room_width * room_height) - total_surface
        
        # Génère la visualisation
        image_data = generate_plan_image(plan_data, (room_width, room_height))
        
        return jsonify({
            'success': True,
            'plan': plan_data,
            'image': image_data,
            'statistics': {
                'zones_count': len(plan_data['zones']),
                'total_surface': round(total_surface, 1),
                'corridor_surface': round(corridor_surface, 1),
                'room_surface': room_width * room_height,
                'efficiency': round((total_surface / (room_width * room_height)) * 100, 1)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_plan_image(plan_data, room_dimensions):
    """Génère une image du plan."""
    zones = plan_data.get("zones", [])
    room_width, room_height = room_dimensions
    
    # Configuration du graphique
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Dessine le contour de la pièce
    room_rect = patches.Rectangle(
        (0, 0), room_width, room_height,
        linewidth=3, 
        edgecolor='black', 
        facecolor='white',
        alpha=1
    )
    ax.add_patch(room_rect)
    
    # Dessine chaque zone
    for zone in zones:
        name = zone.get("name", "Zone")
        x = zone.get("x", 0)
        y = zone.get("y", 0)
        w = zone.get("w", 1)
        h = zone.get("h", 1)
        color = zone.get("color", "#E6E6FA")
        
        # Rectangle de la zone
        rect = patches.Rectangle(
            (x, y), w, h,
            linewidth=2, 
            edgecolor='black', 
            facecolor=color,
            alpha=0.8
        )
        ax.add_patch(rect)
        
        # Texte avec le nom et la surface
        surface = w * h
        text = f"{name}\n{surface:.1f}m²"
        
        ax.text(
            x + w/2, y + h/2, 
            text,
            ha='center', va='center',
            fontsize=9, weight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9),
            wrap=True
        )
    
    # Configuration des axes
    ax.set_xlim(-0.5, room_width + 0.5)
    ax.set_ylim(-0.5, room_height + 0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Largeur (mètres)', fontsize=12)
    ax.set_ylabel('Profondeur (mètres)', fontsize=12)
    ax.set_title('Plan de Cuisine Personnalisé', fontsize=16, weight='bold')
    
    # Convertit en base64
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{image_data}"

@app.route('/api/save-plan', methods=['POST'])
def api_save_plan():
    """API pour sauvegarder un plan personnalisé."""
    try:
        data = request.get_json()
        plan_data = data.get('plan')
        filename = data.get('filename', 'plan_personnalise.json')
        
        # Assure que le nom de fichier est sûr
        filename = filename.replace(' ', '_').replace('/', '_')
        if not filename.endswith('.json'):
            filename += '.json'
        
        output_path = f"data/exports/{filename}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'path': output_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Crée les dossiers nécessaires
    os.makedirs('templates', exist_ok=True)
    os.makedirs('data/exports', exist_ok=True)
    
    print("🎨 Interface Interactive Kitchen Planner")
    print("=" * 40)
    print("📍 URL: http://localhost:5001")
    print("🎯 Interface de personnalisation avancée")
    print("⚙️  Personnalisez chaque aspect de votre cuisine")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
