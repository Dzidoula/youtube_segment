"""
Tests unitaires pour YouTube Segment Downloader
"""

import pytest
from youtube_segment_downloader import time_to_seconds, validate_url


class TestTimeConversion:
    """Tests pour la conversion de temps"""
    
    def test_minutes_seconds_format(self):
        """Test du format MM:SS"""
        assert time_to_seconds("15:21") == 921
        assert time_to_seconds("00:30") == 30
        assert time_to_seconds("1:00") == 60
    
    def test_hours_minutes_seconds_format(self):
        """Test du format HH:MM:SS"""
        assert time_to_seconds("1:15:30") == 4530
        assert time_to_seconds("0:15:21") == 921
        assert time_to_seconds("2:00:00") == 7200
    
    def test_invalid_format(self):
        """Test des formats invalides"""
        with pytest.raises(ValueError):
            time_to_seconds("15")
        with pytest.raises(ValueError):
            time_to_seconds("1:2:3:4")


class TestURLValidation:
    """Tests pour la validation d'URL"""
    
    def test_valid_youtube_urls(self):
        """Test des URLs YouTube valides"""
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ]
        for url in urls:
            assert validate_url(url) == url
    
    def test_invalid_urls(self):
        """Test des URLs invalides"""
        with pytest.raises(ValueError):
            validate_url("https://www.google.com")
        with pytest.raises(ValueError):
            validate_url("not a url")
        with pytest.raises(ValueError):
            validate_url("")


if __name__ == "__main__":
    pytest.main([__file__])
