# YouTube Segment Downloader

[![PyPI version](https://badge.fury.io/py/youtube-segment-downloader.svg)](https://badge.fury.io/py/youtube-segment-downloader)
[![Python](https://img.shields.io/pypi/pyversions/youtube-segment-downloader.svg)](https://pypi.org/project/youtube-segment-downloader/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un package Python simple et puissant pour télécharger des segments spécifiques de vidéos YouTube en format MP4.

## ✨ Fonctionnalités

- ✅ Télécharge uniquement le segment demandé (pas la vidéo complète)
- ✅ Qualité maximale disponible
- ✅ Format MP4 automatique
- ✅ Validation des URLs YouTube
- ✅ Gestion des erreurs robuste
- ✅ Interface CLI simple
- ✅ Utilisation programmatique en Python
- ✅ Affichage de la progression

## 📦 Installation

### Via pip (Recommandé)

```bash
pip install youtube-segment-downloader
```

### Depuis les sources

```bash
git clone https://github.com/yourusername/youtube-segment-downloader.git
cd youtube-segment-downloader
pip install -e .
```

## 📋 Prérequis

Le package nécessite **ffmpeg** installé sur votre système :

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Téléchargez depuis https://ffmpeg.org/download.html

## 🚀 Utilisation

### Interface en ligne de commande

Après installation, la commande `yt-segment` est disponible globalement :

```bash
yt-segment <URL> <début> <fin> [fichier_sortie]
```

**Exemples:**

```bash
# Télécharger de 15:21 à 30:21
yt-segment "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "15:21" "30:21"

# Avec un nom de fichier personnalisé
yt-segment "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "15:21" "30:21" "mon_extrait.mp4"

# Format avec heures (1h15m30s à 1h45m00s)
yt-segment "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "1:15:30" "1:45:00"
```

### Utilisation programmatique en Python

```python
from youtube_segment_downloader import download_segment

# Télécharger un segment
success = download_segment(
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    start_time="15:21",
    end_time="30:21",
    output_file="mon_segment.mp4",
    verbose=True
)

if success:
    print("Téléchargement réussi!")
```

### En tant que module Python

```bash
python -m youtube_segment_downloader "URL" "15:21" "30:21"
```

## 📝 Formats de temps acceptés

- **MM:SS** - Minutes:Secondes (ex: "15:21")
- **HH:MM:SS** - Heures:Minutes:Secondes (ex: "1:15:30")

## 🔧 Comment ça marche

Le package utilise:
1. **yt-dlp** avec l'option `--download-sections` pour télécharger uniquement la partie demandée
2. **ffmpeg** pour découper et fusionner la vidéo et l'audio
3. Format de sortie MP4 pour une compatibilité maximale

## ⚠️ Notes importantes

- Respectez les droits d'auteur et les conditions d'utilisation de YouTube
- Assurez-vous d'avoir une connexion internet stable
- Les temps doivent être valides (le temps de fin doit être après le début)
- Le fichier sera sauvegardé dans le répertoire courant

## 🐛 Dépannage

**"RuntimeError: yt-dlp n'est pas installé"**
```bash
pip install yt-dlp
```

**"RuntimeError: ffmpeg n'est pas installé"**
- Installez ffmpeg selon votre système d'exploitation (voir Prérequis)

**"ValueError: URL YouTube invalide"**
- Vérifiez que l'URL commence par `https://www.youtube.com/watch?v=` ou `https://youtu.be/`

**Le téléchargement est lent**
- C'est normal, yt-dlp télécharge et traite la vidéo en temps réel

## 🧪 Tests

Pour exécuter les tests :

```bash
pip install pytest
pytest tests/
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🔗 Liens

- [PyPI](https://pypi.org/project/youtube-segment-downloader/)
- [GitHub](https://github.com/yourusername/youtube-segment-downloader)
- [Issues](https://github.com/yourusername/youtube-segment-downloader/issues)

## 📊 Changelog

Voir [CHANGELOG.md](CHANGELOG.md) pour l'historique des versions.

---

**Utilisez-le de manière responsable et respectez les droits d'auteur !** 🎬
