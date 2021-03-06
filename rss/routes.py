from flask import Flask, render_template, url_for, flash, redirect, request
import feedparser
from dateutil import parser as date_parser
from rss import app
import asyncio
# from rss import db, bcrypt
from rss import bcrypt
from rss.database import addUser, validateUser, addFeedUrl, fetchrss, Feedfetch, getRssbyId, incrementLikes, incrementDislikes, editFeed, getRssbyName
global admin
q=fetchrss()
rssfeed= Feedfetch()
@app.route('/', methods=['POST', 'GET'])
def index(): 
    return redirect(url_for('login'))
def home():
    return render_template('index.html', title='Rss Feed',rss=rssfeed)

@app.route('/page/<string:id>')
def page(id):
    selectedFeed=getRssbyId(id)
    return render_template('index.html', rss=selectedFeed)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        user=addUser(username,password) 
        return render_template('index.html', title='Rss Feed',rss=rssfeed)
    return render_template('register.html', title='Login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        user=validateUser(username,password)
        global admin
        if user == -1:
            return render_template('login.html')
        elif user == 1:
            admin=1
            return render_template('admin_dashboard.html')
        else:
            admin=0
            return redirect(url_for('allCategories'))
    return render_template('login.html', title='Login')

@app.route("/rss",methods=['POST'])
def rss():
    print(request.form['rss_feed'])
    value = addFeedUrl(request.form['rss_feed'])
    return render_template('admin_dashboard.html')

@app.route("/allCategories")
def allCategories():
    return render_template('index.html', title='Rss Feed',rss=rssfeed,admin=admin)

@app.route("/countLikes",methods=['POST'])
def countLikes():
    rssfeed = incrementLikes(request.json['title'])
    return redirect(url_for('allCategories',rssfeed=rssfeed))

@app.route("/countDislikes",methods=['POST'])
def countDislikes():
    rssfeed = incrementDislikes(request.json['title'])
    return redirect(url_for('allCategories',rssfeed=rssfeed))

@app.route("/updateFeed",methods=['POST'])
def updateFeed():
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        id = request.form['hidtitle']
        rssfeed = editFeed(title,summary,id)
        return render_template('index.html', title='Rss Feed',rss=rssfeed,admin=1)


@app.route('/getFeeds/<string:name>')
def getFeeds(name):
    getfeed=getRssbyName(name)
    return render_template('index.html', rss=getfeed)





