from db import db

def get_reviews(set_id):
    sql = """SELECT U.name, R.trainer_level, R.dumbells, R.comment FROM reviews R, users U WHERE R.creator_id = U.id AND R.set_id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchall()

def get_all_reviews():
    sql = """SELECT id, creator_id, set_id, trainer_level, dumbells, comment FROM reviews"""
    return db.session.execute(sql).fetchall() 


def get_review_average(set_id):
    sql = """SELECT AVG(dumbells) FROM reviews WHERE set_id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()


def get_review_volume(set_id):
    sql = """SELECT COUNT(set_id) FROM reviews WHERE set_id=:set_id"""
    return db.session.execute(sql, {"set_id": set_id}).fetchone()


def add_review(creator_id, set_id, trainer_level, dumbells, comment):
    sql = """INSERT INTO reviews (creator_id, set_id, trainer_level, dumbells, comment)
             VALUES (:creator_id, :set_id, :trainer_level, :dumbells, :comment)"""
    db.session.execute(
        sql, {"creator_id": creator_id, "set_id": set_id, "trainer_level": trainer_level, "dumbells": dumbells, "comment": comment})
    db.session.commit()

def delete(review_id):
    sql = """DELETE FROM reviews WHERE reviews.id=:review_id"""
    db.session.execute(sql, {"review_id": review_id})
    db.session.commit()