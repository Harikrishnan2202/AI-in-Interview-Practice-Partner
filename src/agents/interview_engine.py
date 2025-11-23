"""
Core interview engine - final stable version
Compatible with google-generativeai==0.3.2
"""

import random
from src.llm.gemini_client import GeminiClient
from src.llm.prompts import get_system_instruction, ENCOURAGEMENT_PROMPTS
from src.config import Config


class InterviewEngine:

    def __init__(self, role: str):
        self.role = role
        self.gemini = GeminiClient()
        self.question_count = 0
        self.messages = []

        # FINAL SAFE SYSTEM INSTRUCTION
        system_instruction = (
            get_system_instruction(role)
            + "\nAsk ONLY ONE question in your reply."
            + "\nDo NOT ask multiple questions."
            + "\nKeep replies 1–3 sentences maximum."
        )

        self.gemini.start_chat(system_instruction)

    # ------------ PERSONA FILTER -----------------
    def apply_persona(self, text: str, persona: str) -> str:
        t = text.strip()

        if persona == "confused":
            return f"Umm… I'm not fully sure but {t}?"

        if persona == "efficient":
            return " ".join(t.split()[:6])

        if persona == "chatty":
            return f"{t}. Actually that reminds me of something interesting…"

        if persona == "edge":
            return t + " ?? maybe idk"

        return t

    # ------------ START INTERVIEW ---------------
    def start_interview(self):
        prompt = (
            "Greet the candidate briefly. Then ask ONE question: "
            "'Tell me about yourself.'"
        )

        reply = self._safe_llm(prompt)
        self._save_interviewer(reply)
        self.question_count += 1
        return reply

    # ------------ ANALYZE ANSWER ----------------
    def analyze(self, answer: str):
        words = answer.lower().split()
        return {
            "vague": len(words) < 8,
            "uncertain": any(w in words for w in ["maybe", "um", "idk"]),
        }

    # ------------ PROCESS ANSWER ----------------
    def process_answer(self, answer: str) -> str:
        self._save_candidate(answer)
        analysis = self.analyze(answer)

        if analysis["vague"] and self.question_count < Config.MAX_QUESTIONS:
            return self._probe()

        if self.question_count >= Config.MAX_QUESTIONS:
            return self._closing()

        return self._next_question(analysis)

    # ------------ PROBE FOLLOW-UP ---------------
    def _probe(self):
        prompt = (
            "Ask ONE probing follow-up question requesting clarity "
            "or a specific example."
        )
        reply = self._safe_llm(prompt)
        self._save_interviewer(reply)
        return reply

    # ------------ NEXT QUESTION -----------------
    def _next_question(self, analysis):
        encouragement = random.choice(ENCOURAGEMENT_PROMPTS) if analysis["uncertain"] else ""

        prompt = (
            f"Ask ONE next interview question for the role: {self.role}. "
            "Keep it short, job-related, and professional. "
            f"{encouragement}"
        )

        reply = self._safe_llm(prompt)
        self._save_interviewer(reply)
        self.question_count += 1
        return reply

    # ------------ CLOSING -----------------------
    def _closing(self):
        prompt = (
            "Thank the candidate and ask ONE final question: "
            "'Do you have any questions for me?'"
        )
        reply = self._safe_llm(prompt)
        self._save_interviewer(reply)
        self.question_count += 1
        return reply

    # ------------ SAFE LLM CALL -----------------
    def _safe_llm(self, prompt):
        reply = self.gemini.send_message(prompt)
        if not reply or reply.strip() == "":
            reply = "Could you explain that more clearly?"
        return reply

    # ------------ COMPLETION CHECK ---------------
    def is_complete(self):
        return self.question_count >= Config.MAX_QUESTIONS + 1

    # ------------ TRANSCRIPT --------------------
    def get_transcript(self):
        return "\n".join([
            f"{m['role'].capitalize()}: {m['content']}"
            for m in self.messages
        ])

    def _save_interviewer(self, text):
        self.messages.append({"role": "interviewer", "content": text})

    def _save_candidate(self, text):
        self.messages.append({"role": "candidate", "content": text})
    