from db import db


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
