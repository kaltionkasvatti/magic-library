from app import app
from db import db
from flask import render_template, redirect, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    if session:
        finds = db.session.execute(text("SELECT DISTINCT L.name FROM users U, libraries L WHERE L.userid=U.id AND U.username=:username"), {"username":session["username"]})
        folders = finds.fetchall()
        result = db.session.execute(text("""
            SELECT C.name, C.id FROM cards C, users U , cardlib D 
            WHERE C.userid=U.id  AND C.id=D.card AND D.visible=True AND D.library=0 AND U.username=:username"""), {"username":session["username"]})
        cards = result.fetchall()
        return render_template("index.html", count=len(cards), cards=cards, folders=folders, number=len(folders))
    else:
        return render_template("index.html")

@app.route("/newcard")
def newcard():
    libs = db.session.execute(text("SELECT L.name, L.id FROM libraries L, users U WHERE L.userid=U.id AND U.username = :username"), {"username":session["username"]}).fetchall()
    return render_template("newcard.html", libs=libs )

@app.route("/newcard/send", methods=["POST"])
def cardsend():
    cardname = request.form["cardname"]
    colours = ""
    two_faced = False
    power = None
    toughness = None
    for value in request.form:
        if value[:-1] == "colour":
            colours += request.form[value]
        if value == "twofaced":
            two_faced = request.form["twofaced"]
        if value == "power":
            power = request.form["power"]
        if value == "toughness":
            toughness = request.form["toughness"]
    #try: colour1 = request.form["colour1"]
    ##except: colour1 = ""
    #try: colour2 = request.form["colour2"]
    #except: colour2 = ""
    #try: colour3 = request.form["colour3"]
    #except: colour3 = ""
    #try: colour4 = request.form["colour4"]
    #except: colour4 = ""
    #try: colour5 = request.form["colour5"]
    #except: colour5 = ""
    #colours = colour1 + colour2 + colour3 + colour4 + colour5
    cmc = request.form["cmc"]
    rarity = request.form["rarity"]
    inlibs = []
    libs = request.form["libs"]
    for lib in libs:
        try: inlibs.append((lib[1], request.form[lib[0]]))
        except: pass
    user = db.session.execute(text("SELECT id FROM users WHERE username=:username"), {"username":session["username"]}).fetchone()[0]
    sql= """INSERT INTO cards (name, twofaced, colour, cmc, rarity, power, toughness, userid) 
            VALUES (:cardname, :twofaced, :colours, :cmc, :rarity, :power, :toughness, :user)"""
    db.session.execute(text(sql), {"cardname":cardname, "twofaced":two_faced, "colours":colours, "cmc":cmc, "rarity":rarity, "power":power, "toughness":toughness, "user":user})
    db.session.commit()
    userid = db.session.execute(text("""
                            SELECT id FROM cards WHERE name=:cardname AND rarity=:rarity AND colour=:colours ORDER BY id DESC LIMIT 1"""
                            ), {"cardname":cardname, "rarity":rarity, "colours":colours}).fetchone()[0]
    print(userid)
    if len(inlibs) != 0:
        for i in inlibs:
            sql = "INSERT INTO cardlib (card, library, visible) VALUES (:userid, :library, True)"
            db.session.execute(text(sql), {"userid":userid, "library":i[0]})
    else:
        sql = "INSERT INTO cardlib (card, library, visible) VALUES (:userid, 0, True)"
        db.session.execute(text(sql), {"userid":userid})
    db.session.commit()
    return redirect("/")

@app.route("/signin", methods=["POST"])
def signin():
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    username = request.form["username"]
    if 2 < len(username) < 25 and 2 < len(password) < 25:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
        return redirect("/")
    else:
        return render_template("ohno.html", msg=1)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
        return render_template("ohno.html", msg=0)
    else:
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("ohno.html", msg=0)
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

    

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