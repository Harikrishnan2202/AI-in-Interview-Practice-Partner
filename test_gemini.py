import google.generativeai as genai
from src.config import Config

print("🔍 Testing Gemini API...")

genai.configure(api_key=Config.GEMINI_API_KEY)

MODEL = "gemini-1.5-flash"

try:
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content("Say hi in one short sentence.")
    print("✅ Response:", response.text)
except Exception as e:
    print("❌ ERROR:", e)
import google.generativeai as genai
from src.config import Config

print("🔍 Testing Gemini API...")

genai.configure(api_key=Config.GEMINI_API_KEY)

MODEL = "gemini-1.5-flash"

try:
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content("Say hi in one short sentence.")
    print("✅ Response:", response.text)
except Exception as e:
    print("❌ ERROR:", e)
