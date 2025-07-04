#!/usr/bin/env python3
# render_3d.py - Générateur de visualisations 3D pour les plans de cuisine

import json
import os
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.patches as patches

def create_3d_box(x, y, z, w, h, d):
    """Crée les faces d'une boîte 3D."""
    # Définit les 8 coins de la boîte
    corners = np.array([
        [x, y, z],
        [x + w, y, z],
        [x + w, y + h, z],
        [x, y + h, z],
        [x, y, z + d],
        [x + w, y, z + d],
        [x + w, y + h, z + d],
        [x, y + h, z + d]
    ])
    
    # Définit les 6 faces de la boîte
    faces = [
        [corners[0], corners[1], corners[2], corners[3]],  # face du bas
        [corners[4], corners[5], corners[6], corners[7]],  # face du haut
        [corners[0], corners[1], corners[5], corners[4]],  # face avant
        [corners[2], corners[3], corners[7], corners[6]],  # face arrière
        [corners[1], corners[2], corners[6], corners[5]],  # face droite
        [corners[4], corners[7], corners[3], corners[0]]   # face gauche
    ]
    
    return faces

def get_zone_height(zone_name):
    """Retourne la hauteur appropriée selon le type de zone."""
    heights = {
        'réception': 2.5,
        'stockage': 3.0,
        'préparation': 2.8,
        'cuisson': 2.8,
        'dressage': 2.5,
        'plonge': 2.6,
        'lavage': 2.6,
        'service': 2.4,
        'expédition': 2.5,
        'bar': 2.4,
        'froide': 2.8,
        'chaude': 2.8
    }
    
    zone_lower = zone_name.lower()
    
    for key, height in heights.items():
        if key in zone_lower:
            return height
    
    return 2.7  # Hauteur par défaut

def get_zone_color(zone_name):
    """Retourne une couleur selon le type de zone."""
    colors = {
        'réception': '#87CEEB',      # Bleu ciel
        'stockage': '#98FB98',       # Vert pâle
        'préparation': '#FFB6C1',    # Rose clair
        'cuisson': '#FFA07A',        # Saumon
        'dressage': '#F0E68C',       # Kaki
        'plonge': '#B0C4DE',         # Bleu acier clair
        'lavage': '#B0C4DE',         # Bleu acier clair
        'service': '#DDA0DD',        # Prune
        'expédition': '#D2B48C',     # Tan
        'bar': '#CD853F',            # Pérou
        'froide': '#AFEEEE',         # Turquoise pâle
        'chaude': '#FFE4E1'          # Rose brumeux
    }
    
    zone_lower = zone_name.lower()
    
    for key, color in colors.items():
        if key in zone_lower:
            return color
    
    return '#E6E6FA'  # Lavande par défaut

def render_plan_3d(plan_data, output_path):
    """Génère une visualisation 3D du plan de cuisine."""
    
    zones = plan_data.get('zones', [])
    
    if not zones:
        raise ValueError("Aucune zone trouvée dans le plan")
    
    # Configuration de la figure 3D
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Collections pour stocker les faces
    all_faces = []
    all_colors = []
    
    # Traite chaque zone
    for zone in zones:
        name = zone.get('name', 'Zone')
        x = zone.get('x', 0)
        y = zone.get('y', 0)
        w = zone.get('w', 1)
        h = zone.get('h', 1)
        
        # Hauteur basée sur le type de zone
        zone_height = get_zone_height(name)
        
        # Couleur basée sur le type de zone
        color = get_zone_color(name)
        
        # Crée les faces de la boîte 3D
        faces = create_3d_box(x, y, 0, w, h, zone_height)
        
        # Ajoute les faces à la collection
        for face in faces:
            all_faces.append(face)
            all_colors.append(color)
        
        # Ajoute le label de la zone au centre
        label_x = x + w / 2
        label_y = y + h / 2
        label_z = zone_height / 2
        
        ax.text(label_x, label_y, label_z, name,
                fontsize=10, weight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", 
                         facecolor='white', alpha=0.8))
    
    # Ajoute toutes les faces à la fois
    collection = Poly3DCollection(all_faces, alpha=0.8, linewidths=1, edgecolors='black')
    collection.set_facecolors(all_colors)
    ax.add_collection3d(collection)
    
    # Calcule les limites
    max_x = max(z['x'] + z['w'] for z in zones)
    max_y = max(z['y'] + z['h'] for z in zones)
    max_z = max(get_zone_height(z['name']) for z in zones)
    
    # Configuration des axes
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    ax.set_zlim(0, max_z + 0.5)
    
    ax.set_xlabel('Largeur (mètres)', fontsize=12)
    ax.set_ylabel('Profondeur (mètres)', fontsize=12)
    ax.set_zlabel('Hauteur (mètres)', fontsize=12)
    ax.set_title('Cuisine Professionnelle - Vue 3D', fontsize=16, weight='bold')
    
    # Configuration de la vue
    ax.view_init(elev=20, azim=45)
    
    # Grille et style
    ax.grid(True, alpha=0.3)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Sauvegarde
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

def generate_multiple_views(plan_data, base_output_path):
    """Génère plusieurs vues 3D du même plan."""
    
    views = [
        {'elev': 20, 'azim': 45, 'suffix': '_perspective'},
        {'elev': 90, 'azim': 0, 'suffix': '_top'},
        {'elev': 0, 'azim': 0, 'suffix': '_front'},
        {'elev': 0, 'azim': 90, 'suffix': '_side'}
    ]
    
    zones = plan_data.get('zones', [])
    generated_files = []
    
    for view in views:
        # Configuration de la figure
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        all_faces = []
        all_colors = []
        
        # Génère les boîtes 3D
        for zone in zones:
            name = zone.get('name', 'Zone')
            x = zone.get('x', 0)
            y = zone.get('y', 0)
            w = zone.get('w', 1)
            h = zone.get('h', 1)
            
            zone_height = get_zone_height(name)
            color = get_zone_color(name)
            
            faces = create_3d_box(x, y, 0, w, h, zone_height)
            
            for face in faces:
                all_faces.append(face)
                all_colors.append(color)
        
        # Ajoute les faces
        collection = Poly3DCollection(all_faces, alpha=0.8, linewidths=1, edgecolors='black')
        collection.set_facecolors(all_colors)
        ax.add_collection3d(collection)
        
        # Configuration
        max_x = max(z['x'] + z['w'] for z in zones)
        max_y = max(z['y'] + z['h'] for z in zones)
        max_z = max(get_zone_height(z['name']) for z in zones)
        
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, max_y)
        ax.set_zlim(0, max_z + 0.5)
        
        ax.set_xlabel('Largeur (m)')
        ax.set_ylabel('Profondeur (m)')
        ax.set_zlabel('Hauteur (m)')
        
        # Titre selon la vue
        titles = {
            '_perspective': 'Vue Perspective',
            '_top': 'Vue du Dessus',
            '_front': 'Vue de Face',
            '_side': 'Vue de Côté'
        }
        ax.set_title(f"Cuisine 3D - {titles[view['suffix']]}", fontsize=14, weight='bold')
        
        # Configuration de la vue
        ax.view_init(elev=view['elev'], azim=view['azim'])
        
        # Sauvegarde
        output_file = base_output_path.replace('.png', f"{view['suffix']}.png")
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        generated_files.append(output_file)
        print(f"✅ Vue générée: {os.path.basename(output_file)}")
    
    return generated_files

def main():
    """Point d'entrée principal."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python render_3d.py <plan.json> [output.png]")
        print("  python render_3d.py <plan.json> --multiple")
        print("")
        print("Exemples:")
        print("  python render_3d.py data/exports/plan_brasserie.json")
        print("  python render_3d.py data/exports/plan_brasserie.json plan_3d.png")
        print("  python render_3d.py data/exports/plan_brasserie.json --multiple")
        sys.exit(1)
    
    plan_path = sys.argv[1]
    
    if not os.path.exists(plan_path):
        print(f"❌ Fichier non trouvé: {plan_path}")
        sys.exit(1)
    
    try:
        # Charge le plan
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan_data = json.load(f)
        
        if len(sys.argv) > 2 and sys.argv[2] == '--multiple':
            # Génère plusieurs vues
            base_name = os.path.splitext(os.path.basename(plan_path))[0]
            base_output = f"data/exports/{base_name}_3d.png"
            
            print(f"🎬 Génération de vues multiples pour: {os.path.basename(plan_path)}")
            generated_files = generate_multiple_views(plan_data, base_output)
            
            print(f"🎉 {len(generated_files)} vues 3D générées:")
            for file in generated_files:
                print(f"   📁 {file}")
        
        else:
            # Génère une vue simple
            if len(sys.argv) > 2:
                output_path = sys.argv[2]
            else:
                base_name = os.path.splitext(os.path.basename(plan_path))[0]
                output_path = f"data/exports/{base_name}_3d.png"
            
            print(f"🎨 Génération 3D pour: {os.path.basename(plan_path)}")
            render_plan_3d(plan_data, output_path)
            print(f"✅ Rendu 3D généré: {output_path}")
            
            # Statistiques
            zones_count = len(plan_data.get('zones', []))
            total_volume = sum(
                z['w'] * z['h'] * get_zone_height(z['name']) 
                for z in plan_data.get('zones', [])
            )
            
            print(f"📊 Statistiques:")
            print(f"   • {zones_count} zones")
            print(f"   • Volume total: {total_volume:.1f}m³")
        
    except Exception as e:
        print(f"❌ Erreur lors du rendu 3D: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
