"""
Text-to-speech handler using gTTS with stability improvements.
"""

import os
import hashlib
from gtts import gTTS
from src.config import Config


class TTSHandler:
    """Generates MP3 audio for interviewer messages with caching."""

    def __init__(self):
        os.makedirs(Config.AUDIO_CACHE_DIR, exist_ok=True)
        self.cache_dir = Config.AUDIO_CACHE_DIR

    # ------------------------------------------------------------
    # Cache filename generator
    # ------------------------------------------------------------
    def _get_cache_path(self, text: str) -> str:
        """
        Create a stable hash-based filename for caching.
        """
        hashed = hashlib.md5(text.encode("utf-8")).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed}.mp3")

    # ------------------------------------------------------------
    # Convert text to MP3
    # ------------------------------------------------------------
    def text_to_speech(self, text: str, use_cache: bool = True) -> str:
        """
        Generate speech from text using gTTS.

        Returns:
            Path to MP3 file or None if generation fails.
        """
        if not text or len(text.strip()) == 0:
            print("[TTS] Empty text received.")
            return None

        cache_path = self._get_cache_path(text)

        # Use cache if exists
        if use_cache and os.path.exists(cache_path):
            return cache_path

        # Generate TTS safely
        try:
            # gTTS sometimes fails if text is too long or malformed → split into chunks
            chunks = self._chunk_text(text, max_len=180)

            with open(cache_path, "wb") as outfile:
                for chunk in chunks:
                    try:
                        tts = gTTS(text=chunk, lang=Config.TTS_LANGUAGE, slow=Config.TTS_SLOW)
                        temp_path = cache_path + ".tmp"
                        tts.save(temp_path)

                        # Append chunk audio
                        with open(temp_path, "rb") as f:
                            outfile.write(f.read())

                        os.remove(temp_path)

                    except Exception as e:
                        print(f"[TTS] Error generating chunk: {e}")

            return cache_path

        except Exception as e:
            print(f"[TTS] Error generating TTS: {e}")
            return None

    # ------------------------------------------------------------
    # Split long text into gTTS-safe chunks
    # ------------------------------------------------------------
    def _chunk_text(self, text: str, max_len: int = 180):
        """
        gTTS does not support very long input. This function splits it safely.
        """
        words = text.split()
        chunks = []
        current = []

        for word in words:
            if len(" ".join(current + [word])) > max_len:
                chunks.append(" ".join(current))
                current = []
            current.append(word)

        if current:
            chunks.append(" ".join(current))

        return chunks

    # ------------------------------------------------------------
    # Clear audio cache
    # ------------------------------------------------------------
    def clear_cache(self):
        """Delete all cached MP3 files."""
        try:
            for f in os.listdir(self.cache_dir):
                if f.endswith(".mp3"):
                    os.remove(os.path.join(self.cache_dir, f))
        except Exception as e:
            print(f"[TTS] Error clearing cache: {e}")
