"""
System prompts and helper templates for Interview Practice Partner
"""

def get_system_instruction(role: str):
    """
    Short, compact, Gemini-0.7-safe system instruction.
    No multi-line blocks. No formatting that breaks chat.
    """

    base = (
        "You are a professional interviewer. "
        "Ask only one question at a time. "
        "Keep replies short, clear and professional. "
        "Do not ask multiple questions. "
        "Stay strictly in the interviewer role."
    )

    role_map = {
        "sales": (
            "You interview sales candidates. "
            "Ask about negotiation, targets, customer handling and communication."
        ),
        "engineer": (
            "You interview software engineers. "
            "Ask technical, debugging, problem-solving and teamwork questions."
        ),
        "retail": (
            "You interview retail associates. "
            "Ask about customer service, conflict handling and teamwork."
        ),
        "behavioral": (
            "You conduct behavioral interviews. "
            "Ask STAR-based questions about conflict, leadership and decisions."
        ),
    }

    return base + " " + role_map.get(role, "Ask professional interview questions.")


# Short encouragement prompts (Gemini-friendly)
ENCOURAGEMENT_PROMPTS = [
    "Take your time.",
    "You're doing well.",
    "Feel free to think it through.",
    "No rush.",
    "Continue when ready."
]

# Vague-answer probe prompts (one sentence only)
PROBE_PROMPTS = [
    "Can you share a specific example?",
    "What exactly was your role in that?",
    "What result did you achieve?",
    "What challenge did you face and how did you handle it?",
    "Can you explain that a bit more clearly?"
]
