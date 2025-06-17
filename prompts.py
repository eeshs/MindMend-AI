import openai
from models import db, DistortionType, DistortedPhrase
import re
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DISTORTION_RESOURCES = {
    "Overgeneralization": {
        "video": "https://www.youtube.com/watch?v=qzJrM5xo5B0",
        "learn": "https://cogbtherapy.com/cbt-blog/cognitive-distortions-overgeneralizing"
    },
    "Catastrophizing": {
        "video": "https://www.youtube.com/watch?v=b4pP6HyXRMI",
        "learn": "https://positivepsychology.com/catastrophizing/"
    },
    "Mind Reading": {
        "video": "https://www.youtube.com/watch?v=-NVTv_CMyNM",
        "learn": "https://cogbtherapy.com/cbt-blog/common-cognitive-distortions-mind-reading"
    },
    "All-or-Nothing Thinking": {
        "video": "https://www.youtube.com/watch?v=jkafQlNX3eE",
        "learn": "https://psychcentral.com/lib/cognitive-distortions-negative-thinking"
    },
    "Mental Filtering": {
        "video": "https://www.youtube.com/watch?v=yxyuzF4Hq3Y",
        "learn": "https://psychcentral.com/lib/mental-filtering"
    },
    "Emotional Reasoning": {
        "video": "https://www.youtube.com/watch?v=YBzvkgARehg",
        "learn": "https://nesslabs.com/emotional-reasoning"
    },
    "Labeling": {
        "video": "https://www.youtube.com/watch?v=zRnlVkYS5ko",
        "learn": "https://positivepsychology.com/cognitive-distortions/#labeling"
    },
    "Discounting the Positive": {
        "video": "https://www.youtube.com/watch?v=xdPByl2LjzY",
        "learn": "https://therapyinanutshell.com/cognitive-distortion-of-discounting-the-positive/"
    },
    "Personalization": {
        "video": "https://www.youtube.com/watch?v=JQTAFEZIHMA",
        "learn": "https://cpdonline.co.uk/knowledge-base/mental-health/personalisation"
    },
    "Should Statements": {
        "video": "https://www.youtube.com/watch?v=xfjGJcIWUJs",
        "learn": "https://psychcentral.com/lib/should-statements"
    }
}


def generate_feedback(journal_text):
    prompt = (
        "You are a helpful CBT assistant. Analyze this journal entry. "
        "Identify any of the following cognitive distortions in the entry: overgeneralization, catastrophizing, mind reading, all-or-nothing, mental filtering, emotional reasoning, labeling, discounting the positive, personalization, and should statements."
        "For each distortion, quote a sentence that shows it, explain the pattern in plain English, give 2 similar examples, "
        "and format the feedback like this HTML-friendly structure:\n\n"
        "Detected Pattern: \"Catastrophizing\"\n"
        "“I’ll never recover from this.”\n\n"
        "— This is when the mind jumps to the worst-case scenario.\n\n"
        "Similar examples:\n• “This is a total disaster.”\n• “Everything is ruined.”\n\n"
        "[🎥 Watch: How to stop catastrophizing]\n"
        "[📘 Learn more]"

        f"\n\nJournal Entry:\n{journal_text}\n\n"
        "Format it exactly like the structure above. HTML line breaks are okay."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        feedback = response.choices[0].message.content
    
    
        # Inject resource links based on detected pattern
        pattern_blocks = re.findall(
            r'Detected Pattern:\s*"(.+?)"\s*\n“(.+?)”\s*\n—\s*(.+?)(?=\n\n|$)', 
            feedback, 
            flags=re.DOTALL
        )
        rendered_blocks = []
        for pattern, quote, explanation in pattern_blocks:
            html_block = (
                f'<strong>Detected Pattern:</strong> "{pattern}"<br>'
                f'“{quote}”<br>'
                f'— {explanation}<br>'
            )

            resources = DISTORTION_RESOURCES.get(pattern)
            if resources:
                html_block += (
                    f'[🎥 <a href="{resources["video"]}" target="_blank">Watch</a>] '
                    f'[📘 <a href="{resources["learn"]}" target="_blank">Learn more</a>]'
                )

            rendered_blocks.append(html_block)

        return "<br><br>".join(rendered_blocks)
    
    except Exception as e:
        return f"Error generating feedback: {e}"

def log_distortion(feedback):
    try:
        patterns = re.findall(r'<strong>Detected Pattern:</strong>\s*"(.+?)"', feedback)
        phrases = re.findall(r'“(.+?)”', feedback)
        for pattern, phrase in zip(patterns, phrases):
            # Update distortion type count
            existing_type = DistortionType.query.filter_by(name=pattern).first()
            if existing_type:
                existing_type.count += 1
            else:
                db.session.add(DistortionType(name=pattern, count=1))

            # Update distorted phrase count
            existing_phrase = DistortedPhrase.query.filter_by(pattern=pattern, phrase=phrase).first()
            if existing_phrase:
                existing_phrase.count += 1
            else:
                db.session.add(DistortedPhrase(pattern=pattern, phrase=phrase, count=1))

        db.session.commit()
    except Exception as e:
        print(f"Logging error: {e}")