#!/usr/bin/env python3
"""
YouTube Segment Downloader - Interface Graphique
Application GUI pour télécharger des segments de vidéos YouTube
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import sys

# Import du module de téléchargement
try:
    from youtube_segment_downloader import download_segment, validate_url, time_to_seconds
except ImportError:
    # Si exécuté depuis le répertoire local
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from youtube_segment_downloader import download_segment, validate_url, time_to_seconds


class YouTubeSegmentDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Segment Downloader")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.url_var = tk.StringVar()
        self.start_time_var = tk.StringVar(value="0:00")
        self.end_time_var = tk.StringVar(value="1:00")
        self.output_file_var = tk.StringVar()
        self.is_downloading = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = ttk.Label(
            main_frame, 
            text="🎬 YouTube Segment Downloader",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL YouTube
        ttk.Label(main_frame, text="URL YouTube:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Temps de début
        ttk.Label(main_frame, text="Temps de début:", font=('Arial', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        start_entry = ttk.Entry(main_frame, textvariable=self.start_time_var, width=20)
        start_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="(MM:SS ou HH:MM:SS)", font=('Arial', 8, 'italic')).grid(
            row=2, column=2, sticky=tk.W, padx=(5, 0)
        )
        
        # Temps de fin
        ttk.Label(main_frame, text="Temps de fin:", font=('Arial', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        end_entry = ttk.Entry(main_frame, textvariable=self.end_time_var, width=20)
        end_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="(MM:SS ou HH:MM:SS)", font=('Arial', 8, 'italic')).grid(
            row=3, column=2, sticky=tk.W, padx=(5, 0)
        )
        
        # Fichier de sortie
        ttk.Label(main_frame, text="Fichier de sortie:", font=('Arial', 10)).grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        output_entry = ttk.Entry(main_frame, textvariable=self.output_file_var, width=35)
        output_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Parcourir...", command=self.browse_output)
        browse_btn.grid(row=4, column=2, sticky=tk.W, padx=(5, 0), pady=5)
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, 
            variable=self.progress_var, 
            maximum=100,
            mode='indeterminate'
        )
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Label de statut
        self.status_label = ttk.Label(
            main_frame, 
            text="Prêt à télécharger",
            font=('Arial', 9),
            foreground='green'
        )
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Bouton de téléchargement
        self.download_btn = ttk.Button(
            main_frame,
            text="📥 Télécharger le Segment",
            command=self.start_download,
            style='Accent.TButton'
        )
        self.download_btn.grid(row=7, column=0, columnspan=3, pady=10, ipadx=20, ipady=10)
        
        # Zone de log
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="10")
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=60, wrap=tk.WORD, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # Info footer
        footer_label = ttk.Label(
            main_frame,
            text="💡 Astuce: ffmpeg doit être installé sur votre système",
            font=('Arial', 8, 'italic'),
            foreground='gray'
        )
        footer_label.grid(row=9, column=0, columnspan=3, pady=(10, 0))
        
    def browse_output(self):
        """Ouvre un dialogue pour choisir le fichier de sortie"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("Fichiers MP4", "*.mp4"), ("Tous les fichiers", "*.*")],
            initialfile="segment.mp4"
        )
        if filename:
            self.output_file_var.set(filename)
    
    def log(self, message, level='info'):
        """Ajoute un message au log"""
        self.log_text.config(state='normal')
        
        colors = {
            'info': 'black',
            'success': 'green',
            'error': 'red',
            'warning': 'orange'
        }
        
        tag = f'tag_{level}'
        self.log_text.tag_config(tag, foreground=colors.get(level, 'black'))
        
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
    def update_status(self, message, color='black'):
        """Met à jour le label de statut"""
        self.status_label.config(text=message, foreground=color)
        
    def validate_inputs(self):
        """Valide les entrées utilisateur"""
        # Vérifier l'URL
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube")
            return False
        
        try:
            validate_url(url)
        except ValueError as e:
            messagebox.showerror("Erreur", f"URL invalide: {e}")
            return False
        
        # Vérifier les temps
        start_time = self.start_time_var.get().strip()
        end_time = self.end_time_var.get().strip()
        
        try:
            start_seconds = time_to_seconds(start_time)
            end_seconds = time_to_seconds(end_time)
            
            if end_seconds <= start_seconds:
                messagebox.showerror("Erreur", "Le temps de fin doit être après le temps de début")
                return False
                
        except ValueError as e:
            messagebox.showerror("Erreur", f"Format de temps invalide: {e}")
            return False
        
        return True
    
    def start_download(self):
        """Démarre le téléchargement dans un thread séparé"""
        if self.is_downloading:
            messagebox.showwarning("Attention", "Un téléchargement est déjà en cours")
            return
        
        if not self.validate_inputs():
            return
        
        # Démarrer le téléchargement dans un thread
        self.is_downloading = True
        self.download_btn.config(state='disabled')
        self.progress_bar.start(10)
        
        thread = threading.Thread(target=self.download_thread, daemon=True)
        thread.start()
    
    def download_thread(self):
        """Thread de téléchargement"""
        try:
            url = self.url_var.get().strip()
            start_time = self.start_time_var.get().strip()
            end_time = self.end_time_var.get().strip()
            output_file = self.output_file_var.get().strip() or None
            
            self.log(f"📹 Début du téléchargement...", 'info')
            self.log(f"URL: {url}", 'info')
            self.log(f"Segment: {start_time} → {end_time}", 'info')
            self.update_status("Téléchargement en cours...", 'blue')
            
            # Télécharger
            success = download_segment(
                url=url,
                start_time=start_time,
                end_time=end_time,
                output_file=output_file,
                verbose=False
            )
            
            if success:
                output = output_file or f"segment_{start_time.replace(':', '-')}_{end_time.replace(':', '-')}.mp4"
                self.log(f"✅ Téléchargement réussi: {output}", 'success')
                self.update_status("Téléchargement terminé avec succès!", 'green')
                messagebox.showinfo("Succès", f"Segment téléchargé avec succès!\n\nFichier: {output}")
            else:
                self.log("❌ Échec du téléchargement", 'error')
                self.update_status("Échec du téléchargement", 'red')
                messagebox.showerror("Erreur", "Le téléchargement a échoué. Vérifiez les logs.")
                
        except Exception as e:
            self.log(f"❌ Erreur: {str(e)}", 'error')
            self.update_status("Erreur lors du téléchargement", 'red')
            messagebox.showerror("Erreur", f"Une erreur s'est produite:\n{str(e)}")
        
        finally:
            self.is_downloading = False
            self.root.after(0, self.progress_bar.stop)
            self.root.after(0, lambda: self.download_btn.config(state='normal'))


def main():
    """Point d'entrée principal"""
    root = tk.Tk()
    app = YouTubeSegmentDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
