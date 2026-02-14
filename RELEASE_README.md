# YouTube Segment Downloader - Standalone Application

Download specific segments from YouTube videos with an easy-to-use graphical interface.

## 📥 Download

Choose the version for your operating system:

- **Windows**: [yt-segment-gui-windows.exe](../../releases/latest/download/yt-segment-gui-windows.exe)
- **Linux**: [yt-segment-gui-linux](../../releases/latest/download/yt-segment-gui-linux)
- **macOS**: [yt-segment-gui-macos](../../releases/latest/download/yt-segment-gui-macos)

## ⚡ Quick Start

1. **Install ffmpeg** (required):
   - **Linux**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/download.html

2. **Download the application** for your OS (see links above)

3. **Run the application**:
   - **Linux/Mac**: Make it executable first: `chmod +x yt-segment-gui-linux`
   - **Windows**: Double-click the `.exe` file

4. **Use the application**:
   - Paste a YouTube URL
   - Enter start time (e.g., `1:20`)
   - Enter end time (e.g., `2:38`)
   - Click "Download Segment"

## 📖 Full Documentation

See [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions and troubleshooting.

## ✨ Features

- ✅ Simple graphical interface
- ✅ No Python installation required
- ✅ Download only the segment you need
- ✅ Best quality available (Full HD when possible)
- ✅ Progress indicator
- ✅ Detailed logs
- ✅ Cross-platform (Windows, Linux, macOS)

## 🎬 Screenshot

![Application Screenshot](screenshot.png)

## 🔧 For Developers

If you're a developer, you can also install via pip:

```bash
pip install youtube-segment-downloader
yt-segment "URL" "1:20" "2:38"
```

See the [main README](README.md) for more information.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

Respect YouTube's Terms of Service and copyright laws. This tool is for personal use only.
