#!/usr/bin/env python3
# repair_plans.py - Script pour réparer automatiquement les plans avec chevauchements

import json
import os
import sys

def check_zone_overlap(zone1, zone2):
    """Vérifie si deux zones se chevauchent."""
    x1, y1, w1, h1 = zone1["x"], zone1["y"], zone1["w"], zone1["h"]
    x2, y2, w2, h2 = zone2["x"], zone2["y"], zone2["w"], zone2["h"]
    
    return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)

def find_overlaps(zones):
    """Trouve tous les chevauchements dans un plan."""
    overlaps = []
    for i in range(len(zones)):
        for j in range(i + 1, len(zones)):
            if check_zone_overlap(zones[i], zones[j]):
                overlaps.append((i, j))
    return overlaps

def repair_overlap(zones, i, j):
    """Répare un chevauchement en déplaçant la zone j."""
    zone1, zone2 = zones[i], zones[j]
    
    # Essaie de déplacer la zone2 à droite de zone1
    new_x = zone1["x"] + zone1["w"]
    if new_x + zone2["w"] <= 15:  # Limite de largeur raisonnable
        zone2["x"] = new_x
        return True
    
    # Sinon, essaie de la déplacer en dessous
    new_y = zone1["y"] + zone1["h"]
    if new_y + zone2["h"] <= 10:  # Limite de hauteur raisonnable
        zone2["y"] = new_y
        zone2["x"] = zone1["x"]  # Même colonne
        return True
    
    # Dernier recours : réduire la taille de zone2
    if zone2["w"] > 1:
        zone2["w"] -= 1
        return True
    
    return False

def repair_plan(plan_data):
    """Répare tous les chevauchements dans un plan."""
    zones = plan_data["zones"]
    overlaps = find_overlaps(zones)
    
    if not overlaps:
        return plan_data, "Aucun chevauchement détecté"
    
    repairs_made = 0
    max_attempts = 10
    
    for attempt in range(max_attempts):
        overlaps = find_overlaps(zones)
        if not overlaps:
            break
            
        for i, j in overlaps:
            if repair_overlap(zones, i, j):
                repairs_made += 1
                break  # Répare un chevauchement à la fois
    
    final_overlaps = find_overlaps(zones)
    if final_overlaps:
        return plan_data, f"⚠️  {repairs_made} réparations effectuées, {len(final_overlaps)} chevauchements restants"
    else:
        return plan_data, f"✅ {repairs_made} réparations effectuées, plan maintenant valide"

def main():
    """Point d'entrée principal."""
    if len(sys.argv) < 2:
        print("Usage: python repair_plans.py <fichier_plan.json>")
        print("Ou: python repair_plans.py --all  (pour réparer tous les plans)")
        sys.exit(1)
    
    if sys.argv[1] == "--all":
        # Répare tous les plans dans le dossier exports
        export_dir = "data/exports"
        if not os.path.exists(export_dir):
            print(f"❌ Dossier {export_dir} non trouvé")
            sys.exit(1)
        
        plan_files = [f for f in os.listdir(export_dir) if f.endswith('.json')]
        
        print(f"🔧 Réparation de {len(plan_files)} plans...")
        
        for plan_file in plan_files:
            plan_path = os.path.join(export_dir, plan_file)
            
            try:
                with open(plan_path, 'r', encoding='utf-8') as f:
                    plan_data = json.load(f)
                
                repaired_plan, message = repair_plan(plan_data)
                
                # Sauvegarde le plan réparé
                with open(plan_path, 'w', encoding='utf-8') as f:
                    json.dump(repaired_plan, f, indent=2, ensure_ascii=False)
                
                print(f"📄 {plan_file}: {message}")
                
            except Exception as e:
                print(f"❌ Erreur avec {plan_file}: {e}")
    
    else:
        # Répare un plan spécifique
        plan_path = sys.argv[1]
        
        if not os.path.exists(plan_path):
            print(f"❌ Fichier non trouvé: {plan_path}")
            sys.exit(1)
        
        try:
            with open(plan_path, 'r', encoding='utf-8') as f:
                plan_data = json.load(f)
            
            print(f"🔧 Réparation de {plan_path}...")
            repaired_plan, message = repair_plan(plan_data)
            
            # Sauvegarde le plan réparé
            with open(plan_path, 'w', encoding='utf-8') as f:
                json.dump(repaired_plan, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {message}")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
