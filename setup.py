"""
Configuration du package YouTube Segment Downloader pour PyPI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lire le README pour la description longue
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="youtube-segment-downloader",
    version="1.2.1",
    author="Daniel",
    author_email="",  # Ajoutez votre email si vous voulez
    description="Téléchargez des segments spécifiques de vidéos YouTube en MP4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/youtube-segment-downloader",  # Ajoutez votre URL GitHub
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "yt-dlp>=2023.1.1",
    ],
    entry_points={
        "console_scripts": [
            "yt-segment=youtube_segment_downloader.cli:main",
        ],
    },
    keywords="youtube video download segment clip extract mp4",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/youtube-segment-downloader/issues",
        "Source": "https://github.com/yourusername/youtube-segment-downloader",
    },
)
