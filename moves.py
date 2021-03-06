from db import db
from sqlalchemy.exc import IntegrityError


def validate(name, muscles, description):
    if len(name) < 4 or len(name) > 30 or len(muscles) == 0 or len(description) > 1000:
        return False, "Nimen on oltava 4-30 merkkiä pitkä. Vaikutusalue ei voi olla tyhjä.Kuvaus ei voi olla 1000 merkkiä pitempi."
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
    sql = """SELECT M.id, M.creator_id, M.name, M.muscles, M.description, U.name FROM moves M JOIN users U ON M.creator_id=U.id WHERE M.id=:move_id"""
    return db.session.execute(sql, {"move_id": move_id}).fetchone()


def get_one_move(move_id):
    sql = """SELECT id, creator_id, name, muscles, description FROM moves WHERE moves.id=:move_id"""
    return db.session.execute(sql, {"move_id": move_id}).fetchone()


def get_all():
    sql = """SELECT id, creator_id, name, muscles, description FROM moves ORDER BY name"""
    return db.session.execute(sql).fetchall()


def get_latest():
    sql = """SELECT id, creator_id, name, muscles, description FROM moves ORDER BY id DESC LIMIT 5"""
    return db.session.execute(sql).fetchall()


def get_by_muscles(move_muscles):
    sql = """SELECT id, creator_id, name, muscles, description FROM moves WHERE (:move_muscles)=ANY(muscles) ORDER BY name"""
    return db.session.execute(sql, {"move_muscles": move_muscles}).fetchall()


def get_random_by_muscle(move_muscles, volume):
    sql = """SELECT id, creator_id, name, muscles, description FROM moves WHERE (:move_muscles)=ANY(muscles) ORDER BY RANDOM() LIMIT :volume"""
    return db.session.execute(sql, {"move_muscles": move_muscles, "volume": volume}).fetchall()


def is_only_move_in_sets(move_id):
    sql = """SELECT set_id FROM moves_in_set GROUP BY set_id HAVING COUNT(set_id) = 1"""
    return db.session.execute(sql).fetchall()


def delete(move_id):
    sql = """DELETE FROM moves WHERE moves.id=:move_id"""
    db.session.execute(sql, {"move_id": move_id})
    db.session.commit()


def popular_moves():
    sql = """SELECT id, creator_id, name, muscles, description FROM moves WHERE id IN (SELECT move_id FROM moves_in_set GROUP BY move_id ORDER BY COUNT(move_id) DESC LIMIT 3);"""
    return db.session.execute(sql).fetchall()
