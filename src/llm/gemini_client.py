import google.generativeai as genai
from src.config import Config

class GeminiClient:
    def __init__(self, model_name=None):
        if not Config.GEMINI_API_KEY:
            raise ValueError("Missing GEMINI_API_KEY")

        genai.configure(api_key=Config.GEMINI_API_KEY)

        self.model_name = model_name or Config.GEMINI_MODEL
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = None

    def start_chat(self, system_instruction=None):
        self.chat = self.model.start_chat(history=[])

        if system_instruction:
            try:
                self.chat.send_message(system_instruction)
            except Exception as e:
                print("System Instruction Error:", e)

    def send_message(self, message):
        if not self.chat:
            self.start_chat()

        try:
            response = self.chat.send_message(message)
            return response.text or ""
        except Exception as e:
            print("Gemini Error:", e)
            return "I'm having trouble generating a response."

    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text or ""
        except Exception as e:
            print("GenerateContent Error:", e)
            return "Error generating content."
