from flask import Flask, render_template, request, redirect
from models import db, JournalEntry
from prompts import generate_feedback, log_distortion
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form["entry"]
        feedback = generate_feedback(content)
        new_entry = JournalEntry(content=content, feedback=feedback)
        db.session.add(new_entry)
        db.session.commit()
        log_distortion(feedback)
        return render_template("result.html", entry=content, feedback=feedback, date=new_entry.date)
    return render_template("index.html")

@app.route("/entries")
def show_entries():
    entries = JournalEntry.query.order_by(JournalEntry.id.desc()).all()
    return render_template("entries.html", entries=entries)

@app.route("/summary")
def summary():
    from models import DistortionType, DistortedPhrase
    from reflection_prompts import reflection_prompts
    types = DistortionType.query.order_by(DistortionType.count.desc()).all()
    phrases = DistortedPhrase.query.order_by(DistortedPhrase.count.desc()).all()
    return render_template("summary.html", types=types, phrases=phrases, reflection_prompts=reflection_prompts)

if __name__ == "__main__":
    app.run(debug=True)