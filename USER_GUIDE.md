# Guide Utilisateur - YouTube Segment Downloader

## 📥 Installation

### Prérequis

**ffmpeg** doit être installé sur votre système :

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

#### Windows
Téléchargez depuis https://ffmpeg.org/download.html et ajoutez-le au PATH

### Télécharger l'Application

1. Allez sur la page des releases : https://github.com/yourusername/youtube-segment-downloader/releases
2. Téléchargez le fichier correspondant à votre système :
   - **Linux** : `yt-segment-gui-linux`
   - **Windows** : `yt-segment-gui-windows.exe`
   - **macOS** : `yt-segment-gui-macos`

3. **Linux/Mac uniquement** : Rendez le fichier exécutable
   ```bash
   chmod +x yt-segment-gui-linux
   ```

## 🚀 Utilisation

### Lancer l'Application

**Linux/Mac** :
```bash
./yt-segment-gui-linux
```

**Windows** :
Double-cliquez sur `yt-segment-gui-windows.exe`

### Télécharger un Segment

1. **Copiez l'URL YouTube** de la vidéo que vous voulez télécharger
   - Exemple : `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

2. **Collez l'URL** dans le champ "URL YouTube"

3. **Entrez le temps de début** (format MM:SS ou HH:MM:SS)
   - Exemple : `1:20` pour 1 minute 20 secondes
   - Exemple : `1:15:30` pour 1 heure 15 minutes 30 secondes

4. **Entrez le temps de fin** (format MM:SS ou HH:MM:SS)
   - Exemple : `2:38` pour 2 minutes 38 secondes

5. **(Optionnel) Choisissez le nom du fichier de sortie**
   - Cliquez sur "Parcourir..." pour choisir l'emplacement et le nom
   - Par défaut : `segment_1-20_2-38.mp4`

6. **Cliquez sur "📥 Télécharger le Segment"**

7. **Attendez** que le téléchargement se termine
   - La barre de progression s'anime pendant le téléchargement
   - Les logs affichent la progression

8. **C'est terminé !** 🎉
   - Un message de confirmation s'affiche
   - Le fichier MP4 est sauvegardé à l'emplacement choisi

## 📝 Exemples

### Exemple 1 : Télécharger un court extrait

- **URL** : `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- **Début** : `0:30`
- **Fin** : `1:00`
- **Résultat** : Télécharge 30 secondes de vidéo (de 0:30 à 1:00)

### Exemple 2 : Télécharger un long segment

- **URL** : `https://youtu.be/sDCKsyT_XKo`
- **Début** : `1:20`
- **Fin** : `2:38`
- **Résultat** : Télécharge 1 minute 18 secondes de vidéo

### Exemple 3 : Avec heures

- **URL** : `https://www.youtube.com/watch?v=VIDEO_ID`
- **Début** : `1:15:30` (1h 15min 30s)
- **Fin** : `1:45:00` (1h 45min)
- **Résultat** : Télécharge 29 minutes 30 secondes de vidéo

## ❓ Résolution de Problèmes

### "ffmpeg n'est pas installé"

**Problème** : Le message d'erreur indique que ffmpeg n'est pas trouvé

**Solution** : Installez ffmpeg selon votre système d'exploitation (voir section Prérequis)

### "URL YouTube invalide"

**Problème** : L'URL n'est pas reconnue

**Solution** : 
- Vérifiez que l'URL commence par `https://www.youtube.com/watch?v=` ou `https://youtu.be/`
- Copiez l'URL directement depuis la barre d'adresse du navigateur

### "Format de temps invalide"

**Problème** : Le format de temps n'est pas reconnu

**Solution** :
- Utilisez le format `MM:SS` (ex: `1:30`)
- Ou le format `HH:MM:SS` (ex: `1:15:30`)
- N'utilisez pas de lettres (pas de "1m30s")

### "Le temps de fin doit être après le temps de début"

**Problème** : Le temps de fin est avant ou égal au temps de début

**Solution** : Assurez-vous que le temps de fin est supérieur au temps de début

### Le téléchargement est très lent

**Problème** : Le téléchargement prend beaucoup de temps

**Solution** : 
- C'est normal pour les vidéos en haute qualité
- Vérifiez votre connexion internet
- Essayez avec un segment plus court pour tester

### L'application ne se lance pas

**Linux/Mac** :
- Vérifiez que le fichier est exécutable : `chmod +x yt-segment-gui-linux`
- Lancez depuis le terminal pour voir les erreurs

**Windows** :
- Vérifiez que Windows Defender ne bloque pas l'application
- Faites un clic droit → "Exécuter en tant qu'administrateur"

## 💡 Astuces

- **Raccourcis clavier** : Vous pouvez utiliser Tab pour naviguer entre les champs
- **Copier-coller** : Ctrl+C / Ctrl+V (Cmd+C / Cmd+V sur Mac) fonctionnent normalement
- **Logs** : Consultez la zone de logs en bas pour suivre la progression détaillée
- **Qualité** : L'application télécharge toujours la meilleure qualité disponible

## 📞 Support

Si vous rencontrez des problèmes :

1. Consultez les logs dans l'application
2. Vérifiez que ffmpeg est bien installé : `ffmpeg -version`
3. Ouvrez une issue sur GitHub : https://github.com/yourusername/youtube-segment-downloader/issues

## ⚖️ Avertissement

Respectez les droits d'auteur et les conditions d'utilisation de YouTube. Cet outil est destiné à un usage personnel uniquement.
