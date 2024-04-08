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
data = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = data
db = SQLAlchemy(app)

@app.route("/")
def index():
    if session:
        finds = db.session.execute(text("SELECT DISTINCT L.name FROM users U, libraries L WHERE L.userid=U.id AND U.username=:username"), {"username":session["username"]})
        folders = finds.fetchall()
        result = db.session.execute(text("""
            SELECT C.name, C.id FROM cards C, users U , cardlib D 
            WHERE C.userid=U.id  AND C.id=D.card AND D.visible=True AND U.username=:username"""), {"username":session["username"]})
        cards = result.fetchall()
        return render_template("index.html", count=len(cards), cards=cards, folders=folders, number=len(folders))
    else:
        return render_template("index.html")

@app.route("/newcard")
def newcard():
    libs = db.session.execute(text("SELECT L.name, L.id FROM libraries L, users U WHERE L.userid=U.id AND U.username = :username"), {"username":session["username"]}).fetchall()
    return render_template("newcard.html", libs=libs )

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
    sql = "SELECT name, twofaced, colour, cmc, rarity, power, toughness FROM cards WHERE id=:card"
    result = db.session.execute(text(sql), {"card":card}).fetchone()
    sql = "SELECT name FROM libraries" 
    libs = db.session.execute(text(sql)).fetchall()
    sql = "SELECT library FROM cardlib WHERE card=:card"
    connected = db.session.execute(text(sql), {"card":card}).fetchall()
    return render_template("cardedit.html", id=card, result=result, libs=libs, connected=connected) 