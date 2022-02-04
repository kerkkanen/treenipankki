import os
from db import db
from flask import abort, request, session

def get_all():
    sql = "SELECT id, name FROM sets ORDER BY name"
    return db.session.execute(sql).fetchall()
