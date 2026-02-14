"""
YouTube Segment Downloader - Téléchargez des segments spécifiques de vidéos YouTube
"""

__version__ = "1.0.8"
__author__ = "Daniel"
__license__ = "MIT"

from .downloader import download_segment, time_to_seconds, validate_url

__all__ = ["download_segment", "time_to_seconds", "validate_url"]
