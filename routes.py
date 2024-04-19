from app import app
from db import db
from flask import render_template, redirect, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import searches as se

@app.route("/")
def index():
    if session:
        folders = se.libseek(session["username"])
        cards = se.cardseek(session["username"], folder=0)[0]
        return render_template(
                                "index.html", 
                                count=len(cards), 
                                cards=cards, 
                                folders=folders, 
                                number=len(folders)
                                )
    else:
        return render_template("index.html")
    
@app.route("/search")
def search():

    cardname = None
    rarity =  None
    twofaced = None
    power = None
    toughness = None
    inlib = None
    colours = ""
    cmc = None

    for value in request.args:
        if value[:-1] == "colour":
            colours += request.args[value]
        elif value == "rarity":
            rarity = request.args[value]
        elif value == "cardname":
            cardname = request.args[value]
        elif value == "twofaced":
            twofaced = request.args[value]
        elif value == "ispower":
            power = request.args[value]
        elif value == "power":
            power += request.args[value]
        elif value == "istoughness":
            toughness = request.args[value]
        elif value == "toughness":
            toughness += request.args[value]
        elif value == "iscmc":
            cmc = request.args[value]
        elif value == "cmc":
            cmc += request.args[value]
        elif value == "inlib":
            inlib = request.args[value]
    
    if colours == "":
        colours = None

    libs = [("None", 0)]
    cards = se.cardseek(session["username"], 
                        folder=inlib,
                        name=cardname,
                        cmc=cmc,
                        rarity=rarity,
                        twofaced=twofaced,
                        power=power,
                        toughness=toughness
                        )[0]
    for library in se.libseek(session["username"]):
        libs.append(library)
    return render_template("search.html", cards=cards, libs=libs)

@app.route("/newcard")
def newcard():
    libs = se.libseek(session["username"])
    
    return render_template("newcard.html", libs=libs )

@app.route("/newcard/send", methods=["POST"])
def cardsend():
    cardname = request.form["cardname"]
    cmc = request.form["cmc"]
    rarity = request.form["rarity"]

    if len(cardname) > 0 and len(cmc) > 0 and len(rarity) > 0:

        colours = ""
        two_faced = False
        power = None
        toughness = None
        inlibs = []
        for value in request.form:
            if value[:-1] == "colour":
                colours += request.form[value]
            elif value == "twofaced":
                two_faced = request.form["twofaced"]
            elif value == "power":
                power = request.form["power"]
            elif value == "toughness":
                toughness = request.form["toughness"]
            elif value != "cmc" and value != "rarity" and value != "cardname" and value != "libs" and value != "card":
                inlibs.append((value, request.form[value]))
        

        user = db.session.execute(text("SELECT id FROM users WHERE username=:username"), {
                                        "username":session["username"]
                                        }).fetchone()[0]
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
        card = db.session.execute(text("""
                                SELECT id FROM cards 
                                WHERE name=:cardname AND rarity=:rarity AND colour=:colours 
                                ORDER BY id DESC LIMIT 1
                                """), {
                                "cardname":cardname, "rarity":rarity, "colours":colours
                                }).fetchone()[0]
        
        if len(inlibs) != 0:
            for i in inlibs:
                print(i)
                sql = "INSERT INTO cardlib (card, library, visible) VALUES (:card, :library, True)"
                db.session.execute(text(sql), {"card":card, "library":i[1]})

        else:
            sql = "INSERT INTO cardlib (card, library, visible) VALUES (:card, 0, True)"
            db.session.execute(text(sql), {"card":card})
        db.session.commit()
        return redirect("/")
    
    else:
        return render_template("ohno.html", msg=2)
    
@app.route("/folder", methods=["GET"])
def folder():
    library = request.args["folder"]
    sql = """SELECT C.name, C.id FROM cards C, users U, cardlib D
                WHERE C.userid=U.id  AND C.id=D.card AND D.visible=True 
                AND D.library=:library AND U.username=:username"""
    cards = db.session.execute(text(sql), {"library":library, "username":session["username"]}).fetchall()
    return render_template("folder.html", cards=cards)

@app.route("/cardedit", methods=["GET"])
def cardedit():
    card = request.args["card"]
    sql = "SELECT name, twofaced, colour, cmc, rarity, power, toughness, id FROM cards WHERE id=:card"
    result = db.session.execute(text(sql), {"card":card}).fetchone()
    sql = "SELECT name, id FROM libraries" 
    libs = se.libseek(session["username"])
    sql = "SELECT library FROM cardlib WHERE card=:card"
    places = db.session.execute(text(sql), {"card":card}).fetchall()
    connected = []
    for place in places:
        connected.append(place[0])
    return render_template("cardedit.html", card=card, result=result, libs=libs, connected=connected) 

@app.route("/cardedit/send", methods=["POST"])
def sendedit():
    card = request.form["card"]
    cardname = request.form["cardname"]
    cmc = request.form["cmc"]
    rarity = request.form["rarity"] 
    if len(cardname) > 0 and len(cmc) > 0 and len(rarity) > 0:
        colours = ""
        two_faced = False
        power = None
        toughness = None
        inlibs = []
        for value in request.form:
            if value[:-1] == "colour":
                colours += request.form[value]
            elif value == "twofaced":
                two_faced = request.form["twofaced"]
            elif value == "power":
                power = request.form["power"]
            elif value == "toughness":
                toughness = request.form["toughness"]
            elif value != "cmc" and value != "rarity" and value != "cardname" and value != "libs" and value != "card":
                inlibs.append((value, request.form[value]))
        
        sql = """UPDATE cards SET name=:cardname, 
                                twofaced=:two_faced, 
                                colour=:colours,
                                cmc=:cmc, 
                                rarity=:rarity, 
                                power=:power, 
                                toughness=:toughness 
                                WHERE id=:card"""
        db.session.execute(text(sql), {
                                        "cardname":cardname, 
                                        "two_faced":two_faced, 
                                        "colours":colours, 
                                        "cmc":cmc, 
                                        "rarity":rarity, 
                                        "power":power, 
                                        "toughness":toughness, 
                                        "card":card
                                        })
        sql = """DELETE FROM cardlib WHERE card=:card"""
        db.session.execute(text(sql), {"card":card})
        if len(inlibs) != 0:
            for i in inlibs:
                sql = "INSERT INTO cardlib (card, library, visible) VALUES (:card, :library, True)"
                db.session.execute(text(sql), {"card":card, "library":i[1]})
        else:
            sql = "INSERT INTO cardlib (card, library, visible) VALUES (:card, 0, True)"
            db.session.execute(text(sql), {"card":card})
        db.session.commit()
        return redirect("/")
    else:
        return render_template("ohno.html", msg=2)
    
@app.route("/signin", methods=["POST"])
def signin():
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    username = request.form["username"]
    if 2 < len(username) < 25 and 2 < len(password) < 25:
        if len(se.userseek(username)) == 0:
            sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
            db.session.execute(text(sql), {"username":username, "password":hash_value})
            db.session.commit()
            return redirect("/")
        else:
            return render_template("ohno.html", msg = 3)
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