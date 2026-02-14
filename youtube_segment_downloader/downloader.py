"""
Module principal pour le téléchargement de segments YouTube
"""

import subprocess
import re
from pathlib import Path


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


def download_segment(url, start_time, end_time, output_file=None, verbose=True):
    """
    Télécharge un segment d'une vidéo YouTube
    
    Args:
        url: URL de la vidéo YouTube
        start_time: Temps de début (format "MM:SS" ou "HH:MM:SS")
        end_time: Temps de fin (format "MM:SS" ou "HH:MM:SS")
        output_file: Nom du fichier de sortie (optionnel)
        verbose: Afficher les messages de progression
        
    Returns:
        bool: True si le téléchargement a réussi, False sinon
        
    Raises:
        ValueError: Si les paramètres sont invalides
        RuntimeError: Si yt-dlp ou ffmpeg n'est pas installé
    """
    # Valider l'URL
    url = validate_url(url)
    
    # Convertir les temps en secondes
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)
    duration = end_seconds - start_seconds
    
    if duration <= 0:
        raise ValueError("Le temps de fin doit être après le temps de début")
    
    if verbose:
        print(f"📹 Téléchargement du segment: {start_time} → {end_time}")
        print(f"⏱️  Durée: {duration} secondes")
    
    # Définir le nom du fichier de sortie
    if output_file is None:
        output_file = f"segment_{start_time.replace(':', '-')}_{end_time.replace(':', '-')}.mp4"
    
    # Vérifier que yt-dlp est installé
    try:
        subprocess.run(['yt-dlp', '--version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "yt-dlp n'est pas installé. Installation: pip install yt-dlp"
        )
    
    # Vérifier que ffmpeg est installé
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "ffmpeg n'est pas installé. Installation: sudo apt install ffmpeg (Linux) "
            "ou brew install ffmpeg (Mac)"
        )
    
    # Commande yt-dlp avec options de découpage
    command = [
        'yt-dlp',
        '--download-sections',
        f'*{start_seconds}-{end_seconds}',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '-o', output_file,
        url
    ]
    
    if verbose:
        print(f"🔧 Commande: {' '.join(command)}\n")
    
    try:
        # Exécuter la commande
        result = subprocess.run(command, check=True)
        
        if Path(output_file).exists():
            if verbose:
                print(f"\n✅ Segment téléchargé avec succès: {output_file}")
                print(f"📁 Taille: {Path(output_file).stat().st_size / (1024*1024):.2f} MB")
            return True
        else:
            if verbose:
                print("\n❌ Erreur: Le fichier n'a pas été créé")
            return False
            
    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"\n❌ Erreur lors du téléchargement: {e}")
        return False
    except KeyboardInterrupt:
        if verbose:
            print("\n⚠️  Téléchargement annulé par l'utilisateur")
        return False
