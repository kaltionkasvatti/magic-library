from dotenv import load_dotenv
load_dotenv()
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from app import app

app.secret_key = getenv("SECRET_KEY")
data = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = data
db = SQLAlchemy(app)