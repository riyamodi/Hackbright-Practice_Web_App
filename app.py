from flask import Flask, render_template, redirect, g, url_for, request
import model

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/all_users")
def all_users():
    model.conn_db()
    list_of_users = model.get_all_users()
    html = render_template("all_users.html",list_of_users=list_of_users)
    return html

@app.route("/user")
def get_user_info():
    model.conn_db()
    id = request.args.get("id")
    user = model.get_user(id)
    posts = user.get_posts()
    comments = user.get_comments()
    votes = user.get_votes()

    html = render_template("user.html", user=user, posts=posts, comments=comments, votes=votes)
    return html

@app.route("/post")
def get_post():
    model.conn_db()
    post_id = request.args.get("post_id")
    print "post is: " , post_id
    #need to fix this so I decide whether to search for title or id
    list_posts = model.get_post(title=post_id)
    print "list_posts is: " , list_posts
    html = render_template("post.html",list_posts=list_posts)
    return html

 
if __name__ == "__main__":
    app.run(debug=True)

