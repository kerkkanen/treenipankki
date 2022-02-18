from app import app
from flask import render_template, request, redirect
import users
import moves
import sets


@app.route("/")
def index():

    popular_moves = []
    popular_sets = sets.popular_sets()

    return render_template("index.html")


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
    info = moves.get_info(move_id)
    content = moves.get_content(move_id)
    muscles = ""
    for muscle in content[0]:
        muscles += f"{muscle}, "
    muscles = muscles[0:len(muscles)-2]
 
    return render_template("move.html", id=move_id, name=info[0], creator=info[1], muscles=muscles, description=content[1])


@app.route("/set/<int:set_id>", methods=["get", "post"])
def show_set(set_id):

    if request.method == "GET":
        info = sets.get_info(set_id)
        content = sets.get_content(set_id)
        moveset_ids = sets.get_moves_in_set(set_id)

        moves_in_set = []
        for move_id in moveset_ids:
            move = moves.get_one_move(move_id[1])
            moves_in_set.append(move)

        return render_template("set.html", id=set_id, name=info[0], creator=info[1], description=content[0], moves=moves_in_set)


@app.route("/add_favourite", methods=["get", "post"])
def add_favourite():

    if request.method == "POST":
        users.check_csrf()

        set_id = request.form["add_set"]

        if sets.check_favourite_id(users.user_id(), set_id):
            sets.add_favourite(users.user_id(), set_id)
        
        message = "Setti talletettu omiin suosikkeihin!"

        return redirect("/set/"+str(set_id))


@app.route("/profile/<int:id>", methods=["get"])
def profile(id):
    if request.method == "GET":
        if users.user_id() == id:
            favourite_sets_ids = sets.get_favouritelist(id)
            added_sets = False
            favourites = []
            for set_id in favourite_sets_ids:
                favourites.append(sets.get_one_set(set_id[1]))
            if len(favourites) != 0:
                added_sets = True
            return render_template("profile.html", favourite_sets=favourites, added_sets=added_sets)
        else:
            return render_template("error.html", error="Käyttäjällä ei oikeutta sivulle.")


@app.route("/movelist", methods=["get"])
def movelist():
    if request.method == "GET":
        arms = moves.get_by_muscles("kädet")
        legs = moves.get_by_muscles("jalat ja pakarat")
        backs = moves.get_by_muscles("selkä")
        abs = moves.get_by_muscles("vatsa")
        full = moves.get_by_muscles("koko vartalo")        

        return render_template("movelist.html", arm_moves=arms, leg_moves=legs, back_moves=backs, abs_moves=abs, full_moves=full)


@app.route("/setlist", methods=["get"])
def setlist():
    if request.method == "GET":
        return render_template("setlist.html", sets=sets.get_all())
