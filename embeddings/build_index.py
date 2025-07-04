# embeddings/build_index.py
from sentence_transformers import SentenceTransformer
import json
import os
import numpy as np
import faiss

def build_index():
    """Construit un index FAISS à partir des plans JSON structurés."""
    print("🔍 Chargement du modèle d'embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    structured_dir = "data/structured"
    if not os.path.exists(structured_dir):
        print(f"❌ Dossier {structured_dir} introuvable")
        return
    
    # Collecte des documents et chemins
    documents = []
    file_paths = []
    
    json_files = [f for f in os.listdir(structured_dir) if f.endswith(".json")]
    
    if not json_files:
        print("❌ Aucun fichier JSON trouvé dans data/structured/")
        return
    
    for json_file in json_files:
        file_path = os.path.join(structured_dir, json_file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Crée une description textuelle du plan pour l'embedding
            description = f"Plan avec {len(data.get('equipements', []))} équipements et {len(data.get('zones', []))} zones. "
            
            # Ajoute les équipements
            for eq in data.get("equipements", []):
                description += f"Équipement: {eq.get('nom', 'inconnu')}. "
            
            # Ajoute les zones
            for zone in data.get("zones", []):
                description += f"Zone: {zone.get('nom', 'inconnue')}. "
            
            documents.append(description)
            file_paths.append(json_file)
            
        except Exception as e:
            print(f"❌ Erreur lors de la lecture de {json_file}: {e}")
            continue
    
    if not documents:
        print("❌ Aucun document valide trouvé")
        return
    
    print(f"🔍 Génération des embeddings pour {len(documents)} documents...")
    embeddings = model.encode(documents, show_progress_bar=True)
    
    # Construction de l'index FAISS
    print("🔍 Construction de l'index FAISS...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Sauvegarde
    os.makedirs("data/embeddings", exist_ok=True)
    
    faiss.write_index(index, "data/embeddings/plan_index.faiss")
    
    with open("data/embeddings/paths.json", "w", encoding="utf-8") as f:
        json.dump(file_paths, f, indent=2)
    
    print(f"✅ Index FAISS créé avec {len(documents)} documents")
    print(f"   - Index: data/embeddings/plan_index.faiss")
    print(f"   - Mapping: data/embeddings/paths.json")

if __name__ == "__main__":
    build_index()
