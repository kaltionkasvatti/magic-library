from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from dotenv import load_dotenv
load_dotenv()
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2:///hannolan"
db = SQLAlchemy(app)

@app.route("/")
def index():
    if session:
        finds = db.session.execute(text("SELECT DISTINCT C.library FROM cards C, users U WHERE C.userid=U.id AND U.username=:username AND C.library IS NOT NULL"), {"username":session["username"]})
        folders = finds.fetchall()
        result = db.session.execute(text("SELECT C.name, C.id FROM cards C, users U WHERE C.userid=U.id AND U.username=:username AND C.library IS NULL"), {"username":session["username"]})
        cards = result.fetchall()
        return render_template("index.html", count=len(cards), cards=cards, folders=folders, number=len(folders))
    else:
        return render_template("index.html")

@app.route("/newcard")
def newcard():
    return render_template("newcard.html")

@app.route("/signin", methods=["POST"])
def signin():
    hash_value = generate_password_hash(request.form["password"])
    username = request.form["username"]
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql), {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/cardsend", methods=["POST"])
def cardsend():
    cardname = request.form["cardname"]
    sql= "INSERT INTO cards (name) VALUES (:cardname)"
    db.session.execute(text(sql), {"cardname":cardname})
    db.session.commit()
    return redirect("/")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        return redirect("/ohno")
    else:
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return redirect("/ohno")
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/ohno")
def ohno():
    return render_template("ohno.html")

@app.route("/cardedit", methods=["GET"])
def cardedit():
    card = request.args["card"]
    sql = "SELECT name, twofaced, colour, cmc, set, rarity, power, toughness, library FROM cards WHERE id=:card"
    result = db.session.execute(text(sql), {"card":card}).fetchone()
    return render_template("cardedit.html", name=result[0], twofaced=result[1], colour=result[2], cmc=result[3], set=result[4], rarity=result[5], power=result[6], toughness=result[7], library=result[8], id=card) 