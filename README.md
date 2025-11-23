🎤 AI Interview Practice Partner

A smart, adaptive mock-interview platform built using Streamlit, Google Gemini AI, and agentic workflows.
The system simulates realistic interview conversations across multiple job domains and offers personalized feedback, helping candidates practice and improve their interview performance.

🚀 Overview

The AI Interview Practice Partner is designed to act like a professional interviewer. It can:

Conduct role-specific interview conversations

Ask adaptive questions based on your answers

Encourage you if you appear nervous

Probe deeper when your response is vague

Review the complete interview

Generate detailed feedback with structured scoring

This makes it ideal for mock interviews, practice sessions, and educational or career-enhancement purposes.

🧠 Core Capabilities
🎙️ Real Interview Simulation

Supports multiple interview types:

Software Engineering

Sales

Retail

Behavioral (STAR Method)

Logical question progression

Adaptive follow-ups and probing

🗣️ Voice & Text Input

Submit answers via:

Text typing

Voice (with optional STT support)

🔊 Voice Output (TTS)

Interviewer questions can be spoken aloud using gTTS

Efficient audio caching ensures smooth playback

📊 Automatic Feedback & Scoring

At the end of the interview, the AI evaluates:

Communication

Content quality

Structure of responses

Confidence

Fit for the selected role

A JSON-based evaluation includes:

Strengths

Areas for improvement

Best answer

Weakest answer

Overall feedback summary

🏗️ Project Architecture
interview-practice-partner/
│── app.py                → Main Streamlit application  
│── .env                 → API keys (user-created)
│── requirements.txt     → Project dependencies
│── data/
│     ├── audio_cache/   → TTS cached audio  
│     └── interviews/    → Saved interview sessions  
│── src/
      ├── config.py                     → Central configuration
      ├── agents/
      │      └── interview_engine.py    → Conversation logic & flow
      ├── llm/
      │      ├── gemini_client.py       → Gemini API wrapper
      │      └── prompts.py             → System & feedback prompts
      ├── feedback/
      │      └── analyzer.py            → Interview feedback generator
      ├── voice/
      │      ├── input_handler.py       → Speech-to-text utilities
      │      └── output_handler.py      → Text-to-speech handler
      └── storage/
             └── manager.py             → Stores and retrieves interviews  

⚙️ Setup Instructions
1️⃣ Clone the project
git clone https://github.com/saranyapsmv/interview-practice-partner.git
cd interview-practice-partner

2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure the .env

Create a .env file in the root folder:

GEMINI_API_KEY=your_api_key_here


Replace with your Google Gemini API key.

5️⃣ Run the app
streamlit run app.py

🖼️ How to Use the Application
🏠 Home Screen

Choose your interview type

Enable/disable voice output

View previous interview history

💬 Interview Session

The interviewer asks 5–7 questions

You respond via chat input or microphone

The system adapts questions based on:

Nervousness

Vague answers

Topic relevance

📝 Feedback Screen

Shows:

Overall score

Category-wise scores

Strengths

Improvements

Best & worst answers

Full transcript

All sessions are stored automatically.

💡 Key Features Under the Hood
🔄 Adaptive Question Flow

The engine evaluates your answers and determines whether to:

Ask a deeper probing question

Provide encouragement

Move to next topic

End the interview

🧩 LLM-Driven Analysis

Feedback uses:

gemini-1.5-flash for interview flow

gemini-1.5-pro for deep evaluation

🗃️ Structured History Storage

Every interview is saved as a JSON file containing:

Timestamp

Questions asked

User answers

AI feedback

Duration

🔧 Tech                     Stack
   Layer	                  Technology
  Frontend                 Streamlit
  AI Model	            Google Gemini 1.5
   Voice          	gTTS & SpeechRecognition
  Storage	        Local JSON session storage
 Backend Framework	       Python
🧩 Possible Future Enhancements

Candidate resume upload → tailored interview questions

Multi-round interviews

Dashboard for long-term performance tracking

HR-style scoring rubric customization

Integration with job portals and portfolio platforms

📜 License

This project is released under the MIT License.

🙌 Contributors

Created & enhanced by
SARANYA P