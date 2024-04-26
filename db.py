from dotenv import load_dotenv
load_dotenv()
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from app import app
from sqlalchemy.sql import text

app.secret_key = getenv("SECRET_KEY")
data = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = data
db = SQLAlchemy(app)

def cardinsert(cardname, two_faced, colours, cmc, rarity, user, power = None, toughness = None):
    if toughness is None and power is None:
        sql= """INSERT INTO cards (name, twofaced, colour, cmc, rarity, userid) 
                VALUES (:cardname, :twofaced, :colours, :cmc, :rarity, :user)"""
        db.session.execute(text(sql), {
                                    "cardname":cardname, 
                                    "twofaced":two_faced, 
                                    "colours":colours, 
                                    "cmc":cmc, 
                                    "rarity":rarity, 
                                    "user":user
                                    })
    elif toughness is None and power is not None:
        sql= """INSERT INTO cards (name, twofaced, colour, cmc, rarity, power, userid) 
                VALUES (:cardname, :twofaced, :colours, :cmc, :rarity, :power, :user)"""
        db.session.execute(text(sql), {
                                    "cardname":cardname, 
                                    "twofaced":two_faced, 
                                    "colours":colours, 
                                    "cmc":cmc, 
                                    "rarity":rarity, 
                                    "power":power, 
                                    "user":user
                                    })
    elif toughness is not None and power is None:
        sql= """INSERT INTO cards (name, twofaced, colour, cmc, rarity, toughness, userid) 
                VALUES (:cardname, :twofaced, :colours, :cmc, :rarity, :toughness, :user)"""
        db.session.execute(text(sql), {
                                    "cardname":cardname, 
                                    "twofaced":two_faced, 
                                    "colours":colours, 
                                    "cmc":cmc, 
                                    "rarity":rarity, 
                                    "toughness":toughness, 
                                    "user":user
                                    })
    else:
        sql= """INSERT INTO cards (name, twofaced, colour, cmc, rarity, power, toughness, userid) 
                VALUES (:cardname, :twofaced, :colours, :cmc, :rarity, :power, :toughness, :user)"""
        db.session.execute(text(sql), {
                                    "cardname":cardname, 
                                    "twofaced":two_faced, 
                                    "colours":colours, 
                                    "cmc":cmc, 
                                    "rarity":rarity, 
                                    "power":power, 
                                    "toughness":toughness, 
                                    "user":user
                                    })
    db.session.commit()


def lib_insert(card, library):
    sql = "INSERT INTO cardlib (card, library, visible) VALUES (:card, :library, True)"
    db.session.execute(text(sql), {"card":card, "library":library})
    db.session.commit()