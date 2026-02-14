"""
Module principal pour le téléchargement de segments YouTube
"""

import subprocess
import re
from pathlib import Path
import yt_dlp
import sys
import os


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
    puis dans les emplacements système courants,
    enfin se replie sur la commande 'ffmpeg'.
    """
    if hasattr(sys, '_MEIPASS'):
        # Mode PyInstaller
        bundle_dir = sys._MEIPASS
        for name in ['ffmpeg', 'ffmpeg.exe']:
            p = Path(bundle_dir) / name
            if p.exists():
                return str(p)
    
    # Chemins système courants
    common_paths = [
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        'C:\\ffmpeg\\bin\\ffmpeg.exe',
        os.path.join(os.path.expanduser('~'), 'bin', 'ffmpeg')
    ]
    for path in common_paths:
        if Path(path).exists():
            return path
            
    # Mode normal ou si non trouvé dans le pack
    return 'ffmpeg'


def download_segment(url, start_time, end_time, output_file=None, verbose=True, logger=None, progress_hook=None):
    """
    Télécharge un segment d'une vidéo YouTube avec une efficacité maximale.
    
    Args:
        url: URL de la vidéo YouTube
        start_time: Temps de début ("MM:SS" ou "HH:MM:SS")
        end_time: Temps de fin ("MM:SS" ou "HH:MM:SS")
        output_file: Nom du fichier de sortie
        verbose: Affichage console
        logger: Logger personnalisé pour yt-dlp
        progress_hook: Fonction appelée à chaque mise à jour de progression
        
    Returns:
        bool: Succès ou échec
    """
    try:
        url = validate_url(url)
        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)
        duration = end_seconds - start_seconds
        
        if duration <= 0:
            raise ValueError("Le temps de fin doit être après le temps de début")
        
        if output_file is None:
            output_file = f"segment_{start_time.replace(':', '-')}_{end_time.replace(':', '-')}.mp4"
        
        ffmpeg_path = get_ffmpeg_path()
        
        # Vérification ffmpeg (indispensable pour le découpage)
        try:
            subprocess.run([ffmpeg_path, '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            error_msg = f"FFmpeg introuvable à : {ffmpeg_path}. Veuillez l'installer."
            if logger: logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Configuration optimisée de yt-dlp
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
            'force_keyframes_at_cuts': True,
            'logger': logger,
            'progress_hooks': [progress_hook] if progress_hook else [],
            'quiet': not verbose and logger is None,
            'no_warnings': not verbose and logger is None,
            'retries': 10,
            'fragment_retries': 10,
        }

        if verbose and logger is None:
            print(f"🚀 Démarrage du téléchargement optimisé ({start_time} -> {end_time})")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return Path(output_file).exists()
            
    except Exception as e:
        error_msg = str(e)
        if logger:
            logger.error(error_msg)
        elif verbose:
            print(f"❌ Erreur critique : {error_msg}")
        return False

# Alias pour corriger une potentielle erreur de frappe si nécessaire dans le futur
yt_dl_YoutubeDL = yt_dlp.YoutubeDL
