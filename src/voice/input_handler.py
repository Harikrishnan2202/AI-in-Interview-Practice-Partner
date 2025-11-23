"""
Speech-to-text input handler (STT) using SpeechRecognition.
Improved version with better error handling & noise adjustment.
"""

import os

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None


class STTHandler:
    """Handles speech-to-text conversion safely."""

    def __init__(self):
        self.available = SPEECH_RECOGNITION_AVAILABLE
        self.recognizer = sr.Recognizer() if self.available else None

        if self.available:
            # More stable sensitivity for background noise
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True

    # ------------------------------------------------------------
    # Check availability
    # ------------------------------------------------------------
    def is_available(self) -> bool:
        return self.available

    # ------------------------------------------------------------
    # Live microphone listening
    # ------------------------------------------------------------
    def listen_from_microphone(self, timeout: int = 10, phrase_time_limit: int = 15) -> str:
        """
        Listen to live microphone input and convert speech to text.

        Returns:
            str or None
        """
        if not self.available:
            return None

        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")

                # Auto-adjust for noise
                try:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                except:
                    pass

                # Listen for speech
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                # Convert to text using Google free STT API
                text = self.recognizer.recognize_google(audio)
                return text

        except sr.WaitTimeoutError:
            print("[STT] Listening timed out.")
            return None
        except sr.UnknownValueError:
            print("[STT] Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"[STT] API Request Error: {e}")
            return None
        except Exception as e:
            print(f"[STT] Unexpected error: {e}")
            return None

    # ------------------------------------------------------------
    # Transcribe audio file
    # ------------------------------------------------------------
    def transcribe_audio_file(self, audio_file_path: str) -> str:
        """
        Convert an audio file into text.

        Returns:
            str or None
        """
        if not self.available:
            return None

        if not os.path.exists(audio_file_path):
            print("[STT] Audio file not found.")
            return None

        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except Exception as e:
            print(f"[STT] Error transcribing file: {e}")
            return None
