"""
Interview State Definitions for Future LangGraph Integration
This file models the full state required for a fully adaptive interview agent.
"""

from typing import TypedDict, List, Dict, Optional, Annotated
import operator
from datetime import datetime


class InterviewState(TypedDict, total=False):
    """
    Central interview state object.
    Stored and passed between nodes for LangGraph or advanced orchestration.
    """

    # -------------------------------------------
    # Core identity
    # -------------------------------------------
    role: str                     # "sales", "engineer", "retail", "behavioral"
    persona: str                  # "normal", "confused", "efficient", "chatty", "edge"
    input_mode: str               # "text" or "voice"

    # -------------------------------------------
    # Conversation tracking
    # -------------------------------------------
    messages: Annotated[List[Dict[str, str]], operator.add]  # Full conversation history
    question_count: int           # Total questions asked
    last_answer: Optional[str]    # Last user answer
    last_answer_quality: Optional[str]  # "good", "vague", "off_topic", "detailed"

    # -------------------------------------------
    # Persona & user behavior inference
    # -------------------------------------------
    user_profile: Dict[str, str]  # { "experience_level": "junior/mid/senior", ... }
    topics_covered: List[str]     # Track which role topics were asked
    needs_probing: bool           # Should interviewer probe?
    needs_redirection: bool       # Answer was off-topic?
    needs_encouragement: bool     # Candidate seemed nervous?

    # -------------------------------------------
    # Adaptive scoring & tracking
    # -------------------------------------------
    answer_quality_scores: List[int]   # List of 1–5 quality scores for each answer

    # -------------------------------------------
    # Flow control
    # -------------------------------------------
    is_complete: bool             # Interview finished?
    current_state: str            # Node can use this for debugging (optional)
    session_id: str               # Unique interview ID
    timestamp_start: str          # ISO timestamp
    timestamp_end: Optional[str]  # Filled on completion

    # -------------------------------------------
    # Pending input for multi-step logic (optional)
    # -------------------------------------------
    pending_user_input: Optional[str]


# ------------------------------------------------------
# State Initialization
# ------------------------------------------------------

def create_initial_state(
    role: str,
    persona: str,
    input_mode: str,
    session_id: str,
    timestamp: Optional[str] = None
) -> InterviewState:
    """
    Generate a clean initial interview state.

    Args:
        role: Interview category
        persona: User behavior model
        input_mode: "text" or "voice"
        session_id: Unique interview ID
        timestamp: Start timestamp (default = now)

    Returns:
        InterviewState object
    """

    if timestamp is None:
        timestamp = datetime.now().isoformat()

    return InterviewState(
        # Core
        role=role,
        persona=persona,
        input_mode=input_mode,

        # Conversation
        messages=[],
        question_count=0,
        last_answer=None,
        last_answer_quality=None,

        # Behavior inference
        user_profile={
            "experience_level": "unknown",
            "communication_style": "unknown",
            "nervousness": "unknown"
        },
        topics_covered=[],
        needs_probing=False,
        needs_redirection=False,
        needs_encouragement=False,

        # Scoring
        answer_quality_scores=[],

        # Flow
        current_state="start",
        is_complete=False,
        session_id=session_id,
        timestamp_start=timestamp,
        timestamp_end=None,

        # Pending input
        pending_user_input=None
    )
