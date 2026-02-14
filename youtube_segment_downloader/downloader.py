"""
Module principal pour le téléchargement de segments YouTube
"""

import subprocess
import re
from pathlib import Path
import yt_dlp
import sys


def time_to_seconds(time_str):
    """
    Convertit un format de temps en secondes
    Formats acceptés: "MM:SS" ou "HH:MM:SS"
    
    Args:
        time_str: Chaîne de temps au format MM:SS ou HH:MM:SS
        
    Returns:
        int: Nombre de secondes
        
    Raises:
        ValueError: Si le format de temps est invalide
    """
    parts = time_str.strip().split(':')
    if len(parts) == 2:  # MM:SS
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Format de temps invalide: {time_str}")


def validate_url(url):
    """
    Vérifie que l'URL est une URL YouTube valide
    
    Args:
        url: URL à valider
        
    Returns:
        str: URL validée
        
    Raises:
        ValueError: Si l'URL n'est pas une URL YouTube valide
    """
    youtube_pattern = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+'
    if not re.match(youtube_pattern, url):
        raise ValueError("URL YouTube invalide")
    return url


def get_ffmpeg_path():
    """
    Retourne le chemin vers le binaire ffmpeg.
    Cherche d'abord dans les fichiers packagés par PyInstaller (_MEIPASS), 
    puis dans le système.
    """
    if hasattr(sys, '_MEIPASS'):
        # Mode PyInstaller
        bundle_dir = sys._MEIPASS
        # Tester les noms courants selon l'OS
        for name in ['ffmpeg', 'ffmpeg.exe']:
            p = Path(bundle_dir) / name
            if p.exists():
                return str(p)
    
    # Mode normal ou si non trouvé dans le pack
    return 'ffmpeg'


def download_segment(url, start_time, end_time, output_file=None, verbose=True, logger=None):
    """
    Télécharge un segment d'une vidéo YouTube en utilisant yt-dlp comme bibliothèque Python
    
    Args:
        url: URL de la vidéo YouTube
        start_time: Temps de début (format "MM:SS" ou "HH:MM:SS")
        end_time: Temps de fin (format "MM:SS" ou "HH:MM:SS")
        output_file: Nom du fichier de sortie (optionnel)
        verbose: Afficher les messages de progression
        logger: Objet logger pour yt-dlp (optionnel)
        
    Returns:
        bool: True si le téléchargement a réussi, False sinon
        
    Raises:
        ValueError: Si les paramètres sont invalides
        RuntimeError: Si ffmpeg n'est pas installé
    """
    # Valider l'URL
    url = validate_url(url)
    
    # Convertir les temps en secondes
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)
    duration = end_seconds - start_seconds
    
    if duration <= 0:
        raise ValueError("Le temps de fin doit être après le temps de début")
    
    # Définir le nom du fichier de sortie
    if output_file is None:
        output_file = f"segment_{start_time.replace(':', '-')}_{end_time.replace(':', '-')}.mp4"
    
    # Obtenir le chemin de ffmpeg
    ffmpeg_path = get_ffmpeg_path()
    
    # Vérifier que ffmpeg est installé
    try:
        subprocess.run([ffmpeg_path, '-version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            f"ffmpeg n'est pas installé (utilisé: {ffmpeg_path}). "
            "Installation: sudo apt install ffmpeg (Linux) ou brew install ffmpeg (Mac)"
        )

    # Options pour yt-dlp - OPTIMISÉES POUR LE DÉCOUPAGE EFFICACE
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': output_file,
        'download_sections': [{
            'start_time': start_seconds,
            'end_time': end_seconds,
            'title': 'segment'
        }],
        # Options pour forcer le téléchargement par sections (évite de tout charger)
        'concurrent_fragment_downloads': 5,
        'force_keyframes_at_cuts': True,
        'quiet': not verbose and logger is None,
        'no_warnings': not verbose and logger is None,
        'logger': logger,
        # Argument spécifique pour s'assurer que ffmpeg est utilisé pour le "seeking" distant
        'external_downloader': {
            'default': 'ffmpeg',
        },
        'external_downloader_args': {
            'ffmpeg': [
                '-ss', str(start_seconds),
                '-to', str(end_seconds),
            ],
        },
    }

    if verbose and logger is None:
        print(f"📹 Téléchargement du segment: {start_time} → {end_time}")
        print(f"⏱️  Durée: {duration} secondes")
        print(f"📁 Fichier de sortie: {output_file}\n")

    try:
        with yt_dl_YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if Path(output_file).exists():
            if verbose:
                print(f"\n✅ Segment téléchargé avec succès: {output_file}")
                print(f"📁 Taille: {Path(output_file).stat().st_size / (1024*1024):.2f} MB")
            return True
        else:
            if verbose:
                print("\n❌ Erreur: Le fichier n'a pas été créé")
            return False
            
    except Exception as e:
        if verbose:
            print(f"\n❌ Erreur lors du téléchargement: {e}")
        return False
    except KeyboardInterrupt:
        if verbose:
            print("\n⚠️  Téléchargement annulé par l'utilisateur")
        return False

# Alias pour corriger une potentielle erreur de frappe si nécessaire dans le futur
yt_dl_YoutubeDL = yt_dlp.YoutubeDL
