from flask import Flask, make_response, request, render_template
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "It works!"

@app.route("/word/<word>")
def setcookie(word):
   resp = make_response(f"{word} is the word!")
   resp.set_cookie('word', word)
   return resp

@app.route("/get")
def getcookie():
    word = request.cookies.get('word')
    return f"Your word was '{word}'"

@app.route("/guess",methods=["POST","GET"])
def guess():
    r = random.randint(1,10)
    resp = make_response(f"{r} is the number!")
    resp.set_cookie('word', r)
    return resp

@app.route("/count")
def count():
    n = request.cookies.get('count')
    if n is None:
        # cookie not found
        n = 1
    else:
        n = int(n) + 1
    resp = make_response(render_template('app.html', count=n))
    resp.set_cookie('count', str(n))

    return resp

if __name__ == "__main__":
    app.run("0.0.0.0")
