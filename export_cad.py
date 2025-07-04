#!/usr/bin/env python3
# export_cad.py - Export des plans en formats CAD (DXF)

import json
import os
import sys

def generate_dxf_content(plan_data):
    """Génère le contenu d'un fichier DXF à partir d'un plan."""
    
    zones = plan_data.get('zones', [])
    
    # En-tête DXF minimal
    dxf_content = [
        "999",
        "Kitchen ML Planner - Plan généré automatiquement",
        "0",
        "SECTION",
        "2",
        "HEADER",
        "0",
        "ENDSEC",
        "0",
        "SECTION",
        "2",
        "TABLES",
        "0",
        "TABLE",
        "2",
        "LAYER",
        "70",
        "1",
        "0",
        "LAYER",
        "2",
        "ZONES",
        "70",
        "0",
        "62",
        "7",
        "6",
        "CONTINUOUS",
        "0",
        "ENDTAB",
        "0",
        "ENDSEC",
        "0",
        "SECTION",
        "2",
        "ENTITIES"
    ]
    
    # Facteur d'échelle (1 unité = 1 mètre)
    scale = 1000  # mm
    
    # Génère les rectangles pour chaque zone
    for i, zone in enumerate(zones):
        x, y, w, h = zone['x'] * scale, zone['y'] * scale, zone['w'] * scale, zone['h'] * scale
        
        # Rectangle (4 lignes)
        # Ligne du bas
        dxf_content.extend([
            "0", "LINE",
            "8", "ZONES",  # Layer
            "10", str(x),  # X1
            "20", str(y),  # Y1
            "30", "0.0",   # Z1
            "11", str(x + w),  # X2
            "21", str(y),      # Y2
            "31", "0.0"        # Z2
        ])
        
        # Ligne de droite
        dxf_content.extend([
            "0", "LINE",
            "8", "ZONES",
            "10", str(x + w),
            "20", str(y),
            "30", "0.0",
            "11", str(x + w),
            "21", str(y + h),
            "31", "0.0"
        ])
        
        # Ligne du haut
        dxf_content.extend([
            "0", "LINE",
            "8", "ZONES",
            "10", str(x + w),
            "20", str(y + h),
            "30", "0.0",
            "11", str(x),
            "21", str(y + h),
            "31", "0.0"
        ])
        
        # Ligne de gauche
        dxf_content.extend([
            "0", "LINE",
            "8", "ZONES",
            "10", str(x),
            "20", str(y + h),
            "30", "0.0",
            "11", str(x),
            "21", str(y),
            "31", "0.0"
        ])
        
        # Texte avec le nom de la zone
        text_x = x + (w / 2)
        text_y = y + (h / 2)
        
        dxf_content.extend([
            "0", "TEXT",
            "8", "ZONES",
            "10", str(text_x),  # Position X
            "20", str(text_y),  # Position Y
            "30", "0.0",        # Position Z
            "40", "200.0",      # Hauteur du texte (200mm)
            "1", zone['name'],  # Contenu du texte
            "50", "0.0",        # Angle de rotation
            "7", "STANDARD",    # Style de texte
            "71", "0",          # Flags
            "72", "1",          # Alignement horizontal (centré)
            "73", "2",          # Alignement vertical (centré)
            "11", str(text_x),  # Point d'alignement X
            "21", str(text_y),  # Point d'alignement Y
            "31", "0.0"         # Point d'alignement Z
        ])
    
    # Fin du fichier DXF
    dxf_content.extend([
        "0",
        "ENDSEC",
        "0",
        "EOF"
    ])
    
    return "\n".join(dxf_content)

def export_to_dxf(plan_path, output_path=None):
    """Exporte un plan JSON vers un fichier DXF."""
    
    try:
        # Charge le plan
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan_data = json.load(f)
        
        # Génère le nom de sortie si non spécifié
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(plan_path))[0]
            output_path = f"data/exports/{base_name}.dxf"
        
        # Génère le contenu DXF
        dxf_content = generate_dxf_content(plan_data)
        
        # Sauvegarde
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dxf_content)
        
        print(f"✅ Export DXF réussi: {output_path}")
        
        # Statistiques
        zones_count = len(plan_data.get('zones', []))
        total_surface = sum(z['w'] * z['h'] for z in plan_data.get('zones', []))
        
        print(f"   📊 {zones_count} zones exportées")
        print(f"   📏 Surface totale: {total_surface}m²")
        print(f"   🔧 Compatible AutoCAD, FreeCAD, QCAD")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export DXF: {e}")
        return None

def export_all_to_dxf():
    """Exporte tous les plans JSON en DXF."""
    
    export_dir = "data/exports"
    if not os.path.exists(export_dir):
        print(f"❌ Dossier {export_dir} non trouvé")
        return
    
    json_files = [f for f in os.listdir(export_dir) if f.endswith('.json')]
    
    if not json_files:
        print("❌ Aucun plan JSON trouvé")
        return
    
    print(f"🔄 Export de {len(json_files)} plans en DXF...")
    
    exported_count = 0
    for json_file in json_files:
        json_path = os.path.join(export_dir, json_file)
        
        if export_to_dxf(json_path):
            exported_count += 1
    
    print(f"🎉 {exported_count}/{len(json_files)} plans exportés avec succès")

def main():
    """Point d'entrée principal."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python export_cad.py <fichier_plan.json>")
        print("  python export_cad.py --all")
        print("")
        print("Exemples:")
        print("  python export_cad.py data/exports/plan_brasserie.json")
        print("  python export_cad.py --all")
        sys.exit(1)
    
    if sys.argv[1] == "--all":
        export_all_to_dxf()
    else:
        plan_path = sys.argv[1]
        
        if not os.path.exists(plan_path):
            print(f"❌ Fichier non trouvé: {plan_path}")
            sys.exit(1)
        
        export_to_dxf(plan_path)

if __name__ == "__main__":
    main()
