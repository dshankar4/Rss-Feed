import sqlite3
from flask import flash
import feedparser
from dateutil import parser as date_parser
def addUser(username,password):
    conn = sqlite3.connect('Rss.db')
    c= conn.cursor()
    c.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Users' """)
    if c.fetchone()[0]!=1 : 
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
    c.execute(" SELECT * FROM Users WHERE username = (?) AND password = (?)",(username,password))
    if len(c.fetchall())==0 :
        flash("Incorrect Password  !")
        return -1
    result=c.fetchall()
    for row in result:
        print("%d %s",row["id"],row["username"])
    conn.commit()
    conn.close()
    return 1

def addFeedUrl(feed):
    conn = sqlite3.connect('Rss.db')
    c= conn.cursor()
    c.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Feedurl' """)
    if c.fetchone()[0]!=1 : 
        c.execute("CREATE TABLE Feedurl (link VARCHAR)")
        c.execute("INSERT INTO Feedurl VALUES (:link)",{'link':feed})
    else:
        c.execute("INSERT INTO Feedurl VALUES (:link)",{'link':feed})
    conn.commit()
    conn.close()
    return 1

def feedparse(links):
    conn = sqlite3.connect('Rss.db')
    c= conn.cursor()
    c.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Feed' """)
    if c.fetchone()[0]!=1 : 
        c.execute("CREATE TABLE Feed (title TEXT,img_path TEXT,summary TEXT,link TEXT,published TEXT,news TEXT)")
        for link in links:
            for l in range(0,len(links)):
                feed1 = feedparser.parse(link[0])
                for i in range(0,len(feed1.entries)):
                    entry=feed1.entries[i]
                    date=date_parser.parse(entry.published)
                    if "media_content" in entry.keys():
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':entry.media_content[0]['url'],'news':"hindustan",'published':date})
                    else:
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':"https://www.zylogelastocomp.com/wp-content/uploads/2019/03/notfound.png",'news':"hindustan",'published':date})
                    conn.commit()
    else:
        print("table")
        c.execute("DROP TABLE Feed")
        c.execute("CREATE TABLE Feed (title TEXT,img_path TEXT,summary TEXT,link TEXT,published TEXT,news TEXT)")
        for link in links:
            for j in range(0,len(links)):
                feed1 = feedparser.parse(link[0])
                for q in range(0,len(feed1.entries)):
                    entry=feed1.entries[q]
                    date=date_parser.parse(entry.published)
                    if "media_content" in entry.keys():
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':entry.media_content[0]['url'],'news':"hindustan",'published':date})
                    else:
                        c.execute("INSERT INTO Feed VALUES (:title,:img_path,:summary,:link,:published,:news)",{'title':entry.title,'link':entry.link,'summary':entry.summary,'img_path':"https://www.zylogelastocomp.com/wp-content/uploads/2019/03/notfound.png",'news':"hindustan",'published':date})
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