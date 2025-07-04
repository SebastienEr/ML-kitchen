#!/usr/bin/env python3
"""Simple plan generator using predefined zones.
Usage: python rag/generate_plan.py "Description" output.json
"""
import json
import sys
import os

# allow importing modules from repository root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from plan_utils import calculate_optimal_layout, EQUIPMENT_DATABASE

def build_default_selection():
    zones = {}
    categories = [
        'zones_preparation', 'zones_cuisson', 'zones_stockage',
        'zones_lavage', 'zones_service'
    ]
    for cat in categories:
        z = EQUIPMENT_DATABASE.get(cat, {})
        for name, cfg in z.items():
            zones[name] = {"size": cfg.get('default', 5)}
    return zones

def generate_plan(desc: str):
    selected = build_default_selection()
    room_width = 20
    room_height = 12
    corridor_width = 1.5
    return calculate_optimal_layout(selected, (room_width, room_height), corridor_width)

def main():
    if len(sys.argv) < 2:
        print("Usage: python rag/generate_plan.py \"Brief\" [output.json]")
        sys.exit(1)
    desc = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'generated_plan.json'
    plan = generate_plan(desc)
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    print(f"✅ Plan généré: {output} ({len(plan['zones'])} zones)")

if __name__ == '__main__':
    main()
