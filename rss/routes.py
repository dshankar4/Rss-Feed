from flask import Flask, render_template, url_for, flash, redirect
import feedparser
from dateutil import parser as date_parser
from rss import app
from sqlalchemy import desc
from rss.models import Rss, User
from rss import db, bcrypt
from rss.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

hindustan_url = "https://www.hindustantimes.com/rss/topnews/rssfeed.xml"
businessStandard_url = "https://www.business-standard.com/rss/latest.rss"
feed1 = feedparser.parse(hindustan_url)
feed2 = feedparser.parse(businessStandard_url)
@app.route('/', methods=['POST', 'GET'])
def index():
    db.drop_all()
    for i in range(0,len(feed1.entries)):
        entry=feed1.entries[i]
        db.create_all()
        date=date_parser.parse(entry.published)
        rssfeed=Rss(title=entry.title,link=entry.link,summary=entry.summary,img_path=entry.media_content[0]['url'],news="hindustan",published=date)
        db.session.add(rssfeed)
        db.session.commit()

    for j in range(0,len(feed2.entries)):
        entry=feed2.entries[j]
        db.create_all()
        date=date_parser.parse(entry.published)
        rssfeed=Rss(title=entry.title,link=entry.link,summary=entry.summary,img_path=entry.media_thumbnail[0]['url'] if "media_thumbnail" in entry.keys() else "default.jpg",news="businessStandard",published=date)
        db.session.add(rssfeed)
        db.session.commit()
    contents = Rss.query.order_by(Rss.published).all()
    return render_template('index.html')

@app.route('/hindustan')
def hindustan():
    rss = Rss.query.order_by(desc(Rss.published)).filter_by(news="hindustan").all()
    return render_template('index.html', contents=rss, title="Business Standard")

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))