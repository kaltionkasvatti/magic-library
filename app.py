from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
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