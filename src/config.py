"""
Configuration settings for Interview Practice Partner
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # ✅ Correct models for google-generativeai >= 0.7.0
    GEMINI_MODEL = "models/gemini-2.5-flash"
    GEMINI_FEEDBACK_MODEL = "models/gemini-2.5-pro"

    GEMINI_TEMPERATURE = 0.7
    GEMINI_MAX_TOKENS = 2048

    MIN_QUESTIONS = 5
    MAX_QUESTIONS = 7

    INTERVIEW_ROLES = {
        "sales": "Sales Representative",
        "engineer": "Software Engineer",
        "retail": "Retail Associate",
        "behavioral": "General Behavioral Interview"
    }

    PERSONAS = {
        "normal": "Regular candidate behavior.",
        "confused": "Hesitant, unsure, asks clarifications.",
        "efficient": "Short, minimal answers.",
        "chatty": "Long, emotional answers.",
        "edge": "Unpredictable, broken English."
    }

    PERSONA_LIST = list(PERSONAS.keys())

    DATA_DIR = "data"
    INTERVIEWS_DIR = os.path.join(DATA_DIR, "interviews")
    AUDIO_CACHE_DIR = os.path.join(DATA_DIR, "audio_cache")

    PAGE_TITLE = "🎤 Interview Practice Partner"
    PAGE_ICON = "🎤"
    LAYOUT = "wide"

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in .env")
        os.makedirs(cls.INTERVIEWS_DIR, exist_ok=True)
        os.makedirs(cls.AUDIO_CACHE_DIR, exist_ok=True)
