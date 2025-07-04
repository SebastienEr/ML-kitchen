# ingest/parse_plans.py
import fitz  # PyMuPDF
import json
import os
import re

def parse_plan(pdf_path):
    """Parse un PDF de plan de cuisine et extrait les équipements et zones."""
    doc = fitz.open(pdf_path)
    data = {"equipements": [], "zones": [], "surface_totale": 100}
    
    for page in doc:
        text = page.get_text("text")
        lines = text.splitlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Détection d'équipements (patterns simples)
            if any(word in line.lower() for word in ["four", "frigo", "plan", "évier", "hotte"]):
                # Extraction basique d'un équipement
                parts = line.split()
                if len(parts) >= 2:
                    data["equipements"].append({
                        "nom": " ".join(parts[:2]),
                        "description": line,
                        "type": "equipement"
                    })
            
            # Détection de zones (patterns simples)
            if any(word in line.lower() for word in ["zone", "espace", "aire", "cuisine", "préparation"]):
                data["zones"].append({
                    "nom": line,
                    "type": "zone_preparation"
                })
    
    doc.close()
    return data

def main():
    """Parse tous les PDFs dans data/raw_plans/."""
    os.makedirs("data/structured", exist_ok=True)
    
    raw_plans_dir = "data/raw_plans"
    if not os.path.exists(raw_plans_dir):
        print(f"❌ Dossier {raw_plans_dir} introuvable")
        return
    
    pdf_files = [f for f in os.listdir(raw_plans_dir) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("❌ Aucun fichier PDF trouvé dans data/raw_plans/")
        return
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(raw_plans_dir, pdf_file)
        print(f"📄 Parsing {pdf_file}...")
        
        try:
            parsed_data = parse_plan(pdf_path)
            json_filename = pdf_file.replace(".pdf", ".json")
            json_path = os.path.join("data/structured", json_filename)
            
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {json_filename} créé avec {len(parsed_data['equipements'])} équipements et {len(parsed_data['zones'])} zones")
        
        except Exception as e:
            print(f"❌ Erreur lors du parsing de {pdf_file}: {e}")
    
    print("✅ Parsing terminé.")

if __name__ == "__main__":
    main()
