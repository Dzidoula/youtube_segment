# Guide : Créer des Exécutables Windows avec GitHub Actions

## 📋 Prérequis

1. Un compte GitHub
2. Votre code poussé sur GitHub

## 🚀 Étapes pour Créer l'Exécutable Windows

### 1. Créer un Dépôt GitHub

```bash
# Initialiser git (si pas déjà fait)
cd /home/daniel/Downloads/files
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit: YouTube Segment Downloader v1.0.0"

# Créer le dépôt sur GitHub (via l'interface web)
# Puis lier le dépôt local
git remote add origin https://github.com/VOTRE_USERNAME/youtube-segment-downloader.git
git branch -M main
git push -u origin main
```

### 2. Créer une Release

Une fois le code poussé sur GitHub :

1. **Allez sur votre dépôt GitHub**
   - `https://github.com/VOTRE_USERNAME/youtube-segment-downloader`

2. **Cliquez sur "Releases"** (à droite)

3. **Cliquez sur "Create a new release"**

4. **Remplissez les informations** :
   - **Tag** : `v1.0.0`
   - **Release title** : `YouTube Segment Downloader v1.0.0`
   - **Description** : Copiez le contenu de `RELEASE_README.md`

5. **Cliquez sur "Publish release"**

### 3. GitHub Actions Build Automatiquement

Dès que vous créez la release, GitHub Actions va :

1. ✅ Builder pour **Linux** (Ubuntu)
2. ✅ Builder pour **Windows** (`.exe`)
3. ✅ Builder pour **macOS**

Le processus prend environ **5-10 minutes**.

### 4. Télécharger les Exécutables

Une fois le build terminé :

1. Allez dans l'onglet **"Actions"** de votre dépôt
2. Cliquez sur le workflow "Build Executables"
3. Les exécutables seront automatiquement attachés à votre release :
   - `yt-segment-gui-linux`
   - `yt-segment-gui-windows.exe` ⭐
   - `yt-segment-gui-macos`

## 🔄 Lancer le Build Manuellement

Vous pouvez aussi lancer le build sans créer de release :

1. Allez dans **"Actions"**
2. Sélectionnez **"Build Executables"**
3. Cliquez sur **"Run workflow"**
4. Choisissez la branche (`main`)
5. Cliquez sur **"Run workflow"**

Les exécutables seront disponibles dans les **artifacts** du workflow.

## 📥 Télécharger les Artifacts

Si vous avez lancé manuellement :

1. Allez dans **"Actions"**
2. Cliquez sur le workflow terminé
3. Scrollez en bas vers **"Artifacts"**
4. Téléchargez :
   - `yt-segment-gui-linux`
   - `yt-segment-gui-windows.exe` ⭐
   - `yt-segment-gui-macos`

## 🎯 Résultat Final

Vous aurez 3 exécutables :

### Windows (`.exe`)
- **Nom** : `yt-segment-gui-windows.exe`
- **Taille** : ~15-20 MB
- **Utilisation** : Double-clic pour lancer

### Linux
- **Nom** : `yt-segment-gui-linux`
- **Taille** : ~12 MB
- **Utilisation** : `./yt-segment-gui-linux`

### macOS
- **Nom** : `yt-segment-gui-macos`
- **Taille** : ~15 MB
- **Utilisation** : `./yt-segment-gui-macos`

## 💡 Astuces

### Mettre à Jour les Exécutables

Pour créer de nouveaux exécutables :

1. Modifiez votre code
2. Committez et poussez : `git push`
3. Créez une nouvelle release : `v1.0.1`, `v1.1.0`, etc.
4. GitHub Actions rebuild automatiquement

### Vérifier le Statut du Build

- Badge de statut : Ajoutez dans votre README.md
  ```markdown
  ![Build Status](https://github.com/VOTRE_USERNAME/youtube-segment-downloader/workflows/Build%20Executables/badge.svg)
  ```

### Logs de Build

Si le build échoue :
1. Allez dans **"Actions"**
2. Cliquez sur le workflow échoué
3. Consultez les logs pour voir l'erreur

## 🔐 Permissions

Le workflow utilise `GITHUB_TOKEN` qui est automatiquement fourni par GitHub. Aucune configuration supplémentaire nécessaire.

## ⚠️ Notes Importantes

1. **Première fois** : Le premier build peut prendre plus de temps (téléchargement des dépendances)
2. **Gratuit** : GitHub Actions est gratuit pour les dépôts publics
3. **Limites** : 2000 minutes/mois pour les dépôts privés
4. **ffmpeg** : Les utilisateurs devront toujours installer ffmpeg séparément

## 🎉 C'est Tout !

Une fois configuré, chaque release créera automatiquement des exécutables pour les 3 plateformes !
