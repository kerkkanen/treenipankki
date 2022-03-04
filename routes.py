from app import app
from flask import render_template, request, redirect
import users
import moves
import sets
import reviews


@app.route("/")
def index():

    content = ["/movelist", "/setlist", "/random_set"]

    return render_template("index.html", DropDownMenuLink=content, top_sets=sets.popular_sets(), sets=sets.get_latest(), top_moves=moves.popular_moves(), moves=moves.get_latest())


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

    return render_template("move.html", id=move_id, move=move, muscles=muscles)


@app.route("/set/<int:set_id>", methods=["get", "post"])
def show_set(set_id):

    set = sets.get_info(set_id)
    favourite = sets.is_favourite(users.user_id(), set_id)
    review = reviews.get_reviews(set_id)
    avg = reviews.get_review_average(set_id)
    volume = reviews.get_review_volume(set_id)[0]
    average = 0

    try:
        average = int(avg[0])
    except TypeError:
        average = ""

    if request.method == "GET":
        return render_template("set.html", id=set_id, set=set, moves=sets.get_moves_in_set(set_id), favourite=favourite, review=review, average=average, volume=volume)

    if request.method == "POST":
        users.check_csrf()

        favourite = sets.is_favourite(users.user_id(), set_id)
        if not favourite:
            sets.add_favourite(users.user_id(), set_id)
            favourite = True
        else:
            favourite = False
            sets.delete_favourite(users.user_id(), set_id)
    return render_template("set.html", id=set_id, set=set, moves=sets.get_moves_in_set(set_id), favourite=favourite, review=review, averag=average, volume=volume)


@app.route("/review/<int:set_id>", methods=["post"])
def review(set_id):
    users.check_csrf()

    comment = request.form["comment"]

    if "dumbells" not in request.form or "trainer" not in request.form or len(comment) > 1000:
        set = sets.get_info(set_id)
        favourite = sets.is_favourite(users.user_id(), set_id)
        review = reviews.get_reviews(set_id)
        volume = reviews.get_review_volume(set_id)[0]
        avg = reviews.get_review_average(set_id)
        average = 0

        try:
            average = int(avg[0])
        except TypeError:
            average = ""

        return render_template("set.html", id=set_id, set=set, moves=sets.get_moves_in_set(set_id), favourite=favourite, review=review, average=average, error="Täytä kaikki kohdat.", volume=volume)
    else:
        dumbells = request.form["dumbells"]
        trainer = request.form["trainer"]

        reviews.add_review(users.user_id(), set_id,
                           trainer, int(dumbells), comment)
        return redirect("/set/"+str(set_id))


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
def setlist():
    if request.method == "GET":
        return render_template("setlist.html", sets=sets.get_all())

    if request.method == "POST":

        searched_sets = []

        if "choise" in request.form:
            choise = request.form["choise"]
            if choise == "2-3":
                searched_sets = sets.get_searched_by_volume(2, 3)
            elif choise == "4-6":
                searched_sets = sets.get_searched_by_volume(4, 6)
            elif choise == "7-10":
                searched_sets = sets.get_searched_by_volume(7, 10)
            elif choise == "all":
                return render_template("setlist.html", searched_sets=sets.get_all(), message="Kaikki setit:")
            elif choise == "keskivartalo":
                searched_sets = sets.get_searched_by_area(
                    "vatsa") + sets.get_searched_by_area("selkä")
            else:
                searched_sets = sets.get_searched_by_area(choise)
        else:
            return render_template("setlist.html", error="Valitse näytettävät.")

        message = "Hakutulos:"
        if len(searched_sets) == 0:
            return render_template("setlist.html", error="Pankista ei löytynyt hakuehtoja täyttäviä settejä.")

        return render_template("setlist.html", searched_sets=searched_sets, message=message)


@app.route("/admin", methods=["get", "post"])
def admin():
    move = moves.get_all()
    set = sets.get_all()
    user = users.get_all()
    review = reviews.get_all_reviews()

    if request.method == "GET":
        if users.user_admin():
            return render_template("admin.html", move=move, set=set, user=user, review=review)
        else:
            return render_template("error.html", error="Käyttäjällä ei oikeutta sivulle.")

    if request.method == "POST":
        users.check_csrf()
        error = "Valitse poistettavat."

        if "delete_move" in request.form:
            delete = request.form.getlist("delete_move")
            for move_id in delete:
                one_move_sets = moves.is_only_move_in_sets(move_id)
                for set in one_move_sets:
                    sets.delete(set[0])
                moves.delete(move_id)
            return redirect("/admin")
        elif "delete_set" in request.form:
            delete = request.form.getlist("delete_set")
            for set_id in delete:
                sets.delete(set_id)
            return redirect("/admin")
        elif "delete_user" in request.form:
            delete = request.form.getlist("delete_user")
            for user_id in delete:
                users.delete(user_id)
                empty_sets = sets.sets_without_content()
                for set in empty_sets:
                    sets.delete(set[0])
            return redirect("/admin")
        elif "delete_review" in request.form:
            delete = request.form.getlist("delete_review")
            for review_id in delete:
                reviews.delete(review_id)
            return redirect("/admin")
        else:
            return render_template("admin.html", move=move, set=set, user=user, error=error)


@app.route("/random_set", methods=["get", "post"])
def random_set():

    if request.method == "GET":
        return render_template("random_set.html")

    if request.method == "POST":

        error = "Valitse liikkeiden määrä ja alue."
        volume = 0
        area = ""
        if "area" not in request.form or "volume" not in request.form:
            return render_template("random_set.html", error=error)
        else:
            volume = int(request.form["volume"])
            area = request.form["area"]

            move_ids = []
            move_set = moves.get_random_by_muscle(area, volume)
            full_body_moves = moves.get_random_by_muscle(
                "koko vartalo", volume)

            if len(move_set) == 0:
                return render_template("random_set.html", message="Pankissa ei ole vielä sopivia treeniliikkeitä.")

            while len(move_set) < volume:
                if len(full_body_moves) == 0:
                    break
                move = full_body_moves.pop()
                if move not in move_set:
                    move_set.append(move)

            for move in move_set:
                move_ids.append(move[0])

        return render_template("random_set.html", moves=move_set, move_ids=move_ids, volume=volume, random=True)


@app.route("/add_random", methods=["post"])
def add_random():

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        moves = request.form.getlist("move_ids")
        description = request.form["description"]

        valid, result = sets.add_set(users.user_id(), name, description)
        if not valid:
            return render_template("random_set.html", error=result)

        ids = []
        moves = moves[0][1:-1]
        temp = ""
        for i in range(len(moves)):
            print(i, (len(moves)))
            if moves[i] == "," or moves[i] == "":
                ids.append(int(temp))
                temp = ""
                continue
            else:
                temp += moves[i]
                if i == len(moves)-1:
                    ids.append(int(temp))

        for move_id in ids:
            sets.add_moves_to_set(result, move_id)

        return redirect("/set/"+str(result))
