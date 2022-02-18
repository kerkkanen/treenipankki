import os
from sqlalchemy.exc import IntegrityError
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash


def login(name, password):
    if name == "" or password == "":
        return False, "Nimimerkki tai salasana ei voi olla tyhjä."
    sql = "SELECT password, id FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    if not user:
        return False, "Väärä nimimerkki tai salasana."
    if not check_password_hash(user[0], password):
        return False, "Väärä nimimerkki tai salasana."
    session["user_id"] = user[1]
    session["user_name"] = name
    session["csrf_token"] = os.urandom(16).hex()
    return True, ""


def logout():
    del session["user_id"]
    del session["user_name"]


def user_id():
    return session.get("user_id", 0)

def validate(name, password, password_again):
    if not 4 <= len(name) <= 20 or not 8 <= len(password):
            return False, "Nimimerkin on oltava 4-20 ja salasanan vähintään 8 merkkiä pitkä."
    if password != password_again:
        return False, "Salasanat eivät täsmää."
    return True, ""


def sign_up(name, password):
    hash_value = generate_password_hash(password)
    sql = """INSERT INTO users (name, password)
                 VALUES (:name, :password)"""
    try:        
        db.session.execute(sql, {"name": name, "password": hash_value})
        db.session.commit()        
    except IntegrityError:
        return False, "Nimimerkki on jo olemassa."
    login(name, password)
    return True, ""


def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
