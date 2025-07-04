#!/usr/bin/env python3
# web_interface.py - Interface web pour le générateur de plans de cuisine

import json
import os
import base64
import sys
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour serveur
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ajoute le répertoire racine au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_kitchen_plan(brief):
    """Génère un plan de cuisine basé sur le brief."""
    # Zones de base pour une cuisine professionnelle
    base_zones = [
        {"name": "Réception", "x": 0, "y": 0, "w": 2, "h": 1},
        {"name": "Stockage Sec", "x": 0, "y": 1, "w": 2, "h": 2},
        {"name": "Préparation Froide", "x": 2, "y": 0, "w": 3, "h": 2},
        {"name": "Préparation Chaude", "x": 5, "y": 0, "w": 3, "h": 2},
        {"name": "Cuisson", "x": 8, "y": 0, "w": 3, "h": 2},
        {"name": "Dressage", "x": 11, "y": 0, "w": 2, "h": 1},
        {"name": "Plonge", "x": 2, "y": 2, "w": 4, "h": 1},
        {"name": "Stockage Froid", "x": 6, "y": 2, "w": 3, "h": 1},
        {"name": "Expédition", "x": 11, "y": 1, "w": 2, "h": 1}
    ]
    
    # Adapte selon le brief
    if "petit" in brief.lower() or "compact" in brief.lower():
        zones = base_zones[:5]  # Version réduite
    elif "grand" in brief.lower() or "gastronomique" in brief.lower():
        zones = base_zones  # Version complète
    else:
        zones = base_zones[:7]  # Version standard
    
    return {"zones": zones}

def draw_plan_image(plan_data, output_path):
    """Dessine un plan et sauvegarde l'image."""
    zones = plan_data.get("zones", [])
    
    if not zones:
        raise ValueError("Aucune zone trouvée dans le plan")
    
    # Configuration du graphique
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Couleurs pour différencier les zones
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 
             'lightpink', 'lightgray', 'lightcyan', 'wheat', 'lavender']
    
    max_x = max_y = 0
    
    # Dessine chaque zone
    for i, zone in enumerate(zones):
        if not isinstance(zone, dict):
            continue
            
        name = zone.get("name", f"Zone {i+1}")
        x = zone.get("x", 0)
        y = zone.get("y", 0)
        w = zone.get("w", 1)
        h = zone.get("h", 1)
        
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)
        
        color = colors[i % len(colors)]
        
        # Dessine le rectangle
        rect = patches.Rectangle(
            (x, y), w, h,
            linewidth=2, 
            edgecolor='black', 
            facecolor=color,
            alpha=0.7
        )
        ax.add_patch(rect)
        
        # Ajoute le texte
        ax.text(
            x + w/2, y + h/2, 
            name,
            ha='center', va='center',
            fontsize=10, weight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9)
        )
    
    # Configuration des axes
    ax.set_xlim(-0.5, max_x + 0.5)
    ax.set_ylim(-0.5, max_y + 0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Position X (mètres)', fontsize=12)
    ax.set_ylabel('Position Y (mètres)', fontsize=12)
    ax.set_title('Plan de Cuisine Professionnelle', fontsize=16, weight='bold')
    
    # Sauvegarde
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'kitchen_planner_2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

@app.route('/')
def index():
    """Page d'accueil avec formulaire de génération."""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API pour générer un plan de cuisine."""
    try:
        data = request.get_json()
        brief = data.get('brief', '')
        cuisine_type = data.get('type', 'standard')
        surface = data.get('surface', 25)
        
        if not brief:
            return jsonify({'error': 'Brief requis'}), 400
        
        # Enrichit le brief avec les paramètres
        enhanced_brief = f"{brief}. Type: {cuisine_type}, Surface: {surface}m²"
        
        print(f"🔄 Génération via API: {enhanced_brief}")
        
        # Génère le plan
        plan_data = generate_kitchen_plan(enhanced_brief)
        
        # Crée la visualisation
        output_path = f"data/exports/web_plan_{cuisine_type}.json"
        image_path = f"data/exports/web_plan_{cuisine_type}.png"
        
        # Sauvegarde le plan
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, indent=2, ensure_ascii=False)
        
        # Génère l'image
        draw_plan_image(plan_data, image_path)
        
        # Encode l'image en base64 pour l'API
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'plan': plan_data,
            'image': f"data:image/png;base64,{image_data}",
            'zones_count': len(plan_data.get('zones', [])),
            'total_surface': sum(z['w'] * z['h'] for z in plan_data.get('zones', []))
        })
        
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate', methods=['POST'])
def api_validate():
    """API pour valider un plan."""
    try:
        plan_data = request.get_json()
        
        if not plan_data or 'zones' not in plan_data:
            return jsonify({'error': 'Données de plan invalides'}), 400
        
        # Validation simple
        zones = plan_data['zones']
        overlaps = []
        
        for i in range(len(zones)):
            for j in range(i + 1, len(zones)):
                if check_overlap(zones[i], zones[j]):
                    overlaps.append({
                        'zone1': zones[i]['name'],
                        'zone2': zones[j]['name']
                    })
        
        metrics = {
            'zones_count': len(zones),
            'total_surface': sum(z['w'] * z['h'] for z in zones),
            'average_surface': sum(z['w'] * z['h'] for z in zones) / len(zones) if zones else 0,
            'overlaps': overlaps,
            'is_valid': len(overlaps) == 0
        }
        
        return jsonify(metrics)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def check_overlap(zone1, zone2):
    """Vérifie si deux zones se chevauchent."""
    x1, y1, w1, h1 = zone1["x"], zone1["y"], zone1["w"], zone1["h"]
    x2, y2, w2, h2 = zone2["x"], zone2["y"], zone2["w"], zone2["h"]
    return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)

@app.route('/api/examples')
def api_examples():
    """API pour récupérer les plans d'exemple."""
    try:
        examples = []
        export_dir = "data/exports"
        
        for filename in os.listdir(export_dir):
            if filename.endswith('.json') and not filename.startswith('web_'):
                plan_path = os.path.join(export_dir, filename)
                
                with open(plan_path, 'r', encoding='utf-8') as f:
                    plan_data = json.load(f)
                
                examples.append({
                    'name': filename.replace('.json', '').replace('_', ' ').title(),
                    'filename': filename,
                    'zones_count': len(plan_data.get('zones', [])),
                    'surface': sum(z['w'] * z['h'] for z in plan_data.get('zones', []))
                })
        
        return jsonify(examples)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_plan(filename):
    """Télécharge un plan en JSON."""
    try:
        file_path = os.path.join("data/exports", filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return "Fichier non trouvé", 404
    except Exception as e:
        return f"Erreur: {e}", 500

if __name__ == '__main__':
    # Crée le dossier templates s'il n'existe pas
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🌐 Démarrage du serveur web...")
    print("📍 Interface disponible sur: http://localhost:5000")
    print("🔄 Mode debug activé pour le développement")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
