from flask import Flask, request, session, g, redirect, url_for,\
render_template, flash

import sqlite3

import hashlib

from database import get_db, create_tables, hash_password

# Application configuration
app = Flask(__name__)
app.secret_key = b'not secure, do not do this'


@app.route('/', methods=['POST', 'GET'])
def home():

    if request.method == 'POST':

        if session.get('logged_in'):

            # Save the post
            text = request.form['body']

            db = get_db()
            db.execute("INSERT INTO posts (user_id, date, text)\
                        VALUES (?,datetime('now'),?);", 
                       (session.get('user_id'), text)
                      )

            db.commit()

            flash(f"Post saved!", "info")

        else:
            flash("Login required.", "error")
            return(redirect(url_for('login')))

    db = get_db()
    c = db.execute('SELECT * FROM posts LEFT JOIN users ON posts.user_id=users.id;')
    posts = c.fetchall()

    return(render_template('home.html', posts=posts))


@app.route('/post/<id>', methods=['POST', 'GET'])
def post(id):

    if request.method == 'POST':

        if session.get('logged_in'):

                # Save the post
                text = request.form['body']
                
                if not text:
                    db = get_db()
                    db.execute("INSERT INTO comments (user_id, post_id, date, text)"
                            " VALUES (?,?,datetime('now'),?);", 
                            (session.get('user_id'), id, text)
                            )
                    db.commit() 
                    flash(f"Comment saved!", "info")
                else:
                    flash(f"Error, You need to write something faggot","error")
            
        else:
            flash("Login required.", "error")
            return(redirect(url_for('login')))


    db = get_db()
    c = db.execute('SELECT * FROM comments'
                   ' LEFT JOIN users ON comments.user_id=users.id'
                   ' WHERE comments.post_id=?;', (id,))
    comments = c.fetchall()

    c = db.execute("SELECT * FROM posts "
                   " LEFT JOIN users ON posts.user_id=users.id"
                   " WHERE posts.id=?;",
                   (id,)
                   )
    post = c.fetchone()

    return(render_template('post.html', post=post, comments=comments))



@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        # Connect to the database
        db = get_db()

        # Retrieve the users password from database (and check if user exist)
        c = db.execute("SELECT * FROM users WHERE email=?;", (request.form['email'],))
        user = c.fetchone()
        
        # Check if a user was found
        if user is None:
            flash('User not found.', 'error')
            return render_template('login.html')

        session['logged_in'] = True
        session['email'] = user['email']
        session['name'] = user['name']
        session['user_id'] = user['id']
        flash('You were logged in.', 'info')

        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.','info')
    return redirect(url_for('home'))

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']
        
        if pass1 != pass2: 
            flash("Passwords do not match, try again.", 'error')
        else:
            db=get_db()
            db.execute('insert into users (name, email, password) values (?, ?, ?)',
                       (name, email, hash_password(pass1)))
            db.commit()

            flash(f'User \'{name}\' registered.', 'info')

            return redirect(url_for('login'))

    return render_template('register.html')



if __name__ == "__main__":
    with app.app_context():
        create_tables()

    app.run(port="5000", debug=True)

