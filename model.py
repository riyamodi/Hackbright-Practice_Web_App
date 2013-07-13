import sqlite3

CONN = None
db = None

def conn_db():
    global db, CONN
    CONN = sqlite3.connect("forum.db")
    db = CONN.cursor()

class User(object):
    def __init__(self,id,email):
        self.id = id
        self.email = email

    def get_posts(self):
        query = """select title, created_at, body, id from posts where user_id = ?"""
        db.execute(query, (self.id,))
        posts = db.fetchall()
        post_list = []
        for p in posts:
            p = Post(p[0], p[1], p[2],p[3])
            post_list.append(p)
        return post_list

    def get_comments(self):
        query = """SELECT comments.body,comments.created_at,comments.id,comments.user_id, posts.title
                FROM comments JOIN posts ON comments.post_id=posts.id WHERE comments.user_id = ?"""
        db.execute(query, (self.id,))
        comments = db.fetchall()
        comment_list = []
        for c in comments:
            c = Comment(c[0], c[1], c[2], c[3], c[4])
            comment_list.append(c)
        return comment_list

    def get_votes(self):
        query = """SELECT posts.title, comments.body FROM posts JOIN comments 
                ON posts.id=comments.post_id 
                JOIN votes on votes.comment_id=comments.id  
                WHERE votes.comment_vote=1 and votes.user_id = ?"""
        db.execute(query, (self.id,))
        votes = db.fetchall()
        vote_list = []
        for v in votes:
            v = Vote(v[0], v[1])
            vote_list.append(v)
        return vote_list

class Post(object):
    def __init__(self,title,created_at,body,id):
        self.title = title
        self.created_at = created_at
        self.body = body
        self.id = id

class Comment(object):
    def __init__(self,body,created_at,id,user_id,post_title):
        self.body = body
        self.created_at = created_at
        self.id = id
        self.user_id = user_id
        self.post_title = post_title

class Vote(object):
    def __init__(self,post_title,comment):
        self.post_title = post_title
        self.comment = comment

def get_all_users():
    query = """SELECT id,email FROM users;"""
    db.execute(query, )
    row = db.fetchall()
    return row

def get_user(id):
    query = """SELECT id,email FROM users WHERE id = ?"""
    db.execute(query, (id,))
    row = db.fetchone()
    user = User(row[0],row[1])
    return user
