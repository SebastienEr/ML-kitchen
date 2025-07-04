#!/usr/bin/env python3
# cost_estimation.py - Estimation des coûts pour les plans de cuisine

import json
import os
import sys

# Base de données des coûts par type d'équipement (en euros par m²)
EQUIPMENT_COSTS = {
    "Réception": {
        "base": 800,  # €/m²
        "equipment": ["Table de réception", "Balance", "Étagères"],
        "description": "Zone de réception des marchandises"
    },
    "Stockage": {
        "base": 600,
        "equipment": ["Étagères métalliques", "Contenants hermétiques"],
        "description": "Stockage sec des denrées"
    },
    "Stockage Sec": {
        "base": 600,
        "equipment": ["Étagères métalliques", "Contenants hermétiques"],
        "description": "Stockage sec des denrées"
    },
    "Stockage Froid": {
        "base": 2500,
        "equipment": ["Chambre froide", "Système de réfrigération"],
        "description": "Stockage réfrigéré"
    },
    "Préparation": {
        "base": 1200,
        "equipment": ["Tables inox", "Éviers", "Couteaux", "Planches"],
        "description": "Préparation générale"
    },
    "Préparation Froide": {
        "base": 1500,
        "equipment": ["Tables réfrigérées", "Éviers", "Ustensiles"],
        "description": "Préparation des produits frais"
    },
    "Préparation Chaude": {
        "base": 1800,
        "equipment": ["Tables chauffantes", "Bain-marie", "Ustensiles"],
        "description": "Préparation des plats chauds"
    },
    "Cuisson": {
        "base": 3500,
        "equipment": ["Fours", "Plaques de cuisson", "Friteuses", "Grills"],
        "description": "Zone de cuisson principale"
    },
    "Dressage": {
        "base": 1000,
        "equipment": ["Tables de dressage", "Passe-plats", "Lampes chauffantes"],
        "description": "Finition et présentation des plats"
    },
    "Service": {
        "base": 900,
        "equipment": ["Passe-plats", "Réchauds", "Distributeurs"],
        "description": "Zone de service"
    },
    "Plonge": {
        "base": 2000,
        "equipment": ["Lave-vaisselle industriel", "Éviers", "Tables d'égouttage"],
        "description": "Lavage de la vaisselle"
    },
    "Lavage": {
        "base": 2000,
        "equipment": ["Lave-vaisselle industriel", "Éviers", "Tables d'égouttage"],
        "description": "Lavage de la vaisselle"
    },
    "Expédition": {
        "base": 700,
        "equipment": ["Tables d'expédition", "Chariots", "Étiqueteuse"],
        "description": "Expédition des commandes"
    }
}

# Coûts supplémentaires
ADDITIONAL_COSTS = {
    "infrastructure": 0.15,    # 15% pour électricité, plomberie, ventilation
    "installation": 0.10,      # 10% pour l'installation
    "certification": 0.05,     # 5% pour certifications HACCP
    "contingency": 0.10        # 10% d'imprévu
}

def calculate_zone_cost(zone):
    """Calcule le coût d'une zone."""
    zone_name = zone['name']
    surface = zone['w'] * zone['h']  # m²
    
    # Recherche le coût de base (avec variations de noms)
    base_cost = 1000  # Coût par défaut
    equipment = ["Équipement standard"]
    description = "Zone standard"
    
    for key, data in EQUIPMENT_COSTS.items():
        if key.lower() in zone_name.lower() or zone_name.lower() in key.lower():
            base_cost = data['base']
            equipment = data['equipment']
            description = data['description']
            break
    
    total_cost = base_cost * surface
    
    return {
        'zone': zone_name,
        'surface': surface,
        'cost_per_m2': base_cost,
        'total_cost': total_cost,
        'equipment': equipment,
        'description': description
    }

def calculate_total_estimation(plan_data):
    """Calcule l'estimation complète du plan."""
    zones = plan_data.get('zones', [])
    
    if not zones:
        return None
    
    # Calcul par zone
    zone_costs = []
    total_equipment_cost = 0
    total_surface = 0
    
    for zone in zones:
        zone_cost = calculate_zone_cost(zone)
        zone_costs.append(zone_cost)
        total_equipment_cost += zone_cost['total_cost']
        total_surface += zone_cost['surface']
    
    # Coûts supplémentaires
    infrastructure_cost = total_equipment_cost * ADDITIONAL_COSTS['infrastructure']
    installation_cost = total_equipment_cost * ADDITIONAL_COSTS['installation']
    certification_cost = total_equipment_cost * ADDITIONAL_COSTS['certification']
    contingency_cost = total_equipment_cost * ADDITIONAL_COSTS['contingency']
    
    subtotal = total_equipment_cost + infrastructure_cost + installation_cost + certification_cost
    total_cost = subtotal + contingency_cost
    
    return {
        'zones': zone_costs,
        'summary': {
            'total_surface': total_surface,
            'equipment_cost': total_equipment_cost,
            'infrastructure_cost': infrastructure_cost,
            'installation_cost': installation_cost,
            'certification_cost': certification_cost,
            'contingency_cost': contingency_cost,
            'subtotal': subtotal,
            'total_cost': total_cost,
            'cost_per_m2': total_cost / total_surface if total_surface > 0 else 0
        }
    }

def format_currency(amount):
    """Formate un montant en euros."""
    return f"{amount:,.0f} €".replace(',', ' ')

def print_estimation(estimation):
    """Affiche l'estimation de manière formatée."""
    
    print("💰 ESTIMATION DES COÛTS")
    print("=" * 50)
    print()
    
    # Détail par zone
    print("📋 DÉTAIL PAR ZONE")
    print("-" * 30)
    
    for zone in estimation['zones']:
        print(f"🏷️  {zone['zone']}")
        print(f"   📏 Surface: {zone['surface']}m²")
        print(f"   💶 Coût: {format_currency(zone['cost_per_m2'])}/m² = {format_currency(zone['total_cost'])}")
        print(f"   🔧 Équipements: {', '.join(zone['equipment'])}")
        print()
    
    # Résumé financier
    summary = estimation['summary']
    print("📊 RÉSUMÉ FINANCIER")
    print("-" * 30)
    print(f"📐 Surface totale: {summary['total_surface']}m²")
    print()
    print(f"🔧 Équipements: {format_currency(summary['equipment_cost'])}")
    print(f"⚡ Infrastructure: {format_currency(summary['infrastructure_cost'])}")
    print(f"🔨 Installation: {format_currency(summary['installation_cost'])}")
    print(f"✅ Certification: {format_currency(summary['certification_cost'])}")
    print(f"📊 Sous-total: {format_currency(summary['subtotal'])}")
    print(f"🛡️  Imprévu (10%): {format_currency(summary['contingency_cost'])}")
    print("-" * 30)
    print(f"💰 TOTAL: {format_currency(summary['total_cost'])}")
    print(f"📊 Coût moyen: {format_currency(summary['cost_per_m2'])}/m²")
    print()
    
    # Conseils
    print("💡 CONSEILS D'OPTIMISATION")
    print("-" * 30)
    if summary['cost_per_m2'] > 2500:
        print("⚠️  Coût élevé - Considérez:")
        print("   • Révision des équipements haut de gamme")
        print("   • Optimisation de la surface")
        print("   • Achat groupé d'équipements")
    elif summary['cost_per_m2'] < 1500:
        print("✅ Coût raisonnable - Opportunités:")
        print("   • Investissement dans la qualité")
        print("   • Équipements éco-énergétiques")
        print("   • Formation du personnel")
    else:
        print("👍 Coût dans la moyenne du secteur")
        print("   • Budget équilibré")
        print("   • Bon rapport qualité/prix")

def estimate_plan_cost(plan_path, output_path=None):
    """Estime le coût d'un plan et optionnellement sauvegarde le résultat."""
    
    try:
        # Charge le plan
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan_data = json.load(f)
        
        # Calcule l'estimation
        estimation = calculate_total_estimation(plan_data)
        
        if not estimation:
            print("❌ Impossible de calculer l'estimation")
            return None
        
        # Affiche l'estimation
        print(f"📄 Plan: {os.path.basename(plan_path)}")
        print()
        print_estimation(estimation)
        
        # Sauvegarde si demandé
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(estimation, f, indent=2, ensure_ascii=False)
            print(f"💾 Estimation sauvegardée: {output_path}")
        
        return estimation
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul: {e}")
        return None

def main():
    """Point d'entrée principal."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python cost_estimation.py <fichier_plan.json>")
        print("  python cost_estimation.py <fichier_plan.json> <sortie.json>")
        print("")
        print("Exemples:")
        print("  python cost_estimation.py data/exports/plan_brasserie.json")
        print("  python cost_estimation.py data/exports/plan_brasserie.json estimation.json")
        sys.exit(1)
    
    plan_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(plan_path):
        print(f"❌ Fichier non trouvé: {plan_path}")
        sys.exit(1)
    
    estimate_plan_cost(plan_path, output_path)

if __name__ == "__main__":
    main()
