from app import app
from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def valid_user(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()  
    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False
    return True

def insert_user(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()


def id_user(username):
    return db.session.execute(text("""
                                SELECT id FROM users WHERE username=:username"""
                                ), {
                                "username":username
                                }).fetchone()[0]