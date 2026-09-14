from flask import Flask, render_template, redirect, request
from db import create_db, get_db, close_db

app = Flask(__name__)

@app.route("/")
def viewposts():
    # con = get_db()
    # con.execute("SELECT * FROM ")
    #return render_template("viewposts.html", posts = posts)
    return render_template("home.html")

@app.route("/post")
def createpost():
    if request.method == "POST":
        #title = request.form['title']

        con = get_db()
        #con.execute("INSERT INTO ....?", (name,title,whatever))
        con.commit()
        return redirect("/")
    return render_template("createpost.html")

@app.route("/signup")
def signup():

    return render_template("signup.html")

@app.route("/signin")
def signin():

    return render_template("signin.html")

@app.route("/settings")
def settings():

    return render_template("settings.html")

@app.route("/donate")
def donate():

    return render_template("donate.html")

@app.route("/music")
def music():

    return render_template("music.html")

@app.route("/music/search")
def music_search():

    return render_template("music_search.html")

@app.route("/music/favorites")
def music_favorites():

    return render_template("music_favorites.html")


if __name__ == "__main__":
    with app.app_context():
        create_db()
    app.run("0.0.0.0", debug=True)