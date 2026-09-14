from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/calc/add/',methods = ["GET","POST"])
def add():
    if request.method == "POST":
        word = request.form["word"]
        print("WORD =", word)
    return render_template("add.html")

@app.route('/calc/mul/',methods = ["GET","POST"])
def mul():
    if request.method == "POST":
        word = request.form["word"]
        print("WORD =", word)
    return render_template("mul.html")

if __name__ == "__main__":
    app.run()



