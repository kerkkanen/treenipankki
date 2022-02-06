from app import app
from flask import render_template, request, redirect
import users
import moves
import sets


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

        if users.check_name:
            return render_template("error.html", message="Tunnus on jo käytössä.")

        if not 4 <= len(name) >= 20:
            return render_template("error.html", message="Tunnuksen on oltava 4-20 merkkiä pitkä.")

        password = request.form["password"]
        password_again = request.form["password_again"]
        if password != password_again:
            return render_template("error.html", message="Salasanat eivät täsmää.")
        if not 8 <= len(password) <= 50:
            return render_template("error.html", message="Salasanan on oltava vähintään 8 merkkiä pitkä.")

        if not users.sign_up(name, password):
            return render_template("error.html", message="Tunnuksen luominen ei onnistunut.")
        return redirect("/")


@app.route("/add_move", methods=["get", "post"])
def add_move():
    if request.method == "GET":
        return render_template("add_move.html")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]

        if moves.check_name:
            return render_template("error.html", message=f"Pankista löytyy jo liike nimeltä {name}.")        
        if len(name) < 4 or len(name) > 30:
            return render_template("error.html", message="Nimen on oltava 4-30 merkkiä pitkä.")

        muscles = request.form["muscles"]
        if len(muscles) == 0:
            return render_template("error.html", message="Liikkeen vaikutusalue puuttuu.")

        description = request.form["description"]
        if len(description) > 2000:
            return render_template("error.html", message="Kuvaus ei voilla 2000 merkkiä pitempi.")

        move_id = moves.add_move(users.user_id(), name, muscles, description)

        return redirect("/move/"+str(move_id))

@app.route("/add_set", methods=["get", "post"])
def add_set():
    if request.method == "GET":
        arms = moves.get_by_muscles("kädet")
        legs = moves.get_by_muscles("jalat ja pakarat")
        backs = moves.get_by_muscles("selkä")
        abs = moves.get_by_muscles("vatsa")
        full = moves.get_by_muscles("koko vartalo")
        return render_template("add_set.html", arm_moves=arms, leg_moves=legs, back_moves=backs, abs_moves=abs, full_moves=full)

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]

        if sets.check_name:
            return render_template("error.html", message=f"Pankista löytyy jo setti nimeltä {name}.")   
        if len(name) < 4 or len(name) > 30:
            return render_template("error.html", message="Nimen on oltava 4-30 merkkiä pitkä.")
        

        chosen = request.form.getlist("chosen")
        if not 2 <= len(chosen) <= 10:
            return render_template("error.html", message="Settiin voi valita 2-10 liikettä.")

        description = request.form["description"]
        if len(description) > 2000:
            return render_template("error.html", message="Kuvaus ei voilla 2000 merkkiä pitempi.")

        set_id = sets.add_set(users.user_id(), name, description)

        for move_id in chosen:
            sets.add_moves_to_set(set_id, move_id)

        return redirect("/set/"+str(set_id))


@app.route("/move/<int:move_id>")
def show_move(move_id):
    info = moves.get_info(move_id)
    content = moves.get_content(move_id)

    return render_template("move.html", id=move_id, name=info[0], creator=info[1], muscles=content[0], description=content[1])

@app.route("/set/<int:set_id>")
def show_set(set_id):
    info = sets.get_info(set_id)
    content = sets.get_content(set_id)
    moveset_ids = sets.get_moveset_moves(set_id)

    setmoves = []
    for move_id in moveset_ids:
        setmoves.append(moves.get_one_move(move_id[1]))
        

    return render_template("set.html", id=set_id, name=info[0], creator=info[1], description=content[0], moves=setmoves)

@app.route("/profile/<int:id>", methods=["get"])
def profile(id):
    if request.method == "GET":
        correct_id = users.user_id()
        if correct_id == id:
            return render_template("profile.html", id=correct_id)
        else:
            return render_template("error.html", messager="Käyttäjällä ei oikeutta sivulle.")


@app.route("/movelist", methods=["get"])
def movelist():
    if request.method == "GET":
        return render_template("movelist.html", moves=moves.get_all())


@app.route("/setlist", methods=["get"])
def setlist():
    if request.method == "GET":
        return render_template("setlist.html", sets=sets.get_all())
