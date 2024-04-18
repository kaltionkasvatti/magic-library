from db import db
from flask import session
from sqlalchemy.sql import text

def seekname(name, user, folder):
    frontseek = """SELECT 
            C.id, 
            C.name, 
            C.twofaced, 
            C.colour, 
            C.rarity, 
            C.power, 
            C.toughness
            FROM cards C, cardlib D, users U
            WHERE C.id=D.card 
            AND C.userid=U.id
            AND C.name LIKE :name
            AND U.username = :user
            AND D.library = :folder
            """
    
    backseek = """SELECT
            B.id,
            B.name,
            B.cmc,
            B.power,
            B.toughness
            FROM cards C, cardlib D, backside B, users U
            WHERE C.id = B.frontid
            AND B.frontid = D.card
            AND C.userid = U.id
            AND B.name LIKE :name
            AND U.username = :user
            AND D.library = :folder
            """
    front = db.session.execute(text(frontseek), {"name":name, "user":user, "folder":folder}).fetchall()
    back = db.session.execute(text(backseek), {"name":name, "user":user, "folder":folder}).fetchall()
    return (front, back)

def seekuser(username):
    sql = """SELECT id FROM users WHERE username=:username"""
    return db.session.execute(text(sql), {"username":username}).fetchall()
