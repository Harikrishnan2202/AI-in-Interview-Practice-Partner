import google.generativeai as genai
from src.config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

print("\n📌 Available Models:\n")
for m in genai.list_models():
    print("-", m.name)
