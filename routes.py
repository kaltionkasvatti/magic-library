from app import app
from db import db, cardinsert, lib_insert
from flask import abort, render_template, redirect, request, session
from sqlalchemy.sql import text
import searches as se
import users as us
from secrets import token_hex

@app.route("/")
def index():
    if session:
        folders = se.libseek(session["username"])
        cards = se.cardseek(session["username"], folder=0)
        return render_template(
                                "index.html", 
                                count=len(cards[0]), 
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
        print(request.args[value])
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
                        colours=colours,
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
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
                power = power if len(power) >= 1 else None
            elif value == "toughness":
                toughness = request.form["toughness"]
                toughness = toughness if len(toughness) >= 1 else None
            elif (
                value != "cmc" 
                and value != "rarity" 
                and value != "cardname" 
                and value != "libs" 
                and value != "card"
                and value != "csrf_token"
                ):
                inlibs.append((value, request.form[value]))
        

        user = us.id_user(session["username"])
        cardinsert(cardname, two_faced, colours, cmc, rarity, user, power, toughness)
        
        card = db.session.execute(text("""
                                SELECT id FROM cards 
                                WHERE name=:cardname AND rarity=:rarity AND colour=:colours 
                                ORDER BY id DESC LIMIT 1
                                """), {
                                "cardname":cardname, "rarity":rarity, "colours":colours
                                }).fetchone()[0]
        
        if len(inlibs) != 0:
            for i in inlibs:
                lib_insert(card, i[1])
        else:
            lib_insert(card, 0)

        if two_faced:
            return render_template("newback.html", card=card, msg = 0)
        else:
            return redirect("/")
    else:
        return render_template("ohno.html", msg=2)
    
@app.route("/folder", methods=["GET"])
def folder():
    library = request.args["folder"]
    cards = se.cardseek(session["username"], folder=library)
    cmcavg = se.cmcavg(library)
    return render_template("folder.html", cards=cards, folder=library, cmcavg=cmcavg)


@app.route("/folder/new", methods=["POST"])
def new_folder():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = request.form["name"]
    sql = """INSERT INTO libraries (userid, name) VALUES (:user, :name)"""
    db.session.execute(text(sql), {"name":name, "user":se.userseek(session["username"])})
    db.session.commit()
    return redirect("/")


@app.route("/folder/delete", methods=["POST"])
def del_folder():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    id = request.form["id"]
    sql = """UPDATE cardlib SET library = 0 WHERE library = :id"""
    db.session.execute(text(sql), {"id":id})
    sql = """DELETE FROM libraries WHERE id = :id"""
    db.session.execute(text(sql), {"id":id})
    db.session.commit()
    return redirect("/")


@app.route("/cardedit", methods=["GET"])
def cardedit():
    card = request.args["card"]
    sql = "SELECT name, twofaced, colour, cmc, rarity, power, toughness, id FROM cards WHERE id=:card"
    result = db.session.execute(text(sql), {"card":card}).fetchone()
    libs = se.libseek(session["username"])
    sql = "SELECT library FROM cardlib WHERE card=:card"
    places = db.session.execute(text(sql), {"card":card}).fetchall()
    connected = []
    for place in places:
        connected.append(place[0])
    return render_template("cardedit.html", card=card, result=result, libs=libs, connected=connected) 

@app.route("/cardedit/send", methods=["POST"])
def sendedit():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
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
                print(two_faced)
            elif value == "power":
                power = request.form["power"]
                power = None if power == "" else power
            elif value == "toughness":
                toughness = request.form["toughness"]
                toughness = None if toughness == "" else toughness
            elif (value != "cmc"
                  and value != "rarity"
                  and value != "cardname"
                  and value != "libs"
                  and value != "card"
                  and value != "csrf_token"
                  ):
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
                lib_insert(card, i[1])
        else:
            lib_insert(card, 0)

        if two_faced:
            return render_template("newback.html", card=card, msg = 0)
        else:
            return redirect("/")
    else:
        return render_template("ohno.html", msg=2)
    
@app.route("/backsend", methods=["POST"])
def backsend():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    cardname = None
    cmc = None
    card = None
    power = None
    toughness = None

    for value in request.form:
        if value == "card":
            card = request.form[value]
        elif value == "cardname":
            cardname = request.form[value]
        elif value == "cmc":
            cmc = request.form[value]
        elif value == "power":
            power = request.form[value]
            power = None if power == "" else power
        elif value == "toughness":
            toughness = request.form[value]
            toughness = None if toughness == "" else toughness

    if cardname is not None and cmc is not None and card is not None:
        sql = """INSERT INTO backside (frontid, name, cmc, power, toughness) 
        VALUES (:card, :cardname, :cmc, :power, :toughness)"""
        db.session.execute(text(sql), {
                                        "card":card,
                                       "cardname":cardname,
                                       "cmc":cmc,
                                       "power":power,
                                       "toughness":toughness
                                       })
        db.session.commit()
        return redirect("/")

    else:
        render_template("newback.html", card=card, msg=1)


@app.route("/delcard", methods=["GET"])
def delcard():
    card = request.args["card"]
    sql = "UPDATE cardlib SET visible = False WHERE card = :card"
    db.session.execute(text(sql), {"card":card})
    db.session.commit()
    return redirect("/")
    
@app.route("/signin", methods=["POST"])
def signin():
    password = request.form["password"]
    username = request.form["username"]
    if 2 < len(username) < 25 and 2 < len(password) < 25:
        if len(se.userseek(username)) == 0:
            us.insert_user(username, password)
            return redirect("/")
        
        else:
            return render_template("ohno.html", msg = 3)
        
    else:
        return render_template("ohno.html", msg=1)


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    if not us.valid_user(username, password):
        return render_template("ohno.html", msg=0)
    
    session["username"] = username
    session["csrf_token"] = token_hex(16)
    return redirect("/")


@app.route("/logout")
def logout():
    del session["csrf_token"]
    del session["username"]
    
    return redirect("/")