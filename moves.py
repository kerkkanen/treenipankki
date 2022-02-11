from db import db
from sqlalchemy.exc import IntegrityError


def validate(name, muscles, description):
    if len(name) < 4 or len(name) > 30:
        return False, "Nimen on oltava 4-30 merkkiä pitkä."
    if len(muscles) == 0:
        return False, "Liikkeen vaikutusalue puuttuu."
    if len(description) > 2000:
        return False, "Kuvaus ei voi olla 2000 merkkiä pitempi."
    return True, ""


def add_move(creator_id, name, muscles, description):
    sql = """INSERT INTO moves (creator_id, name, muscles, description)
             VALUES (:creator_id, :name, :muscles, :description) RETURNING id"""
    try:
        move_id = db.session.execute(
            sql, {"creator_id": creator_id, "name": name, "muscles": muscles, "description": description}).fetchone()[0]
        db.session.commit()
    except IntegrityError:
        return False, f"Liike {name} on jo olemassa."
    return True, move_id


def get_info(move_id):
    sql = """SELECT moves.name, users.name FROM moves, users WHERE moves.id=:move_id AND moves.creator_id=users.id"""
    return db.session.execute(sql, {"move_id": move_id}).fetchone()


def get_content(move_id):
    sql = """SELECT moves.muscles, moves.description FROM moves WHERE moves.id=:move_id"""
    return db.session.execute(sql, {"move_id": move_id}).fetchone()


def get_one_move(move_id):
    sql = """SELECT * FROM moves WHERE moves.id=:move_id"""
    return db.session.execute(sql, {"move_id": move_id}).fetchone()


def get_all():
    sql = """SELECT * FROM moves ORDER BY name"""
    return db.session.execute(sql).fetchall()


def get_by_muscles(move_muscles):
    sql = """SELECT * FROM moves WHERE moves.muscles=:move_muscles ORDER BY name"""
    return db.session.execute(sql, {"move_muscles": move_muscles}).fetchall()


def check_name(name):
    sql = "SELECT * FROM moves WHERE name=:name"
    result = db.session.execute(sql, {"name": name}).fetchall()
    if len(result) == 0:
        return False
    else:
        return True
