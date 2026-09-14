from flask import Flask, render_template, request, redirect,url_for
import subprocess
import platform
import time



app = Flask(__name__)

@app.route("/")
def root():
    return render_template("adone.html")

@app.route("/calc/<x>+<int:y>")
def add(x,y):
    x = int(x)
    c = x + y 
    return f"<h1>Calculator 2000!</h1>{x}+{y}={c}"
    #return render_template("look.html", a=x, b=y, result=c )
    #return render_template("look.html", a=a, b=b, result=result )

# from flask import Flask, render_template, request
@app.route("/calc/mul", methods=["GET", "POST"])
def mul():
    a,b,c,d = "","","",None
    errors = []
    if request.method == "POST":
        try:
            a = float(request.form['a'])
        except:
            errors.append(f"a needs to be an integer, not '{request.form['a']}'")

        try:
            b = float(request.form['b'])
        except: 
            errors.append(f"b needs to be an integer, not '{request.form['a']}'")

        try:
            c = float(request.form['c'])
        except: 
            errors.append(f"c needs to be an integer, not '{request.form['a']}'")
        if errors == []:
            d = a * b * c
    return render_template("mul.html", a=a, b=b, c=c, result=d, errors=errors)
    

@app.route('/open_calculator', methods=['POST'])
def open_calculator():
    system = platform.system()
    if system == "Windows":
        proc = subprocess.Popen("calc.exe")
        time.sleep(1)  # Give it time to open
    elif system == "Darwin":  # macOS
        subprocess.Popen(["open", "-a", "Calculator"])
    elif system == "Linux":
        subprocess.Popen(["gnome-calculator"])
    
    return redirect(url_for("mul"))

if __name__ == "__main__":
    app.run(debug=True)
