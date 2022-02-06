import os
from db import db
from flask import abort, request, session


def get_all():
    sql = "SELECT * FROM sets ORDER BY name"
    return db.session.execute(sql).fetchall()


def add_set(creator_id, name, description):
    sql = """INSERT INTO sets (creator_id, name, description)
             VALUES (:creator_id, :name, :description) RETURNING id"""
    set_id = db.session.execute(
        sql, {"creator_id": creator_id, "name": name, "description": description}).fetchone()[0]
    db.session.commit()
    return set_id


def add_moves_to_set(set_id, move_id):
    sql = """INSERT INTO movesets (set_id, move_id)
            VALUES (:set_id, :move_id)"""
    db.session.execute(sql, {"set_id": set_id, "move_id": move_id})
    db.session.commit()


def get_info(set_id):
    sql = """SELECT sets.name, users.name FROM sets, users WHERE sets.id=:set_id AND sets.creator_id=users.id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()


def get_content(set_id):
    sql = """SELECT sets.description FROM sets WHERE sets.id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()


def get_moveset_moves(set_id):
    sql = """SELECT * FROM movesets WHERE set_id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchall()

def check_name(name):
    sql = "SELECT * FROM sets WHERE name=:name"
    result = db.session.execute(sql, {"name":name}).fetchall()
    if len(result) == 0:
        return False
    else:
        return True