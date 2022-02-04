from app import app
from flask import render_template, request, redirect
import users
import moves


@app.route("/")
def index():
    return render_template("index.html", moves=moves.get_all())


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
        if len(password) < 8:
            return render_template("error.html", message="Salasanan oltava vähintään 8 merkkiä pitkä.")
        if not users.sign_up(name, password):
            return render_template("error.html", message="Tunnuksen luominen ei onnistunut.")
        return redirect("/")


@app.route("/add_move", methods=["get", "post"])
def add_move():
    if request.method == "GET":
        return render_template("add_move.html")

    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 4 or len(name) > 30:
            return render_template("error.html", message="Nimen on oltava 4-30 merkkiä pitkä.")

        muscles = request.form.getlist("muscles")
        description = request.form["description"]

        move_id = moves.add_move(users.user_id(), name, muscles, description)

        return redirect("/move/"+str(move_id))


@app.route("/move/<int:move_id>")
def show_move(move_id):
    info = moves.get_info(move_id)
    content = moves.get_content(move_id)

    

    return render_template("move.html", id=move_id, name=info[0], creator=info[1], muscles=content[0], description=content[1])
