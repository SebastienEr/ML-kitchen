#!/usr/bin/env python3
# start_web.py - Lanceur pour l'interface web complète

import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées."""
    try:
        import flask
        import matplotlib
        import sentence_transformers
        import faiss
        import numpy as np
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Installez avec: pip install -r requirements.txt")
        return False

def setup_data():
    """Vérifie et prépare les données nécessaires."""
    
    # Crée les dossiers nécessaires
    os.makedirs("data/exports", exist_ok=True)
    os.makedirs("data/embeddings", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    # Vérifie l'index FAISS
    if not os.path.exists("data/embeddings/plan_index.faiss"):
        print("🔄 Construction de l'index FAISS...")
        try:
            subprocess.run([sys.executable, "embeddings/build_index.py"], check=True)
            print("✅ Index FAISS créé")
        except subprocess.CalledProcessError:
            print("⚠️  Impossible de créer l'index, fonctionnera en mode dégradé")
    
    # Vérifie les plans d'exemple
    if not os.path.exists("data/exports/plan_brasserie.json"):
        print("🔄 Génération des plans d'exemple...")
        try:
            subprocess.run(["bash", "demo.sh"], check=True)
            print("✅ Plans d'exemple créés")
        except subprocess.CalledProcessError:
            print("⚠️  Impossible de créer les plans d'exemple")

def open_browser():
    """Ouvre le navigateur après un délai."""
    time.sleep(2)  # Attend que le serveur démarre
    webbrowser.open("http://localhost:5000")

def main():
    """Point d'entrée principal."""
    
    print("🍳 Kitchen ML Planner - Interface Web")
    print("=" * 40)
    print()
    
    # Vérifications préliminaires
    if not check_dependencies():
        sys.exit(1)
    
    print("🔧 Préparation de l'environnement...")
    setup_data()
    
    print()
    print("🌐 Démarrage du serveur web...")
    print("📍 URL: http://localhost:5000")
    print("🔄 Mode debug activé")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter")
    print()
    
    # Programme l'ouverture du navigateur
    timer = Timer(2.0, open_browser)
    timer.start()
    
    try:
        # Lance le serveur Flask
        from web_interface import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
