#!/usr/bin/env python3
"""
YouTube Segment Downloader - Interface Graphique (v1.2.0)
Application GUI pour télécharger des segments de vidéos YouTube
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import sys
import queue
import time

# Import du module de téléchargement
try:
    from youtube_segment_downloader import download_segment, validate_url, time_to_seconds
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from youtube_segment_downloader import download_segment, validate_url, time_to_seconds


class YtdlpLogger:
    """Interface de logging pour yt-dlp qui renvoie les messages à la GUI"""
    def __init__(self, gui):
        self.gui = gui

    def debug(self, msg):
        # On ne logue pas les messages de progression bruts s'ils sont gérés par le hook
        if not msg.startswith('[download]'):
            self.gui.queue_log(f"DEBUG: {msg}", 'info')

    def info(self, msg):
        self.gui.queue_log(msg, 'info')

    def warning(self, msg):
        self.gui.queue_log(f"⚠️ {msg}", 'warning')

    def error(self, msg):
        self.gui.queue_log(f"❌ {msg}", 'error')


class YouTubeSegmentDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Segment Downloader Pro")
        self.root.geometry("650x650")
        self.root.resizable(True, True)
        
        # File d'attente pour les messages (thread-safety)
        self.msg_queue = queue.Queue()
        
        # Variables
        self.url_var = tk.StringVar()
        self.start_time_var = tk.StringVar(value="0:00")
        self.end_time_var = tk.StringVar(value="1:00")
        self.output_file_var = tk.StringVar()
        self.is_downloading = False
        self.stop_requested = False
        
        self.create_widgets()
        
        # Démarrer la vérification de la queue
        self.root.after(100, self.process_queue)
        
    def create_widgets(self):
        # Configuration des colonnes
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Large.TButton", font=('Arial', 12, 'bold'))
        style.configure("Accent.TButton", foreground="white", background="#007bff")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)
        
        # Titre
        title_label = ttk.Label(
            main_frame, 
            text="🎬 YouTube Segment Downloader",
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL YouTube
        ttk.Label(main_frame, text="URL YouTube:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var)
        url_entry.grid(row=1, column=1, columnspan=2, sticky="we", pady=5)
        
        # Configuration des entrées de temps
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=2, column=0, columnspan=3, sticky="we", pady=10)
        time_frame.columnconfigure(1, weight=1)
        time_frame.columnconfigure(3, weight=1)

        ttk.Label(time_frame, text="Début:", font=('Arial', 10)).grid(row=0, column=0, padx=(0, 5))
        ttk.Entry(time_frame, textvariable=self.start_time_var, width=12).grid(row=0, column=1, sticky="w")
        
        ttk.Label(time_frame, text="Fin:", font=('Arial', 10)).grid(row=0, column=2, padx=(20, 5))
        ttk.Entry(time_frame, textvariable=self.end_time_var, width=12).grid(row=0, column=3, sticky="w")
        
        ttk.Label(time_frame, text="(Format MM:SS ou HH:MM:SS)", font=('Arial', 8, 'italic')).grid(row=0, column=4, padx=(10, 0))
        
        # Fichier de sortie
        ttk.Label(main_frame, text="Sortie:", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        output_entry = ttk.Entry(main_frame, textvariable=self.output_file_var)
        output_entry.grid(row=4, column=1, sticky="we", pady=5)
        
        browse_btn = ttk.Button(main_frame, text="📂 Parcourir", command=self.browse_output)
        browse_btn.grid(row=4, column=2, sticky=tk.W, padx=(5, 0), pady=5)
        
        # Zone de progression et boutons d'action
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=5, column=0, columnspan=3, sticky="we", pady=20)
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        self.download_btn = ttk.Button(
            action_frame,
            text="📥 Télécharger",
            command=self.start_download,
            style="Large.TButton"
        )
        self.download_btn.grid(row=0, column=0, padx=5, sticky="we", ipady=5)

        self.cancel_btn = ttk.Button(
            action_frame,
            text="🛑 Annuler",
            command=self.cancel_download,
            state="disabled"
        )
        self.cancel_btn.grid(row=0, column=1, padx=5, sticky="we", ipady=5)

        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, 
            variable=self.progress_var, 
            maximum=100
        )
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky="we", pady=(0, 10))

        # Label de statut
        self.status_label = ttk.Label(
            main_frame, 
            text="Prêt",
            font=('Arial', 10, 'italic'),
            foreground='gray'
        )
        self.status_label.grid(row=7, column=0, columnspan=3, pady=5)
        
        # Zone de log
        log_frame = ttk.LabelFrame(main_frame, text="Terminal de contrôle", padding="10")
        log_frame.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        self.log_text = tk.Text(
            log_frame, 
            height=12, 
            width=70, 
            wrap=tk.WORD, 
            state='disabled', 
            font=('Courier', 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white"
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text['yscrollcommand'] = scrollbar.set
        
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("Fichiers MP4", "*.mp4"), ("Tous les fichiers", "*.*")],
            initialfile="segment.mp4"
        )
        if filename:
            self.output_file_var.set(filename)
    
    def queue_log(self, message, level='info'):
        self.msg_queue.put(('log', message, level))
        
    def update_status(self, message, color='black'):
        self.msg_queue.put(('status', message, color))

    def update_progress(self, percent):
        self.msg_queue.put(('progress', percent))

    def process_queue(self):
        try:
            while True:
                task = self.msg_queue.get_nowait()
                if task[0] == 'log':
                    self._real_log(task[1], task[2])
                elif task[0] == 'status':
                    self._real_update_status(task[1], task[2])
                elif task[0] == 'progress':
                    self.progress_var.set(task[1])
                self.msg_queue.task_done()
        except queue.Empty:
            pass
        finally:
            self.root.after(50, self.process_queue)

    def _real_log(self, message, level='info'):
        self.log_text.config(state='normal')
        colors = {'info': '#d4d4d4', 'success': '#4ec9b0', 'error': '#f44747', 'warning': '#d7ba7d'}
        tag = f'tag_{level}'
        self.log_text.tag_config(tag, foreground=colors.get(level, '#d4d4d4'))
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
    def _real_update_status(self, message, color='black'):
        self.status_label.config(text=message, foreground=color)
        
    def validate_inputs(self):
        if not self.url_var.get().strip():
            messagebox.showerror("Erreur", "URL manquante")
            return False
        return True
    
    def cancel_download(self):
        if self.is_downloading:
            self.stop_requested = True
            self.queue_log("🛑 Demande d'annulation envoyée...", 'warning')
            self.cancel_btn.config(state='disabled')

    def progress_hook(self, d):
        """Hook appelé par yt-dlp pour mettre à jour la progression"""
        if self.stop_requested:
            raise Exception("Téléchargement annulé par l'utilisateur")
            
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                percent = float(p)
                self.update_progress(percent)
                self.update_status(f"Téléchargement : {percent}%", "blue")
            except:
                pass
        elif d['status'] == 'finished':
            self.update_progress(100)
            self.update_status("Fusion et finalisation...", "purple")

    def start_download(self):
        if self.is_downloading or not self.validate_inputs():
            return
        
        self.is_downloading = True
        self.stop_requested = False
        self.download_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.progress_var.set(0)
        
        # Nettoyage logs
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')
        
        threading.Thread(target=self.download_thread, daemon=True).start()
    
    def download_thread(self):
        try:
            url = self.url_var.get().strip()
            start_time = self.start_time_var.get().strip()
            end_time = self.end_time_var.get().strip()
            output_file = self.output_file_var.get().strip() or None
            
            self.queue_log(f"🚀 Initialisation (Segment: {start_time} - {end_time})", 'info')
            
            success = download_segment(
                url=url,
                start_time=start_time,
                end_time=end_time,
                output_file=output_file,
                verbose=True,
                logger=YtdlpLogger(self),
                progress_hook=self.progress_hook
            )
            
            if success:
                self.queue_log(f"✅ Succès ! Fichier prêt.", 'success')
                self.update_status("Terminé", "green")
                messagebox.showinfo("Terminé", "Le téléchargement est réussi.")
            else:
                if not self.stop_requested:
                    self.queue_log("❌ Échec du téléchargement.", "error")
                    self.update_status("Erreur", "red")
                
        except Exception as e:
            if "annulé" in str(e):
                self.queue_log("ℹ️ Téléchargement annulé.", "warning")
                self.update_status("Annulé", "orange")
            else:
                self.queue_log(f"🔥 Erreur : {str(e)}", 'error')
                self.update_status("Échec critique", 'red')
        
        finally:
            self.is_downloading = False
            self.root.after(0, lambda: self.download_btn.config(state='normal'))
            self.root.after(0, lambda: self.cancel_btn.config(state='disabled'))


def main():
    root = tk.Tk()
    YouTubeSegmentDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
