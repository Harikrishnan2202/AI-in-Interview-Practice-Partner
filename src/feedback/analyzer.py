"""
Feedback Analyzer – Generates structured interview feedback
compatible with google-generativeai==0.3.2
"""

import json
from src.llm.gemini_client import GeminiClient


class FeedbackAnalyzer:

    def __init__(self):
        # Use same model (gemini-pro)
        self.gemini = GeminiClient()

    def analyze_interview(self, role: str, transcript: str):
        """
        Analyze interview transcript and return structured feedback.
        Gemini output is parsed safely without requiring strict JSON.
        """

        prompt = f"""
You are an interview evaluation assistant.

Evaluate the following mock interview for a **{role}** role.

Provide structured results.

Return your feedback in EXACTLY the following JSON format:

{{
  "overall_score": <number 1-10>,
  "scores": {{
    "communication": <1-10>,
    "structure": <1-10>,
    "confidence": <1-10>,
    "content_quality": <1-10>,
    "role_fit": <1-10>
  }},
  "strengths": [
    "<strength 1>",
    "<strength 2>",
    "<strength 3>"
  ],
  "improvements": [
    "<improvement 1>",
    "<improvement 2>",
    "<improvement 3>"
  ],
  "best_answer": "<text>",
  "needs_work": "<text>",
  "summary": "<2-3 sentence summary>"
}}

Interview Transcript:
{transcript}

IMPORTANT RULES:
- Do NOT include explanations outside the JSON.
- Do NOT add any markdown.
- Return ONLY the JSON object.
"""

        # Gemini generates the JSON-like feedback
        raw_output = self.gemini.generate_content(prompt).strip()

        # Cleanup: remove accidental ``` or text before JSON
        cleaned = raw_output
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

        # Best-effort JSON parsing
        try:
            feedback = json.loads(cleaned)
        except Exception:
            # Fallback structure in case JSON fails
            feedback = {
                "overall_score": 7,
                "scores": {
                    "communication": 7,
                    "structure": 7,
                    "confidence": 7,
                    "content_quality": 7,
                    "role_fit": 7
                },
                "strengths": ["Good participation", "Clear answers", "Professional tone"],
                "improvements": ["More examples needed", "Use STAR format", "Give measurable results"],
                "best_answer": "N/A",
                "needs_work": "N/A",
                "summary": raw_output  # use raw text as summary fallback
            }

        return feedback
