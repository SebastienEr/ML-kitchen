#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍳 Kitchen Planner Pro - Interface Web Moderne
Interface interactive avancée pour la planification de cuisines professionnelles
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import math
from rag.generate_plan import search_similar_plans

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'data/exports'
STATIC_FOLDER = 'static'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Equipment database with detailed specifications
EQUIPMENT_DATABASE = {
    'four': {
        'name': '🔥 Four',
        'category': 'cuisson',
        'default_width': 120,
        'default_height': 80,
        'min_width': 80,
        'max_width': 200,
        'min_height': 60,
        'max_height': 120,
        'power': 15000,  # Watts
        'temperature_max': 300,
        'color': '#ff6b6b',
        'description': 'Four professionnel électrique ou gaz'
    },
    'plancha': {
        'name': '🍳 Plancha',
        'category': 'cuisson',
        'default_width': 100,
        'default_height': 60,
        'min_width': 60,
        'max_width': 150,
        'min_height': 40,
        'max_height': 80,
        'power': 8000,
        'temperature_max': 350,
        'color': '#ffd93d',
        'description': 'Plancha électrique professionnelle'
    },
    'friteuse': {
        'name': '🍟 Friteuse',
        'category': 'cuisson',
        'default_width': 80,
        'default_height': 60,
        'min_width': 40,
        'max_width': 120,
        'min_height': 40,
        'max_height': 80,
        'power': 12000,
        'temperature_max': 200,
        'color': '#ff9f43',
        'description': 'Friteuse professionnelle double bac'
    },
    'grill': {
        'name': '🥩 Grill',
        'category': 'cuisson',
        'default_width': 100,
        'default_height': 70,
        'min_width': 60,
        'max_width': 140,
        'min_height': 50,
        'max_height': 100,
        'power': 10000,
        'temperature_max': 400,
        'color': '#6c5ce7',
        'description': 'Grill contact professionnel'
    },
    'frigo': {
        'name': '🧊 Frigo',
        'category': 'refrigeration',
        'default_width': 60,
        'default_height': 120,
        'min_width': 50,
        'max_width': 100,
        'min_height': 100,
        'max_height': 200,
        'power': 500,
        'temperature_min': 2,
        'temperature_max': 8,
        'color': '#74b9ff',
        'description': 'Réfrigérateur professionnel'
    },
    'congelateur': {
        'name': '🧊 Congélateur',
        'category': 'refrigeration',
        'default_width': 60,
        'default_height': 100,
        'min_width': 50,
        'max_width': 100,
        'min_height': 80,
        'max_height': 180,
        'power': 800,
        'temperature_min': -18,
        'temperature_max': -10,
        'color': '#0984e3',
        'description': 'Congélateur professionnel'
    },
    'cellule': {
        'name': '🏠 Cellule',
        'category': 'refrigeration',
        'default_width': 80,
        'default_height': 80,
        'min_width': 60,
        'max_width': 120,
        'min_height': 60,
        'max_height': 120,
        'power': 1200,
        'temperature_min': -5,
        'temperature_max': 10,
        'color': '#00b894',
        'description': 'Cellule de refroidissement rapide'
    },
    'cave': {
        'name': '🍷 Cave',
        'category': 'refrigeration',
        'default_width': 100,
        'default_height': 60,
        'min_width': 60,
        'max_width': 150,
        'min_height': 40,
        'max_height': 100,
        'power': 300,
        'temperature_min': 8,
        'temperature_max': 18,
        'color': '#8e44ad',
        'description': 'Cave à vin climatisée'
    },
    'plonge': {
        'name': '🚿 Plonge',
        'category': 'lavage',
        'default_width': 120,
        'default_height': 60,
        'min_width': 80,
        'max_width': 200,
        'min_height': 40,
        'max_height': 80,
        'power': 0,
        'water_consumption': 50,  # L/h
        'color': '#00cec9',
        'description': 'Plonge 2 ou 3 bacs avec égouttoir'
    },
    'lave-vaisselle': {
        'name': '🍽️ Lave-vaisselle',
        'category': 'lavage',
        'default_width': 80,
        'default_height': 80,
        'min_width': 60,
        'max_width': 120,
        'min_height': 60,
        'max_height': 100,
        'power': 8000,
        'water_consumption': 100,
        'color': '#55a3ff',
        'description': 'Lave-vaisselle à capot professionnel'
    },
    'evier': {
        'name': '🚰 Évier',
        'category': 'lavage',
        'default_width': 60,
        'default_height': 40,
        'min_width': 40,
        'max_width': 100,
        'min_height': 30,
        'max_height': 60,
        'power': 0,
        'water_consumption': 10,
        'color': '#81ecec',
        'description': 'Évier simple avec robinet mitigeur'
    },
    'bac': {
        'name': '🗃️ Bac',
        'category': 'lavage',
        'default_width': 80,
        'default_height': 40,
        'min_width': 40,
        'max_width': 120,
        'min_height': 30,
        'max_height': 60,
        'power': 0,
        'water_consumption': 5,
        'color': '#a29bfe',
        'description': 'Bac de trempage inox'
    },
    'table': {
        'name': '📋 Table',
        'category': 'preparation',
        'default_width': 120,
        'default_height': 60,
        'min_width': 60,
        'max_width': 200,
        'min_height': 40,
        'max_height': 80,
        'power': 0,
        'color': '#fd79a8',
        'description': 'Table de travail inox avec desserte'
    },
    'billot': {
        'name': '🪓 Billot',
        'category': 'preparation',
        'default_width': 80,
        'default_height': 60,
        'min_width': 50,
        'max_width': 120,
        'min_height': 40,
        'max_height': 80,
        'power': 0,
        'color': '#fdcb6e',
        'description': 'Billot de découpe en bois dur'
    },
    'plan': {
        'name': '📏 Plan',
        'category': 'preparation',
        'default_width': 100,
        'default_height': 50,
        'min_width': 60,
        'max_width': 160,
        'min_height': 40,
        'max_height': 70,
        'power': 0,
        'color': '#fab1a0',
        'description': 'Plan de travail avec rangements'
    },
    'etagere': {
        'name': '📚 Étagère',
        'category': 'preparation',
        'default_width': 40,
        'default_height': 100,
        'min_width': 30,
        'max_width': 80,
        'min_height': 60,
        'max_height': 200,
        'power': 0,
        'color': '#e17055',
        'description': 'Étagère murale 4 niveaux'
    }
}

# HACCP compliance rules
HACCP_RULES = {
    'min_corridor_width': 120,  # cm
    'min_distance_cooking_cold': 100,  # cm
    'min_distance_raw_cooked': 80,  # cm
    'door_swing_clearance': 90,  # cm
    'emergency_exit_width': 80,  # cm
    'max_walking_distance': 500  # cm
}

class KitchenLayoutEngine:
    """Moteur de génération et validation de layouts de cuisine"""
    
    def __init__(self):
        self.equipment_db = EQUIPMENT_DATABASE
        self.haccp_rules = HACCP_RULES
    
    def validate_layout(self, layout_data):
        """Valide un layout selon les règles HACCP et de sécurité"""
        violations = []
        equipment = layout_data.get('equipment', [])
        
        # Check overlaps
        for i, eq1 in enumerate(equipment):
            for j, eq2 in enumerate(equipment[i+1:], i+1):
                if self._check_overlap(eq1, eq2):
                    violations.append({
                        'type': 'overlap',
                        'message': f"Chevauchement entre {eq1['name']} et {eq2['name']}",
                        'severity': 'error',
                        'elements': [i, j]
                    })
        
        # Check corridor widths
        corridors = self._detect_corridors(equipment)
        for corridor in corridors:
            if corridor['width'] < self.haccp_rules['min_corridor_width']:
                violations.append({
                    'type': 'corridor_width',
                    'message': f"Couloir trop étroit: {corridor['width']}cm (min: {self.haccp_rules['min_corridor_width']}cm)",
                    'severity': 'warning',
                    'location': corridor['location']
                })
        
        # Check cooking/cold separation
        cooking_equipment = [eq for eq in equipment if self.equipment_db.get(eq['type'], {}).get('category') == 'cuisson']
        cold_equipment = [eq for eq in equipment if self.equipment_db.get(eq['type'], {}).get('category') == 'refrigeration']
        
        for cooking in cooking_equipment:
            for cold in cold_equipment:
                distance = self._calculate_distance(cooking, cold)
                if distance < self.haccp_rules['min_distance_cooking_cold']:
                    violations.append({
                        'type': 'thermal_separation',
                        'message': f"Distance insuffisante entre {cooking['name']} et {cold['name']}: {distance:.0f}cm",
                        'severity': 'warning',
                        'elements': [cooking, cold]
                    })
        
        return violations
    
    def _check_overlap(self, eq1, eq2):
        """Vérifie si deux équipements se chevauchent"""
        return not (eq1['x'] + eq1['width'] <= eq2['x'] or
                   eq2['x'] + eq2['width'] <= eq1['x'] or
                   eq1['y'] + eq1['height'] <= eq2['y'] or
                   eq2['y'] + eq2['height'] <= eq1['y'])
    
    def _calculate_distance(self, eq1, eq2):
        """Calcule la distance entre deux équipements"""
        center1_x = eq1['x'] + eq1['width'] / 2
        center1_y = eq1['y'] + eq1['height'] / 2
        center2_x = eq2['x'] + eq2['width'] / 2
        center2_y = eq2['y'] + eq2['height'] / 2
        
        return math.sqrt((center1_x - center2_x)**2 + (center1_y - center2_y)**2)
    
    def _detect_corridors(self, equipment):
        """Détecte les couloirs dans le layout"""
        # Simplified corridor detection
        corridors = []
        # This would need more sophisticated implementation
        # For now, return a basic corridor
        corridors.append({
            'width': 150,
            'location': {'x': 100, 'y': 100, 'width': 400, 'height': 150}
        })
        return corridors
    
    def calculate_efficiency(self, layout_data):
        """Calcule l'efficacité du layout"""
        equipment = layout_data.get('equipment', [])
        if not equipment:
            return 100
        
        # Facteurs d'efficacité
        factors = {
            'space_utilization': self._calculate_space_utilization(equipment),
            'workflow_efficiency': self._calculate_workflow_efficiency(equipment),
            'haccp_compliance': self._calculate_haccp_compliance(equipment)
        }
        
        # Moyenne pondérée
        efficiency = (
            factors['space_utilization'] * 0.3 +
            factors['workflow_efficiency'] * 0.4 +
            factors['haccp_compliance'] * 0.3
        )
        
        return round(efficiency, 1)
    
    def _calculate_space_utilization(self, equipment):
        """Calcule l'utilisation de l'espace"""
        if not equipment:
            return 100
        
        total_equipment_area = sum(eq['width'] * eq['height'] for eq in equipment)
        total_kitchen_area = 800 * 600  # Taille par défaut
        
        utilization = (total_equipment_area / total_kitchen_area) * 100
        return min(100, max(50, utilization))
    
    def _calculate_workflow_efficiency(self, equipment):
        """Calcule l'efficacité du flux de travail"""
        # Analyse des distances entre zones
        prep_equipment = [eq for eq in equipment if self.equipment_db.get(eq['type'], {}).get('category') == 'preparation']
        cooking_equipment = [eq for eq in equipment if self.equipment_db.get(eq['type'], {}).get('category') == 'cuisson']
        
        if not prep_equipment or not cooking_equipment:
            return 80
        
        # Distance moyenne entre préparation et cuisson
        total_distance = 0
        count = 0
        for prep in prep_equipment:
            for cooking in cooking_equipment:
                total_distance += self._calculate_distance(prep, cooking)
                count += 1
        
        if count == 0:
            return 80
        
        avg_distance = total_distance / count
        # Plus la distance est courte, meilleure est l'efficacité
        efficiency = max(60, 100 - (avg_distance / 10))
        return round(efficiency, 1)
    
    def _calculate_haccp_compliance(self, equipment):
        """Calcule la conformité HACCP"""
        violations = self.validate_layout({'equipment': equipment})
        error_count = len([v for v in violations if v['severity'] == 'error'])
        warning_count = len([v for v in violations if v['severity'] == 'warning'])
        
        # Pénalités
        penalty = (error_count * 20) + (warning_count * 10)
        compliance = max(50, 100 - penalty)
        
        return round(compliance, 1)

# Initialize layout engine
layout_engine = KitchenLayoutEngine()

@app.route('/')
def index():
    """Page d'accueil - Configurateur de cuisine"""
    return render_template('kitchen_configurator.html')

@app.route('/planner')
def planner():
    """Interface principale du planificateur"""
    return render_template('modern_kitchen_planner.html')

@app.route('/api/equipment')
def get_equipment():
    """Retourne la base de données d'équipements"""
    return jsonify(EQUIPMENT_DATABASE)

@app.route('/api/validate', methods=['POST'])
def validate_layout():
    """Valide un layout selon les règles HACCP"""
    try:
        layout_data = request.json
        violations = layout_engine.validate_layout(layout_data)
        efficiency = layout_engine.calculate_efficiency(layout_data)
        
        return jsonify({
            'success': True,
            'violations': violations,
            'efficiency': efficiency,
            'stats': {
                'total_equipment': len(layout_data.get('equipment', [])),
                'total_chefs': len(layout_data.get('chefs', [])),
                'total_surface': sum(eq['width'] * eq['height'] for eq in layout_data.get('equipment', [])) / 10000  # m²
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_layout():
    """Optimise automatiquement un layout"""
    try:
        layout_data = request.json
        
        # Algorithme d'optimisation simple
        optimized_equipment = []
        equipment = layout_data.get('equipment', [])
        
        # Regrouper par catégorie
        categories = {}
        for eq in equipment:
            category = EQUIPMENT_DATABASE.get(eq['type'], {}).get('category', 'other')
            if category not in categories:
                categories[category] = []
            categories[category].append(eq)
        
        # Placer par zones
        y_offset = 100
        for category, items in categories.items():
            x_offset = 100
            for item in items:
                optimized_item = item.copy()
                optimized_item['x'] = x_offset
                optimized_item['y'] = y_offset
                optimized_equipment.append(optimized_item)
                x_offset += item['width'] + 50
            y_offset += 150
        
        efficiency = layout_engine.calculate_efficiency({'equipment': optimized_equipment})
        
        return jsonify({
            'success': True,
            'optimized_layout': {
                'equipment': optimized_equipment,
                'chefs': layout_data.get('chefs', [])
            },
            'efficiency': efficiency
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_layout():
    """Exporte le layout avec image et métadonnées"""
    try:
        layout_data = request.json
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate image
        image_path = generate_layout_image(layout_data, timestamp)
        
        # Save JSON metadata
        json_path = os.path.join(UPLOAD_FOLDER, f'layout_{timestamp}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'layout': layout_data,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'efficiency': layout_engine.calculate_efficiency(layout_data),
                    'violations': layout_engine.validate_layout(layout_data),
                    'stats': {
                        'total_equipment': len(layout_data.get('equipment', [])),
                        'total_chefs': len(layout_data.get('chefs', [])),
                        'total_surface': sum(eq['width'] * eq['height'] for eq in layout_data.get('equipment', [])) / 10000
                    }
                }
            }, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'files': {
                'image': f'layout_{timestamp}.png',
                'metadata': f'layout_{timestamp}.json'
            },
            'download_urls': {
                'image': f'/download/layout_{timestamp}.png',
                'metadata': f'/download/layout_{timestamp}.json'
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def generate_layout_image(layout_data, timestamp):
    """Génère une image du layout"""
    # Dimensions de l'image
    width, height = 1200, 800
    padding = 50
    
    # Créer l'image
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Dessiner le cadre de la cuisine
    draw.rectangle([padding, padding, width-padding, height-padding], outline='black', width=3)
    
    # Dessiner les équipements
    equipment = layout_data.get('equipment', [])
    for eq in equipment:
        x = eq['x'] + padding
        y = eq['y'] + padding
        w = eq['width']
        h = eq['height']
        
        # Couleur selon le type
        eq_info = EQUIPMENT_DATABASE.get(eq['type'], {})
        color = eq_info.get('color', '#cccccc')
        
        # Dessiner l'équipement
        draw.rectangle([x, y, x+w, y+h], fill=color, outline='black', width=2)
        
        # Ajouter le nom (si la zone est assez grande)
        if w > 60 and h > 30:
            # Utiliser une police par défaut
            try:
                # Essayer de charger une police système
                font = ImageFont.load_default()
            except:
                font = None
            
            text = eq.get('name', eq['type'])
            if font:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            else:
                text_width = len(text) * 6
                text_height = 10
            
            if text_width < w and text_height < h:
                text_x = x + (w - text_width) // 2
                text_y = y + (h - text_height) // 2
                draw.text((text_x, text_y), text, fill='black', font=font)
        
        # Ajouter les dimensions
        dim_text = f"{w}×{h}cm"
        if font:
            bbox = draw.textbbox((0, 0), dim_text, font=font)
            dim_width = bbox[2] - bbox[0]
        else:
            dim_width = len(dim_text) * 6
        
        dim_x = x + (w - dim_width) // 2
        dim_y = y + h + 5
        draw.text((dim_x, dim_y), dim_text, fill='gray', font=font)
    
    # Dessiner les cuisiniers
    chefs = layout_data.get('chefs', [])
    for chef in chefs:
        x = chef['x'] + padding
        y = chef['y'] + padding
        
        # Dessiner un cercle pour représenter le cuisinier
        draw.ellipse([x-15, y-15, x+15, y+15], fill='orange', outline='darkred', width=2)
        draw.text((x-10, y-6), '👨‍🍳', fill='white')
    
    # Ajouter le titre
    title = f"Plan de Cuisine - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    if font:
        draw.text((padding, 10), title, fill='black', font=font)
    else:
        draw.text((padding, 10), title, fill='black')
    
    # Sauvegarder l'image
    image_path = os.path.join(UPLOAD_FOLDER, f'layout_{timestamp}.png')
    img.save(image_path, 'PNG', quality=95)
    
    return image_path

@app.route('/download/<filename>')
def download_file(filename):
    """Télécharge un fichier exporté"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Fichier non trouvé", 404

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Retourne des suggestions d'amélioration"""
    try:
        layout_data = request.json
        violations = layout_engine.validate_layout(layout_data)
        
        suggestions = []
        
        # Suggestions basées sur les violations
        for violation in violations:
            if violation['type'] == 'overlap':
                suggestions.append({
                    'type': 'positioning',
                    'title': 'Résoudre les chevauchements',
                    'description': violation['message'],
                    'priority': 'high',
                    'action': 'move_equipment'
                })
            elif violation['type'] == 'corridor_width':
                suggestions.append({
                    'type': 'spacing',
                    'title': 'Élargir les couloirs',
                    'description': violation['message'],
                    'priority': 'medium',
                    'action': 'increase_spacing'
                })
            elif violation['type'] == 'thermal_separation':
                suggestions.append({
                    'type': 'safety',
                    'title': 'Séparer cuisson et froid',
                    'description': violation['message'],
                    'priority': 'medium',
                    'action': 'relocate_equipment'
                })
        
        # Suggestions générales
        equipment = layout_data.get('equipment', [])
        if len(equipment) > 10:
            suggestions.append({
                'type': 'optimization',
                'title': 'Optimiser la disposition',
                'description': 'Votre cuisine contient beaucoup d\'équipements. Considérez regrouper par zones fonctionnelles.',
                'priority': 'low',
                'action': 'optimize_layout'
            })
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-ml', methods=['POST'])
def generate_ml_plan():
    """Génère un plan de cuisine par IA à partir d'un brief utilisateur"""
    try:
        data = request.get_json()
        brief = data.get('brief', '')
        if not brief:
            return jsonify({'success': False, 'error': 'Brief requis'}), 400
        # Recherche les plans similaires
        similar_plans = search_similar_plans(brief, top_k=3)
        if not similar_plans:
            return jsonify({'success': False, 'error': 'Aucun plan similaire trouvé'}), 404
        # Pour l'instant, retourne le plan le plus proche (améliorable)
        plan = similar_plans[0]
        return jsonify({'success': True, 'plan': plan})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test')
def test():
    """Page de test simple"""
    return render_template('test_simple.html')

@app.route('/test-workflow')
def test_workflow():
    """Page de test du workflow complet"""
    return render_template('test_workflow.html')

if __name__ == '__main__':
    print("🍳 Kitchen Planner Pro - Interface Moderne")
    print("=" * 50)
    print(f"📍 URL: http://localhost:5003")
    print("🎯 Interface drag & drop avec cotations")
    print("⚙️  Validation HACCP en temps réel")
    print("👨‍🍳 Simulation avec cuisiniers")
    print("📏 Dimensions et mesures")
    print("🚪 Battements de portes")
    print("🛤️  Couloirs et circulation")
    
    app.run(host='0.0.0.0', port=5004, debug=True)
