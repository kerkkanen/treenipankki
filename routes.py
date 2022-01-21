from app import app
from flask import render_template, request, redirect

@app.route("/")
def index():
    return render_template("index.html")

#@app.route("/sign_up", methods=["get", "post"])
#def sign_up():
#    if request.method == "GET":
#        return render_template("sign_up.html")

#    if request.method == "POST":
#        name = request.form["name"]
#        if len(name) < 1 or len (name) > 20:
#            return render_template("error.html", message="Nimimerkin pituus on oltava 1-20 merkkiä.")

#        password = request.form["password"]
#        password_again = request.form["password_again"]
#        if password != password_again:
#            return render_template("error.html", message="Salasanat eivät tärmää.")
#        if len(password) < 4 or len(password) > 20:
#            return render_template("error.html", message="Salasanan oltava 4-20 merkkiä pitkä.")


