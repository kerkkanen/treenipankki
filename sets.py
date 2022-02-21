from db import db
from sqlalchemy.exc import IntegrityError


def get_all():
    sql = "SELECT * FROM sets ORDER BY name"
    return db.session.execute(sql).fetchall()


def get_latest():
    sql = "SELECT * FROM sets ORDER BY id DESC LIMIT 5"
    return db.session.execute(sql).fetchall()


def get_favourite_sets(user_id):
    sql = """SELECT * FROM sets WHERE id IN (SELECT set_id FROM favourite_sets WHERE user_id=:user_id)"""
    return db.session.execute(sql, {"user_id": user_id}).fetchall()


def validate(name, chosen, description):
    if len(name) < 4 or len(name) > 30 or not 2 <= len(chosen) <= 10 or len(description) > 1000:
        return False, "Nimen on oltava 4-30 merkkiä pitkä. Settiin on valittava 2-10 liikettä. Kuvaus ei voi olla 1000 merkkiä pitempi."
    return True, ""


def add_set(creator_id, name, description):
    sql = """INSERT INTO sets (creator_id, name, description)
             VALUES (:creator_id, :name, :description) RETURNING id"""
    try:
        set_id = db.session.execute(
            sql, {"creator_id": creator_id, "name": name, "description": description}).fetchone()[0]
        db.session.commit()
    except IntegrityError:
        return False, f"Setti {name} on jo olemassa."
    return True, set_id


def add_moves_to_set(set_id, move_id):
    sql = """INSERT INTO moves_in_set (set_id, move_id)
            VALUES (:set_id, :move_id)"""
    db.session.execute(sql, {"set_id": set_id, "move_id": move_id})
    db.session.commit()


def get_info(set_id):
    sql = """SELECT *, users.name FROM sets, users WHERE sets.id=:set_id AND sets.creator_id=users.id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()


def get_moves_in_set(set_id):
    sql = """SELECT * FROM moves WHERE id IN (SELECT move_id FROM moves_in_set WHERE set_id=:set_id)"""
    return db.session.execute(sql, {"set_id": set_id}).fetchall()


def get_set_ids_by_move(move_id):
    sql = """ SELECT * FROM moves_in_set WHERE move_id=:move_id"""
    return db.session.execute(sql, {"move_id": move_id}).fetchall()


def get_one_set(set_id):
    sql = """SELECT * FROM sets WHERE sets.id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()


def check_favourite_id(user_id, set_id):
    sql = """SELECT * FROM favourite_sets WHERE set_id=:set_id AND user_id=:user_id """
    result = db.session.execute(
        sql, {"user_id": user_id, "set_id": set_id}).fetchall()
    if len(result) == 0:
        return True
    else:
        return False


def add_favourite(user_id, set_id):
    sql = """INSERT INTO favourite_sets (user_id, set_id)
             VALUES (:user_id, :set_id)"""
    db.session.execute(sql, {"user_id": user_id, "set_id": set_id})
    db.session.commit()


def popular_sets():
    pass


def get_searched_ids(area):
    sql = """SELECT * FROM sets WHERE id IN (SELECT set_id FROM moves_in_set JOIN moves WHERE moves.muscles=:area)"""
    return db.session.execute(sql, {"area": area}).fetchall()

def get_set_ids_by_move(move_id):
    sql = """ SELECT * FROM moves_in_set WHERE move_id=:move_id"""
    return db.session.execute(sql, {"move_id": move_id}).fetchall()
