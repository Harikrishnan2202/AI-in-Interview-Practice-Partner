# Quick Start Guide 🚀

## Get Started in 3 Minutes!

### Step 1: Add your API Key
Create a `.env` file in the project root:
```bash
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### Step 2: Activate Environment & Install (if not done already)
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Interview

1. Click one of the four interview buttons (try "Sales Interview")
2. Read the opening question  
3. Type your answer in the chat box at the bottom
4. Continue for 5-7 questions
5. Click "End Interview & Get Feedback"
6. View your detailed feedback!

## Testing Edge Cases

**Confused User:**
- Answer first question with: "I'm not sure what you're asking"
- Watch system provide guidance

**Efficient User:**
- Give short, direct answers
- See quick pace maintained

**Chatty User:**
- Give very long, detailed answers with tangents
- Observe gentle redirection

## Tips for Demo Video

1. **Show UI**: Start by showing the welcome screen
2. **Pick Role**: Select "Software Engineer" or "Sales"
3. **Good Flow**: Answer 3-4 questions naturally
4. **Show Feedback**: Complete interview and show detailed scores
5. **Show History**: Go back to home and view past interviews
6. **Test Persona**: Do a second interview as "confused user"
7. **Highlight**: Point out adaptive AI behavior

## Troubleshooting

**Can't find .env file?**
```bash
cd /Users/tanmay.khanna@grofers.com/Desktop/Practice/interview-practice-partner
ls -la .env
```

**Dependencies failing?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Streamlit not found?**
```bash
source venv/bin/activate
which streamlit
```

---

Need more help? Check the full README.md!
