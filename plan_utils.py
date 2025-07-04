"""Utility functions for generating kitchen layouts."""

# Equipment database extracted from interactive_planner
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
    }
}


def get_zone_info(zone_name):
    for category, zones in EQUIPMENT_DATABASE.items():
        if zone_name in zones:
            return zones[zone_name]
    return None


def calculate_optimal_layout(selected_zones, room_dimensions, corridor_width):
    total_width, total_height = room_dimensions
    zones = []
    if not selected_zones:
        return {"zones": zones}
    sorted_zones = sorted(selected_zones.items(), key=lambda x: x[1]['size'], reverse=True)
    x, y = 0, 0
    row_height = 0
    max_width = total_width - corridor_width
    for zone_name, zone_config in sorted_zones:
        zone_info = get_zone_info(zone_name)
        if not zone_info:
            continue
        size = zone_config['size']
        width = min(size * 0.6, max_width)
        height = size / width if width > 0 else 1
        if x + width > max_width:
            x = 0
            y += row_height + corridor_width
            row_height = 0
        if y + height > total_height - corridor_width:
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
