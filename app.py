"""
Interview Practice Partner - Main Streamlit Application
"""

import streamlit as st
from datetime import datetime
import os

# Modules
from src.config import Config
from src.agents.interview_engine import InterviewEngine
from src.feedback.analyzer import FeedbackAnalyzer
from src.storage.manager import StorageManager
from src.voice.output_handler import TTSHandler
from src.voice.input_handler import STTHandler

# Page Setup
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.interview_active = False
    st.session_state.interview_engine = None
    st.session_state.messages = []
    st.session_state.session_id = None
    st.session_state.role = None
    st.session_state.input_mode = "text"
    st.session_state.start_time = None
    st.session_state.tts_enabled = True
    st.session_state.show_feedback = False
    st.session_state.feedback_data = None
    st.session_state.persona = "normal"

# Managers
storage = StorageManager()
tts_handler = TTSHandler()
stt_handler = STTHandler()


# ------------------------------
# Helper: API Key Validation
# ------------------------------
def validate_api_key():
    try:
        Config.validate()
        return True
    except ValueError as e:
        st.error(f"❌ {e}")
        st.info("Please create a `.env` file with:")
        st.code("GEMINI_API_KEY=your_api_key_here")
        return False


# ------------------------------
# Start Interview
# ------------------------------
def start_new_interview(role: str, persona: str, input_mode: str):
    st.session_state.role = role
    st.session_state.persona = persona
    st.session_state.input_mode = input_mode
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.start_time = datetime.now()
    st.session_state.messages = []
    st.session_state.show_feedback = False
    st.session_state.feedback_data = None

    st.session_state.interview_engine = InterviewEngine(role)

    opening = st.session_state.interview_engine.start_interview()
    st.session_state.messages.append({
        "role": "interviewer",
        "content": opening
    })

    st.session_state.interview_active = True


# ------------------------------
# End Interview & Generate Feedback
# ------------------------------
def end_interview():
    if st.session_state.interview_engine:
        with st.spinner("Analyzing your interview performance..."):
            analyzer = FeedbackAnalyzer()
            transcript = st.session_state.interview_engine.get_transcript()
            feedback = analyzer.analyze_interview(st.session_state.role, transcript)

            st.session_state.feedback_data = feedback
            st.session_state.show_feedback = True

            duration = (datetime.now() - st.session_state.start_time).total_seconds()
            data = {
                "session_id": st.session_state.session_id,
                "role": st.session_state.role,
                "persona": st.session_state.persona,
                "input_mode": st.session_state.input_mode,
                "timestamp_start": st.session_state.start_time.isoformat(),
                "duration_seconds": int(duration),
                "messages": st.session_state.messages,
                "feedback": feedback
            }
            storage.save_interview(data)

        st.session_state.interview_active = False


# ------------------------------
# Display Feedback
# ------------------------------
def display_feedback(feedback):
    st.header("📊 Interview Feedback")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric("Overall Score", f"{feedback.get('overall_score', 0)}/10")

    st.divider()

    st.subheader("Detailed Scores")
    scores = feedback.get("scores", {})
    col1, col2 = st.columns(2)

    with col1:
        for key in ["communication", "content_quality", "structure"]:
            value = scores.get(key, 0)
            st.progress(value / 10, text=f"{key.replace('_', ' ').title()}: {value}/10")

    with col2:
        for key in ["confidence", "role_fit"]:
            value = scores.get(key, 0)
            st.progress(value / 10, text=f"{key.replace('_', ' ').title()}: {value}/10")

    st.divider()

    st.subheader("💪 Strengths")
    for s in feedback.get("strengths", []):
        st.success("✓ " + s)

    st.subheader("📈 Areas for Improvement")
    for i in feedback.get("improvements", []):
        st.info("→ " + i)

    st.divider()

    st.subheader("🎯 Answer Analysis")
    st.write("**Best Answer:**")
    st.write(feedback.get("best_answer", "N/A"))

    st.write("**Needs Work:**")
    st.write(feedback.get("needs_work", "N/A"))

    st.divider()

    st.subheader("📝 Summary")
    st.write(feedback.get("summary", "N/A"))


# ------------------------------
# MAIN APP
# ------------------------------
def main():
    # Sidebar UI
    with st.sidebar:
        st.title("⚙️ Settings")

        st.markdown("### Select Persona")
        persona_choice = st.selectbox("Persona", Config.PERSONA_LIST)
        st.session_state.persona = persona_choice

        st.markdown("### Text-to-Speech")
        st.session_state.tts_enabled = st.checkbox("Enable Voice Output", value=True)

        st.divider()

        st.markdown("### Interview Stats")
        stats = storage.get_stats()
        st.metric("Total Interviews", stats.get("total_interviews", 0))
        st.metric("Average Score", f"{stats.get('average_score', 0)}/10")

        st.divider()
        if st.button("🗑️ Clear Audio Cache"):
            tts_handler.clear_cache()
            st.success("Audio cache cleared.")

    # API Key check
    if not validate_api_key():
        return

    # Home screen
    if not st.session_state.interview_active and not st.session_state.show_feedback:
        st.title("🎤 Interview Practice Partner")
        st.markdown("AI-powered interview simulation with **adaptive personas** and **intelligent feedback**.")

        st.divider()
        st.subheader("🎯 Choose Interview Type")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💼 Sales Interview"):
                start_new_interview("sales", st.session_state.persona, "text")
                st.rerun()

            if st.button("💻 Software Engineer"):
                start_new_interview("engineer", st.session_state.persona, "text")
                st.rerun()

        with col2:
            if st.button("🛍️ Retail Associate"):
                start_new_interview("retail", st.session_state.persona, "text")
                st.rerun()

            if st.button("📋 Behavioral Interview"):
                start_new_interview("behavioral", st.session_state.persona, "text")
                st.rerun()

        st.divider()
        st.subheader("📚 Previous Interviews")

        history = storage.list_interviews(limit=10)
        if history:
            for log in history:
                with st.expander(f"{log['role'].title()} — {log['timestamp'][:10]} (Score: {log.get('overall_score', 'N/A')})"):
                    if st.button("View Session", key=log['session_id']):
                        data = storage.load_interview(log['session_id'])
                        st.session_state.messages = data["messages"]
                        st.session_state.feedback_data = data["feedback"]
                        st.session_state.show_feedback = True
                        st.session_state.role = data["role"]
                        st.rerun()
        else:
            st.info("No previous sessions found.")

    # Interview Active
    elif st.session_state.interview_active:
        st.title(f"🎤 {Config.INTERVIEW_ROLES[st.session_state.role]}")
        st.subheader(f"Persona: **{st.session_state.persona}**")

        st.divider()

        # Chat display
        for msg in st.session_state.messages:
            if msg["role"] == "interviewer":
                with st.chat_message("assistant", avatar="👔"):
                    st.write(msg["content"])
            else:
                with st.chat_message("user", avatar="🙋"):
                    st.write(msg["content"])

        # User input
        if not st.session_state.interview_engine.is_complete():
            user_text = st.chat_input("Type your answer here...")

            if user_text:
                # Apply persona modifications
                persona_input = st.session_state.interview_engine.apply_persona(user_text, st.session_state.persona)

                st.session_state.messages.append({"role": "candidate", "content": persona_input})
                reply = st.session_state.interview_engine.process_answer(persona_input)

                st.session_state.messages.append({"role": "interviewer", "content": reply})
                st.rerun()

            if st.button("✅ End Interview & Get Feedback"):
                end_interview()
                st.rerun()
        else:
            st.success("Interview completed!")
            if st.button("📊 View Feedback"):
                end_interview()
                st.rerun()

    # Feedback Screen
    elif st.session_state.show_feedback:
        st.title("📊 Interview Feedback")
        display_feedback(st.session_state.feedback_data)

        st.divider()
        if st.button("🔄 Start New Interview"):
            st.session_state.show_feedback = False
            st.session_state.feedback_data = None
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
