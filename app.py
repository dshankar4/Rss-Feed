from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
import feedparser

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Rss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), unique=True, nullable=False)
    link = db.Column(db.String(400), unique=True, nullable=False)
    summary = db.Column(db.String(400), nullable=False)
    published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    news = db.Column(db.String(20), nullable=False)
   
    def __repr__(self):
        return'<Task %r>' % self.id

hindustan_url = "https://www.hindustantimes.com/rss/topnews/rssfeed.xml"
timesofindia_url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
feed1 = feedparser.parse(hindustan_url)
feed2 = feedparser.parse(timesofindia_url)
@app.route('/', methods=['POST', 'GET'])
def index():
    db.drop_all()
    for i in range(0,len(feed1.entries)):
        entry=feed1.entries[i]
        db.create_all()
        rssfeed=Rss(title=entry.title,link=entry.link,summary=entry.summary,news="hindustan")
        db.session.add(rssfeed)
        db.session.commit()

    for j in range(0,len(feed2.entries)):
        entry=feed2.entries[j]
        db.create_all()
        rssfeed=Rss(title=entry.title,link=entry.link,summary=entry.summary,news="timesofindia")
        db.session.add(rssfeed)
        db.session.commit()
    contents = Rss.query.order_by(Rss.published).all()
    return render_template('index.html')

@app.route('/hindustan')
def hindustan():
    rss = Rss.query.filter_by(news="hindustan").all()
    return render_template('index.html', contents=rss)

@app.route('/timesofindia')
def timesofindia():
    rss = Rss.query.filter_by(news="timesofindia").all()
    return render_template('index.html', contents=rss)

if __name__ == '__main__':
    app.run(debug=True)

