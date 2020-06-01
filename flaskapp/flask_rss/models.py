from datetime import datetime
from flask_rss import db
class Rss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), unique=True, nullable=False)
    link = db.Column(db.String(400), unique=True, nullable=False)
    summary = db.Column(db.String(400), nullable=False)
    published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    news = db.Column(db.String(20), nullable=False)
   
    def __repr__(self):
        return f"Title('{self.title}', '{self.link}', '{self.id}')"



