import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(name, password):
    sql = "SELECT password, id FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = name
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]


def sign_up(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password)
                 VALUES (:name, :password)"""
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(name, password)