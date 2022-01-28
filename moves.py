import os
from db import db
from flask import abort, request, session


def add_move(name, muscles, description):
    sql = """INSERT INTO moves (name, muscles, description
        VALUES (:name, :muscles: description"""
    move_id = db.session.execute(
        sql, {"name": name, "muscles": muscles, "description": description})
    db.session.commit()

    return move_id
