# Magic: The Gathering -korttitietokanta

Sovelluksessa näkyy kaikki käyttäjän kansiot (korttien säilytyspaikat),
joissa on lista niiden sisältämistä korteista. Käyttäjä voi myös lisätä ja 
hakea kortteja ja lisätä niitä omaan kirjastoonsa.

**Ominaisuuksia:**

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. (toimii)
- Käyttäjä näkee listan kansioistaan ja niiden sisällä listan kansion pelikorteista (toimii)
- Käyttäjä voi lisätä pelikortteja tietokantaan ja muokata niiden ominaisuuksia (lisääminen ja muokkaaminen toimii)
- Pelikorteilla on useita ominaisuuksia kuten harvinaisuus, sen "hinta" ja voimia (lisätty tietokantaan tarvittavat)
- Käyttäjän lisätessä kortin tietokantaan sovellus hakee kortin kuvan netistä (scryfall.com) (Toteutus epätodennäköinen)
- Käyttäjä voi hakea korttia nimellä tai rajatusta valikoimasta ominaisuuksia (toimii)
- Käyttäjä voi poistaa kortin tietokannastaan, jos se on siellä (toimii)
- Jokaisen listan kohdalla on valikoidut tiedot listan korttien ominaisuuksista (pelkkä nimi tällä hetkellä)
- Kansiossa näkyy statistiikkaa sen sisältämistä korteista (toimii)


# Paikallinen käyttö

Kloonaa repositorio omalle koneellesi:
`git@github.com:kaltionkasvatti/magic-library.git`

Siirry komentorivillä kyseiseen kirjastoon.

Luo `.env` -tiedosto seuraavilla muuttujilla:
`DATABASE_URL=<local-postgres-address>`
`SECRET_KEY=<your-secret-key>`

Käynnistä virtuaaliympäristö:
`python3 -m venv venv`
`source venv/bin/activate`

Asenna riippuvuudet:
`pip install -r requirements.txt`

Määritä tietokanta:
`psql < schema.sql`

Käynnistä sovellus:
`flask run`