from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class DistortionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))                  
    count = db.Column(db.Integer, default=1)

class DistortedPhrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pattern = db.Column(db.String(100))
    phrase = db.Column(db.String(300))
    count = db.Column(db.Integer, default=1)