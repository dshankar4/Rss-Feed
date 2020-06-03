from datetime import datetime
from dateutil import parser as date_parser
from rss import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Rss(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), nullable=False)
    link = db.Column(db.String(400), unique=True, nullable=False)
    summary = db.Column(db.String(400), nullable=False)
    img_path = db.Column(db.String(400), nullable=False, default="default.jpg")
    published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    news = db.Column(db.String(20), nullable=False)
   
    def __repr__(self):
        return'<Task %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

