from flask import Flask, render_template, url_for, flash, redirect, request
import feedparser
from dateutil import parser as date_parser
from rss import app
from sqlalchemy import desc
from rss.models import Rss, User, Feed
from rss import db, bcrypt
from rss.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

hindustan_url = "https://www.hindustantimes.com/rss/topnews/rssfeed.xml"
businessStandard_url = "https://www.news18.com/rss/india.xml"
feed1 = feedparser.parse(hindustan_url)
feed2 = feedparser.parse(businessStandard_url)
@app.route('/', methods=['POST', 'GET'])
def index():
    db.create_all()
    url=Feed.query.order_by(Feed.id).all()
    db.drop_all()
    for l in range(0,len(url)):
        feed1 = feedparser.parse(url[l].link)
        for i in range(0,len(feed1.entries)):
            entry=feed1.entries[i]
            db.create_all()
            date=date_parser.parse(entry.published)
            if "media_content" in entry.keys():
                rssfeed=Rss(title=entry.title,link=entry.link,summary=entry.summary,img_path=entry.media_content[0]['url'],news="hindustan",published=date)
            else:
                 rssfeed=Rss(title=entry.title,link=entry.link,summary=entry.summary,img_path="default.jpg",news="hindustan",published=date) 
            db.session.add(rssfeed)
            db.session.commit()

    # for j in range(0,len(feed2.entries)):
    #     entry=feed2.entries[j]
    #     date=date_parser.parse(entry.published)
    #     rssfeed=Rss(title=entry.title,link=entry.link,summary=entry.summary,img_path=entry.media_thumbnail[0]['url'] if "media_thumbnail" in entry.keys() else "default.jpg",news="businessStandard",published=date)
    #     db.session.add(rssfeed)
    #     db.session.commit()
    contents = Rss.query.order_by(Rss.published).all()
    return render_template('index.html')

@app.route('/hindustan')
def hindustan():
    rss = Rss.query.order_by(desc(Rss.published)).filter_by(news="hindustan").all()
    return render_template('index.html', contents=rss, title="Hindustan Times")
@app.route('/businessStandard')
def businessStandard():
    rss = Rss.query.filter_by(news="businessStandard").all()
    return render_template('index.html', contents=rss, title="Business Standard")

@app.route('/page/<string:id>')
def page(id):
    rss = Rss.query.filter_by(id=int(id)).all()
    return render_template('index.html', contents=rss, title=rss[0].news)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.create_all()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return render_template('admin_dashboard.html')
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db.create_all()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return render_template('admin_dashboard.html')
        else:
            flash(f'Incorrect email and password!', 'danger')
            return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    return redirect(url_for('index'))

@app.route("/rss",methods=['POST'])
def rss():
    value = Feed(link=request.form['rss_feed'])
    db.session.add(value)
    db.session.commit()
    return request.form['rss_feed']