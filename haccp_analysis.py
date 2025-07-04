#!/usr/bin/env python3
# haccp_analysis.py - Analyse de conformité HACCP pour les plans de cuisine

import json
import os
import sys
from datetime import datetime

# Règles HACCP de base
HACCP_RULES = {
    "marche_avant": {
        "description": "Principe de marche en avant pour éviter les contaminations croisées",
        "zones_sales": ["réception", "stockage", "lavage", "plonge"],
        "zones_propres": ["préparation", "cuisson", "dressage", "service"],
        "critical": True
    },
    "separation_chaud_froid": {
        "description": "Séparation physique des zones chaudes et froides",
        "zones_chaudes": ["cuisson", "préparation chaude", "grillade", "friture"],
        "zones_froides": ["préparation froide", "stockage froid"],
        "min_distance": 1.5,  # mètres
        "critical": True
    },
    "ventilation": {
        "description": "Ventilation adéquate pour les zones de cuisson",
        "zones_requises": ["cuisson", "grillade", "friture", "préparation chaude"],
        "critical": False
    },
    "lavage_proximite": {
        "description": "Zone de lavage proche des zones de préparation",
        "zones_preparation": ["préparation", "préparation froide", "préparation chaude"],
        "max_distance": 3.0,  # mètres
        "critical": False
    },
    "stockage_acces": {
        "description": "Accès facile aux zones de stockage",
        "zones_stockage": ["stockage", "stockage sec", "stockage froid"],
        "zones_acces": ["réception", "préparation"],
        "max_distance": 4.0,
        "critical": False
    }
}

# Points critiques de contrôle (CCP)
CRITICAL_CONTROL_POINTS = {
    "reception": {
        "temperature": "Contrôle température des livraisons",
        "tracabilite": "Enregistrement des fournisseurs",
        "verification": "Vérification qualité produits"
    },
    "stockage_froid": {
        "temperature": "Maintien chaîne du froid (0-4°C)",
        "separation": "Séparation viandes/légumes",
        "rotation": "FIFO - Premier entré, premier sorti"
    },
    "preparation": {
        "hygiene": "Lavage des mains fréquent",
        "desinfection": "Désinfection des surfaces",
        "temperature": "Contrôle température produits"
    },
    "cuisson": {
        "temperature": "Température cœur 63°C minimum",
        "duree": "Temps de cuisson respecté",
        "refroidissement": "Refroidissement rapide si nécessaire"
    }
}

def calculate_distance(zone1, zone2):
    """Calcule la distance entre deux zones."""
    x1 = zone1['x'] + zone1['w'] / 2
    y1 = zone1['y'] + zone1['h'] / 2
    x2 = zone2['x'] + zone2['w'] / 2
    y2 = zone2['y'] + zone2['h'] / 2
    
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def find_zones_by_type(zones, zone_types):
    """Trouve les zones correspondant à certains types."""
    found_zones = []
    
    for zone in zones:
        zone_name = zone['name'].lower()
        for zone_type in zone_types:
            if zone_type in zone_name:
                found_zones.append(zone)
                break
    
    return found_zones

def check_marche_avant(zones):
    """Vérifie le principe de marche en avant."""
    issues = []
    recommendations = []
    
    zones_sales = find_zones_by_type(zones, HACCP_RULES["marche_avant"]["zones_sales"])
    zones_propres = find_zones_by_type(zones, HACCP_RULES["marche_avant"]["zones_propres"])
    
    if not zones_sales:
        issues.append("Aucune zone 'sale' identifiée (réception, stockage, lavage)")
    
    if not zones_propres:
        issues.append("Aucune zone 'propre' identifiée (préparation, cuisson, service)")
    
    # Vérifie que les zones sales sont avant les zones propres dans le flux
    for zone_sale in zones_sales:
        for zone_propre in zones_propres:
            if zone_sale['x'] > zone_propre['x']:
                issues.append(f"Zone '{zone_sale['name']}' (sale) après '{zone_propre['name']}' (propre)")
    
    if not issues:
        recommendations.append("Flux de marche en avant respecté")
    else:
        recommendations.append("Réorganiser le flux : Réception → Stockage → Préparation → Cuisson → Service")
    
    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "recommendations": recommendations,
        "critical": HACCP_RULES["marche_avant"]["critical"]
    }

def check_separation_chaud_froid(zones):
    """Vérifie la séparation des zones chaudes et froides."""
    issues = []
    recommendations = []
    
    zones_chaudes = find_zones_by_type(zones, HACCP_RULES["separation_chaud_froid"]["zones_chaudes"])
    zones_froides = find_zones_by_type(zones, HACCP_RULES["separation_chaud_froid"]["zones_froides"])
    
    min_distance = HACCP_RULES["separation_chaud_froid"]["min_distance"]
    
    for zone_chaude in zones_chaudes:
        for zone_froide in zones_froides:
            distance = calculate_distance(zone_chaude, zone_froide)
            if distance < min_distance:
                issues.append(f"Zones '{zone_chaude['name']}' et '{zone_froide['name']}' trop proches ({distance:.1f}m < {min_distance}m)")
    
    if not issues:
        recommendations.append("Séparation chaud/froid respectée")
    else:
        recommendations.append(f"Maintenir au moins {min_distance}m entre zones chaudes et froides")
    
    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "recommendations": recommendations,
        "critical": HACCP_RULES["separation_chaud_froid"]["critical"]
    }

def check_lavage_proximite(zones):
    """Vérifie la proximité des zones de lavage."""
    issues = []
    recommendations = []
    
    zones_preparation = find_zones_by_type(zones, HACCP_RULES["lavage_proximite"]["zones_preparation"])
    zones_lavage = find_zones_by_type(zones, ["lavage", "plonge"])
    
    if not zones_lavage:
        issues.append("Aucune zone de lavage identifiée")
        recommendations.append("Ajouter une zone de lavage/plonge")
        return {
            "passed": False,
            "issues": issues,
            "recommendations": recommendations,
            "critical": HACCP_RULES["lavage_proximite"]["critical"]
        }
    
    max_distance = HACCP_RULES["lavage_proximite"]["max_distance"]
    
    for zone_prep in zones_preparation:
        min_dist_to_lavage = min(calculate_distance(zone_prep, zone_lav) for zone_lav in zones_lavage)
        if min_dist_to_lavage > max_distance:
            issues.append(f"Zone '{zone_prep['name']}' trop loin du lavage ({min_dist_to_lavage:.1f}m > {max_distance}m)")
    
    if not issues:
        recommendations.append("Zones de lavage bien positionnées")
    else:
        recommendations.append(f"Rapprocher les zones de lavage des zones de préparation (max {max_distance}m)")
    
    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "recommendations": recommendations,
        "critical": HACCP_RULES["lavage_proximite"]["critical"]
    }

def check_stockage_acces(zones):
    """Vérifie l'accessibilité des zones de stockage."""
    issues = []
    recommendations = []
    
    zones_stockage = find_zones_by_type(zones, HACCP_RULES["stockage_acces"]["zones_stockage"])
    zones_acces = find_zones_by_type(zones, HACCP_RULES["stockage_acces"]["zones_acces"])
    
    if not zones_stockage:
        issues.append("Aucune zone de stockage identifiée")
    
    max_distance = HACCP_RULES["stockage_acces"]["max_distance"]
    
    for zone_stock in zones_stockage:
        min_dist_to_acces = min(calculate_distance(zone_stock, zone_acc) for zone_acc in zones_acces) if zones_acces else float('inf')
        if min_dist_to_acces > max_distance:
            issues.append(f"Zone '{zone_stock['name']}' difficile d'accès ({min_dist_to_acces:.1f}m > {max_distance}m)")
    
    if not issues:
        recommendations.append("Zones de stockage facilement accessibles")
    else:
        recommendations.append(f"Rapprocher les zones de stockage des accès (max {max_distance}m)")
    
    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "recommendations": recommendations,
        "critical": HACCP_RULES["stockage_acces"]["critical"]
    }

def generate_ccp_checklist(zones):
    """Génère une checklist des points critiques de contrôle."""
    checklist = {}
    
    for zone in zones:
        zone_name = zone['name'].lower()
        
        for ccp_type, controls in CRITICAL_CONTROL_POINTS.items():
            if ccp_type in zone_name:
                checklist[zone['name']] = {
                    "type": ccp_type,
                    "controls": controls,
                    "location": f"Position: ({zone['x']}, {zone['y']}) - {zone['w']}x{zone['h']}m"
                }
    
    return checklist

def analyze_haccp_compliance(plan_data):
    """Analyse complète de conformité HACCP."""
    zones = plan_data.get('zones', [])
    
    if not zones:
        return {
            "error": "Aucune zone trouvée dans le plan",
            "compliance_score": 0
        }
    
    # Exécute tous les tests
    tests = {
        "marche_avant": check_marche_avant(zones),
        "separation_chaud_froid": check_separation_chaud_froid(zones),
        "lavage_proximite": check_lavage_proximite(zones),
        "stockage_acces": check_stockage_acces(zones)
    }
    
    # Calcule le score de conformité
    total_tests = len(tests)
    passed_tests = sum(1 for test in tests.values() if test['passed'])
    critical_failed = sum(1 for test in tests.values() if not test['passed'] and test['critical'])
    
    compliance_score = (passed_tests / total_tests) * 100
    
    # Si des tests critiques échouent, le score est fortement réduit
    if critical_failed > 0:
        compliance_score = max(compliance_score - (critical_failed * 30), 0)
    
    # Génère la checklist CCP
    ccp_checklist = generate_ccp_checklist(zones)
    
    return {
        "compliance_score": compliance_score,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "critical_failed": critical_failed,
        "tests": tests,
        "ccp_checklist": ccp_checklist,
        "zones_analyzed": len(zones)
    }

def print_haccp_report(analysis):
    """Affiche un rapport HACCP formaté."""
    
    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        return
    
    print("🏥 ANALYSE HACCP - CONFORMITÉ SANITAIRE")
    print("=" * 50)
    print()
    
    # Score global
    score = analysis['compliance_score']
    if score >= 90:
        status = "🟢 EXCELLENT"
    elif score >= 75:
        status = "🟡 SATISFAISANT"
    elif score >= 50:
        status = "🟠 À AMÉLIORER"
    else:
        status = "🔴 NON CONFORME"
    
    print(f"📊 Score de conformité: {score:.1f}% {status}")
    print(f"✅ Tests réussis: {analysis['passed_tests']}/{analysis['total_tests']}")
    if analysis['critical_failed'] > 0:
        print(f"⚠️  Tests critiques échoués: {analysis['critical_failed']}")
    print()
    
    # Détail des tests
    print("📋 DÉTAIL DES VÉRIFICATIONS")
    print("-" * 30)
    
    for test_name, result in analysis['tests'].items():
        status_icon = "✅" if result['passed'] else "❌"
        critical_mark = " [CRITIQUE]" if result['critical'] else ""
        
        print(f"{status_icon} {test_name.replace('_', ' ').title()}{critical_mark}")
        
        if result['issues']:
            for issue in result['issues']:
                print(f"   ⚠️  {issue}")
        
        for rec in result['recommendations']:
            print(f"   💡 {rec}")
        print()
    
    # Points critiques de contrôle
    if analysis['ccp_checklist']:
        print("🎯 POINTS CRITIQUES DE CONTRÔLE (CCP)")
        print("-" * 30)
        
        for zone_name, ccp_info in analysis['ccp_checklist'].items():
            print(f"📍 {zone_name}")
            print(f"   📍 {ccp_info['location']}")
            
            for control_name, control_desc in ccp_info['controls'].items():
                print(f"   ✓ {control_desc}")
            print()
    
    # Recommandations générales
    print("📝 RECOMMANDATIONS GÉNÉRALES")
    print("-" * 30)
    
    if score < 75:
        print("• Formation du personnel aux bonnes pratiques HACCP")
        print("• Mise en place d'un plan de nettoyage et désinfection")
        print("• Documentation des procédures de contrôle")
    
    if analysis['critical_failed'] > 0:
        print("• URGENT: Corriger les non-conformités critiques avant ouverture")
        print("• Audit HACCP par un professionnel recommandé")
    
    print("• Affichage des consignes d'hygiène dans chaque zone")
    print("• Contrôle régulier des températures")
    print("• Traçabilité complète des produits")

def main():
    """Point d'entrée principal."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python haccp_analysis.py <plan.json>")
        print("  python haccp_analysis.py <plan.json> <rapport.json>")
        print("")
        print("Exemples:")
        print("  python haccp_analysis.py data/exports/plan_brasserie.json")
        print("  python haccp_analysis.py data/exports/plan_brasserie.json rapport_haccp.json")
        sys.exit(1)
    
    plan_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(plan_path):
        print(f"❌ Fichier non trouvé: {plan_path}")
        sys.exit(1)
    
    try:
        # Charge le plan
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan_data = json.load(f)
        
        print(f"📄 Analyse HACCP pour: {os.path.basename(plan_path)}")
        print()
        
        # Analyse HACCP
        analysis = analyze_haccp_compliance(plan_data)
        
        # Affiche le rapport
        print_haccp_report(analysis)
        
        # Sauvegarde si demandé
        if output_path:
            # Ajoute des métadonnées
            analysis['metadata'] = {
                "plan_file": plan_path,
                "analysis_date": datetime.now().isoformat(),
                "analyzer_version": "1.0"
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Rapport sauvegardé: {output_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
