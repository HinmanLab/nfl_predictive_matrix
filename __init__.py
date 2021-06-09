from flask import Flask, redirect, url_for, render_template, request, session

from config import Config

import nfl_matrix

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/input', methods=["POST", "GET"])
def input():
    if request.method == "POST":
        user_nfl = request.form["nfl_input"]
        session["user"] = user_nfl
        return redirect(url_for("output"))
    else:
        return render_template("input.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route("/output")
def output():
    if "user" in session:
        user = session["user"]
        matrix_output = nfl_matrix.collect(user)
        return render_template("output.html", value=matrix_output, user_nfl=user)
    else:
        return redirect(url_for("input"))

if __name__ == '__main__':
    app.run(debug=True)
    