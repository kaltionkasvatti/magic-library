from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2:///hannolan"
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text("SELECT name FROM cards"))
    cards = result.fetchall()
    return render_template("index.html", count=len(cards), cards=cards)

@app.route("/newcard")
def newcard():
    return render_template("newcard.html")

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
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")