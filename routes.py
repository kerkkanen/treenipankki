from app import app
from flask import render_template, request, redirect
import users
import moves
import sets


@app.route("/")
def index():

    return render_template("index.html", sets=sets.get_latest(), moves=moves.get_latest())


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        valid, error = users.login(name, password)

        if not valid:
            return render_template("login.html", error=error)
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

        valid, error = users.validate(name, password, password_again)
        if not valid:
            return render_template("sign_up.html", error=error)

        valid, error = users.sign_up(name, password)
        if valid:
            return redirect("/")
        return render_template("sign_up.html", error=error)


@app.route("/add_move", methods=["get", "post"])
def add_move():
    if request.method == "GET":
        return render_template("add_move.html")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        muscles = request.form.getlist("muscles")
        description = request.form["description"]

        valid, error = moves.validate(name, muscles, description)

        if not valid:
            return render_template("add_move.html", error=error)

        valid, result = moves.add_move(
            users.user_id(), name, muscles, description)
        if not valid:
            return render_template("add_move.html", error=result)

        return redirect("/move/"+str(result))


@app.route("/add_set", methods=["get", "post"])
def add_set():
    arms = moves.get_by_muscles("kädet")
    legs = moves.get_by_muscles("jalat ja pakarat")
    backs = moves.get_by_muscles("selkä")
    abs = moves.get_by_muscles("vatsa")
    full = moves.get_by_muscles("koko vartalo")

    if request.method == "GET":
        return render_template("add_set.html", arm_moves=arms, leg_moves=legs, back_moves=backs, abs_moves=abs, full_moves=full)

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        chosen = request.form.getlist("chosen")
        description = request.form["description"]

        valid, error = sets.validate(name, chosen, description)
        if not valid:
            return render_template("add_set.html", error=error, arm_moves=arms, leg_moves=legs, back_moves=backs, abs_moves=abs, full_moves=full)

        valid, result = sets.add_set(users.user_id(), name, description)
        if not valid:
            return render_template("add_set.html", error=result, arm_moves=arms, leg_moves=legs, back_moves=backs, abs_moves=abs, full_moves=full)

        for move_id in chosen:
            sets.add_moves_to_set(result, move_id)

        return redirect("/set/"+str(result))


@app.route("/move/<int:move_id>")
def show_move(move_id):
    move = moves.get_info(move_id)

    muscles = ""
    for muscle in move[3]:
        muscles += f"{muscle}, "
    muscles = muscles[0:len(muscles)-2]

    return render_template("move.html", id=move_id, name=move[2], creator=move[6], muscles=muscles, description=move[4])


@app.route("/set/<int:set_id>", methods=["get", "post"])
def show_set(set_id):

    set = sets.get_info(set_id)

    if request.method == "GET":
        return render_template("set.html", id=set_id, name=set[2], creator=set[5], description=set[3], moves=sets.get_moves_in_set(set_id))

    if request.method == "POST":
        users.check_csrf()

        set_id = request.form["add_set"]

        if sets.check_favourite_id(users.user_id(), set_id):
            sets.add_favourite(users.user_id(), set_id)
            message = "Setti talletettu omiin suosikkeihin!"
            return render_template("set.html", id=set_id, name=set[2], creator=set[5], description=set[3], moves=sets.get_moves_in_set(set_id), message=message)
        else:
            error = "Setti on jo omissa suosikeissa."
            return render_template("set.html", id=set_id, name=set[2], creator=set[5], description=set[3], moves=sets.get_moves_in_set(set_id), error=error)



@app.route("/profile/<int:id>", methods=["get", "post"])
def profile(id):
    if request.method == "GET":
        if users.user_id() == id:
            favourites = sets.get_favourite_sets(id)
            added_sets = False
            if len(favourites) != 0:
                added_sets = True
            return render_template("profile.html", favourite_sets=favourites, added_sets=added_sets)
        else:
            return render_template("error.html", error="Käyttäjällä ei oikeutta sivulle.")

    if request.method == "GET":
        users.check_csrf()


@app.route("/movelist", methods=["get"])
def movelist():
    if request.method == "GET":
        arms = moves.get_by_muscles("kädet")
        legs = moves.get_by_muscles("jalat ja pakarat")
        backs = moves.get_by_muscles("selkä")
        abs = moves.get_by_muscles("vatsa")
        full = moves.get_by_muscles("koko vartalo")

        return render_template("movelist.html", arm_moves=arms, leg_moves=legs, back_moves=backs, abs_moves=abs, full_moves=full)


@app.route("/setlist", methods=["get", "post"])
#TÄMÄ EI TOIMI KORJAA
def setlist():
    if request.method == "GET":
        return render_template("setlist.html", sets=sets.get_all())

    if request.method == "POST":

        searched_set_ids = []
        area = request.form["area"]
        if area == "all":
            return render_template("setlist.html", searched_sets=sets.get_all(), message="Kaikki setit:")
            
        if area == "keskivartalo":
            searched_set_ids = sets.get_searched_ids(
                "vatsa") + sets.get_searched_ids("selkä")
        else:
            searched_set_ids = sets.get_searched_ids(area)

        searched_sets = []

        for set_id in searched_set_ids:
            set = sets.get_one_set(set_id[0])
            if set not in searched_sets:
                searched_sets.append(set)

        return render_template("setlist.html", searched_sets=searched_sets, message="Hakutulos:")
