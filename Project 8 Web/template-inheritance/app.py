from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def demo():
   return render_template("demo.html")

@app.route("/one")
def one():
   return render_template("one.html")

@app.route("test")
def layout():
     return render_template("layout.html")

if __name__ == "__main__":
        app.run(debug="True")
