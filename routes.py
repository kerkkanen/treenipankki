from app import app
from flask import render_template, request, redirect
import users
import moves


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        if not users.login(name, password):
            return render_template("error.html", message="Väärä nimimerkki tai salasana.")
        return redirect("/")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/sign_up", methods=["get", "post"])
def sign_up():
    if request.method == "GET":
        return render_template("sign_up.html")

    if request.method == "POST":
        name = request.form["name"]

        password = request.form["password"]
        password_again = request.form["password_again"]
        if password != password_again:
            return render_template("error.html", message="Salasanat eivät täsmää.")
        if len(password) < 4 or len(password) > 20:
            return render_template("error.html", message="Salasanan oltava 4-20 merkkiä pitkä.")

        if not users.sign_up(name, password):
            return render_template("error.html", message="Tunnuksen luominen ei onnistunut.")
        return redirect("/")


@app.route("/add_move", methods=["get", "post"])
def add_move():
    if request.method == "GET":
        return render_template("add_move.html")

    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Nimen on oltava 1-20 merkkiä pitkä.")

        muscles = request.form.getlist("muscles")
        description = request.form["description"]

        move_id = moves.add_move(name, muscles, description)
        return redirect("/")