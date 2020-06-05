import sqlite3
from flask import flash
import feedparser
from dateutil import parser as date_parser
def addUser(username,password):
    conn = sqlite3.connect('Rss.db')
    c= conn.cursor()
    c.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Users' """)
    if c.fetchone()[0]!=    1 : 
        flag=1
        c.execute("""CREATE TABLE Users (id INTEGER,username TEXT,password TEXT)""")
        c.execute("INSERT INTO Users VALUES (:id, :username,:password)",{'id':1,'username':'admin','password':'admin'})
    else:
        flag=0
        c.execute("INSERT INTO Users VALUES (:id, :username,:password)",{'id':0, 'username':username,'password':password})
    conn.commit()
    conn.close()
    return flag

def validateUser(username,password):
    print("inside validation")
    conn = sqlite3.connect('Rss.db')
    c = conn.cursor()
    c.execute(" SELECT * FROM Users WHERE username = (:username)",{'username':username})
    result=c.fetchall()
    if len(result)==0 :
        flash("Incorrect Password  !")
        return -1
    conn.commit()
    conn.close()
    return result[0][0]

def addFeedUrl(feed):
    conn = sqlite3.connect('Rss.db')
    c= conn.cursor()
    c.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Feedurl' """)
    if c.fetchone()[0]!=1 : 
        c.execute("CREATE TABLE Feedurl (link VARCHAR,time )")
        c.execute("INSERT INTO Feedurl VALUES (:link)",{'link':feed})
    else:
        c.execute("INSERT INTO Feedurl VALUES (:link)",{'link':feed})
    conn.commit()
    conn.close()
    return 1

def feedparse(links):
    conn = sqlite3.connect('Rss.db')
    c= conn.cursor()
    news_type=["topnews","lifestyle","india","business","sports","world","politics","tech"]
    c.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Feed' """)
    if c.fetchone()[0]!=1 :
        c.execute("CREATE TABLE Feed (title TEXT,img_path TEXT,summary TEXT,link TEXT,published TEXT,news TEXT, likes INTEGER, dislikes INTEGER)")
        for link in links:
            for element in news_type:
                if element in link[0]:
                    news=element
                    break
                else:
                    news="allcategory"
                    continue
            feed1 = feedparser.parse(link[0])
            for i in range(0,len(feed1.entries)):
                entry=feed1.entries[i]
                title=str(entry.title)
                c.execute("SELECT * FROM Feed where title = (:title)",{'title':title})
                if c.fetchone():
                    continue
                else:
                    date=date_parser.parse(entry.published)
                    if "media_thumbnail" in entry.keys():
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news,:likes,:dislikes)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':entry.media_thumbnail[0]['url'],'news':news,'published':date,'likes':0,'dislikes':0})
                    elif "postimage" in entry.keys():
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news,:likes,:dislikes)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':entry.postimage,'news':news,'published':date,'likes':0,'dislikes':0})
                    elif "media_content" in entry.keys():
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news,:likes,:dislikes)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':entry.media_content[0]['url'],'news':news,'published':date,'likes':0,'dislikes':0})
                    else:
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news,:likes,:dislikes)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':"https://www.zylogelastocomp.com/wp-content/uploads/2019/03/notfound.png",'news':news,'published':date,'likes':0,'dislikes':0})
                    conn.commit()
    else:
        for link in links:
            for element in news_type:
                if element in link[0]:
                    news=element
                    break
                else:
                    news="allcategory"
                    continue
            feed1 = feedparser.parse(link[0])
            for q in range(0,len(feed1.entries)):
                entry=feed1.entries[q]
                title=str(entry.title)
                c.execute("SELECT * FROM Feed where title = (:title)",{'title':title})
                if c.fetchone():
                    continue
                else:
                    date=date_parser.parse(entry.published)
                    if "media_thumbnail" in entry.keys():
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news,:likes,:dislikes)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':entry.media_thumbnail[0]['url'],'news':news,'published':date,'likes':0,'dislikes':0})
                    elif "postimage" in entry.keys():
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news,:likes,:dislikes)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':entry.postimage,'news':news,'published':date,'likes':0,'dislikes':0})
                    elif "media_content" in entry.keys():
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news,:likes,:dislikes)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':entry.media_content[0]['url'],'news':news,'published':date,'likes':0,'dislikes':0})
                    else:
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news,:likes,:dislikes)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':"https://www.zylogelastocomp.com/wp-content/uploads/2019/03/notfound.png",'news':news,'published':date,'likes':0,'dislikes':0})
                    conn.commit()
    conn.close()
    return 1

def fetchrss():
    conn = sqlite3.connect('Rss.db')
    c = conn.cursor()
    c.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Feedurl' """)
    if c.fetchone()[0]==1 :
        c.execute(" SELECT * FROM Feedurl")
        feedparse(c.fetchall())  
    conn.close()
    return 1            

def Feedfetch():
    conn = sqlite3.connect('Rss.db')
    c = conn.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Feed' ")
    if c.fetchone()[0]==1 :
        c.execute(" SELECT * FROM Feed ")
        rssfeed=c.fetchall()
    conn.close()
    return rssfeed

def getRssbyId(id):
    conn = sqlite3.connect('Rss.db')
    c = conn.cursor()
    c.execute(" SELECT * FROM Feed where title = (:title)",{'title':id})
    conn.commit()
    rsspage=c.fetchall()
    conn.close()
    return rsspage

def incrementLikes(id):
    conn = sqlite3.connect('Rss.db')
    c = conn.cursor()
    c.execute(" UPDATE Feed SET likes = likes+1 WHERE title = (:title)",{'title':id})
    conn.commit()
    conn.close()
    feed=Feedfetch()
    return feed

def incrementDislikes(id):
    conn = sqlite3.connect('Rss.db')
    c = conn.cursor()
    c.execute(" UPDATE Feed SET dislikes = dislikes+1 WHERE title = (:title)",{'title':id})
    conn.commit()
    conn.close()
    feed=Feedfetch()
    return feed

def editFeed(title,summary,id):
    conn = sqlite3.connect('Rss.db')
    c = conn.cursor()
    c.execute(" UPDATE Feed SET title = (:title), summary = (:summary) WHERE title = (:id)",{'title':title,'summary':summary,'id':id})
    conn.commit()
    conn.close()
    feed=Feedfetch()
    return feed

def getRssbyName(name):
    conn = sqlite3.connect('Rss.db')
    c = conn.cursor()
    c.execute(" SELECT * FROM Feed where news = (:news)",{'news':name})
    conn.commit()
    rsspage=c.fetchall()
    conn.close()
    return rsspage
