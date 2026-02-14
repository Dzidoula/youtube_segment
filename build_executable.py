#!/usr/bin/env python3
"""
Script pour construire l'exécutable standalone avec PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path


def check_pyinstaller():
    """Vérifie si PyInstaller est installé"""
    try:
        import PyInstaller
        print("✅ PyInstaller est installé")
        return True
    except ImportError:
        print("❌ PyInstaller n'est pas installé")
        print("📦 Installation: pip install pyinstaller")
        return False


def build_executable():
    """Construit l'exécutable avec PyInstaller"""
    print("\n🔨 Construction de l'exécutable...")
    print("=" * 60)
    
    # Trouver le chemin de pyinstaller dans le venv
    venv_pyinstaller = Path('./venv/bin/pyinstaller')
    if venv_pyinstaller.exists():
        pyinstaller_cmd = str(venv_pyinstaller)
    else:
        pyinstaller_cmd = 'pyinstaller'
    
    # Options PyInstaller
    options = [
        pyinstaller_cmd,
        '--onefile',  # Un seul fichier exécutable
        '--windowed',  # Pas de console (GUI uniquement)
        '--name=yt-segment-gui',  # Nom de l'exécutable
        '--clean',  # Nettoyer les fichiers temporaires
        '--noconfirm',  # Ne pas demander de confirmation
        # Ajouter les dépendances
        '--hidden-import=youtube_segment_downloader',
        '--hidden-import=youtube_segment_downloader.downloader',
        '--hidden-import=youtube_segment_downloader.cli',
        # Fichier source
        'youtube_segment_downloader_gui.py'
    ]
    
    try:
        result = subprocess.run(options, check=True)
        
        print("\n" + "=" * 60)
        print("✅ Construction réussie!")
        print(f"📁 Exécutable créé dans: ./dist/yt-segment-gui")
        print("\n💡 Pour tester:")
        print("   ./dist/yt-segment-gui")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de la construction: {e}")
        return False


def main():
    """Fonction principale"""
    print("🎬 YouTube Segment Downloader - Build Script")
    print("=" * 60)
    
    # Vérifier PyInstaller
    if not check_pyinstaller():
        print("\n📦 Voulez-vous installer PyInstaller maintenant? (y/n)")
        response = input("> ").strip().lower()
        if response == 'y':
            print("\n📦 Installation de PyInstaller...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        else:
            print("❌ PyInstaller est requis pour construire l'exécutable")
            return 1
    
    # Vérifier que le fichier GUI existe
    if not Path('youtube_segment_downloader_gui.py').exists():
        print("❌ Fichier youtube_segment_downloader_gui.py introuvable")
        return 1
    
    # Construire l'exécutable
    if build_executable():
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
