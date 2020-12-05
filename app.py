from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app=Flask(__name__)
app.secret_key="12301983"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
db = SQLAlchemy(app)
idklienta=0
today=date.today()

class baza(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    nazwabanku=db.Column(db.String, nullable=True)
    suma=db.Column(db.String, nullable=True)
    miejsc=db.Column(db.String, nullable=True)
    ulica=db.Column(db.String, nullable=True)
    kodp=db.Column(db.String, nullable=True)
    nrtel=db.Column(db.String, nullable=True)
    email=db.Column(db.String, nullable=True)
    www=db.Column(db.String, nullable=True)
    zrzeszenie=db.Column(db.String, nullable=True)
    imienazw=db.Column(db.String, nullable=True)
    komentarz=db.Column(db.String, nullable=True)
    data=db.Column(db.TEXT, nullable=True)
    #def __repr__(self):
     #   return f"baza('{self.nazwa}','{self.suma}','{self.miejsc}','{self.ulica}','{self.kodp}','{self.nrtel}','{self.email}','{self.www}','{self.zrzeszenie}','{self.imienazw}','{self.komentarz}')"
    def __init__(self,nazwabanku,suma,miejsc,ulica,kodp,nrtel,email,www,zrzeszenie,imienazw,komentarz,data):
        self.id
        self.nazwabanku=nazwabanku
        self.suma=suma
        self.miejsc=miejsc
        self.ulica=ulica
        self.kodp=kodp
        self.nrtel=nrtel
        self.email=email
        self.www=www
        self.zrzeszenie=zrzeszenie
        self.imienazw=imienazw
        self.komentarz=komentarz
        self.data=data

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/baza_danych", methods=["POST", "GET"])
def baza_danych():
    if request.method=="POST":
        nazwabanku1= request.form["bank"]
        session["nazwa"] = nazwabanku1

        suma1= request.form["suma"]
        session["suma"] = suma1

        miejsc1= request.form["miejscowosc"]
        session["miejsce"] = miejsc1

        ulica1= request.form["ulica"]
        session["ulica"] = ulica1
        
        kodp1= request.form["kodp"]
        session["kodp"] = kodp1

        nrtel1= request.form["nrtel"]
        session["nrtel"] = nrtel1

        email1= request.form["email"]
        session["email"] = email1

        www1= request.form["www"]
        session["www"] = www1

        zrzeszenie1= request.form["zrzeszenie"]
        session["zrzeszenie"] = zrzeszenie1

        imienazw1= request.form["imienazw"]
        session["imienazw"] = imienazw1

        komentarz1= request.form["komentarz"]
        session["komentarz"] = komentarz1

        data1= request.form["data"]
        session["data"] = data1
        
        klient=baza(nazwabanku1,suma1,miejsc1,ulica1,kodp1,nrtel1,email1,www1,zrzeszenie1,imienazw1,komentarz1,data1)
        global idklienta 
        idklienta=klient
        db.session.add(klient)
        db.session.commit()
        return redirect(url_for("baza_danych"))
    else:
        return render_template("baza.html", today=today)

@app.route("/dl/<int:id>")
def usun(id):
    delete=baza.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    return redirect("/widok_bazy")

@app.route("/update/<int:id>", methods=["POST", "GET"])
def edytuj(id):
    update=baza.query.get(id)
    if request.method=="POST":
        update.nazwabanku=request.form['nazwa']
        update.suma=request.form['suma']
        update.miejsc=request.form['miejsc']
        update.ulica=request.form['ulica']
        update.kodp=request.form['kodp']
        update.nrtel=request.form['nrtel']
        update.email=request.form['email']
        update.www=request.form['www']
        update.zrzeszenie=request.form['zrzeszenie']
        update.imienazw=request.form['imienazw']
        update.komentarz=request.form['komentarz']
        update.data=request.form['datakal']

        db.session.commit()
        return redirect("/widok_bazy")
    else:
        return render_template("pojwid.html", item=update, today=today)
    


@app.route("/widok_bazy", methods=["POST", "GET"])
def widok():
    return render_template("widok.html", values=baza.query.all(), today=today)

@app.route("/widok_bazy/<int:id>", methods=["POST", "GET"])
def rek(id):
    ajdi=baza.query.get(id)
    return render_template("pojwid.html", item=baza.query.filter_by(id=id).first(), today=today)

@app.route("/search", methods=["POST", "GET"]) 
def search():
    name=request.form["searchobject"]
    return render_template("widok.html", values=baza.query.filter_by(nazwabanku=name), today=today)

@app.route("/kalendarz",  methods=["POST", "GET"])
def kalendarz():
    return render_template("kalendarz.html", values=baza.query.filter(baza.data>=today).order_by(baza.data), today=today)

@app.route("/wyloguj")
def wyloguj():
    return

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
