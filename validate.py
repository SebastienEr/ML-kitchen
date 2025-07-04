#!/usr/bin/env python3
"""
Script de validation pour tester la qualité des plans générés
"""

import json
import os
from pathlib import Path

def validate_plan(plan_path):
    """Valide un plan JSON selon les critères de qualité."""
    try:
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        
        zones = plan.get('zones', [])
        if not zones:
            return False, "Aucune zone trouvée"
        
        issues = []
        
        # Vérification de la structure des zones
        for i, zone in enumerate(zones):
            if not isinstance(zone, dict):
                issues.append(f"Zone {i}: Structure invalide")
                continue
            
            required_fields = ['name', 'x', 'y', 'w', 'h']
            for field in required_fields:
                if field not in zone:
                    issues.append(f"Zone {i}: Champ '{field}' manquant")
            
            # Vérification des types
            if 'name' in zone and not isinstance(zone['name'], str):
                issues.append(f"Zone {i}: 'name' doit être une chaîne")
            
            for coord in ['x', 'y', 'w', 'h']:
                if coord in zone and not isinstance(zone[coord], (int, float)):
                    issues.append(f"Zone {i}: '{coord}' doit être numérique")
            
            # Vérification des valeurs logiques
            if 'w' in zone and zone['w'] <= 0:
                issues.append(f"Zone {i}: Largeur invalide")
            if 'h' in zone and zone['h'] <= 0:
                issues.append(f"Zone {i}: Hauteur invalide")
            if 'x' in zone and zone['x'] < 0:
                issues.append(f"Zone {i}: Position X négative")
            if 'y' in zone and zone['y'] < 0:
                issues.append(f"Zone {i}: Position Y négative")
        
        # Vérification des chevauchements
        for i, zone1 in enumerate(zones):
            for j, zone2 in enumerate(zones[i+1:], i+1):
                if zones_overlap(zone1, zone2):
                    issues.append(f"Zones {i} et {j}: Chevauchement détecté")
        
        # Vérification de la couverture
        total_area = sum(zone.get('w', 0) * zone.get('h', 0) for zone in zones)
        if total_area > 200:  # Surface max raisonnable
            issues.append("Surface totale excessive (>200m²)")
        
        if issues:
            return False, "; ".join(issues)
        
        return True, f"Plan valide avec {len(zones)} zones"
    
    except Exception as e:
        return False, f"Erreur de lecture: {str(e)}"

def zones_overlap(zone1, zone2):
    """Vérifie si deux zones se chevauchent."""
    try:
        x1, y1, w1, h1 = zone1['x'], zone1['y'], zone1['w'], zone1['h']
        x2, y2, w2, h2 = zone2['x'], zone2['y'], zone2['w'], zone2['h']
        
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)
    except KeyError:
        return False

def analyze_plan_quality(plan_path):
    """Analyse la qualité d'un plan selon différents critères."""
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)
    
    zones = plan.get('zones', [])
    
    # Métriques de qualité
    metrics = {
        'nb_zones': len(zones),
        'surface_totale': sum(z.get('w', 0) * z.get('h', 0) for z in zones),
        'zones_essentielles': 0,
        'flux_optimise': False,
        'surface_moyenne': 0
    }
    
    # Zones essentielles pour une cuisine professionnelle
    essential_zones = ['réception', 'stockage', 'préparation', 'cuisson', 'service', 'plonge']
    
    for zone in zones:
        zone_name = zone.get('name', '').lower()
        if any(essential in zone_name for essential in essential_zones):
            metrics['zones_essentielles'] += 1
    
    if metrics['nb_zones'] > 0:
        metrics['surface_moyenne'] = metrics['surface_totale'] / metrics['nb_zones']
    
    # Vérification du flux (zones ordonnées logiquement)
    zone_names = [z.get('name', '').lower() for z in zones]
    flux_keywords = ['réception', 'stockage', 'préparation', 'cuisson', 'service']
    last_pos = -1
    flux_ok = True
    
    for keyword in flux_keywords:
        for i, name in enumerate(zone_names):
            if keyword in name:
                if i < last_pos:
                    flux_ok = False
                last_pos = i
                break
    
    metrics['flux_optimise'] = flux_ok
    
    return metrics

def main():
    """Fonction principale de validation."""
    print("🔍 Validation des plans générés")
    print("=" * 50)
    
    exports_dir = Path("data/exports")
    json_files = list(exports_dir.glob("*.json"))
    
    if not json_files:
        print("❌ Aucun fichier JSON trouvé dans data/exports/")
        return
    
    total_files = len(json_files)
    valid_files = 0
    
    for json_file in json_files:
        print(f"\n📄 Validation de {json_file.name}")
        
        is_valid, message = validate_plan(json_file)
        
        if is_valid:
            print(f"✅ {message}")
            valid_files += 1
            
            # Analyse de qualité
            metrics = analyze_plan_quality(json_file)
            print(f"   📊 Métriques:")
            print(f"      - Zones: {metrics['nb_zones']}")
            print(f"      - Surface totale: {metrics['surface_totale']}m²")
            print(f"      - Surface moyenne: {metrics['surface_moyenne']:.1f}m²")
            print(f"      - Zones essentielles: {metrics['zones_essentielles']}")
            print(f"      - Flux optimisé: {'✅' if metrics['flux_optimise'] else '❌'}")
        else:
            print(f"❌ {message}")
    
    print("\n" + "=" * 50)
    print(f"📈 Résumé: {valid_files}/{total_files} plans valides")
    
    if valid_files == total_files:
        print("🎉 Tous les plans sont valides !")
    else:
        print("⚠️  Certains plans nécessitent des corrections")

if __name__ == "__main__":
    main()
