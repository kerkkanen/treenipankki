from db import db


def get_all():
    sql = "SELECT * FROM sets ORDER BY name"
    return db.session.execute(sql).fetchall()


def get_favouritelist(user_id):
    sql = "SELECT * FROM favourite_sets WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id": user_id}).fetchall()


def add_set(creator_id, name, description):
    sql = """INSERT INTO sets (creator_id, name, description)
             VALUES (:creator_id, :name, :description) RETURNING id"""
    set_id = db.session.execute(
        sql, {"creator_id": creator_id, "name": name, "description": description}).fetchone()[0]
    db.session.commit()
    return set_id


def add_moves_to_set(set_id, move_id):
    sql = """INSERT INTO moves_in_set (set_id, move_id)
            VALUES (:set_id, :move_id)"""
    db.session.execute(sql, {"set_id": set_id, "move_id": move_id})
    db.session.commit()


def get_info(set_id):
    sql = """SELECT sets.name, users.name FROM sets, users WHERE sets.id=:set_id AND sets.creator_id=users.id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()


def get_content(set_id):
    sql = """SELECT sets.description FROM sets WHERE sets.id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()


def get_moves_in_set(set_id):
    sql = """SELECT * FROM moves_in_set WHERE set_id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchall()


def check_name(name):
    sql = "SELECT * FROM sets WHERE name=:name"
    result = db.session.execute(sql, {"name": name}).fetchall()
    if len(result) == 0:
        return False
    else:
        return True

def get_one_set(set_id):
    sql = """SELECT * FROM sets WHERE sets.id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()

def check_favourite_id(user_id, set_id):
    sql = """SELECT * FROM favourite_sets WHERE user_id=:user_id AND set_id=:set_id"""
    result = db.session.execute(sql, {"user_id":user_id, "set_id":set_id}).fetchall()
    if len(result) == 0:
        return True
    else:
        return False

def add_favourite(user_id, set_id):
    sql = """INSERT INTO favourite_sets (user_id, set_id)
             VALUES (:user_id, :set_id)"""
    db.session.execute(sql, {"user_id": user_id, "set_id": set_id})
    db.session.commit()