from flask import render_template, url_for, flash, redirect
from flask_rss import app
from flask_rss.models import Rss
from flask_rss import db
import feedparser
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






