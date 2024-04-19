from db import db
from flask import session
from sqlalchemy.sql import text

def cardseek(
            user: str, 
            folder = None,
            name = None,
            cmc = None,
            twofaced = None,
            colours = None,
            rarity = None,
            power = None, #str
            toughness = None #str
            ):
    
    variables = {}
    variables["user"] = user
    frontseek = """SELECT 
            C.id, 
            C.name, 
            C.twofaced, 
            C.colour, 
            C.cmc,
            C.rarity, 
            C.power, 
            C.toughness
            FROM cards C, cardlib D, users U
            WHERE C.id=D.card 
            AND C.userid=U.id
            AND U.username = :user
            """
    if folder is not None:
        frontseek = frontseek + " AND D.library = :folder"
        variables["folder"] = folder

    if cmc is not None and len(cmc) > 1:
        frontseek = frontseek + " AND C.cmc" + cmc[0] + " " + str(int(cmc[1:]))

    if name is not None:
        frontseek = frontseek + " AND C.name LIKE :name"
        variables["name"] = '%' + name + '%'

    if twofaced is not None:
        frontseek = frontseek + " AND C.twofaced = :twofaced"
        variables["twofaced"] = twofaced

    if colours is not None:
        for i in range(0,len(colours)):
            frontseek = frontseek + " AND C.colour LIKE :colour" + str(i)
            variables["colour" + str(i)] = '%' + colours[i] + '%'

    if rarity is not None:
        frontseek = frontseek + " AND C.rarity = :rarity"
        variables["rarity"] = rarity

    if power is not None and len(power) > 1:
        frontseek = frontseek + " AND C.power " + power[0] + " " + str(int(power[1:]))

    if toughness is not None and len(toughness) > 1:
        frontseek = frontseek + " AND C.toughness " + toughness[0] + " " + str(int(toughness[1:]))
    
    front = db.session.execute(text(frontseek), variables).fetchall()

    
    backseek = """SELECT
            id,
            name,
            cmc,
            power,
            toughness
            FROM backside
            WHERE id = 0
            """
    
    for card in front:
        backseek = backseek + " OR frontid = " + str(card[0])

    back = db.session.execute(text(backseek)).fetchall()
    return (front, back)

def userseek(username):
    sql = """SELECT id FROM users WHERE username=:username"""
    return db.session.execute(text(sql), {"username":username}).fetchall()

def libseek(username):
    sql = "SELECT L.name, L.id FROM libraries L, users U WHERE U.id = L.userid AND U.username=:username"
    return db.session.execute(text(sql), {"username": username}).fetchall()

