from flask import Flask
from flask import render_template
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
