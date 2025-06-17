
# MindMend AI — AI-Powered Cognitive Distortion Journal

Journaling is shown to be one of the most powerful tools that can be used to regulate mental health and is backed by cognitive behavioral therapy (CBT) research. Writing about your thoughts and emotions can help regulate mood, reduce anxiety, and most importantly identify harmful thinking patterns. The issue is that when re-reading journal entries, most people are not familiar with the clinically-identified cognitive distortions(harmful thinking patterns) and much less are able to accurately identify them in their own writing. This is the gap that MindMend AI aims to fill.

MindMend AI is a Flask-based journaling web app that uses GPT-4 to detect cognitive distortions in journal entries. It provides CBT-style feedback, tracks recurring thought patterns over time, and displays reflection prompts to support self-awareness and therapeutic conversations.

---

##  Features

- 💬 **Journal Entry Submission** – Users can write free-form text entries to express their thoughts and emotions.
- 🤖 **AI-Powered Feedback** – GPT-4 analyzes entries for 10+ cognitive distortions (e.g., catastrophizing, mind reading) and returns labeled feedback.
- 📊 **Summary Dashboard** – Tracks and visualizes the most common distortion types and phrases across all entries.
- 🧭 **Reflection Prompts** – Offers targeted, distortion-specific CBT reflection questions to encourage deeper thinking.
- 🗂 **Past Entries** – Browse previous journal entries and corresponding AI feedback.
- 🕒 **Timestamped Entries** – Each submission is saved with the date and time for easy review.

---

## Tech Stack

- **Frontend**: HTML, CSS (Jinja templates)
- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **AI Model**: OpenAI GPT-4 via `openai` Python SDK
- **Environment Variables**: Used to securely store the OpenAI API key

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/reflectify.git
cd reflectify
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the root folder:

```env
OPENAI_API_KEY=your-openai-api-key
```

### 5. Run the App

```bash
flask run
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 📁 Project Structure

```
/MindMendAI/
│
├── app.py                   # Main Flask app
├── models.py                # SQLAlchemy database models
├── prompts.py               # GPT feedback + distortion detection logic
├── reflection_prompts.py    # Dictionary of CBT reflection prompts
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── entries.html
│   └── summary.html
├── static/                  # (Optional) CSS or image assets
├── journal.db               # SQLite database (created on first run)
├── .env                     # Environment variables (excluded from Git)
└── requirements.txt         # Python dependencies
```

---

## Distortion Types Detected

- Overgeneralization  
- Catastrophizing  
- Mind Reading  
- All-or-Nothing Thinking  
- Mental Filtering  
- Emotional Reasoning  
- Labeling  
- Discounting the Positive  
- Personalization  
- "Should" Statements  

---

## Security Notes

- API keys are managed through environment variables using `.env`
- Do **not** hardcode secrets in your codebase
- Use `python-dotenv` for local development key loading

---


## ***Important Note***

This app is designed to support mental health reflection, not replace therapy. 

---


