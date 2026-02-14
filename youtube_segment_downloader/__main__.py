"""
Point d'entrée pour l'exécution en tant que module
Usage: python -m youtube_segment_downloader <URL> <début> <fin> [fichier_sortie]
"""

from .cli import main

if __name__ == "__main__":
    main()
