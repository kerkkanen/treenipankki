import os
from db import db
from flask import abort, request, session


def add_move(creator_id, name, muscles, description):
    sql = """INSERT INTO moves (creator_id, name, muscles, description)
             VALUES (:creator_id, :name, :muscles, :description) RETURNING id"""
    move_id = db.session.execute(
        sql, {"creator_id": creator_id, "name": name, "muscles": muscles, "description": description}).fetchone()[0]
    db.session.commit()

    return move_id

def get_info(move_id):
     sql = """SELECT moves.name, users.name FROM moves, users WHERE moves.id=:move_id AND moves.creator_id=users.id"""
     return db.session.execute(sql, {"move_id": move_id}).fetchone()

def get_content(move_id):
     sql = """SELECT moves.muscles, moves.description FROM moves WHERE moves.id=:move_id"""
     return db.session.execute(sql, {"move_id": move_id}).fetchone()

def get_all():
    sql = "SELECT id, name FROM moves ORDER BY name"
    return db.session.execute(sql).fetchall()