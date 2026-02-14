"""
Interface en ligne de commande pour YouTube Segment Downloader
"""

import sys
from .downloader import download_segment


def main():
    """Fonction principale pour l'interface CLI"""
    if len(sys.argv) < 4:
        print("Usage: yt-segment <URL> <début> <fin> [fichier_sortie]")
        print("\nExemples:")
        print('  yt-segment "https://www.youtube.com/watch?v=..." "15:21" "30:21"')
        print('  yt-segment "https://www.youtube.com/watch?v=..." "1:15:30" "1:45:00" "mon_segment.mp4"')
        print("\nFormats de temps acceptés: MM:SS ou HH:MM:SS")
        sys.exit(1)
    
    url = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    try:
        success = download_segment(url, start_time, end_time, output_file)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
