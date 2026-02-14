# Guide de Publication sur PyPI

## 📦 Fichiers de Distribution Créés

Les fichiers suivants ont été créés dans le dossier `dist/` :

- `youtube_segment_downloader-1.0.0.tar.gz` (9.2 KB) - Archive source
- `youtube_segment_downloader-1.0.0-py3-none-any.whl` (7.7 KB) - Wheel Python

## 🚀 Publication sur PyPI

### Étape 1 : Créer un Compte PyPI

1. Allez sur https://pypi.org/account/register/
2. Créez un compte
3. Vérifiez votre email

### Étape 2 : Installer Twine

```bash
pip install twine
```

### Étape 3 : (Recommandé) Tester sur TestPyPI

Avant de publier sur PyPI officiel, testez sur TestPyPI :

```bash
# Créer un compte sur https://test.pypi.org/account/register/

# Uploader sur TestPyPI
twine upload --repository testpypi dist/*

# Tester l'installation
pip install --index-url https://test.pypi.org/simple/ youtube-segment-downloader
```

### Étape 4 : Publier sur PyPI Officiel

```bash
# Uploader sur PyPI
twine upload dist/*

# Vous serez invité à entrer votre nom d'utilisateur et mot de passe PyPI
```

### Étape 5 : Vérifier la Publication

Visitez : https://pypi.org/project/youtube-segment-downloader/

## 🔐 Utiliser un Token API (Recommandé)

Pour plus de sécurité, utilisez un token API au lieu du mot de passe :

1. Allez sur https://pypi.org/manage/account/token/
2. Créez un nouveau token
3. Créez un fichier `~/.pypirc` :

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

## 📝 Commandes Utiles

```bash
# Vérifier les fichiers avant upload
twine check dist/*

# Uploader une version spécifique
twine upload dist/youtube_segment_downloader-1.0.0*

# Uploader avec verbose
twine upload --verbose dist/*
```

## 🔄 Publier une Nouvelle Version

1. Mettez à jour le numéro de version dans :
   - `youtube_segment_downloader/__init__.py`
   - `setup.py`
   - `pyproject.toml`

2. Mettez à jour `CHANGELOG.md`

3. Reconstruisez le package :
```bash
rm -rf dist/ build/ *.egg-info
python -m build
```

4. Uploadez la nouvelle version :
```bash
twine upload dist/*
```

## ⚠️ Important

- **Ne publiez jamais de secrets** (tokens, mots de passe) dans le code
- **Testez toujours** sur TestPyPI avant PyPI
- **Vérifiez les fichiers** avec `twine check` avant upload
- **Utilisez des tokens API** au lieu de mots de passe
- **Suivez le versioning sémantique** (MAJOR.MINOR.PATCH)

## 📊 Après Publication

Une fois publié, les utilisateurs pourront installer votre package avec :

```bash
pip install youtube-segment-downloader
```

Et utiliser la commande :

```bash
yt-segment "URL" "1:20" "2:38"
```
